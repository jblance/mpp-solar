from pydantic import BaseModel
#from powermon.dto.response_definition_dto import ResponseDefinitionDTO


class CommandDefinitionDTO(BaseModel):

    command_code: str
    description: str
    help_text: str | None
    response_type: str | None
    responses: list | None
    #test_responses : list[bytes] | None
    regex : str | None
