import logging
import serial
import time

from .port import Port

log = logging.getLogger("SerialPort")


class SerialPort(Port):
    def __init__(self, path, baud, protocol) -> None:
        log.debug(f"Initializing usbserial port. path:{path}, baud: {baud}")
        self.path = path
        self.baud = baud
        self.protocol = protocol
        self.port = None
        self.error = None

    def connect(self) -> None:
        log.debug(f"usbserial port connecting. path:{self.path}, baud:{self.baud}")
        try:
            self.port = serial.Serial(port=self.path, baudrate=self.baud, timeout=1, write_timeout=1)
        except Exception as e:
            log.warning(f"Error openning serial port: {e}")
            self.error = e
        return

    def disconnect(self) -> None:
        log.debug("usbserial port disconnecting")
        if self.port is not None:
            self.port.close()
        return

    def send_and_receive(self, full_command) -> dict:
        response_line = None
        log.debug(f"port {self.port}")
        if self.port is None:
            log.error("Port not available")
            return {"ERROR": [f"Serial command execution failed {self.error}", ""]}
        try:
            log.debug("Executing command via usbserial...")
            self.port.reset_input_buffer()
            self.port.reset_output_buffer()
            c = self.port.write(full_command)
            log.debug(f"Wrote {c} bytes")
            self.port.flush()
            time.sleep(0.1)  # give serial port time to receive the data
            response_line = self.port.read_until(b"\r")
            log.debug("serial response was: %s", response_line)
            return response_line
        except Exception as e:
            log.warning(f"Serial read error: {e}")
        log.info("Command execution failed")
        return {"ERROR": ["Serial command execution failed", ""]}
