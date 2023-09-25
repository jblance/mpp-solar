from typing import Optional
from pydantic import BaseModel, Field

from .protocolDTO import ProtocolDTO


class PortDTO(BaseModel):
    type: str
    path: Optional[str]
    baud: int = Field(default=9600)
    protocol: ProtocolDTO
