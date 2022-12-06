# shamelessly stolen from ccrisan https://github.com/qtoggle/qtoggleserver-mppsolar/blob/master/qtoggleserver/mppsolar/io.py
import logging
import os
import time

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger("HIDFullIO")


class HIDFullIO(BaseIO):
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
            log.debug("USB open error: {}".format(e))
            return {"ERROR": ["USB open error: {}".format(e), ""]}
        # Send the command to the open usb connection
        to_send = full_command
        try:
            log.debug(f"length of to_send: {len(to_send)}")
        except:  # noqa: E722
            import pdb

            pdb.set_trace()

        # Send all at once
        log.debug("1 chunk send")
        time.sleep(0.35)
        os.write(usb0, to_send)

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
