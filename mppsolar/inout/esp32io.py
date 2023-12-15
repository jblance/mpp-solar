import logging
import time

from machine import UART

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger("ESP32IO")


class ESP32IO(BaseIO):
    """
    Uses ESP32 ESP32 for  serial connection, sends command (multiple times if needed)
    and returns the byte_response
    """

    def __init__(self, device_path, serial_baud=2400) -> None:
        self._serial_port = device_path
        self._serial_baud = serial_baud

    def send_and_receive(self, *args, **kwargs) -> dict:
        full_command = get_kwargs(kwargs, "full_command")
        log.info(f"ESP32 serial connection: executing {full_command}")

        response_line = None
        uart_no = self._serial_port.lower().split("esp")[1]
        log.debug(f"port {self._serial_port}, baudrate {self._serial_baud}, uart# {uart_no}")
        try:
            with UART(uart_no, self._serial_baud) as s:
                # Execute command multiple times, increase timeouts each time
                s.init(self._baud_rate, timeout=1000)
                s.write(full_command)
                time.sleep(0.5)  # give serial port time to receive the data
                response_line = s.readline()
                log.debug("esp32 serial response was: %s", response_line)
                return response_line
        except Exception as e:
            log.warning("ESP32 Serial read error: {}".format(e))
        log.info("Command execution failed")
        return {"ERROR": ["Serial command execution failed", ""]}
