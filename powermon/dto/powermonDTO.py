from pydantic import BaseModel
from .scheduleDTO import ScheduleDTO
from .deviceDTO import DeviceDTO

class PowermonDTO(BaseModel):
    name: str
    loop_duration: int
    device: DeviceDTO
    schedules: list[ScheduleDTO]
