from pydantic import BaseModel


# TODO: update
class CommandDTO(BaseModel):
    command: str
    commandType: str
