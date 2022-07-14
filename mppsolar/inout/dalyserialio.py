import logging
import serial
import time

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger("DalySerialIO")


class DalySerialIO(BaseIO):
    def __init__(self, *args, **kwargs) -> None:
        self._serial_port = get_kwargs(kwargs, "device_path")
        self._serial_baud = get_kwargs(kwargs, "serial_baud")

    def send_and_receive(self, *args, **kwargs) -> dict:
        full_command = get_kwargs(kwargs, "full_command")
        response_line = b""
        log.debug(f"port {self._serial_port}, baudrate {self._serial_baud}")
        try:
            with serial.serial_for_url(self._serial_port, self._serial_baud) as s:
                log.debug("Executing command via dalyserialio...")
                s.timeout = 0.5
                s.write_timeout = 1
                s.reset_input_buffer()
                s.reset_output_buffer()
                s.write(full_command)
                # read until no more data
                while True:
                    time.sleep(0.5)  # give serial port time to receive the data
                    to_read = s.in_waiting
                    log.debug(f"bytes waiting {to_read}")
                    if to_read == 0:
                        break
                    # got some data to read
                    response_line += s.read(to_read)

                log.debug("serial response was: %s", response_line)
                return response_line
        except Exception as e:
            log.warning(f"Serial read error: {e}")
        log.info("Command execution failed")
        return {"ERROR": ["Serial command execution failed", ""]}
