from enum import StrEnum, auto

import yaml
import json
import logging
from powermon.outputs import getOutputFromConfig


from powermon.model.dto.commandDTO import CommandDTO
from powermon.model.dto.scheduleDTO import ScheduleDTO
from .command import Command
from powermon.libs.mqttbroker import MqttBroker


log = logging.getLogger("Schedule")


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




