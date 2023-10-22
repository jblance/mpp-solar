from typing import Optional

from pydantic import BaseModel

from .portDTO import PortDTO
from .commandDTO import CommandDTO


class DeviceDTO(BaseModel):
    device_id: str
    model: Optional[str]
    manufacturer: Optional[str]
    port: PortDTO
    commands: list[CommandDTO]
