import logging
from time import localtime, strftime, time
from powermon.commands.trigger import Trigger
from powermon.outputs import getOutputs
from powermon.dto.commandDTO import CommandDTO
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.outputs.abstractoutput import OutputType
from powermon.outputs.api_mqtt import API_MQTT
from powermon.commands.commanddefinition import CommandDefinition

log = logging.getLogger("Command")


class Command:
    def __init__(self, code : str, commandtype: str, outputs: list[AbstractOutput], trigger : Trigger):

        self.code = code
        self.command_description = 'Not set'
        self.type = commandtype
        self.set_outputs(outputs)
        
        self.trigger = trigger

        self.last_run = None
        self.next_run = self.trigger.nextRun(command=self)
        self.full_command = None
        self.command_definition : dict[str, list] = {}
        self.device_id = None
        log.debug(self)
        
    def get_full_command(self) -> str | None:
        return self.full_command
    
    def set_command_definition(self, command_definition : dict):
        self.command_definition = command_definition
        self.command_description = command_definition["description"]
        for output in self.outputs:
            output.formatter.set_command_description(self.command_description)
    
    def set_outputs(self, outputs : list[AbstractOutput]):
        self.outputs = outputs
        for output in self.outputs:
            output.set_command(self.code)

    def set_device_id(self, device_id):
        self.device_id = device_id
        for output in self.outputs:
            output.set_device_id(device_id)

    def __str__(self):
        if self.code is None:
            return "empty command object"
        if self.last_run is None:
            last_run = "Not yet run"
        else:
            last_run = strftime("%d %b %Y %H:%M:%S", localtime(self.last_run))
        if self.next_run is None:
            next_run = "unknown"
        else:
            next_run = strftime("%d %b %Y %H:%M:%S", localtime(self.next_run))

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

    def dueToRun(self):
        return self.trigger.isDue(command=self)

    def touch(self):
        # store run time (as secs since epoch)
        self.last_run = time()
        # update next run time
        self.next_run = self.trigger.nextRun(command=self)

    def to_dto(self):
        return CommandDTO(
            command_code = self.code,
            device_id=self.device_id,
            result_topic = None,
            trigger = self.trigger.to_DTO(),
            outputs=[output.to_DTO() for output in self.outputs],
        )
