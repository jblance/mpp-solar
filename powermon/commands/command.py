"""command.py"""
import logging
from time import localtime, strftime

from powermon.commands.command_definition import CommandDefinition
from powermon.commands.response import Response
from powermon.commands.response_definition import ResponseDefinition
from powermon.commands.trigger import Trigger
from powermon.dto.commandDTO import CommandDTO
from powermon.outputs import getOutputs
from powermon.outputs.abstractoutput import AbstractOutput, OutputType
from powermon.outputs.api_mqtt import API_MQTT

log = logging.getLogger("Command")


class Command:
    """
    Command object, holds the details of the command, including:
    - trigger
    - outputs
    """

    def __init__(self, code: str, commandtype: str, outputs: list[AbstractOutput], trigger: Trigger):
        self.code = code
        self.command_description = "Not set"
        self.type = commandtype
        self.set_outputs(outputs)

        self.trigger: Trigger = trigger

        self.full_command = None
        self.command_definition: CommandDefinition = None
        self.device_id = None
        log.debug(self)

    def get_full_command(self) -> str | None:
        """return the full command, including CRC and/or headers"""
        return self.full_command

    def set_command_definition(self, command_definition: CommandDefinition):
        if command_definition is None:
            raise ValueError("CommandDefinition cannot be None")
        if command_definition.is_command_code_valid(self.code) == False:
            raise ValueError(f"Command code {self.code} is not valid for command definition regex {command_definition.regex}")
        self.command_definition = command_definition
        self.command_description = command_definition.description
        for output in self.outputs:
            output.formatter.set_command_description(self.command_description)

    def get_response_definitions(self) -> list[ResponseDefinition]:
        return self.command_definition.response_definitions

    def set_outputs(self, outputs: list[AbstractOutput]):
        self.outputs = outputs
        for output in self.outputs:
            output.set_command(self.code)

    def set_device_id(self, device_id):
        self.device_id = device_id
        for output in self.outputs:
            output.set_device_id(device_id)

    def set_full_command(self, full_command):
        self.full_command = full_command

    def validate_and_translate_raw_value(self, raw_value: str, index: int) -> list[Response]:
        if len(self.command_definition.response_definitions) <= index:
            raise IndexError(f"Index {index} is out of range for command {self.code}")
        response_definition: ResponseDefinition = self.command_definition.response_definitions[index]
        try:
            # The template should be passed in during construction since we will have that information already
            if response_definition.is_info():
                return response_definition.response_from_raw_values(self.code)
            else:
                return response_definition.response_from_raw_values(raw_value)
        except ValueError:
            error = Response(
                data_name=response_definition.get_description(), data_value=response_definition.get_invalid_message(raw_value), data_unit=""
            )
            error.is_valid = False
            return [error]

    def __str__(self):
        if self.code is None:
            return "empty command object"

        last_run = self.trigger.get_last_run()
        next_run = self.trigger.get_next_run()

        _outs = ""
        for output in self.outputs:
            _outs += str(output)

        return f"Command: {self.code=} {self.full_command=}, {self.type=}, [{_outs=}], {last_run=}, {next_run=}, {str(self.trigger)}, {self.command_definition=}"

    @classmethod
    def from_config(cls, config=None) -> "Command":
        # need to have a config defined
        # minimum is
        # - command: QPI
        if not config:
            log.warning("Invalid command config")
            raise TypeError("Invalid command config")
            # return None

        code = config.get("command")
        if code is None:
            log.info("command must be defined")
            raise TypeError("command must be defined")
        commandtype = config.get("type", "basic")
        outputs = getOutputs(config.get("outputs", ""))
        trigger = Trigger.fromConfig(config=config.get("trigger"))
        return cls(code=code, commandtype=commandtype, outputs=outputs, trigger=trigger)

    @classmethod
    def from_DTO(cls, command_dto: CommandDTO) -> "Command":
        trigger = Trigger.from_DTO(command_dto.trigger)
        command = cls(code=command_dto.command_code, commandtype="basic", outputs=[], trigger=trigger)
        outputs = []
        for output_dto in command_dto.outputs:
            if output_dto.type == OutputType.API_MQTT:
                outputs.append(API_MQTT.from_DTO(output_dto))
        command.set_outputs(outputs=outputs)
        return command

    def set_mqtt_broker(self, mqtt_broker):
        for output in self.outputs:
            output.set_mqtt_broker(mqtt_broker)

    def is_due(self):
        return self.trigger.is_due()

    def touch(self):
        self.trigger.touch()

    def to_dto(self):
        return CommandDTO(
            command_code=self.code,
            device_id=self.device_id,
            result_topic=self.outputs[0].get_topic(),
            trigger=self.trigger.to_DTO(),
            outputs=[output.to_DTO() for output in self.outputs],
        )
