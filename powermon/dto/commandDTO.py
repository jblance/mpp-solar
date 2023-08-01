from pydantic import BaseModel
from .triggerDTO import TriggerDTO


# TODO: update
class CommandDTO(BaseModel):
    command: str
    result_topic: str
    trigger: TriggerDTO
