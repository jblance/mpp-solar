import logging

from powermon.outputs.abstractoutput import AbstractOutput
from powermon.dto.resultDTO import ResultDTO
from powermon.commands.result import Result
from powermon.libs.mqttbroker import MqttBroker
from powermon.dto.outputDTO import OutputDTO
from powermon.dto.commandDTO import CommandDTO
from powermon.formats.simple import SimpleFormat

log = logging.getLogger("API_MQTT")


class API_MQTT(AbstractOutput):
    
    
    
    def __init__(self) -> None:
        self.command_code : str = "not_set"
        self.device_id : str = "not_set"

        self.topic_base : str = "powermon/"
        self.topic_type : str = "results/"

    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg powermon/status/total_output_active_power/value 1250"
    
    def set_formatter(self, formatter):
        self.formatter = formatter

    def set_command(self, command_name):
        self.command_code = command_name

    def set_mqtt_broker(self, mqtt_broker: MqttBroker):
        self.mqtt_broker = mqtt_broker

    def set_device_id(self, device_id):
        self.device_id = device_id

    def get_topic(self) -> str:
        return  CommandDTO.get_command_result_topic().format(device_id=self.device_id, command_name=self.command_code)

    def to_DTO(self) -> OutputDTO:
        return OutputDTO(type="api_mqtt", format=self.formatter.to_DTO())


    def process(self, result: Result):
        # exit if no data
        if result.raw_response is None:
            return

        # exit if no broker
        if self.mqtt_broker is None:
            log.error("No mqtt broker supplied")
            raise RuntimeError("No mqtt broker supplied")

        # build the messages...
        result_dto = ResultDTO(device_identifier=result.get_device_id(), command_code=result.command_code, data=result.get_responses())
        self.mqtt_broker.publish(self.get_topic(), result_dto.json())

        
    @classmethod
    def from_DTO(cls, dto: OutputDTO) -> "API_MQTT":
        formatter = SimpleFormat.from_DTO(dto.format)
        api_mqtt = cls()
        api_mqtt.set_formatter(formatter)
    
    @classmethod
    def from_config(cls, output_config) -> "API_MQTT":
        return cls()
