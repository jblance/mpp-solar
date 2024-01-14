""" outputs / api_mqtt.py """
import logging

# from powermon.dto.resultDTO import ResultDTO
from powermon.commands.result import Result
# from powermon.device import Device
from powermon.dto.commandDTO import CommandDTO
from powermon.dto.outputDTO import OutputDTO
from powermon.formats.simple import SimpleFormat
from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("ApiMqtt")


class ApiMqtt(AbstractOutput):
    """ docstring about ApiMqtt """  # TODO: update docstring and __str__
    def __str__(self):
        return "outputs .... TODO"

    def __init__(self):
        super().__init__(name="ApiMqtt")
        self.topic_base : str = "powermon/"
        self.topic_type : str = "results/"

    def get_topic(self) -> str:
        return CommandDTO.get_command_result_topic().format(device_id=self.device_id, command_name=self.command_code)

    def process(self, command=None, result: Result=None, mqtt_broker=None, device_info=None):
        # exit if no data
        if result.raw_response is None:
            return

        # exit if no broker
        if mqtt_broker is None:
            log.error("No mqtt broker supplied")
            raise RuntimeError("No mqtt broker supplied")

        result_dto = result.to_dto()
        mqtt_broker.publish(self.get_topic(), result_dto.json())

    @classmethod
    def from_dto(cls, dto: OutputDTO) -> "ApiMqtt":
        formatter = SimpleFormat.from_dto(dto.format)
        api_mqtt = cls()
        api_mqtt.set_formatter(formatter)

    @classmethod
    def from_config(cls, output_config) -> "ApiMqtt":
        log.debug("config: %s", output_config)  # TODO: sort from_config
        return cls()
