# import importlib
import logging
from enum import Enum, auto

from mppsolar.helpers import get_kwargs


class PortType(Enum):
    UNKNOWN = auto()
    TEST = auto()
    USB = auto()
    TUSB = auto()
    ESP32 = auto()
    SERIAL = auto()
    JKBLE = auto()
    MQTT = auto()
    VSERIAL = auto()
    DALYSERIAL = auto()


log = logging.getLogger("io")


def get_port_type(port):
    if port is None:
        return PortType.UNKNOWN

    port = port.lower()
    # check for test type port
    if "test" in port:
        log.debug("port matches test")
        return PortType.TEST
    # mqtt
    elif "mqtt" in port:
        log.debug("port matches mqtt")
        return PortType.MQTT
    # USB type ports
    elif "hidraw" in port:
        log.debug("port matches hidraw")
        return PortType.USB
    elif "mppsolar" in port:
        log.debug("port matches mppsolar")
        return PortType.USB
    elif "hidfull" in port:
        log.debug("port matches hidfull")
        return PortType.TUSB
    # ESP type ports
    elif "esp" in port:
        log.debug("port matches esp")
        return PortType.ESP32
    # JKBLE type ports
    elif ":" in port:
        # all mac addresses currently return as JKBLE
        log.debug("port matches jkble ':'")
        return PortType.JKBLE
    elif "jkble" in port:
        log.debug("port matches jkble")
        return PortType.JKBLE
    elif "daly" in port:
        log.debug("port matches daly")
        return PortType.DALYSERIAL
    elif "vserial" in port:
        log.debug("port matches vserial")
        return PortType.VSERIAL
    elif "serial" in port:
        log.debug("port matches serial")
        return PortType.SERIAL
    elif "ttyusb" in port:
        log.debug("port matches ttyusb")
        return PortType.SERIAL
    else:
        return PortType.UNKNOWN


def get_port(*args, **kwargs):
    port = get_kwargs(kwargs, "port")
    baud = get_kwargs(kwargs, "baud", 2400)
    porttype = get_kwargs(kwargs, "porttype", None)

    if porttype:
        log.info(f"Port overide - using port '{porttype}'")
        port_type = get_port_type(porttype)
    else:
        port_type = get_port_type(port)

    if port_type == PortType.TEST:
        log.info("Using testio for communications")
        from mppsolar.inout.testio import TestIO
        _port = TestIO(device_path=port)

    elif port_type == PortType.USB:
        log.info("Using hidrawio for communications")
        from mppsolar.inout.hidrawio import HIDRawIO
        _port = HIDRawIO(device_path=port)

    elif port_type == PortType.TUSB:
        log.info("Using hidfullio for communications")
        from mppsolar.inout.hidfullio import HIDFullIO
        _port = HIDFullIO(device_path=port)

    elif port_type == PortType.ESP32:
        log.info("Using esp32io for communications")
        from mppsolar.inout.esp32io import ESP32IO
        _port = ESP32IO(device_path=port)

    elif port_type == PortType.JKBLE:
        log.info("Using jkbleio for communications")
        from mppsolar.inout.jkbleio import JkBleIO
        _port = JkBleIO(device_path=port)

    elif port_type == PortType.SERIAL:
        log.info("Using serialio for communications")
        from mppsolar.inout.serialio import SerialIO
        _port = SerialIO(device_path=port, serial_baud=baud)

    elif port_type == PortType.DALYSERIAL:
        log.info("Using dalyserialio for communications")
        from mppsolar.inout.dalyserialio import DalySerialIO
        _port = DalySerialIO(device_path=port, serial_baud=baud)

    elif port_type == PortType.VSERIAL:
        log.info("Using vserialio for communications")
        from mppsolar.inout.vserialio import VSerialIO
        _port = VSerialIO(device_path=port, serial_baud=baud, records=30)

    elif port_type == PortType.MQTT:
        mqtt_broker = get_kwargs(kwargs, "mqtt_broker", "localhost")
        name = get_kwargs(kwargs, "name", "unnamed")
        # mqtt_port = get_kwargs(kwargs, "mqtt_port", 1883)
        # mqtt_user = get_kwargs(kwargs, "mqtt_user")
        # mqtt_pass = get_kwargs(kwargs, "mqtt_pass")
        log.info(f"Using mqttio for communications broker {mqtt_broker}")

        from mppsolar.inout.mqttio import MqttIO

        _port = MqttIO(
            client_id=name,
            mqtt_broker=mqtt_broker,
            # mqtt_port=mqtt_port,
            # mqtt_user=mqtt_user,
            # mqtt_pass=mqtt_pass,
        )

    else:
        _port = None
    return _port
