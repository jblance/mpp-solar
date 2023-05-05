from pydantic import BaseModel
from .scheduleDTO import ScheduleDTO
from .deviceDTO import DeviceDTO

class PowermonDTO(BaseModel):
    name: str
    loopDuration: int
    device: DeviceDTO
    schedulesCommands: list[ScheduleDTO]
