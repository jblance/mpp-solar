from pydantic import BaseModel
from typing import Optional

from .protocolDTO import ProtocolDTO


class PortDTO(BaseModel):
    type: str
    path: Optional[str]
    baud: Optional[int]
    protocol: ProtocolDTO
