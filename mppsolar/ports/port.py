from abc import ABC, abstractmethod
import logging

# from time import sleep
log = logging.getLogger("Port")


class Port(ABC):
    @abstractmethod
    def send_and_receive(self, *args, **kwargs) -> dict:
        raise NotImplementedError

    def connect(self) -> None:
        log.debug("connect not implemented")
        return

    def disconnect(self) -> None:
        log.debug("disconnect not implemented")
        return

    def process_command(self, command, protocol):
        # Band-aid solution, need to reduce what is sent
        log.debug(f"Command {command}")
        full_command = protocol.get_full_command(command)

        raw_response = self.send_and_receive(
            command=command,
            full_command=full_command,
            protocol=protocol,
            command_defn=protocol.get_command_defn(command),
        )
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

        if isinstance(raw_response, dict):
            return raw_response

        # Decode response
        decoded_response = protocol.decode(raw_response, command)
        log.info(f"Decoded response {decoded_response}")

        return decoded_response
