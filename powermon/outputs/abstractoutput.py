from abc import ABC, abstractmethod
import logging
from strenum import LowercaseStrEnum
from enum import auto

from powermon.libs.mqttbroker import MqttBroker
from powermon.formats.abstractformat import AbstractFormat
from powermon.dto.outputDTO import OutputDTO


from powermon.libs.mqttbroker import MqttBroker
from powermon.formats.abstractformat import AbstractFormat



log = logging.getLogger("Output")

class OutputType(LowercaseStrEnum):
    API_MQTT = auto()
    MQTT = auto()
    SCREEN = auto()

class AbstractOutput(ABC):

    def __init__(self, formatter : AbstractFormat):
        self.formatter = formatter

    def set_formatter(self, formatter : AbstractFormat):
        return NotImplemented

    @abstractmethod
    def process(self, result):
        pass

    def set_mqtt_broker(self, mqtt_broker: MqttBroker):
        pass

    def set_command(self, command_name):
        pass

    def set_device_id(self, device_id):
        pass
    
    def to_DTO(self):
        return NotImplemented
    
        
    