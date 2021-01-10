import logging
import serial
import time

from .baseio import BaseIO

log = logging.getLogger("MPP-Solar")


class SerialIO(BaseIO):
    def __init__(self, device_path, serial_baud) -> None:
        self._serial_port = device_path
        if serial_baud is None:
            self._serial_baud = 2400
        else:
            self._serial_baud = serial_baud

    def send_and_receive(self, command, show_raw, protocol) -> dict:
        full_command = protocol.get_full_command(command)
        log.info(f"full command {full_command} for command {command}")
        command_defn = protocol.get_command_defn(command)

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
                decoded_response = protocol.decode(response_line, show_raw)
                log.debug(f"Decoded response {decoded_response}")
                # add command name and description to response
                decoded_response["_command"] = command
                if command_defn is not None:
                    decoded_response["_command_description"] = command_defn["description"]
                log.info(f"Decoded response {decoded_response}")
                return decoded_response
        except Exception as e:
            log.warning(f"Serial read error: {e}")
        log.info("Command execution failed")
        return {"ERROR": ["Serial command execution failed", ""]}
