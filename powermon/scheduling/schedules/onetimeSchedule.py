from .abstractSchedule import AbstractSchedule
from .abstractSchedule import ScheduleType
from powermon.dto.scheduleDTO import ScheduleDTO


class OneTimeSchedule(AbstractSchedule):
    def __init__(self, name: str):
        super().__init__(name)
        self.has_run = False
        self.scheduleType = ScheduleType.LOOP

    def __str__(self):
        return f"ScheduleType: {self.scheduleType}, Commands: {self.commands}"

    def toDTO(self):
        _command_dtos = []
        for command in self.get_commands():
            _command_dtos.append(command.toDTO())
        dto = ScheduleDTO(name=self.name, type=ScheduleType.ONCE, loopCount=0, commands=_command_dtos)
        return dto

    def is_due(self):
        if self.has_run:
            return False
        else:
            self.has_run = True
            return True
