from enum import StrEnum, auto
from time import sleep, time
import yaml
import json
import logging
from powermon.outputs import getOutputFromConfig

from powermon.model.dto.powermonDTO import PowermonDTO
from powermon.model.dto.commandDTO import CommandDTO
from powermon.model.dto.scheduleDTO import ScheduleDTO
from .device import Device
from powermon.libs.mqttbroker import MqttBroker


log = logging.getLogger("Schedule")

class Command:
    def __init__(self, command, commandType, outputs, port):
        self.command = command
        self.commandType = commandType
        self.outputs = outputs
        self.port = port

    def __str__(self):
        return f"Command: {self.command}, CommandType: {self.commandType}, Outputs: {self.outputs}"
    
    def toDTO(self):
        dto = CommandDTO(
            command=self.command,
            commandType=self.commandType,
        )
        return dto

    def run(self):
        log.debug(f"Running command: {self.command}")
        results = self.port.process_command(command=self.command)
        for output in self.outputs:
            log.debug(f"Output: {output}")
            output.output(data=results)


class CommandScheduleType(StrEnum):
    LOOP = auto()
    TIME = auto()
    ONCE = auto()

class InformalScheduledCommandInterface:
    def is_due(self):
        raise NotImplementedError
    

class LoopCommandSchedule(InformalScheduledCommandInterface):
    def __init__(self, name: str, loopCount: int, command: Command):
        self.scheduleType = CommandScheduleType.LOOP
        self.name = name
        self.loopCount = loopCount
        self.command = command

        self.currentLoopCount = loopCount # Set to loopCount so that the first loop will run

    def __str__(self):
        return f"ScheduleType: {self.scheduleType}, LoopCount: {self.loopCount}, Commands: {self.command}"

    def toDTO(self):
        dto = ScheduleDTO(name=self.name, type=self.scheduleType, loopCount=self.loopCount, command=self.command.toDTO())
        return dto

    def is_due(self):
        if self.currentLoopCount < self.loopCount:
            self.currentLoopCount += 1
            return False
        else:
            self.currentLoopCount = 1
            return True
        

class OneTimeCommandSchedule(InformalScheduledCommandInterface):
    def __init__(self, name: str, _command: Command):
        self.scheduleType = CommandScheduleType.ONCE
        self.name = name
        self.command = _command
        self.has_run = False
    
    def __str__(self):
        return f"ScheduleType: {self.scheduleType}, Commands: {self.command}"
    
    def toDTO(self):
        dto = ScheduleDTO(name=self.name, scheduleType=self.scheduleType, loopCount=0, command=self.command.toDTO())
        return dto
    
    def is_due(self):
        if self.has_run:
            log.debug("One time command has already run")
            return False
        else:
            log.debug("One time command is due to run")
            self.has_run = True
            return True    


class Coordinator:
    def __init__(self, name, scheduledCommands: list[InformalScheduledCommandInterface], loopDuration: int, mqtt_broker: MqttBroker, device: Device):
        self.name = name
        self.scheduledCommands = scheduledCommands
        self.loopDuration = loopDuration
        self.inDelay = False
        self.mqtt_broker = mqtt_broker
        self.device = device
        self.delayRemaining = loopDuration

    def __str__(self):
        return f"Schedule: {self.scheduledCommands}, {self.loopDuration}"
    
    def toDTO(self) -> PowermonDTO:
        commandSchedules = []
        for scheduledCommand in self.scheduledCommands:
            commandSchedules.append(scheduledCommand.toDTO())
        dto = PowermonDTO(name=self.name, loopDuration=self.loopDuration, device=self.device.toDTO(), schedulesCommands=commandSchedules)
        return dto

    
    def addOneTimeCommandFromConfig(self, scheduleConfig):
        schedule = ScheduleDTO(scheduleConfig)
        command = self.parseCommandConfig(scheduleConfig["command"], self.mqtt_broker, self.device)
        self.scheduledCommands.append(OneTimeCommandSchedule(schedule.name, {command}))


    #The hook for the port to connect before the main loops starts
    def beforeLoop(self):
        self.device.port.connect()
    
    def runLoop(self) -> bool:
        start_time = time()
        if(self.inDelay is False):
            for scheduledCommand in self.scheduledCommands:
                if scheduledCommand.is_due():
                    scheduledCommand.command.run()
                    
        # Small pause to ....
        sleep(0.5)
        elapsed_time = time() - start_time
        self.delayRemaining = self.delayRemaining - elapsed_time
        if self.delayRemaining > 0 and not self.inDelay:
            log.debug(f"delaying for {self.loopDuration}sec, delayRemaining: {self.delayRemaining}")
            self.inDelay = True
        if self.delayRemaining < 0:
            log.debug(f"Next loop: {self.loopDuration}, {self.delayRemaining}")
            self.inDelay = False
            self.delayRemaining = self.loopDuration

        #If loopDuration is 0, then we only want to run once
        if self.loopDuration == 0:
            log.debug("loopDuration is once, returning False")
            return False
        else:
            return True

    #TODO: this should follow the same pattern as the other parsers
    @classmethod
    def parseCommandConfig(cls, command_config : dict, computed_topic : str, schedule_name: str, mqtt_broker : MqttBroker, device: Device) -> Command:
        
        _command_query = command_config["command_query"]
        _commandType = command_config["type"]
        computed_topic = computed_topic + _command_query

        _outputs = []
        for outputConfig in command_config["outputs"]:
            _output = getOutputFromConfig(outputConfig, computed_topic, schedule_name, device, mqtt_broker)
            logging.debug(f"output: {_output}")
            _outputs.append(_output)

        return Command(_command_query, _commandType, _outputs, device.port)

    #TODO: this should follow the same pattern as the other parsers
    @classmethod
    def parseCoordinatorConfig(cls, config, device, mqtt_broker):
        logging.debug("parseCoordinatorConfig")
        logging.debug(f"config: {config}")
        _name = config["name"]
        _loopDuration = config["loop"]
        if(_loopDuration == "once"):
            _loopDuration = 0

        _schedules = []
        for schedule in config["schedules"]:
            _scheduleType = schedule["type"]
            _scheduleName = schedule["name"]
            if _scheduleType == CommandScheduleType.LOOP:
                _loopCount = schedule["loopCount"]
            elif _scheduleType == CommandScheduleType.TIME:
                _runTime = schedule["runTime"]

            computed_topic = f"powermon/{_name}/results/{_scheduleName}/"

            command_config = schedule["command"]
            _command = (cls.parseCommandConfig(command_config,computed_topic, _scheduleName, mqtt_broker, device))
            
            if _scheduleType == CommandScheduleType.LOOP:
                _schedules.append(LoopCommandSchedule(_scheduleName, _loopCount, _command))
            elif _scheduleType == CommandScheduleType.ONCE:
                _schedules.append(OneTimeCommandSchedule(_scheduleName, _command))
            else:
                raise KeyError(f"Undefined schedule type: {_scheduleType}")

        schedule = Coordinator(_name, _schedules, _loopDuration, mqtt_broker, device)
        return schedule



