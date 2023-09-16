import logging
import random

from powermon.dto.portDTO import PortDTO
from powermon.commands.result import Result
from powermon.ports.abstractport import AbstractPort
from powermon.protocols import get_protocol_definition
from powermon.commands.command import Command

log = logging.getLogger("test")


class TestPort(AbstractPort):
    @classmethod
    def fromConfig(cls, config=None):
        log.debug(f"building test port. config:{config}")
        response_number = config.get("response_number", None)
        # get protocol handler, default to PI30 if not supplied
        protocol = get_protocol_definition(protocol=config.get("protocol", "PI30"))
        return cls(response_number=response_number, protocol=protocol)

    def __init__(self, response_number, protocol):
        super().__init__(protocol=protocol)
        self.response_number = response_number

    def __str__(self):
        return "Test port"

    def toDTO(self) -> PortDTO:
        dto = PortDTO(type="test", protocol=self.get_protocol().toDTO())
        return dto

    def connect(self) -> int:
        log.debug("Test port connected")
        return 1

    def disconnect(self) -> None:
        log.debug("Test port disconnected")
        return

    def send_and_receive(self, command: Command) -> Result:
        command_defn = command.command_definition
        
        result = Result(command.code)

        if command_defn is not None:
            # Have test data defined, so use that
            number_of_test_responses = len(command_defn["test_responses"])
            if self.response_number is not None and self.response_number < number_of_test_responses:
                self._test_data = command_defn["test_responses"][self.response_number]
            else:
                self._test_data = command_defn["test_responses"][random.randrange(number_of_test_responses)]
        else:
            # No test responses defined
            log.warn("Testing a command with no test responses defined")
            self._test_data = None
        response = self._test_data
        log.debug(f"Raw response {response}")
        result.raw_response = response
        return result
    