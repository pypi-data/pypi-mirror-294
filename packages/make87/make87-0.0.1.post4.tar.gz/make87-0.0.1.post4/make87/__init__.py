import importlib
import json
import os
from functools import partial
from typing import Dict, Callable, Literal, Annotated, Type
from typing import List, Union
from typing import Optional

import zenoh
from datetime import datetime

from google.protobuf.message import Message
from pydantic import BaseModel, Field

_SESSION: Optional[zenoh.Session] = None


class PUB(BaseModel):
    socket_type: Literal["PUB"]
    topic_name: str
    topic_key: str
    message_type: str


class SUB(BaseModel):
    socket_type: Literal["SUB"]
    topic_name: str
    topic_key: str
    message_type: str


Socket = Annotated[Union[PUB, SUB], Field(discriminator="socket_type")]


class Sockets(BaseModel):
    sockets: List[Socket]


class Peripheral(BaseModel):
    name: str
    mount: Union[str, int]  # support `int` to pass AVFoundation index used on macOS
    # TODO: Fix up above to match structs in make87 core


class Peripherals(BaseModel):
    peripherals: List[Peripheral]


def _import_class_from_string(path) -> Type[Message]:
    *module_path, class_name = path.split(".")
    # Append `_messages` to package name, so it's `make87_messages`
    module_path[0] += "_messages"
    module_name = ".".join(module_path)
    # append `_pb2` to module and class name because this is how protobuf compiler names them
    module_name += "_pb2"
    # Import the module dynamically
    module = importlib.import_module(module_name)
    # Get the class from the module
    cls = getattr(module, class_name)

    return cls


class Topic:
    def __init__(self, name: str):
        self.name = name


class PublisherTopic(Topic):
    def __init__(self, name: str, message_type: str, session: zenoh.Session):
        super().__init__(name)
        # check if session is set otherwise initialize it
        self.name = name
        self._session = session
        self._message_type: Type[Message] = _import_class_from_string(message_type)
        self._pub = session.declare_publisher(f"{name}")

    @property
    def message_type(self) -> Type[Message]:
        return self._message_type

    def publish(self, message: Message) -> None:
        if not message.HasField("timestamp"):
            message.timestamp.FromDatetime(datetime.now())
        self._pub.put(message.SerializeToString())


class SubscriberTopic(Topic):
    def __init__(self, name: str, message_type: str, session: zenoh.Session):
        super().__init__(name)
        self._subscribers = []
        self.name = name
        self._message_type: Type[Message] = _import_class_from_string(message_type)
        self._session = session

    def decode_message(self, *args, callback: Callable, **kwargs):
        sample = args[0]
        message = self._message_type()
        message.ParseFromString(sample.payload)
        callback(message)

    def subscribe(self, callback: Callable) -> None:
        retrieve_callback = partial(self.decode_message, callback=callback)
        sub = self._session.declare_subscriber(f"{self.name}", retrieve_callback)
        self._subscribers.append(sub)


_TOPICS: Dict[str, Union[PublisherTopic, SubscriberTopic]] = {}


def get_topic(name: str) -> Union[PublisherTopic, SubscriberTopic]:
    global _SESSION
    if _SESSION is None:
        initialize()
    global _TOPICS
    if name not in _TOPICS:
        raise ValueError(f"Topic {name} not found. Available topics: {list(_TOPICS.keys())}")

    return _TOPICS[name]


def initialize_peripherals() -> None:
    try:
        peripheral_data_env = os.environ.get("PERIPHERALS", '{"peripherals":[]}')
        peripheral_data = Peripherals.model_validate_json(peripheral_data_env)
    except json.JSONDecodeError:
        raise ValueError("`PERIPHERALS` environment variable is not a valid JSON string.")

    for peripheral in peripheral_data.peripherals:
        peripheral_names.add(peripheral.name, peripheral.mount)


def initialize() -> None:
    try:
        socket_data_env = os.environ["SOCKETS"]
        socket_data = Sockets.model_validate_json(socket_data_env)
    except KeyError:
        raise ValueError("`SOCKETS` environment variable not set")
    except json.JSONDecodeError:
        raise ValueError("`SOCKETS` environment variable is not a valid JSON string.")

    config = None
    if "COMM_CONFIG" in os.environ:
        config = json.loads(os.environ["COMM_CONFIG"])
        config = zenoh.Config.from_obj(config)
    session = zenoh.open(config=config)
    global _TOPICS
    for socket in socket_data.sockets:
        topic_names.add(socket.topic_name, socket.topic_key)
        if isinstance(socket, PUB):
            _TOPICS[socket.topic_key] = PublisherTopic(
                name=socket.topic_key, message_type=socket.message_type, session=session
            )
        elif isinstance(socket, SUB):
            _TOPICS[socket.topic_key] = SubscriberTopic(
                name=socket.topic_key, message_type=socket.message_type, session=session
            )
        else:
            raise ValueError(f"Invalid socket type {socket.socket_type}")

    global _SESSION
    _SESSION = session


def cleanup() -> None:
    global _SESSION
    if _SESSION is not None:
        _SESSION.close()
        _SESSION = None
        global _TOPICS
        _TOPICS = {}


class TopicNamesLookup:
    """Holds topic names and their keys for deployment. Used by developer to put in placeholder in their app logic.
    Is being filled at runtime by the `initialize` function."""

    def __init__(self):
        self._attributes: Optional[Dict[str, str]] = None

    def __getattr__(self, name: str) -> str:
        if self._attributes is None:
            self._attributes = {}
            initialize()
        if name in self._attributes:
            return self._attributes[name]
        else:
            raise AttributeError(
                f"Topic name {name} not found. Make sure it is correctly defined in your `MAKE87` manifest file."
            )

    def add(self, name: str, value: str):
        self._attributes[name] = value


topic_names = TopicNamesLookup()


class PeripheralNamesLookup:
    """Holds peripheral names and their mount points for deployment. Used by developer to put in placeholder in their
    app logic. Is being filled at runtime by the `initialize` function."""

    def __init__(self):
        self._attributes: Optional[Dict[str, str]] = None

    def __getattr__(self, name: str) -> str:
        if self._attributes is None:
            self._attributes = {}
            initialize_peripherals()
        if name in self._attributes:
            return self._attributes[name]
        else:
            raise AttributeError(
                f"Peripheral name {name} not found. Make sure it is correctly defined in your `MAKE87` manifest file."
            )

    def add(self, name: str, value: str):
        self._attributes[name] = value


peripheral_names = PeripheralNamesLookup()
