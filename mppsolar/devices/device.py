# import importlib
import logging
from abc import ABC

from mppsolar.version import __version__  # noqa: F401
from mppsolar.helpers import get_kwargs
from mppsolar.inout import get_port
from mppsolar.protocols import get_protocol  # , get_device_id

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
        log.debug(f"__init__ name {self._name}, port {self._port}, protocol {self._protocol}")

    def __str__(self):
        """
        Build a printable representation of this class
        """
        return f"{self._classname} device - name: {self._name}, port: {self._port}, protocol: {self._protocol}"

    def run_command(self, command) -> dict:
        """
        generic method for running a 'raw' command
        """
        log.info(f"Running command {command}")

        if self._protocol is None:
            log.error("Attempted to run command with no protocol defined")
            return {"ERROR": ["Attempted to run command with no protocol defined", ""]}
        if self._port is None:
            log.error(f"No communications port defined - unable to run command {command}")
            return {
                "ERROR": [
                    f"No communications port defined - unable to run command {command}",
                    "",
                ]
            }

        if command == "list_commands":
            return self._protocol.list_commands()
        if command == "get_status":
            return self.get_status()
        if command == "get_settings":
            return self.get_settings()
        if command == "get_device_id":
            return self._get_device_id()
        if command == "get_version":
            return self.get_version()

        if not command:
            command = self._protocol.DEFAULT_COMMAND

        # Send command and receive data
        full_command = self._protocol.get_full_command(command)
        log.info(f"full command {full_command} for command {command}")
        if full_command is None:
            log.error(f"full_command not found for {command} in protocol {self._protocol._protocol_id}")
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
        # if isinstance(raw_response, dict):
        #     return raw_response

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

    def _get_device_id(self) -> dict:
        # Try to work out the 'id' for this device
        # need to know what port/porttype we are connected to
        # then ...ABC

        # return get_device_id()
        _id = ""
        if self._protocol.ID_COMMANDS:
            # print(self._protocol.ID_COMMANDS)
            for line in self._protocol.ID_COMMANDS:
                if isinstance(line, tuple):
                    command = line[0]
                else:
                    command = line
                result = self.run_command(command)
                if isinstance(line, tuple):
                    key = line[1]
                else:
                    key = list(result).pop()

                # last_key = list(result).pop()
                value = result[key][0]

                if not _id:
                    _id = f"{value}"
                else:
                    _id = f"{_id}:{value}"
            log.info(f"DeviceId: {_id}")
            return {"_command": "Get Device ID", "_command_description": "Generate a device id", "DeviceID": [_id, ""]}
        else:
            return {
                "_command": "Get Device ID",
                "_command_description": "Generate a device id",
                "DeviceID": ["getDeviceId not supported for this protocol", ""],
            }

    def get_version(self) -> dict:
        return {
            "_command": "Get Version",
            "_command_description": "Output the mpp-solar software version",
            "MPP-Solar Software Version": [__version__, ""],
        }
