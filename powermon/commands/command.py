""" commands / command.py """
import logging
from enum import Enum
from datetime import date, datetime, timedelta  # pylint: disable=W0611 # noqa: 401

from powermon.commands.command_definition import CommandDefinition
from powermon.commands.result import Result, ResultType, ResultError
from powermon.commands.trigger import Trigger
from powermon.dto.commandDTO import CommandDTO
from powermon.errors import ConfigError, InvalidResponse, InvalidCRC, CommandExecutionFailed
from powermon.outputs import OutputType, multiple_from_config
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.outputs.api_mqtt import ApiMqtt

log = logging.getLogger("Command")


class CommandType(Enum):
    """ enum of valid types of Results """
    VICTRON_PING = 1
    VICTRON_GET_FW = 3
    VICTRON_GET_ID = 4
    VICTRON_RESTART = 6
    VICTRON_GET = 7
    VICTRON_SET = 8
    VICTRON_ASYNC = 'A'
    VICTRON_LISTEN = 'L'
    SERIAL_READONLY = 'serial_readonly'
    SERIAL_READ_UNTIL_DONE = 'serial_read_util_done'
    PI18_QUERY = 'pi18_query'
    PI18_SETTER = 'pi18_setter'
    JKSERIAL_SETTER = 'jkserial_setter'
    JKSERIAL_READ = 'jkserial_read'
    JKSERIAL_ACTIVATION = 'jkserial_activation'


class Command():
    """
    Command object, holds the details of the command, including:
    - command code
    - command type
    - command definition (inc overrides)
    - trigger
    - outputs
    """
    def __str__(self):
        if self.code is None:
            return "empty command object"

        if isinstance(self.trigger, Trigger):
            last_run = self.trigger.get_last_run()
            next_run = self.trigger.get_next_run()
        else:
            last_run = ""
            next_run = ""

        _outs = ""
        for output in self.outputs:
            _outs += str(output)

        return f"Command: {self.code=} {self.full_command=}, {self.command_type=}, \
            [{_outs=}], {last_run=}, {next_run=}, {str(self.trigger)}, {str(self.command_definition)} {self.override=} {self.template=}"

    def __init__(self, code: str, commandtype: str, outputs: list[AbstractOutput], trigger: Trigger):
        self.code = code
        self.command_type = commandtype
        self.outputs: list[AbstractOutput] = outputs
        self.trigger: Trigger = trigger

        self.command_definition: CommandDefinition
        self.template: str = None
        self.full_command: str = None
        self.override: str

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
        template = None
        if commandtype == 'templated':
            log.debug("got a templated command: %s", code)
            template = code
            try:
                code = eval(template)  # pylint: disable=W0123
            except SyntaxError as ex:
                print(ex)
                return
        override = config.get("override", None)
        # if override is not None:
        #     print("override: %s" % override)
        outputs = multiple_from_config(config.get("outputs", ""))
        trigger = Trigger.from_config(config=config.get("trigger"))
        command_object = cls(code=code, commandtype=commandtype, outputs=outputs, trigger=trigger)
        command_object.override = override
        command_object.template = template
        return command_object

    @classmethod
    def from_dto(cls, command_dto: CommandDTO) -> "Command":
        """ build object from data transfer object """
        trigger = Trigger.from_dto(command_dto.trigger)
        command = cls(code=command_dto.command_code, commandtype="basic", outputs=[], trigger=trigger)
        outputs = []
        for output_dto in command_dto.outputs:
            if output_dto.type == OutputType.API_MQTT:
                outputs.append(ApiMqtt.from_dto(output_dto))
        command.outputs = outputs
        return command

    @classmethod
    def from_code(cls, command_code) -> "Command":
        """ build object from just a code """
        return cls(code=command_code, commandtype="basic", outputs=[], trigger=None)

    def build_result(self, raw_response=None, protocol=None) -> Result:
        """ build a result object from the raw_response """
        log.debug("build_result: for command with 'code: %s, command_definition: %s'", self.code, self.command_definition)
        try:
            # check response is valid
            protocol.check_valid(raw_response, self.command_definition)
            # check crc is correct
            protocol.check_crc(raw_response, self.command_definition)
            # trim response
            trimmed_response = protocol.trim_response(raw_response, self.command_definition)
            # split response
            responses = protocol.split_response(trimmed_response, self.command_definition)
            # build the Result object
            result = Result(command=self, raw_response=raw_response, responses=responses)
        except (InvalidResponse, InvalidCRC, CommandExecutionFailed) as e:
            result = ResultError(command=self, raw_response=e, responses=[e.__context__, str(e)])
            result.result_type = ResultType.ERROR
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
        return getattr(self, "_command_definition", None)

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
    def override(self):
        """ dict of override options """
        # use getattr and return None if _override not set
        return getattr(self, "_override", None)

    @override.setter
    def override(self, value):
        self._override = value

    @property
    def outputs(self) -> list[AbstractOutput]:
        """ a list of output objects """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs: list[AbstractOutput]):
        self._outputs = outputs

    def is_due(self):
        """ is this command due to run? """
        if isinstance(self.trigger, Trigger):
            return self.trigger.is_due()
        # no trigger, so always run?
        return True

    def touch(self):
        """ update trigger run times and re-expand templates """
        if isinstance(self.trigger, Trigger):
            self.trigger.touch()
        # re-eval template if needed
        if self.command_type == 'templated':
            log.debug("updating templated command: %s", self.template)
            try:
                self.code = eval(self.template)  # pylint: disable=W0123
                log.info("templated command now: %s", self.code)
                # print(self.template)
                # print(self.code)
            except SyntaxError as ex:
                print(ex)
                return

    def to_dto(self):
        """ return the command data transfer object """
        return CommandDTO(
            command_code=self.code,
            device_id="not set",
            result_topic=self.outputs[0].topic,
            trigger=self.trigger.to_dto(),
            outputs=[output.to_dto() for output in self.outputs],
        )
