import logging
import time

import serial

from powermon.dto.portDTO import PortDTO
from powermon.ports.abstractport import AbstractPort
from powermon.protocols import get_protocol

log = logging.getLogger("SerialPort")


class SerialPort(AbstractPort):
    @classmethod
    def fromConfig(cls, config=None):
        log.debug(f"building serial port. config:{config}")
        path = config.get("path", "/dev/ttyUSB0")
        baud = config.get("baud", 2400)
        # get protocol handler, default to PI30 if not supplied
        protocol = get_protocol(protocol=config.get("protocol", "PI30"))
        return cls(path=path, baud=baud, protocol=protocol)

    def __init__(self, path, baud, protocol) -> None:
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
            return {"ERROR": [f"Serial command execution failed {self.error}", ""]}  # FIXME do this properly
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
        return {"ERROR": ["Serial command execution failed", ""]}  # FIXME do this properly
