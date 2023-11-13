""" dto / commandDTO.py """
from pydantic import BaseModel
from .triggerDTO import TriggerDTO
from .outputDTO import OutputDTO


class CommandDTO(BaseModel):
    """ model/allowed elements for a command data transfer object """
    command_code: str
    device_id: str
    result_topic: None | str = None
    trigger: TriggerDTO
    outputs: list[OutputDTO]

    @classmethod
    def run_api_command(cls, command_code: str, device_id: str) -> "CommandDTO":
        # FIXME: whats going on here - needs moving
        command_dto : CommandDTO = CommandDTO(
            command_code=command_code,
            device_id=device_id,
            result_topic=cls.get_command_result_topic().format(device_id=device_id, command_name=command_code),
            trigger=TriggerDTO(
                trigger_type="once",
                value="0"
                ),
            outputs=[])
        return command_dto

    @classmethod
    def get_command_result_topic(cls) -> str:
        # FIXME: needs moving and fixing (to return config value)
        return "powermon/{device_id}/results/{command_name}"
