from .abstractSchedule import AbstractSchedule
from .abstractSchedule import ScheduleType
from powermon.dto.scheduleDTO import ScheduleDTO

class LoopSchedule(AbstractSchedule):
    def __init__(self, name: str, loopCount: int):
        super().__init__(name)
        self.loopCount = loopCount
        self.currentLoopCount = loopCount # Set to loopCount so that the first loop will run

    def __str__(self):
        return f"ScheduleType: {self.scheduleType}, LoopCount: {self.loopCount}, Commands: {self.command}"

    def toDTO(self):
        _command_dtos = []
        for command in self.get_commands():
            _command_dtos.append(command.toDTO())
        dto = ScheduleDTO(name=self.name, type=ScheduleType.LOOP, loopCount=self.loopCount, commands=_command_dtos)
        return dto

    def is_due(self):
        if self.currentLoopCount < self.loopCount:
            self.currentLoopCount += 1
            return False
        else:
            self.currentLoopCount = 1
            return True