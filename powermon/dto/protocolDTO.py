from pydantic import BaseModel
from typing import Optional


class ProtocolDTO(BaseModel):
    protocol_id: str
    commands: dict