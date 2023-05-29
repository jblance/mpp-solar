from pydantic import BaseModel


# TODO: update
class ResultDTO(BaseModel):
    schedule_name: str
    result: str