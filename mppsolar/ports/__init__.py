import importlib
import logging
from mppsolar.ports.serialport import SerialPort
import mppsolar.ports.testport
from mppsolar.ports.usbport import USBPort
from enum import StrEnum, auto


class PortType(StrEnum):
    UNKNOWN = auto()
    TEST = auto()
    USB = auto()
    ESP32 = auto()
    SERIAL = auto()
    JKBLE = auto()
    MQTT = auto()
    VSERIAL = auto()
    DALYSERIAL = auto()
    BLE = auto()


log = logging.getLogger("ports")


def get_port(portType, portPath, baud, protocol):
    # return None if port type is not defined
    if portType is None:
        return None

    portObject = None

    if portType == PortType.SERIAL:
        portObject = SerialPort(portPath, baud, protocol)
    elif portType == PortType.USB:
        portObject = USBPort(portPath, protocol)

    return portObject
