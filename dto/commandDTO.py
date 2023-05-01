from pydantic import BaseModel

class CommandDTO(BaseModel):
    command: str
    commandType: str