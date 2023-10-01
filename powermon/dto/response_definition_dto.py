from pydantic import BaseModel
from powermon.commands.result import ResultType


class ResponseDefinitionDTO(BaseModel):
    response_type : ResultType
    responses: list