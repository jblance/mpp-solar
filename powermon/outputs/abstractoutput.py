""" outputs / abstractoutput.py """
import logging
from abc import ABC, abstractmethod

# from powermon.libs.mqttbroker import MqttBroker
from powermon.commands.result import Result
from powermon.dto.outputDTO import OutputDTO
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("Output")


class AbstractOutput(ABC):
    """ base class for all output modules """
    def __init__(self, name=None) -> None:
        self.name = name
        self.command_code : str = "not_set"
        self.device_id : str = "not_set"
        self.topic = None
        self.formatter = None

    def set_formatter(self, formatter : AbstractFormat):
        """ set the formatter for this output """
        self.formatter = formatter

    @abstractmethod
    def process(self, result: Result, mqtt_broker=None):
        """ entry point of any output class """
        raise NotImplementedError("need to implement process function")

    def set_command(self, command_name):
        """ set the command_code """
        self.command_code = command_name

    def set_device_id(self, device_id):
        """ store the device_id """
        self.device_id = device_id

    def set_topic(self, topic):
        self.topic = topic

    def get_topic(self):
        return self.topic

    def to_dto(self) -> OutputDTO:
        """ convert output object to a data transfer object """
        if self.formatter is None:
            format_dto = "None"
        else:
            format_dto = self.formatter.to_dto()
        return OutputDTO(type=self.name, format=format_dto)
