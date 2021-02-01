import logging

from .device import AbstractDevice
from ..io.jkbleio import JkBleIO

log = logging.getLogger("MPP-Solar")


class jkbms(AbstractDevice):
    def __init__(self, *args, **kwargs) -> None:
        self._classname = "jkbms"
        super().__init__(*args, **kwargs)

    def run_command(self, command) -> dict:
        """
        jkbms method for running a 'raw' command
        """
        log.info(f"JKBMS Running command {command}")
        # this is duplicated from parent
        if self._protocol is None:
            log.error("Attempted to run command with no protocol defined")
            return {"ERROR": ["Attempted to run command with no protocol defined", ""]}
        if self._port is None:
            log.error(f"No communications port defined - unable to run command {command}")
            return {
                "ERROR": [
                    f"No communications port defined - unable to run command {command}",
                    "",
                ]
            }

        # Send command and receive data
        full_command = self._protocol.get_full_command(command)
        log.info(f"full command {full_command} for command {command}")

        # JkBleIO is very different from the others, only has protocol jk02 and jk04, maybe change full_command?
        if isinstance(self._port, JkBleIO):
            # need record type, SOR
            raw_response = self._port.send_and_receive(command=command, protocol=self._protocol)

            log.debug(f"Send and Receive Response {raw_response}")

            # Handle errors; dict is returned on exception
            # Maybe there should a decode for ERRORs and WARNINGS...
            if isinstance(raw_response, dict):
                return raw_response

            # Decode response
            decoded_response = self._protocol.decode(raw_response, command)
            log.info(f"Decoded response {decoded_response}")
            return decoded_response

        else:
            return super().run_command(command)
