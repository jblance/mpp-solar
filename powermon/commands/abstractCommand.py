from abc import ABC, abstractmethod
from powermon.dto.commandDTO import CommandDTO
import logging


log = logging.getLogger("Command")

class CommandType():
    POLL = "poll"

class AbstractCommand(ABC):
    def __init__(self,  schedule_name, outputs, port):
        self.schedule_name = schedule_name
        self.outputs = outputs
        self.port = port

    def get_schedule_name(self):
        return self.schedule_name
    
    @abstractmethod
    def toDTO(self):
        pass

    @abstractmethod
    def run(self):
        pass