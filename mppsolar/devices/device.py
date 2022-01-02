# import importlib
import logging
from abc import ABC

import paho.mqtt.client as mqtt

from mppsolar.helpers import get_kwargs
from mppsolar.io import get_port
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
        self.command_requests = []
        self._name = get_kwargs(kwargs, "name")
        self._port = get_port(**kwargs)
        self._protocol = get_protocol(get_kwargs(kwargs, "protocol"))
        pause_loops = get_kwargs(kwargs, "pause_loops")
        if pause_loops is None:
            self._pause_loops = 0
        else:
            self._pause_loops = int(pause_loops)
        self._current_loop = 0

        self.commands = list(filter(None, get_kwargs(kwargs, "commands")))
        self.mqtt_output_topic = get_kwargs(kwargs, "mqtt_output_topic")
        self.outputs = get_kwargs(kwargs, "outputs")
        self.filter = get_kwargs(kwargs, "filter")
        self.excl_filter = get_kwargs(kwargs, "excl_filter")
        self.mqtt_broker = get_kwargs(kwargs, "mqtt_broker")
        self.commands_topic = get_kwargs(kwargs, "commands_topic")

        if(self.mqtt_broker is not None and self.commands_topic is not None):
            log.debug('Setup mqtt client')
            self.client = mqtt.Client()
            self.client.username_pw_set(self.mqtt_broker.username, self.mqtt_broker.password)
            self.client.connect(self.mqtt_broker.name, self.mqtt_broker.port)
            self.client.subscribe((self.commands_topic, 2))
            self.client.on_message = self.receive_command_request
            self.client.loop_start()

        log.debug(f"__init__ name {self._name}, port {self._port}, protocol {self._protocol}, loops {self._pause_loops}")

    def receive_command_request(self, client, userdata, message):
        command = str(message.payload.decode("utf-8"))
        log.debug(f"received command request: {command}")
        self.command_requests.append(command)

    def get_mqtt_output_topic(self):
        return self.mqtt_output_topic

    def get_filter(self):
        return self.filter

    def get_excl_filter(self):
        return self.excl_filter

    def __str__(self):
        """
        Build a printable representation of this class
        """
        return f"{self._classname} device - name: {self._name}, port: {self._port}, protocol: {self._protocol}, pause_loops: {self._pause_loops}"


    def get_commands(self):
        all_commands = self.commands + self.command_requests
        self.command_requests.clear()
        return all_commands

    def run_command(self, command) -> dict:
        """
        generic method for running a 'raw' command
        """
        log.info(f"Running command {command}")

        if self._current_loop < self._pause_loops:
            log.debug(f"on loop {self._current_loop} of {self._pause_loops} not running")
            self._current_loop += 1
            return None
        else:
            self._current_loop = 0;

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
