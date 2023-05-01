import logging

from mppsolar.protocols import get_protocol
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

    # get protocol handler
    protocol = get_protocol(protocol=port_config.get("protocol"))

    # port type is mandatory
    portType = port_config.get("type")
    log.debug(f"portType: {portType}")

    # return None if port type is not defined
    if portType is None:
        return None

    # build port object
    if portType == PortType.SERIAL:
        portObject = SerialPort(config=port_config, protocol=protocol)
    elif portType == PortType.USB:
        portObject = USBPort(config=port_config, protocol=protocol)

    # Pattern for port types that cause problems when imported
    elif portType == PortType.TEST:
        log.debug("portType test found")
        from powermon.ports.testport import TestPort

        portObject = TestPort(config=port_config, protocol=protocol)

    else:
        log.info("port type object not found for %s", portType)

    return portObject
