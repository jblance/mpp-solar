# import importlib
import logging
from ..helpers import get_kwargs

PORT_TYPE_UNKNOWN = 0
PORT_TYPE_TEST = 1
PORT_TYPE_USB = 2
PORT_TYPE_ESP32 = 4
PORT_TYPE_SERIAL = 8
PORT_TYPE_JKBLE = 16
PORT_TYPE_MQTT = 32
PORT_TYPE_VSERIAL = 64
PORT_TYPE_DALYSERIAL = 128

log = logging.getLogger("io")


def get_port_type(port):
    if port is None:
        return PORT_TYPE_UNKNOWN

    port = port.lower()
    # check for test type port
    if "test" in port:
        log.debug("port matches test")
        return PORT_TYPE_TEST
    # mqtt
    elif "mqtt" in port:
        log.debug("port matches mqtt")
        return PORT_TYPE_MQTT
    # USB type ports
    elif "hidraw" in port:
        log.debug("port matches hidraw")
        return PORT_TYPE_USB
    elif "mppsolar" in port:
        log.debug("port matches mppsolar")
        return PORT_TYPE_USB
    # ESP type ports
    elif "esp" in port:
        log.debug("port matches esp")
        return PORT_TYPE_ESP32
    # JKBLE type ports
    elif ":" in port:
        # all mac addresses currently return as JKBLE
        log.debug("port matches jkble ':'")
        return PORT_TYPE_JKBLE
    elif "jkble" in port:
        log.debug("port matches jkble")
        return PORT_TYPE_JKBLE
    elif "daly" in port:
        log.debug("port matches daly")
        return PORT_TYPE_DALYSERIAL
    elif "vserial" in port:
        log.debug("port matches vserial")
        return PORT_TYPE_VSERIAL
    elif "serial" in port:
        log.debug("port matches serial")
        return PORT_TYPE_SERIAL
    elif "ttyusb" in port:
        log.debug("port matches ttyusb")
        return PORT_TYPE_SERIAL
    else:
        return PORT_TYPE_UNKNOWN


def get_port(*args, **kwargs):
    port = get_kwargs(kwargs, "port")
    baud = get_kwargs(kwargs, "baud", 2400)
    porttype = get_kwargs(kwargs, "porttype", None)

    if porttype:
        log.info(f"Port overide - using port '{porttype}'")
        port_type = get_port_type(porttype)
    else:
        port_type = get_port_type(port)

    if port_type == PORT_TYPE_TEST:
        log.info("Using testio for communications")
        from mppsolar.io.testio import TestIO

        _port = TestIO(device_path=port)

    elif port_type == PORT_TYPE_USB:
        log.info("Using hidrawio for communications")
        from mppsolar.io.hidrawio import HIDRawIO

        _port = HIDRawIO(device_path=port)

    elif port_type == PORT_TYPE_ESP32:
        log.info("Using esp32io for communications")
        from mppsolar.io.esp32io import ESP32IO

        _port = ESP32IO(device_path=port)

    elif port_type == PORT_TYPE_JKBLE:
        log.info("Using jkbleio for communications")
        from mppsolar.io.jkbleio import JkBleIO

        _port = JkBleIO(device_path=port)

    elif port_type == PORT_TYPE_SERIAL:
        log.info("Using serialio for communications")
        from mppsolar.io.serialio import SerialIO

        _port = SerialIO(device_path=port, serial_baud=baud)

    elif port_type == PORT_TYPE_DALYSERIAL:
        log.info("Using dalyserialio for communications")
        from mppsolar.io.dalyserialio import DalySerialIO

        _port = DalySerialIO(device_path=port, serial_baud=baud)

    elif port_type == PORT_TYPE_VSERIAL:
        log.info("Using vserialio for communications")
        from mppsolar.io.vserialio import VSerialIO

        _port = VSerialIO(device_path=port, serial_baud=baud, records=30)

    elif port_type == PORT_TYPE_MQTT:
        mqtt_broker = get_kwargs(kwargs, "mqtt_broker", "localhost")
        name = get_kwargs(kwargs, "name", "unnamed")
        # mqtt_port = get_kwargs(kwargs, "mqtt_port", 1883)
        # mqtt_user = get_kwargs(kwargs, "mqtt_user")
        # mqtt_pass = get_kwargs(kwargs, "mqtt_pass")
        log.info(f"Using mqttio for communications broker {mqtt_broker}")

        from mppsolar.io.mqttio import MqttIO

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
