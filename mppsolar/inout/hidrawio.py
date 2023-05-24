# shamelessly stolen from ccrisan https://github.com/qtoggle/qtoggleserver-mppsolar/blob/master/qtoggleserver/mppsolar/io.py
import logging
import os
import time

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger("HIDRawIO")


class HIDRawIO(BaseIO):
    def __init__(self, device_path: str) -> None:
        # self._fd = os.open(device_path, flags=os.O_RDWR | os.O_NONBLOCK)
        self._device = device_path

    def send_and_receive(self, *args, **kwargs) -> dict:
        full_command = get_kwargs(kwargs, "full_command")
        response_line = bytes()
        usb0 = None
        try:
            usb0 = os.open(self._device, os.O_RDWR | os.O_NONBLOCK)
        except Exception as e:
            log.error("USB open error: {}".format(e))
            return {"ERROR": ["USB open error: {}".format(e), ""]}
        # Send the command to the open usb connection
        cmd_len = len(full_command)
        log.debug(f"length of to_send: {cmd_len}")
        # for command of len < 8 it ok just to send
        # otherwise need to pack to a multiple of 8 bytes and send 8 at a time
        if cmd_len <= 8:
            # Send all at once
            log.debug("sending full_command in on shot")
            time.sleep(0.05)
            os.write(usb0, full_command)
        else:
            log.debug("multiple chunk send")
            chunks = [full_command[i:i + 8] for i in range(0, cmd_len, 8)]
            for chunk in chunks:
                # pad chunk to 8 bytes
                if len(chunk) < 8:
                    padding = 8 - len(chunk)
                    chunk += b'\x00' * padding
                log.debug("sending chunk: %s" % (chunk))
                time.sleep(0.05)
                os.write(usb0, chunk)
        time.sleep(0.25)
        # Read from the usb connection
        # try to a max of 100 times
        for x in range(100):
            # attempt to deal with resource busy and other failures to read
            try:
                time.sleep(0.15)
                r = os.read(usb0, 256)
                response_line += r
            except Exception as e:
                log.debug("USB read error: {}".format(e))
            # Finished is \r is in byte_response
            if bytes([13]) in response_line:
                # remove anything after the \r
                response_line = response_line[: response_line.find(bytes([13])) + 1]
                break
        log.debug("usb response was: %s", response_line)
        os.close(usb0)
        return response_line
