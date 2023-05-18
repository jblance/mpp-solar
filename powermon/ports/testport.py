import logging
import random

from powermon.dto.portDTO import PortDTO
from powermon.ports.abstractport import AbstractPort

log = logging.getLogger("test")


class TestPort(AbstractPort):
    def __init__(self, config=None):
        super().__init__(config)
        log.debug(f"Initializing test port. config:{config}")

    def __str__(self):
        return "Test port"

    def toDTO(self) -> PortDTO:
        dto = PortDTO(type="test", protocol=self.protocol.toDTO())
        return dto

    def protocol(self):
        return super().protocol()

    def connect(self) -> None:
        log.debug("Test port connected")
        return

    def disconnect(self) -> None:
        log.debug("Test port disconnected")
        return

    def send_and_receive(self, command) -> dict:
        command_defn = self.protocol.get_command_defn(command)

        if command_defn is not None:
            # Have test data defined, so use that
            number_of_test_responses = len(command_defn["test_responses"])
            self._test_data = command_defn["test_responses"][random.randrange(number_of_test_responses)]
        else:
            # No test responses defined
            log.warn("Testing a command with no test responses defined")
            self._test_data = None
        response = self._test_data
        log.debug(f"Raw response {response}")
        return response
