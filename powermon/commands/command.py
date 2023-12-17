""" commands / command.py """
import logging

from powermon.commands.command_definition import CommandDefinition
from powermon.commands.result import Result
from powermon.commands.trigger import Trigger
from powermon.dto.commandDTO import CommandDTO
from powermon.errors import ConfigError
from powermon.outputs import OutputType, multiple_from_config
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.outputs.api_mqtt import ApiMqtt

log = logging.getLogger("Command")


class Command():
    """
    Command object, holds the details of the command, including:
    - trigger
    - outputs
    """
    def __str__(self):
        if self.code is None:
            return "empty command object"

        last_run = self.trigger.get_last_run()
        next_run = self.trigger.get_next_run()

        _outs = ""
        for output in self.outputs:
            _outs += str(output)

        return f"Command: {self.code=} {self.full_command=}, {self.type=}, \
            [{_outs=}], {last_run=}, {next_run=}, {str(self.trigger)}, {str(self.command_definition)}"

    def __init__(self, code: str, commandtype: str, outputs: list[AbstractOutput], trigger: Trigger):
        self.code = code
        self.type = commandtype

        self.outputs = outputs
        self.trigger: Trigger = trigger

        self.full_command = None


    @classmethod
    def from_config(cls, config=None) -> "Command":
        """build object from config dict"""
        # need to have a config defined
        # minimum is
        # - command: QPI
        if not config:
            log.warning("Invalid command config")
            raise ConfigError("Invalid command config")
            # return None

        code = config.get("command")
        if code is None:
            log.info("command must be defined")
            raise ConfigError("command must be defined in config")
        commandtype = config.get("type", "basic")
        outputs = multiple_from_config(config.get("outputs", ""))
        trigger = Trigger.from_config(config=config.get("trigger"))
        return cls(code=code, commandtype=commandtype, outputs=outputs, trigger=trigger)

    @classmethod
    def from_DTO(cls, command_dto: CommandDTO) -> "Command":
        """ build object from data transfer object """
        trigger = Trigger.from_DTO(command_dto.trigger)
        command = cls(code=command_dto.command_code, commandtype="basic", outputs=[], trigger=trigger)
        outputs = []
        for output_dto in command_dto.outputs:
            if output_dto.type == OutputType.API_MQTT:
                outputs.append(ApiMqtt.from_DTO(output_dto))
        command.outputs = outputs
        return command

    def build_result(self, raw_response=None, protocol=None) -> Result:
        """ build a result object from the raw_response """
        log.debug("build_result: for command with 'code: %s, command_definition: %s'", self.code, self.command_definition)
        trimmed_response = protocol.check_response_and_trim(raw_response)
        result = Result(
            result_type=self.command_definition.result_type,
            command_definition=self.command_definition,
            raw_response=raw_response,
            trimmed_response=trimmed_response
        )
        return result

    @property
    def full_command(self) -> str | None:
        """return the full command, including CRC and/or headers"""
        return self._full_command

    @full_command.setter
    def full_command(self, full_command):
        """ store the full command """
        self._full_command = full_command

    @property
    def command_definition(self) -> CommandDefinition:
        """ the definition of this command """
        return self._command_definition

    @command_definition.setter
    def command_definition(self, command_definition: CommandDefinition):
        """store the definition of the command"""
        log.debug("Setting command_definition to: %s", command_definition)
        if command_definition is None:
            raise ValueError("CommandDefinition cannot be None")

        # Check if the definition is valid for the command
        if command_definition.is_command_code_valid(self.code) is False:
            raise ValueError(f"Command code {self.code} is not valid for command definition regex {command_definition.regex}")
        self._command_definition = command_definition

    @property
    def outputs(self) -> list[AbstractOutput]:
        """ a list of output objects """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs: list[AbstractOutput]):
        self._outputs = outputs

    def is_due(self):
        """ is this command due to run? """
        return self.trigger.is_due()

    def touch(self):
        """ update trigger run time """
        self.trigger.touch()

    def to_dto(self):
        """ return the command data transfer object """
        return CommandDTO(
            command_code=self.code,
            device_id="not set",
            result_topic=self.outputs[0].get_topic(),
            trigger=self.trigger.to_dto(),
            outputs=[output.to_dto() for output in self.outputs],
        )
