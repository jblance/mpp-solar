import logging
import serial
import time

from .baseio import BaseIO

log = logging.getLogger('powermon')


class SerialIO(BaseIO):
    def __init__(self, serial_port, serial_baud=2400) -> None:
        self._serial_port = serial_port
        self._serial_baud = serial_baud

    def send_and_receive(self, command, show_raw, protocol) -> dict:
        full_command = protocol.get_full_command(command, show_raw)
        log.info(f'full command {full_command} for command {command}')

        response_line = None
        log.debug(f'port {self._serial_port}, baudrate {self._serial_baud}')
        try:
            with serial.serial_for_url(self._serial_port, self._serial_baud) as s:
                # Execute command multiple times, increase timeouts each time
                for x in range(1, 5):
                    log.debug(f'Command execution attempt {x}...')
                    s.timeout = 1 + x
                    s.write_timeout = 1 + x
                    s.flushInput()
                    s.flushOutput()
                    s.write(full_command)
                    time.sleep(0.5 * x)  # give serial port time to receive the data
                    response_line = s.readline()
                    log.debug('serial response was: %s', response_line)
                    decoded_response = protocol.decode(response_line)
                    log.debug(f'Decoded response {decoded_response}')
                    return decoded_response
        except Exception as e:
            log.warning(f"Serial read error: {e}")
        log.info('Command execution failed')
        return {'error': 'Serial command execution failed'}
