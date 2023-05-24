from typing import Optional

from pydantic import BaseModel

from .portDTO import PortDTO


class DeviceDTO(BaseModel):
    identifier: Optional[str]
    model: Optional[str]
    manufacturer: Optional[str]
    port: PortDTO
