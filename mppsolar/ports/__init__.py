import importlib
import logging
from enum import Enum, auto


class PortType(Enum):
    UNKNOWN = auto()
    TEST = auto()
    USB = auto()
    ESP32 = auto()
    SERIAL = auto()
    JKBLE = auto()
    MQTT = auto()
    VSERIAL = auto()
    DALYSERIAL = auto()


log = logging.getLogger("ports")


def get_port(config):
    log.info(f"Geting port for config '{config}'")
    porttype = config.pop("type", None)

    # return None if port type is not defined
    if porttype is None:
        return None

    # check for
    porttype_id = porttype.lower()
    # Try to import the porttype module with the supplied name (may not exist)
    try:
        port_module = importlib.import_module("mppsolar.ports." + porttype_id, ".")
    except ModuleNotFoundError:
        log.error(f"No module found for porttype {porttype_id}")
        return None
    # Find the protocol class - classname must be the same as the protocol_id
    try:
        port_class = getattr(port_module, porttype_id)
    except AttributeError:
        log.error(f"Module {port_module} has no attribute {porttype_id}")
        return None
    # Return the instantiated class
    return port_class(config)
