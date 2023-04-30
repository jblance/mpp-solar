from pydantic import BaseModel
from .portDTO import PortDTO

class DeviceDTO(BaseModel):
    name: str
    identifier: str
    model: str
    manufacturer: str
    port: PortDTO