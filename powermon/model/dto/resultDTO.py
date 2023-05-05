from pydantic import BaseModel

class ResultDTO(BaseModel):
    schedule_name: str
    result: str