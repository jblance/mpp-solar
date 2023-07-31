from pydantic import BaseModel


# TODO: update
class ResultDTO(BaseModel):
    device_identifier: str
    command: str
    formatted_data: list[str]