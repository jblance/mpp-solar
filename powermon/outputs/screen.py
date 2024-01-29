""" outputs / screen.py """
import logging

from powermon.commands.result import Result
# from powermon.device import Device
# from powermon.dto.outputDTO import OutputDTO
# from powermon.formats.abstractformat import AbstractFormat
from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("screen")


class Screen(AbstractOutput):
    """outputs the results to the screen as per the formatter supplied """
    def __init__(self):
        super().__init__(name="Screen")

    def __str__(self):
        return "outputs.Screen: outputs the results to the screen as per the formatter supplied"

    def process(self, command=None, result: Result = None, mqtt_broker=None, device_info=None):
        log.info("Using output sender: screen")
        log.debug("formatter: %s, result: %s, mqtt_broker: %s, device_info: %s", self.formatter, result, mqtt_broker, device_info)

        formatted_data = self.formatter.format(command=command, result=result, device_info=device_info)
        if formatted_data is None:
            print("Nothing returned from data formatting")
            return

        for line in formatted_data:
            print(line)

        if result.error:
            print("Errors occurred during processing")
            for error in result.error_messages:
                print(error)

    @classmethod
    def from_config(cls, output_config) -> "Screen":
        """If we need to include any config for the Screen output but the processing here"""
        log.debug("config: %s", output_config)
        return cls()
