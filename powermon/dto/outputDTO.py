from pydantic import BaseModel
from .formatDTO import FormatDTO

class OutputDTO(BaseModel):
    type: str
    format: FormatDTO
