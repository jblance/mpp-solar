from pydantic import BaseModel


# TODO: update
class ResultDTO(BaseModel):
    result: list[str]