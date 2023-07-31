from pydantic import BaseModel
from .triggerDTO import TriggerDTO


# TODO: update
class CommandDTO(BaseModel):
    command: str
    trigger: TriggerDTO
