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
        log.debug(f"send_and_receive: port {self._serial_port}, baudrate {self._serial_baud}")
        try:
            with serial.serial_for_url(self._serial_port, self._serial_baud) as s:
                log.debug("send_and_receive: Executing command via dalyserialio...")
                s.timeout = 1
                s.write_timeout = 1
                s.flushInput()
                s.flushOutput()
                s.write(full_command)
                # read until no more data
                for _ in range(10):
                    time.sleep(0.1)  # give serial port time to receive the data
                    _line = s.readline()
                    if _line != "":
                        # got some data
                        response_line += _line
                    else:
                        # data finished
                        break

                log.debug("send_and_receive: serial response was: %s", response_line)
                return response_line
        except Exception as e:
            log.warning(f"send_and_receive: Serial read error: {e}")
        log.info("Command execution failed")
        return {"ERROR": ["Serial command execution failed", ""]}
