from pydantic import BaseModel


class FormatDTO(BaseModel):
    type: str