from pydantic import BaseModel
from .triggerDTO import TriggerDTO
from .outputDTO import OutputDTO


class CommandDTO(BaseModel):
    command: str
    device_id: str
    result_topic: str
    trigger: TriggerDTO
    outputs: list[OutputDTO]

    @classmethod
    def run_api_command(cls, command_code: str, device_id: str) -> "CommandDTO":
        command_dto : CommandDTO = CommandDTO(
            command=command_code, 
            device_id=device_id,
            result_topic=f"powermon/{device_id}/result/{command_code}", 
            trigger=TriggerDTO(
                trigger_type="once",
                value="0"
                ),
            outputs=[])
        return command_dto