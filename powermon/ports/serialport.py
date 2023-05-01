import logging
import serial
import time
from dto.portDTO import PortDTO

from .abstractport import AbstractPort

log = logging.getLogger("SerialPort")


class SerialPort(AbstractPort):
    def __init__(self, path, baud, protocol) -> None:
        log.debug(f"Initializing usbserial port. path:{path}, baud: {baud}")
        self.path = path
        self.baud = baud
        self.protocol = protocol
        self.serialPort = None
        self.error = None

    def toDTO(self) -> PortDTO:
        dto = PortDTO(type="serial", path=self.path, baud=self.baud, protocol=self.protocol.toDTO())
        return dto

    def connect(self) -> None:
        log.debug(f"usbserial port connecting. path:{self.path}, baud:{self.baud}")
        try:
            self.serialPort = serial.Serial(port=self.path, baudrate=self.baud, timeout=1, write_timeout=1)
        except Exception as e:
            log.error(f"Error openning serial port: {e}")
            self.error = e
        return

    def disconnect(self) -> None:
        log.debug("usbserial port disconnecting")
        if self.serialPort is not None:
            self.serialPort.close()
        return

    def send_and_receive(self, command) -> dict:
        full_command = self.protocol.get_full_command(command)
        response_line = None
        log.debug(f"port {self.serialPort}")
        if self.serialPort is None:
            log.error("Port not available")
            return {"ERROR": [f"Serial command execution failed {self.error}", ""]}
        try:
            log.debug("Executing command via usbserial...")
            self.serialPort.reset_input_buffer()
            self.serialPort.reset_output_buffer()
            c = self.serialPort.write(full_command)
            log.debug(f"Wrote {c} bytes")
            self.serialPort.flush()
            time.sleep(0.1)  # give serial port time to receive the data
            response_line = self.serialPort.read_until(b"\r")
            log.debug("serial response was: %s", response_line)
            return response_line
        except Exception as e:
            log.warning(f"Serial read error: {e}")
        log.info("Command execution failed")
        return {"ERROR": ["Serial command execution failed", ""]}
