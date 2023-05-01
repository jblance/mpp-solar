from pydantic import BaseModel
from .commandDTO import CommandDTO

class ScheduleDTO(BaseModel):
    name: str
    type: str
    loopCount: int
    command: CommandDTO
