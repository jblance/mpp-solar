""" powermon / ports / __init__.py """
import logging

from powermon.errors import ConfigError
from powermon.ports.porttype import PortType
from powermon.ports.serialport import SerialPort
from powermon.ports.testport import TestPort
from powermon.ports.usbport import USBPort

# Set-up logger
log = logging.getLogger("ports")


def from_config(port_config):
    """ get a port object from config data """
    log.debug("port_config: %s", port_config)

    port_object = None
    if not port_config:
        raise ConfigError("no port config supplied")

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
        case PortType.BLE:
            log.debug("port_type BLE found")
            from powermon.ports.bleport import BlePort
            port_object = BlePort.from_config(config=port_config)
        case _:
            log.info("port type object not found for %s", port_type)
            raise ConfigError(f"Invalid port type: '{port_type}'")

    return port_object
