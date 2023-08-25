from typing import Optional

from pydantic import BaseModel

from .portDTO import PortDTO
from .commandDTO import CommandDTO


# TODO: update
class DeviceDTO(BaseModel):
    identifier: str
    model: Optional[str]
    manufacturer: Optional[str]
    port: PortDTO
    commands: list[CommandDTO]
