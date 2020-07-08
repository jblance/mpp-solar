import logging
from machine import UART
import time

from .baseio import BaseIO

log = logging.getLogger('powermon')


class ESP32IO(BaseIO):
    """
    Uses ESP32 ESP32 for  serial connection, sends command (multiple times if needed)
    and returns the byte_response
    """
    def __init__(self, serial_port, serial_baud=2400) -> None:
        self._serial_port = serial_port
        self._serial_baud = serial_baud

    def send_and_receive(self, command, show_raw, protocol) -> dict:
        log.info(f'ESP32 serial connection: executing {command}')
        full_command = protocol.get_full_command(command, show_raw)
        log.info(f'full command {full_command} for command {command}')

        response_line = None
        uart_no = self._serial_port.lower().split('esp')[1]
        log.debug(f'port {self._serial_port}, baudrate {self._serial_baud}, uart# {uart_no}')
        try:
            with UART(uart_no, self._serial_baud) as s:
                # Execute command multiple times, increase timeouts each time
                s.init(self._baud_rate, timeout=1000)
                s.write(full_command)
                time.sleep(0.5)  # give serial port time to receive the data
                response_line = s.readline()
                log.debug('esp32 serial response was: %s', response_line)
                decoded_response = protocol.decode(response_line)
                log.debug(f'Decoded response {decoded_response}')
                return decoded_response
        except Exception as e:
            log.warning("ESP32 Serial read error: {}".format(e))
        log.info('Command execution failed')
        return {'error': 'Serial command execution failed'}
