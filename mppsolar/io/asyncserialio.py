import logging
import serial
import time

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger("MPP-Solar")


class AsyncSerialIO(BaseIO):
    def __init__(self, *args, **kwargs) -> None:
        self._serial_port = get_kwargs(kwargs, "device_path")
        self._serial_baud = get_kwargs(kwargs, "serial_baud")
        self._records = get_kwargs(kwargs, "records")

    def send_and_receive(self, *args, **kwargs) -> dict:
        # full_command = get_kwargs(kwargs, "full_command")
        responses = b""
        log.debug(f"port {self._serial_port}, baudrate {self._serial_baud}, records {self._records}")
        try:
            with serial.serial_for_url(self._serial_port, self._serial_baud) as s:
                # log.debug(f"Executing command via serialio...")
                s.timeout = 1
                # s.write_timeout = 1
                # s.flushInput()
                # s.flushOutput()
                # s.write(full_command)
                # time.sleep(0.1)  # give serial port time to receive the data
                for _ in range(self._records):
                    response_line = s.read_until(b"\n")
                    log.debug("asyncserial response was: %s", response_line)
                    responses += response_line
                return responses
        except Exception as e:
            log.warning(f"AsyncSerial read error: {e}")
        log.info("Command execution failed")
        return {"ERROR": ["AsyncSerial command execution failed", ""]}
