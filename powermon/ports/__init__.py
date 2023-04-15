from mppsolar.protocols import get_protocol

import importlib

from powermon.ports.port import PortType
from powermon.ports.serialport import SerialPort
from powermon.ports.usbport import USBPort

def getPortFromConfig(port_config):

    # get protocol handler
    protocol = get_protocol(protocol=port_config["protocol"])
    #log.debug(f"protocol: {protocol}")

    portType = port_config["type"]
    portPath = port_config.get("path", None)
    portBaud = port_config.get("baud", None)
    # return None if port type is not defined
    if portType is None:
        return None

    portObject = None

    if portType == PortType.SERIAL:
        portObject = SerialPort(portPath, portBaud, protocol)
    elif portType == PortType.USB:
        portObject = USBPort(portPath, protocol)

    #Pattern for port types that cause problems when imported
    elif portType == PortType.TEST:
        porttype_id = 'testport'
        port_module = importlib.import_module("powermon.ports." + porttype_id, ".")
        port_class = getattr(port_module, porttype_id)
        portObject = port_class()

    return portObject