from pydantic import BaseModel
from .commandDTO import CommandDTO


# TODO: remove
class ScheduleDTO(BaseModel):
    name: str
    type: str
    loopCount: int
    commands: list[CommandDTO]
