import logging

from powermon.ports.abstractport import PortType
from powermon.ports.serialport import SerialPort
from powermon.ports.usbport import USBPort

# Set-up logger
log = logging.getLogger("ports")


def getPortFromConfig(port_config):
    log.debug(f"port_config: {port_config}")

    portObject = None

    if not port_config:
        log.info("no port config supplied, defaulting to test port")
        port_config = {"type": "test", "protocol": "PI30"}

    # port type is mandatory
    portType = port_config.get("type")
    log.debug(f"portType: {portType}")

    # return None if port type is not defined
    if portType is None:
        return None

    # build port object
    if portType == PortType.SERIAL:
        portObject = SerialPort.fromConfig(config=port_config)
    elif portType == PortType.USB:
        portObject = USBPort.fromConfig(config=port_config)

    # Pattern for port types that cause problems when imported
    elif portType == PortType.TEST:
        log.debug("portType test found")
        from powermon.ports.testport import TestPort
        portObject = TestPort.fromConfig(config=port_config)

    else:
        log.info("port type object not found for %s", portType)

    return portObject
