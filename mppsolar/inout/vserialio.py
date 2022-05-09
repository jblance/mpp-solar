import logging
import serial

# import time

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger("VSerialIO")


class VSerialIO(BaseIO):
    def __init__(self, *args, **kwargs) -> None:
        self._serial_port = get_kwargs(kwargs, "device_path")
        self._serial_baud = get_kwargs(kwargs, "serial_baud")
        self._records = get_kwargs(kwargs, "records")

    def send_and_receive(self, *args, **kwargs) -> dict:
        # self._port.send_and_receive(
        #    command=command,
        #    full_command=full_command,
        #    protocol=self._protocol,
        #    command_defn=self._protocol.get_command_defn(command),

        full_command = get_kwargs(kwargs, "full_command")
        # print(full_command)
        # "VEDTEXT"
        responses = b""
        log.debug(
            f"port {self._serial_port}, baudrate {self._serial_baud}, records {self._records}"
        )

        if full_command == "VEDTEXT":
            # Just grab _records from the serial port
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
                        log.debug("vserial response was: %s", response_line)
                        responses += response_line
                    return responses
            except Exception as e:
                log.warning(f"VSerial read error: {e}")
            log.info(f"Error occured while grabbing data from {self._serial_port}")
            return {
                "ERROR": [
                    f"Error occured while grabbing data from {self._serial_port}",
                    "",
                ]
            }
        else:
            # Have a command to send...
            try:
                with serial.serial_for_url(self._serial_port, self._serial_baud) as s:
                    log.debug("Executing command via vserialio...")
                    s.timeout = 1
                    s.write_timeout = 1
                    s.flushInput()
                    s.flushOutput()
                    s.write(full_command)
                    # time.sleep(0.1)  # give serial port time to receive the data
                    response_line = s.read_until(b"\n")
                    log.debug("vserial response was: %s", response_line)
                    return response_line
            except Exception as e:
                log.warning(f"VSerial read error: {e}")
            log.info(
                f"Error occured while processing command {full_command} on {self._serial_port}"
            )
            return {
                "ERROR": [
                    f"Error occured while processing command {full_command} on {self._serial_port}",
                    "",
                ]
            }
