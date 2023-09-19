from pydantic import BaseModel
from powermon.protocols import ResponseType


class ResponseDefinitionDTO(BaseModel):
    response_type : ResponseType
    responses: list