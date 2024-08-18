import logging
import serial
import time

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger("JKSerialIO")


class JKSerialIO(BaseIO):
    def __init__(self, *args, **kwargs) -> None:
        self._serial_port = get_kwargs(kwargs, "device_path")
        self._serial_baud = get_kwargs(kwargs, "serial_baud")
        self.no_data_counter = 0

    def pattern_matched(self, data):
        if len(data) >= 5:
            return (
                data[-5] == 0x68 and
                data[-4] == 0x00 and
                data[-3] == 0x00
                # data[-2] and data[-1] can be anything, so no specific check needed
            )
        return False

    def send_and_receive(self, *args, **kwargs) -> dict:
        full_command = get_kwargs(kwargs, "full_command")
        response_line = None
        log.debug(f"port {self._serial_port}, baudrate {self._serial_baud}")
        try:
            with serial.serial_for_url(self._serial_port, self._serial_baud) as s:
                log.debug("Executing command via jkserialio...")
                s.timeout = 1
                s.write_timeout = 1
                s.flushInput()
                s.flushOutput()
                s.write(full_command)
                time.sleep(0.1)

                while self.no_data_counter < 5:  # Try up to 5 times with no new data before exiting
                    if s.in_waiting > 0:
                        if response_line is None:
                            response_line = bytearray()
                        response_line.extend(s.read(s.in_waiting))
                        self.no_data_counter = 0  # Reset counter if data was received
        
                        # Check if the last 5 bytes match the pattern
                    if self.pattern_matched(response_line):
                        log.debug("JK serial end frame pattern matched.")
                        break  # Exit the loop if the pattern is matched
                else:
                    self.no_data_counter += 1
                    time.sleep(0.01)

                log.debug("serial response was: %s", response_line)
                return response_line
        except Exception as e:
            log.warning(f"Serial read error: {e}")
        log.info("Command execution failed")
        return {"ERROR": ["Serial command execution failed", ""]}
