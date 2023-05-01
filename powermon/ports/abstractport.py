from abc import ABC, abstractmethod
import logging
from enum import StrEnum, auto

from mppsolar.protocols.abstractprotocol import AbstractProtocol

# from time import sleep
log = logging.getLogger("Port")

class PortType(StrEnum):
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
    def __init__(self, protocol : AbstractProtocol):
        self.protocol = protocol

    @abstractmethod
    def connect(self) -> None:
        log.debug("Port connect not implemented")
        return

    @abstractmethod
    def disconnect(self) -> None:
        log.debug("Port disconnect not implemented")
        return

    @abstractmethod
    def send_and_receive(self, command) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    def toDTO(self):
        raise NotImplementedError

    # Question: Should we make this an abstract method?
    def process_command(self, command):
        # Band-aid solution, need to reduce what is sent
        log.debug(f"Command {command}")
        full_command = self.protocol.get_full_command(command)
        log.debug(f"Full Command {full_command}")

        raw_response = self.send_and_receive(command)
        log.debug(f"Send and Receive Response {raw_response}")

        # Handle errors
        # Maybe there should a decode for ERRORs and WARNINGS...
        # Some inverters return the command if the command is unknown:
        if raw_response == full_command:
            return {
                "ERROR": [
                    f"Inverter returned the command string for {command} - the inverter didnt recognise this command",
                    "",
                ]
            }
        # dict is returned on exception
        # Question: What case is this covering?
        if isinstance(raw_response, dict):
            return raw_response

        # Decode response
        decoded_response = self.protocol.decode(raw_response, command)
        log.info(f"Decoded response {decoded_response}")

        return decoded_response