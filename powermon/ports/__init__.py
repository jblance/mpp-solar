from mppsolar.protocols import get_protocol

# import importlib

from powermon.ports.abstractport import PortType
from powermon.ports.serialport import SerialPort
from powermon.ports.usbport import USBPort


def getPortFromConfig(port_config):
    # get protocol handler
    protocol = get_protocol(protocol=port_config["protocol"])
    # log.debug(f"protocol: {protocol}")

    # port type is mandatory
    portType = port_config["type"]

    # return None if port type is not defined
    if portType is None:
        return None

    # build port object
    portObject = None

    if portType == PortType.SERIAL:
        portObject = SerialPort(config=port_config, protocol=protocol)
    elif portType == PortType.USB:
        portObject = USBPort(config=port_config, protocol=protocol)

    # Pattern for port types that cause problems when imported
    elif portType == PortType.TEST:
        from powermon.ports.testport import TestPort

        portObject = TestPort(config=port_config, protocol=protocol)

    return portObject
