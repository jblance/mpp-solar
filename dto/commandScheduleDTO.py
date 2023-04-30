from pydantic import BaseModel
from .commandDTO import CommandDTO

class CommandScheduleDTO(BaseModel):
    type: str
    commands: list[CommandDTO]
