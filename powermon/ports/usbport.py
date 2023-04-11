import logging
import os
import time

from mppsolar.helpers import get_kwargs

from .port import Port

log = logging.getLogger("USBPort")


class usbport(Port):
    def __init__(self, *args, **kwargs) -> None:
        config = get_kwargs(kwargs, "config")
        self.path = config["path"]
        self.protocol = config["protocol"]
        log.debug(f"Initializing usb port. path:{self.path}, protocol: {self.protocol}")

    def protocol(self):
        return self.protocol

    def connect(self) -> None:
        log.debug(f"USBPort connecting. path:{self.path}, protocol: {self.protocol}")
        try:
            self.port = os.open(self.path, os.O_RDWR | os.O_NONBLOCK)
            log.debug(f"USBPort port number ${self.port}")
        except Exception as e:
            log.warning(f"Error openning usb port: {e}")
            self.error = e
        return

    def disconnect(self) -> None:
        log.debug(f"USBPort disconnecting {self.port}")

    def send_and_receive(self, *args, **kwargs) -> dict:
        full_command = get_kwargs(kwargs, "full_command")
        response_line = bytes()
        self.connect()
        
        # Send the command to the open usb connection
        to_send = full_command
        try:
            log.debug(f"length of to_send: {len(to_send)}")
        except:  # noqa: E722
            import pdb

            pdb.set_trace()
        if len(to_send) <= 8:
            # Send all at once
            log.debug("1 chunk send")
            time.sleep(0.35)
            try:
                os.write(self.port, to_send)
            except Exception as e:
                log.debug("USB read error: {}".format(e))
            
        elif len(to_send) > 8 and len(to_send) < 11:
            log.debug("2 chunk send")
            time.sleep(0.35)
            os.write(self.port, to_send[:5])
            time.sleep(0.35)
            os.write(self.port, to_send[5:])
        else:
            while len(to_send) > 0:
                log.debug("multiple chunk send")
                # Split the byte command into smaller chucks
                send, to_send = to_send[:8], to_send[8:]
                log.debug("send: {}, to_send: {}".format(send, to_send))
                time.sleep(0.35)
                os.write(self.port, send)
        time.sleep(0.25)
        # Read from the usb connection
        # try to a max of 100 times
        for x in range(100):
            # attempt to deal with resource busy and other failures to read
            try:
                time.sleep(0.15)
                r = os.read(self.port, 256)
                response_line += r
            except Exception as e:
                log.debug("USB read error: {}".format(e))
            # Finished is \r is in byte_response
            if bytes([13]) in response_line:
                # remove anything after the \r
                response_line = response_line[: response_line.find(bytes([13])) + 1]
                break
        log.debug("usb response was: %s", response_line)
        os.close(self.port)
        return response_line
