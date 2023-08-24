from abc import ABC, abstractmethod
import logging

from powermon.libs.mqttbroker import MqttBroker
from powermon.formats.abstractformat import AbstractFormat



log = logging.getLogger("Output")


class AbstractOutput(ABC):


    def set_formatter(self, formatter : AbstractFormat):
        return NotImplemented

    @abstractmethod
    def process(self, result):
        pass

    def set_mqtt_broker(self, mqtt_broker: MqttBroker):
        pass

    def set_command(self, command_name):
        pass

    