from abc import ABC, abstractmethod
from powermon.commands.command import Command

class ScheduleType():
    LOOP = "loop"
    ONCE = "once"

class AbstractSchedule(ABC):

    def __init__(self, name: str):
        self.name = name
        self.commands = list()

    @abstractmethod
    def is_due(self):
        pass

    def add_command(self, command : Command):
        if command.get_schedule_name() == self.name:
            self.commands.append(command)
        else:
            raise Exception(f"Command {command} is not for schedule {self.name}")
        
    def get_commands(self):
        return self.commands
        
    def runCommands(self):
        for command in self.commands:
            command.run()