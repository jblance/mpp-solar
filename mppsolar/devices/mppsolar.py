import logging

from .device import AbstractDevice
from ..io.testio import TestIO
from ..io.testio import JkBleIO

log = logging.getLogger("MPP-Solar")


class mppsolar(AbstractDevice):
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"mppsolar __init__ args {args}")
        log.debug(f"mppsolar __init__ kwargs {kwargs}")
        super().__init__()
        self._name = kwargs["name"]
        self.set_port(**kwargs)
        self.set_protocol(**kwargs)
        log.debug(
            f"mppsolar __init__ name {self._name}, port {self._port}, protocol {self._protocol}"
        )

    def __str__(self):
        """
        Build a printable representation of this class
        """
        return (
            f"mppsolar device - name: {self._name}, port: {self._port}, protocol: {self._protocol}"
        )

    def run_command(self, command, show_raw=False) -> dict:
        """
        generic method for running a 'raw' command
        """
        log.info(f"Running command {command}")

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
            raw_response = self._port.send_and_receive(full_command, self._protocol)

        # Band-aid solution, can't really segregate TestIO from protocols w/o major rework of TestIO
        elif isinstance(self._port, TestIO):
            raw_response = self._port.send_and_receive(
                full_command, self._protocol.get_command_defn(command)
            )
        else:
            raw_response = self._port.send_and_receive(full_command)
        log.debug(f"Send and Receive Response {raw_response}")

        # Handle errors; dict is returned on exception
        # Maybe there should a decode for ERRORs and WARNINGS...
        if isinstance(raw_response, dict):
            return raw_response

        # Decode response
        decoded_response = self._protocol.decode(raw_response, show_raw, command)
        log.debug(f"Decoded response {decoded_response}")
        log.info(f"Decoded response {decoded_response}")

        return decoded_response

    def get_status(self, show_raw) -> dict:
        # Run all the commands that are defined as status from the protocol definition
        data = {}
        for command in self._protocol.STATUS_COMMANDS:
            data.update(self.run_command(command))
        return data

    def get_settings(self, show_raw) -> dict:
        # Run all the commands that are defined as settings from the protocol definition
        data = {}
        for command in self._protocol.SETTINGS_COMMANDS:
            data.update(self.run_command(command))
        return data
