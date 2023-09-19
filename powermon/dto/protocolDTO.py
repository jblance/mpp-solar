from pydantic import BaseModel
from .command_definition_dto import CommandDefinitionDTO


class ProtocolDTO(BaseModel):
    protocol_id: str
    commands: dict[str, CommandDefinitionDTO]