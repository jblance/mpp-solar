from enum import StrEnum, auto
from time import sleep, time
import logging

log = logging.getLogger("schedule")

class Schedule:
    def __init__(self, scheduledCommands, loopDuration):
        self.scheduledCommands = scheduledCommands
        self.loopDuration = loopDuration
        self.inDelay = False
        self.delayRemaining = loopDuration

    def __str__(self):
        return f"Schedules: {self.scheduledCommands}"
    
    def runLoop(self):
        start_time = time()
        for scheduledCommand in self.scheduledCommands:
            if scheduledCommand.is_due():
                for command in scheduledCommand.commands:
                    command.run()
        # Small pause to ....
        sleep(0.1)
        elapsed_time = time() - start_time
        self.delayRemaining = self.delayRemaining - elapsed_time
        if self.delayRemaining > 0 and not self.inDelay:
            log.debug(f"delaying for {self.loopDuration}sec, delayRemaining: {self.delayRemaining}")
            self.inDelay = True
        if self.delayRemaining < 0:
            log.debug(f"Next loop: {self.loopDuration}, {self.delayRemaining}")
            self.inDelay = False
            self.delayRemaining = self.loopDuration + self.delayRemaining


class CommandScheduleType(StrEnum):
    LOOP = auto()
    TIME = auto()
    ONCE = auto()

class InformalScheduledCommandInterface:
    def is_due(self):
        raise NotImplementedError

class LoopCommandSchedule(InformalScheduledCommandInterface):
    def __init__(self, loopCount, commands):
        self.scheduleType = CommandScheduleType.LOOP
        self.loopCount = loopCount
        self.commands = commands

        self.currentLoopCount = 0

    def __str__(self):
        return f"ScheduleType: {self.scheduleType}, LoopCount: {self.loopCount}, Commands: {self.commands}"

    def is_due(self):
        if self.currentLoopCount < self.loopCount:
            self.currentLoopCount += 1
            return False
        else:
            self.currentLoopCount = 0
            return True


class Command:
    def __init__(self, command, commandType, outputs, port):
        self.command = command
        self.commandType = commandType
        self.outputs = outputs
        self.port = port

    def __str__(self):
        return f"Command: {self.command}, CommandType: {self.commandType}, Outputs: {self.outputs}"
    
    def run(self):
        log.debug(f"Running command: {self.command}")
        self.port.connect()
        results = self.port.process_command(command=self.command)
        for output in self.outputs:
            log.debug(f"Output: {output}")
            output.send(results)
    
class Output:
    def __init__(self, outputType, tag):
        self.outputType = outputType
        self.tag = tag

    def __str__(self):
        return f"OutputType: {self.outputType}, Tag: {self.tag}"
    
    def send(self, results):
        log.debug(f"Sending results: {results} to {self.outputType} with tag: {self.tag}")