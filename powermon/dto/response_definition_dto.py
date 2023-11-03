from pydantic import BaseModel
from powermon.commands.reading_definition import ReadingType


class ResponseDefinitionDTO(BaseModel):
    response_type : ReadingType
    responses: list