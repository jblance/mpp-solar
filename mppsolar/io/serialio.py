import logging
import serial
import time

from .baseio import BaseIO

log = logging.getLogger("MPP-Solar")


class SerialIO(BaseIO):
    def __init__(self, device_path, serial_baud) -> None:
        self._serial_port = device_path
        self._serial_baud = serial_baud

    def send_and_receive(self, full_command) -> dict:
        response_line = None
        log.debug(f"port {self._serial_port}, baudrate {self._serial_baud}")
        try:
            with serial.serial_for_url(self._serial_port, self._serial_baud) as s:
                log.debug(f"Executing command via serialio...")
                s.timeout = 1
                s.write_timeout = 1
                s.flushInput()
                s.flushOutput()
                s.write(full_command)
                time.sleep(0.1)  # give serial port time to receive the data
                response_line = s.read_until(expected=b"\r")
                log.debug("serial response was: %s", response_line)
                return response_line
        except Exception as e:
            log.warning(f"Serial read error: {e}")
        log.info("Command execution failed")
        return {"ERROR": ["Serial command execution failed", ""]}
