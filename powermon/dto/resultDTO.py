from typing import Iterable
from pydantic import BaseModel



# TODO: update
class ResultDTO(BaseModel):
    device_identifier: str
    command_code: str
    data: dict 