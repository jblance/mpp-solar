""" powermon / ports / usbport.py """
import logging
import os
import time

from powermon.dto.portDTO import PortDTO
from powermon.commands.result import Result, ResultType
from powermon.ports.abstractport import AbstractPort
from powermon.protocols import get_protocol_definition
from powermon.commands.command import Command

log = logging.getLogger("USBPort")


class USBPort(AbstractPort):
    """ usb port object """
    @classmethod
    def from_config(cls, config=None):
        log.debug("building usb port. config:%s", config)
        path = config.get("path", "/dev/hidraw0")
        # get protocol handler, default to PI30 if not supplied
        protocol = get_protocol_definition(protocol=config.get("protocol", "PI30"))
        return cls(path=path, protocol=protocol)

    def __init__(self, path, protocol) -> None:
        super().__init__(protocol=protocol)
        self.path = path
        self.port = None

    def to_dto(self):
        dto = PortDTO(type="usb", path=self.path, protocol=self.protocol.to_dto())
        return dto

    def is_connected(self) -> bool:
        return self.port is not None

    def connect(self) -> bool:
        if self.is_connected():
            log.debug("USBPort already connected")
            return True
        log.debug("USBPort connecting. path:%s, protocol:%s", self.path, self.protocol)
        try:
            self.port = os.open(self.path, os.O_RDWR | os.O_NONBLOCK)
            log.debug("USBPort port number $%s", self.port)
        except Exception as e:
            log.warning("Error openning usb port: %s", e)
            self.port = None
            self.error_message = e
        return self.is_connected()

    def disconnect(self) -> None:
        log.debug("USBPort disconnecting: %i", self.port)
        if self.port is not None:
            os.close(self.port)
        self.port = None

    def send_and_receive(self, command: Command) -> Result:
        if not self.is_connected():
            log.warning("USBPort not connected")
            return command.build_result(result_type=ResultType.ERROR, raw_response=b"USBPort not connected", protocol=self.protocol)
        response_line = bytes()

        # Send the command to the open usb connection
        full_command = command.full_command
        cmd_len = len(full_command)
        log.debug("length of to_send: %i", cmd_len)
        # for command of len < 8 it ok just to send
        # otherwise need to pack to a multiple of 8 bytes and send 8 at a time
        if cmd_len <= 8:
            # Send all at once
            log.debug("sending full_command in on shot")
            time.sleep(0.05)
            os.write(self.port, full_command)
        else:
            log.debug("multiple chunk send")
            chunks = [full_command[i:i + 8] for i in range(0, cmd_len, 8)]
            for chunk in chunks:
                # pad chunk to 8 bytes
                if len(chunk) < 8:
                    padding = 8 - len(chunk)
                    chunk += b'\x00' * padding
                log.debug("sending chunk: %s", chunk)
                time.sleep(0.05)
                os.write(self.port, chunk)
        time.sleep(0.25)
        # Read from the usb connection
        # try to a max of 100 times
        for _ in range(100):
            # attempt to deal with resource busy and other failures to read
            try:
                time.sleep(0.15)
                r = os.read(self.port, 256)
                response_line += r
            except Exception as e:
                log.debug("USB read error: %s", e)
            # Finished is \r is in byte_response
            if bytes([13]) in response_line:
                # remove anything after the \r
                response_line = response_line[: response_line.find(bytes([13])) + 1]
                break
        log.debug("usb response was: %s", response_line)
        # response = self.get_protocol().check_response_and_trim(response_line)
        result = command.build_result(raw_response=response_line, protocol=self.protocol)

        return result
