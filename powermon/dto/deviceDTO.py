from typing import Optional

from pydantic import BaseModel

from .portDTO import PortDTO


# TODO: update
class DeviceDTO(BaseModel):
    identifier: Optional[str]
    model: Optional[str]
    manufacturer: Optional[str]
    port: PortDTO
