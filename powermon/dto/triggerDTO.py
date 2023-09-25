from pydantic import BaseModel


class TriggerDTO(BaseModel):
    trigger_type: str
    value: str | int