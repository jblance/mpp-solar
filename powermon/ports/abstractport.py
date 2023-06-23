import logging
from abc import ABC, abstractmethod
from enum import auto

from strenum import LowercaseStrEnum

from powermon.libs.result import Result


log = logging.getLogger("Port")


class PortType(LowercaseStrEnum):
    UNKNOWN = auto()
    TEST = auto()
    USB = auto()
    ESP32 = auto()
    SERIAL = auto()
    JKBLE = auto()
    MQTT = auto()
    VSERIAL = auto()
    DALYSERIAL = auto()
    BLE = auto()


class AbstractPort(ABC):
    @abstractmethod
    def connect(self) -> None:
        log.debug("Port connect not implemented")
        return

    @abstractmethod
    def disconnect(self) -> None:
        log.debug("Port disconnect not implemented")
        return

    @abstractmethod
    def send_and_receive(self, result) -> Result:
        raise NotImplementedError

    @abstractmethod
    def toDTO(self):
        raise NotImplementedError

    def run_command(self, command):
        # takes a command object, runs the command and returns a result object (replaces process_command)
        log.debug(f"Command {command}")
        # update run times
        command.touch()
        # update full_command - expand any template / add crc etc
        # updates every run incase something has changed
        command.full_command = self.protocol.get_full_command(command.name)
        result = Result(command)
        # run the command via the 'send_and_receive port function
        result = self.send_and_receive(result)
        log.debug(f"after send_and_receive {result}")
        return result

    # def process_command(self, command):
    #     # Band-aid solution, need to reduce what is sent
    #     log.debug(f"Command {command}")
    #     full_command = self.protocol.get_full_command(command)
    #     log.debug(f"Full Command {full_command}")

    #     raw_response = self.send_and_receive(command)
    #     log.debug(f"Send and Receive Response {raw_response}")

    #     # Handle errors
    #     # Maybe there should a decode for ERRORs and WARNINGS...
    #     # Some inverters return the command if the command is unknown:
    #     if raw_response == full_command:
    #         return {
    #             "ERROR": [
    #                 f"Inverter returned the command string for {command} - the inverter didnt recognise this command",
    #                 "",
    #             ]
    #         }
    #     # dict is returned on exception
    #     # QUESTION: What case is this covering?
    #     if isinstance(raw_response, dict):
    #         return raw_response

    #     # Decode response
    #     decoded_response = self.protocol.decode(raw_response, command)
    #     log.info(f"Decoded response {decoded_response}")

    #     return decoded_response
