from typing import Optional
from pydantic import BaseModel



class ResultDTO(BaseModel):
    device_identifier: str
    command_code: str
    data: dict | list 