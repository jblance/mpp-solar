
from powermon.dto.commandDTO import CommandDTO
import logging


log = logging.getLogger("Command")

class Command:
    def __init__(self, command_query, commandType, schedule_name, outputs, port):
        self.command_query = command_query
        self.commandType = commandType
        self.schedule_name = schedule_name
        self.outputs = outputs
        self.port = port

    def __str__(self):
        return f"Command: {self.command_query}, CommandType: {self.commandType}, Outputs: {self.outputs}"
    
    def toDTO(self):
        dto = CommandDTO(
            command=self.command_query,
            commandType=self.commandType,
        )
        return dto
    
    def get_schedule_name(self):
        return self.schedule_name

    def run(self):
        log.debug(f"Running command: {self.command_query}")
        results = self.port.process_command(command=self.command_query)
        for output in self.outputs:
            log.debug(f"Output: {output}")
            output.output(data=results)
