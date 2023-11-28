""" ports/__init__.py """
import logging
from enum import auto

from strenum import LowercaseStrEnum

from powermon.ports.serialport import SerialPort
from powermon.ports.testport import TestPort
from powermon.ports.usbport import USBPort
from powermon.errors import ConfigError

# Set-up logger
log = logging.getLogger("ports")


class PortType(LowercaseStrEnum):
    """ enumeration of supported / known port types """
    UNKNOWN = auto()
    TEST = auto()
    SERIAL = auto()
    USB = auto()

    BLE = auto()

    JKBLE = auto()
    MQTT = auto()
    VSERIAL = auto()
    DALYSERIAL = auto()
    ESP32 = auto()


def from_config(port_config):
    """ get a port object from config data """
    log.debug("port_config: %s", port_config)

    port_object = None
    if not port_config:
        log.info("no port config supplied, defaulting to test port")  # QUESTION: does this make sense, maybe should return None
        port_config = {"type": "test", "protocol": "PI30"}

    # port type is mandatory
    port_type = port_config.get("type")
    log.debug("portType: %s", port_type)

    # return None if port type is not defined
    if port_type is None:
        return None

    # build port object
    match port_type:
        case PortType.TEST:
            port_object = TestPort.from_config(config=port_config)
        case PortType.SERIAL:
            port_object = SerialPort.from_config(config=port_config)
        case PortType.USB:
            port_object = USBPort.from_config(config=port_config)

        # Pattern for port types that cause problems when imported
        # case PortType.BLE:
        #     log.debug("port_type BLE found")
        #     from powermon.ports.bleport import BlePort
        #     port_object = BlePort.fromConfig(config=port_config)

        case _:
            log.info("port type object not found for %s", port_type)
            raise ConfigError(f"Invalid port type: '{port_type}'")

    return port_object
