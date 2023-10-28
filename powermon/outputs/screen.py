import logging
from powermon.formats.abstractformat import AbstractFormat

from powermon.outputs.abstractoutput import AbstractOutput
from powermon.dto.outputDTO import OutputDTO
from powermon.commands.result import Result

log = logging.getLogger("screen")


class Screen(AbstractOutput):
    def __init__(self):
        self.name = "Screen"

    def __str__(self):
        return "outputs.Screen: outputs the results to the screen as per the formatter supplied"
        

    def set_formatter(self, formatter: AbstractFormat):
        self.formatter = formatter
        
    def to_dto(self) -> OutputDTO:
        return OutputDTO(type=self.name, format=self.formatter.to_dto())

    def process(self, result: Result):
        log.info("Using output sender: screen")
        log.debug("formatter: %s" % self.formatter)

        formatted_data = self.formatter.format(result)
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
        return cls()