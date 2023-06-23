import logging
import random

from powermon.dto.portDTO import PortDTO
from powermon.libs.result import Result
from powermon.ports.abstractport import AbstractPort
from powermon.protocols import get_protocol

log = logging.getLogger("test")


class TestPort(AbstractPort):
    @classmethod
    def fromConfig(cls, config=None):
        log.debug(f"building test port. config:{config}")
        response_number = config.get("response_number", None)
        # get protocol handler, default to PI30 if not supplied
        protocol = get_protocol(protocol=config.get("protocol", "PI30"))
        return cls(response_number=response_number, protocol=protocol)

    def __init__(self, response_number, protocol):
        self.response_number = response_number
        self.protocol = protocol

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

    def send_and_receive(self, result) -> Result:
        command_defn = result.command.command_defn

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
