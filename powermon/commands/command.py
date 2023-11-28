""" commands / command.py """
import logging

from powermon.commands.command_definition import CommandDefinition
# from powermon.commands.result import ResultType
from powermon.commands.parameter import Parameter
# from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition
from powermon.commands.result import Result
from powermon.commands.trigger import Trigger
from powermon.dto.commandDTO import CommandDTO
from powermon.outputs import OutputType, getOutputs
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.outputs.api_mqtt import ApiMqtt

# from time import localtime, strftime


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
            [{_outs=}], {last_run=}, {next_run=}, {str(self.trigger)}, {self.command_definition=}"

    def __init__(self, code: str, commandtype: str, outputs: list[AbstractOutput], trigger: Trigger):
        self.code = code
        self.command_description = "Not set"
        self.type = commandtype
        self.set_outputs(outputs)

        self.trigger: Trigger = trigger

        self.full_command = None
        self.command_definition: CommandDefinition = None
        self.device_id = None  # TODO: shouldnt need this
        log.debug(self)

    @classmethod
    def from_config(cls, config=None) -> "Command":
        """build object from config dict"""
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

    def build_result(self, raw_response=None, protocol=None) -> Result:
        log.debug(f"build_result: code:{self.code}, command_definition:{self.command_definition}")
        trimmed_response = protocol.check_response_and_trim(raw_response)
        result = Result(
            self.code, result_type=self.command_definition.result_type,
            reading_definitions=self.get_reading_definitions(),
            parameters=self.command_definition.parameters, raw_response=trimmed_response
        )
        return result

    def set_full_command(self, full_command):
        """store the full command"""
        self.full_command = full_command

    def get_full_command(self) -> str | None:
        """return the full command, including CRC and/or headers"""
        return self.full_command

    def set_command_definition(self, command_definition: CommandDefinition):
        """store the definition of the command"""
        if command_definition is None:
            raise ValueError("CommandDefinition cannot be None")

        # Check if the definition is valid for the command
        if command_definition.is_command_code_valid(self.code) is False:
            raise ValueError(f"Command code {self.code} is not valid for command definition regex {command_definition.regex}")
        self.command_definition = command_definition
        self.command_description = command_definition.description

        # set command description in each of the outputs
        # QUESTION: why, cant we just pass the command object?
        for output in self.outputs:
            output.formatter.set_command_description(self.command_description)

    def get_reading_definitions(self) -> list[ReadingDefinition]:
        return self.command_definition.reading_definitions

    def set_outputs(self, outputs: list[AbstractOutput]):
        self.outputs = outputs
        for output in self.outputs:
            output.set_command(self.code)  # TODO: shouldnt need this

    def set_device_id(self, device_id):  # TODO: shouldnt need this
        self.device_id = device_id
        for output in self.outputs:
            output.set_device_id(device_id)

    def get_parameters(self) -> dict[str, Parameter]:
        return self.command_definition.parameters



    @classmethod
    def from_DTO(cls, command_dto: CommandDTO) -> "Command":
        trigger = Trigger.from_DTO(command_dto.trigger)
        command = cls(code=command_dto.command_code, commandtype="basic", outputs=[], trigger=trigger)
        outputs = []
        for output_dto in command_dto.outputs:
            if output_dto.type == OutputType.API_MQTT:
                outputs.append(ApiMqtt.from_DTO(output_dto))
        command.set_outputs(outputs=outputs)
        return command

    def is_due(self):
        """is this command due to run?"""
        return self.trigger.is_due()

    def touch(self):
        self.trigger.touch()

    def to_dto(self):
        return CommandDTO(
            command_code=self.code,
            device_id=self.device_id,
            result_topic=self.outputs[0].get_topic(),
            trigger=self.trigger.to_dto(),
            outputs=[output.to_dto() for output in self.outputs],
        )
