from abc import ABC, abstractmethod
from powermon.commands.abstractCommand import AbstractCommand


class ScheduleType:
    LOOP = "loop"
    ONCE = "once"
    TIME = "time"


class AbstractSchedule(ABC):
    def __init__(self, name: str):
        self.name = name
        self.commands = list()

    @abstractmethod
    def is_due(self):
        pass

    @abstractmethod
    def toDTO(self):
        pass

    def add_command(self, command: AbstractCommand):
        if command.get_schedule_name() == self.name:
            self.commands.append(command)
        else:
            raise Exception(f"Command {command} is not for schedule {self.name}")

    def get_commands(self):
        return self.commands

    def runCommands(self):
        for command in self.commands:
            command.run()
