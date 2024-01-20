""" protocol __init__.py """
import importlib
import logging
from enum import auto

from strenum import LowercaseStrEnum

from powermon.errors import ConfigError

log = logging.getLogger("protocols")


class Protocol(LowercaseStrEnum):
    """ enumerate available protocols """
    PI30 = auto()
    PI30MAX = auto()
    VED = auto()


def get_protocol_definition(protocol):
    """
    Get the protocol based on the protocol name
    """

    log.debug("Protocol: %s", protocol)

    protocol_id = protocol.lower()

    match protocol_id:
        case Protocol.PI30:
            from powermon.protocols.pi30 import PI30
            return PI30()
        case Protocol.PI30MAX:
            from powermon.protocols.pi30max import PI30MAX
            return PI30MAX()
        case Protocol.VED:
            from powermon.protocols.ved import VictronEnergyDirect
            return VictronEnergyDirect()
        case _:
            raise ConfigError(f"Invalid protocol_id, no protocol found for: '{protocol_id}'") 
    return None


def list_protocols():
    """ helper function to display a list of supported protocols """
    print("Supported protocols")
    for name in Protocol:
        try:
            _module_class = importlib.import_module("powermon.protocols." + name, ".")
            _module = getattr(_module_class, name)
        except ModuleNotFoundError as exc:
            log.info("Error in module %s: %s", name, exc)
            continue
        except AttributeError as exc:
            log.info("Error in module %s: %s", name, exc)
            continue
        print(f"{name}: {_module()}")
