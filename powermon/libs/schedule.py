from enum import StrEnum, auto
from time import sleep, time
import yaml
import json
import logging
from powermon.outputs import getOutputFromConfig

from dto.scheduleDTO import ScheduleDTO
from dto.commandDTO import CommandDTO
from dto.commandScheduleDTO import CommandScheduleDTO
from .device import Device


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

    

class Schedule:
    def __init__(self, scheduledCommands, loopDuration, mqtt_broker, device: Device):
        self.scheduledCommands = scheduledCommands
        self.loopDuration = loopDuration
        self.inDelay = False
        self.mqtt_broker = mqtt_broker
        self.device = device

        if(loopDuration == "once"):
            self.delayRemaining = 0
        else:
            self.delayRemaining = loopDuration

    def __str__(self):
        return f"Schedule: {self.scheduledCommands}, {self.loopDuration}"
    
    def toDTO(self) -> ScheduleDTO:
        commandSchedules = []
        for scheduledCommand in self.scheduledCommands:
            commandSchedules.append(scheduledCommand.toDTO())
        dto = ScheduleDTO(loopDuration=self.loopDuration, device=self.device.toDTO(), schedulesCommands=commandSchedules)
        return dto

    
    def addOneTimeCommandFromConfig(self, commandConfig):
        command = self.parseCommandConfig(commandConfig, self.mqtt_broker, self.device)
        self.scheduledCommands.append(OneTimeCommandSchedule({command}))


    #The hook for the port to connect before the main loops starts
    def beforeLoop(self):
        self.device.port.connect()
    
    def runLoop(self) -> bool:
        start_time = time()
        if(self.inDelay is False):
            for scheduledCommand in self.scheduledCommands:
                if scheduledCommand.is_due():
                    for command in scheduledCommand.commands:
                        command.run()
                    
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

        if self.loopDuration == "once":
            log.debug("loopDuration is once, returning False")
            return False
        else:
            return True

    #TODO: this should follow the same pattern as the other parsers
    @classmethod
    def parseCommandConfig(cls, command, mqtt_broker, device) -> Command:
        
        _command = command["command"]
        _commandType = command["type"]
        _outputs = []
        for outputConfig in command["outputs"]:
            logging.debug(f"command: {command}")
            _output = getOutputFromConfig(outputConfig,device, mqtt_broker)
            logging.debug(f"output: {_output}")
            _outputs.append(_output)

        return Command(_command, _commandType, _outputs, device.port)

    #TODO: this should follow the same pattern as the other parsers
    @classmethod
    def parseScheduleConfig(cls, config, device, mqtt_broker):
        logging.debug("parseScheduleConfig")
        _loopDuration = config["loop"]

        _schedules = []
        for schedule in config["schedules"]:
            _scheduleType = schedule["type"]
            if _scheduleType == CommandScheduleType.LOOP:
                _loopCount = schedule["loopCount"]
            elif _scheduleType == CommandScheduleType.TIME:
                _runTime = schedule["runTime"]

            _commands = []
            for command in schedule["commands"]:
                _commands.append(cls.parseCommandConfig(command, mqtt_broker, device))
            
            if _scheduleType == CommandScheduleType.LOOP:
                _schedules.append(LoopCommandSchedule(_loopCount, _commands))
            elif _scheduleType == CommandScheduleType.ONCE:
                _schedules.append(OneTimeCommandSchedule(_commands))
            else:
                raise KeyError(f"Undefined schedule type: {_scheduleType}")

        schedule = Schedule(_schedules, _loopDuration, mqtt_broker, device)
        return schedule


class CommandScheduleType(StrEnum):
    LOOP = auto()
    TIME = auto()
    ONCE = auto()

class InformalScheduledCommandInterface:
    def is_due(self):
        raise NotImplementedError
    

class LoopCommandSchedule(InformalScheduledCommandInterface):
    def __init__(self, loopCount, commands: list):
        self.scheduleType = CommandScheduleType.LOOP
        self.loopCount = loopCount
        self.commands = commands

        self.currentLoopCount = loopCount # Set to loopCount so that the first loop will run

    def __str__(self):
        return f"ScheduleType: {self.scheduleType}, LoopCount: {self.loopCount}, Commands: {self.commands}"

    def toDTO(self):
        commandDTOs = []
        for command in self.commands:
            commandDTOs.append(command.toDTO())
        dto = CommandScheduleDTO(type=self.scheduleType, commands=commandDTOs)
        return dto

    def is_due(self):
        if self.currentLoopCount < self.loopCount:
            self.currentLoopCount += 1
            return False
        else:
            self.currentLoopCount = 1
            return True
        

class OneTimeCommandSchedule(InformalScheduledCommandInterface):
    def __init__(self, _commands):
        self.scheduleType = CommandScheduleType.ONCE
        self.commands = _commands
        self.has_run = False
    
    def __str__(self):
        return f"ScheduleType: {self.scheduleType}, Commands: {self.commands}"
    
    def toDTO(self):
        commandDTOs = []
        for command in self.commands:
            commandDTOs.append(command.toDTO())
        dto = CommandScheduleDTO(scheduleType=self.scheduleType, commands=commandDTOs)
        return dto
    
    def is_due(self):
        if self.has_run:
            log.debug("One time command has already run")
            return False
        else:
            log.debug("One time command is due to run")
            self.has_run = True
            return True


