from powermon.dto.commandDTO import CommandDTO
import logging

from powermon.commands.abstractCommand import AbstractCommand
from powermon.ports.abstractport import AbstractPort
from powermon.outputs.abstractoutput import AbstractOutput


log = logging.getLogger("Command")

class PollCommand(AbstractCommand):
    def __init__(self, command_query, commandType, schedule_name, outputs : list[AbstractOutput], port : AbstractPort):
        super().__init__(schedule_name, outputs, port)
        self.command_query = command_query
        self.commandType = commandType

    def toDTO(self):
        dto = CommandDTO(
            command=self.command_query,
            commandType=self.commandType,
        )
        return dto

    def run(self):
        log.debug(f"Running command: {self.command_query}")
        results = self.port.process_command(command=self.command_query)
        for output in self.outputs:
            log.debug(f"Output: {output}")
            output.output(data=results)