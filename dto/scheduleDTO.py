from pydantic import BaseModel
from .commandScheduleDTO import CommandScheduleDTO
from .deviceDTO import DeviceDTO

class ScheduleDTO(BaseModel):
    loopDuration: int
    device: DeviceDTO
    schedulesCommands: list[CommandScheduleDTO]
