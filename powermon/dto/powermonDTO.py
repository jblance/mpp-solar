from pydantic import BaseModel
from .deviceDTO import DeviceDTO


class PowermonDTO(BaseModel):
    name: str
    loop_duration: int
    device: DeviceDTO
