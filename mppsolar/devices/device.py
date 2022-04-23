# import importlib
import logging
from abc import ABC

from mppsolar.helpers import get_kwargs
from mppsolar.inout import get_port
from mppsolar.protocols import get_protocol

PORT_TYPE_UNKNOWN = 0
PORT_TYPE_TEST = 1
PORT_TYPE_USB = 2
PORT_TYPE_ESP32 = 4
PORT_TYPE_SERIAL = 8
PORT_TYPE_JKBLE = 16
PORT_TYPE_MQTT = 32
PORT_TYPE_VSERIAL = 64
PORT_TYPE_DALYSERIAL = 128

# log = None
log = logging.getLogger("device")


class AbstractDevice(ABC):
    """
    Abstract device class
    """

    def __init__(self, *args, **kwargs):
        global log
        # self._protocol = None
        # self._protocol_class = None
        # self._port = None
        log.debug(f"__init__ args {args}")
        log.debug(f"__init__ kwargs {kwargs}")
        self._name = get_kwargs(kwargs, "name")
        self._port = get_port(**kwargs)
        self._protocol = get_protocol(get_kwargs(kwargs, "protocol"))
        log.debug(
            f"__init__ name {self._name}, port {self._port}, protocol {self._protocol}"
        )

    def __str__(self):
        """
        Build a printable representation of this class
        """
        return f"{self._classname} device - name: {self._name}, port: {self._port}, protocol: {self._protocol}"

    # TODO: remove commented code once certain nothing has broken
    # def get_port_type(self, port):
    #     if port is None:
    #         return PORT_TYPE_UNKNOWN

    #     port = port.lower()
    #     # check for test type port
    #     if "test" in port:
    #         log.debug("port matches test")
    #         return PORT_TYPE_TEST
    #     # mqtt
    #     elif "mqtt" in port:
    #         log.debug("port matches mqtt")
    #         return PORT_TYPE_MQTT
    #     # USB type ports
    #     elif "hidraw" in port:
    #         log.debug("port matches hidraw")
    #         return PORT_TYPE_USB
    #     elif "mppsolar" in port:
    #         log.debug("port matches mppsolar")
    #         return PORT_TYPE_USB
    #     # ESP type ports
    #     elif "esp" in port:
    #         log.debug("port matches esp")
    #         return PORT_TYPE_ESP32
    #     # JKBLE type ports
    #     elif ":" in port:
    #         # all mac addresses currently return as JKBLE
    #         log.debug("port matches jkble ':'")
    #         return PORT_TYPE_JKBLE
    #     elif "jkble" in port:
    #         log.debug("port matches jkble")
    #         return PORT_TYPE_JKBLE
    #     elif "daly" in port:
    #         log.debug("port matches daly")
    #         return PORT_TYPE_DALYSERIAL
    #     elif "vserial" in port:
    #         log.debug("port matches vserial")
    #         return PORT_TYPE_VSERIAL
    #     elif "serial" in port:
    #         log.debug("port matches serial")
    #         return PORT_TYPE_SERIAL
    #     elif "ttyusb" in port:
    #         log.debug("port matches ttyusb")
    #         return PORT_TYPE_SERIAL
    #     else:
    #         return PORT_TYPE_UNKNOWN

    # def set_protocol(self, *args, **kwargs):
    #     """
    #     Set the protocol for this device
    #     """
    #     protocol = get_kwargs(kwargs, "protocol")
    #     log.debug(f"Protocol {protocol}")
    #     if protocol is None:
    #         self._protocol = None
    #         self._protocol_class = None
    #         return
    #     protocol_id = protocol.lower()
    #     # Try to import the protocol module with the supplied name (may not exist)
    #     try:
    #         proto_module = importlib.import_module("mppsolar.protocols." + protocol_id, ".")
    #     except ModuleNotFoundError:
    #         log.error(f"No module found for protocol {protocol_id}")
    #         self._protocol = None
    #         self._protocol_class = None
    #         return
    #     # Find the protocol class - classname must be the same as the protocol_id
    #     try:
    #         self._protocol_class = getattr(proto_module, protocol_id)
    #     except AttributeError:
    #         log.error(f"Module {proto_module} has no attribute {protocol_id}")
    #         self._protocol = None
    #         self._protocol_class = None
    #         return
    #     # Instantiate the class
    #     # TODO: fix protocol instantiate
    #     self._protocol = self._protocol_class(
    #         "init_var", proto_keyword="value", second_keyword=123
    #     )

    # def set_port(self, *args, **kwargs):
    #     port = get_kwargs(kwargs, "port")
    #     baud = get_kwargs(kwargs, "baud", 2400)
    #     porttype = get_kwargs(kwargs, "porttype")

    #     if porttype:
    #         log.info(f"Port overide - using port '{porttype}'")
    #         port_type = self.get_port_type(porttype)
    #     else:
    #         port_type = self.get_port_type(port)

    #     if port_type == PORT_TYPE_TEST:
    #         log.info("Using testio for communications")
    #         from mppsolar.inout.testio import TestIO

    #         self._port = TestIO(device_path=port)

    #     elif port_type == PORT_TYPE_USB:
    #         log.info("Using hidrawio for communications")
    #         from mppsolar.inout.hidrawio import HIDRawIO

    #         self._port = HIDRawIO(device_path=port)

    #     elif port_type == PORT_TYPE_ESP32:
    #         log.info("Using esp32io for communications")
    #         from mppsolar.inout.esp32io import ESP32IO

    #         self._port = ESP32IO(device_path=port)

    #     elif port_type == PORT_TYPE_JKBLE:
    #         log.info("Using jkbleio for communications")
    #         from mppsolar.inout.jkbleio import JkBleIO

    #         self._port = JkBleIO(device_path=port)

    #     elif port_type == PORT_TYPE_SERIAL:
    #         log.info("Using serialio for communications")
    #         from mppsolar.inout.serialio import SerialIO

    #         self._port = SerialIO(device_path=port, serial_baud=baud)

    #     elif port_type == PORT_TYPE_DALYSERIAL:
    #         log.info("Using dalyserialio for communications")
    #         from mppsolar.inout.dalyserialio import DalySerialIO

    #         self._port = DalySerialIO(device_path=port, serial_baud=baud)

    #     elif port_type == PORT_TYPE_VSERIAL:
    #         log.info("Using vserialio for communications")
    #         from mppsolar.inout.vserialio import VSerialIO

    #         self._port = VSerialIO(device_path=port, serial_baud=baud, records=30)

    #     elif port_type == PORT_TYPE_MQTT:

    #         mqtt_broker = get_kwargs(kwargs, "mqtt_broker", "localhost")
    #         # mqtt_port = get_kwargs(kwargs, "mqtt_port", 1883)
    #         # mqtt_user = get_kwargs(kwargs, "mqtt_user")
    #         # mqtt_pass = get_kwargs(kwargs, "mqtt_pass")
    #         log.info(f"Using mqttio for communications broker {mqtt_broker}")

    #         from mppsolar.inout.mqttio import MqttIO

    #         self._port = MqttIO(
    #             client_id=self._name,
    #             mqtt_broker=mqtt_broker,
    #             # mqtt_port=mqtt_port,
    #             # mqtt_user=mqtt_user,
    #             # mqtt_pass=mqtt_pass,
    #         )

    #     else:
    #         self._port = None

    # def list_commands(self):
    #     # print(f"{'Parameter':<30}\t{'Value':<15} Unit")
    #     if self._protocol is None:
    #         log.error("Attempted to list commands with no protocol defined")
    #         return {"ERROR": ["Attempted to list commands with no protocol defined", ""]}
    #     result = {}
    #     result["_command"] = "command help"
    #     result[
    #         "_command_description"
    #     ] = f"List available commands for protocol {str(self._protocol._protocol_id, 'utf-8')}"
    #     for command in self._protocol.COMMANDS:
    #         if "help" in self._protocol.COMMANDS[command]:
    #             info = (
    #                 self._protocol.COMMANDS[command]["description"]
    #                 + self._protocol.COMMANDS[command]["help"]
    #             )
    #         else:
    #             info = self._protocol.COMMANDS[command]["description"]
    #         result[command] = [info, ""]
    #     return result

    # def list_outputs(self):
    #     import pkgutil

    #     print("device list outouts")
    #     pkgpath = __file__
    #     pkgpath = pkgpath[: pkgpath.rfind("/")]
    #     pkgpath += "/../outputs"
    #     # print(pkgpath)
    #     result = {}
    #     result["_command"] = "outputs help"
    #     result["_command_description"] = "List available output modules"
    #     for _, name, _ in pkgutil.iter_modules([pkgpath]):
    #         # print(name)
    #         _module_class = importlib.import_module("mppsolar.outputs." + name, ".")
    #         _module = getattr(_module_class, name)
    #         # print(_module())
    #         result[name] = (str(_module()), "", "")
    #     # print(result)
    #     return result

    # def run_commands(self, commands) -> dict:
    #     """
    #     Run multiple commands sequentially
    #     :param commands: List of commands to run, either with or without an alias.
    #     If an alias is provided, it will be substituted in place of cmd name in the returned dict
    #     Additional elements in the tuple will be passed to run_command as ordered
    #     Example: ['QPIWS', ...] or [('QPIWS', 'ALIAS'), ...] or [('QPIWS', 'ALIAS', True), ...] or mix and match
    #     :return: Dictionary of responses
    #     """
    #     responses = {}
    #     for i, command in enumerate(commands):
    #         if isinstance(command, str):
    #             responses[command] = self.run_command(command)
    #         elif isinstance(command, tuple) and len(command) > 0:
    #             if len(command) == 1:  # Treat as string
    #                 responses[command[0]] = self.run_command(command[0])
    #             elif len(command) == 2:
    #                 responses[command[1]] = self.run_command(command[0])
    #             else:
    #                 responses[command[1]] = self.run_command(command[0], *command[2:])
    #         else:
    #             responses["Command {:d}".format(i)] = {
    #                 "ERROR": ["Unknown command format", "(Indexed from 0)"]
    #             }
    #     return responses

    def run_command(self, command) -> dict:
        """
        generic method for running a 'raw' command
        """
        log.info(f"Running command {command}")

        if self._protocol is None:
            log.error("Attempted to run command with no protocol defined")
            return {"ERROR": ["Attempted to run command with no protocol defined", ""]}
        if self._port is None:
            log.error(
                f"No communications port defined - unable to run command {command}"
            )
            return {
                "ERROR": [
                    f"No communications port defined - unable to run command {command}",
                    "",
                ]
            }

        if command == "list_commands":
            return self._protocol.list_commands()
        if command == "list_outputs":
            return self.list_outputs()
        if command == "get_status":
            return self.get_status()
        if command == "get_settings":
            return self.get_settings()
        if not command:
            command = self._protocol.DEFAULT_COMMAND

        # Send command and receive data
        full_command = self._protocol.get_full_command(command)
        log.info(f"full command {full_command} for command {command}")
        if full_command is None:
            log.error(
                f"full_command not found for {command} in protocol {self._protocol._protocol_id}"
            )
            return {
                "ERROR": [
                    f"full_command not found for {command} in protocol {self._protocol._protocol_id}",
                    "",
                ]
            }

        # Band-aid solution, need to reduce what is sent
        raw_response = self._port.send_and_receive(
            command=command,
            full_command=full_command,
            protocol=self._protocol,
            command_defn=self._protocol.get_command_defn(command),
        )
        log.debug(f"Send and Receive Response {raw_response}")

        # Handle errors
        # Maybe there should a decode for ERRORs and WARNINGS...
        # Some inverters return the command if the command is unknown:
        if raw_response == full_command:
            return {
                "ERROR": [
                    f"Inverter returned the command string for {command} - the inverter didnt recognise this command",
                    "",
                ]
            }
        # dict is returned on exception

        if isinstance(raw_response, dict):
            return raw_response

        # Decode response
        decoded_response = self._protocol.decode(raw_response, command)
        log.info(f"Decoded response {decoded_response}")

        return decoded_response

    def get_status(self) -> dict:
        # Run all the commands that are defined as status from the protocol definition
        data = {}
        for command in self._protocol.STATUS_COMMANDS:
            data.update(self.run_command(command))
        return data

    def get_settings(self) -> dict:
        # Run all the commands that are defined as settings from the protocol definition
        data = {}
        for command in self._protocol.SETTINGS_COMMANDS:
            data.update(self.run_command(command))
        return data
