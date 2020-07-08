# shamelessly stolen from ccrisan https://github.com/qtoggle/qtoggleserver-mppsolar/blob/master/qtoggleserver/mppsolar/io.py
import logging
import os
import time

from .baseio import BaseIO

log = logging.getLogger('powermon')


class HIDRawIO(BaseIO):
    def __init__(self, device_path: str) -> None:
        # self._fd = os.open(device_path, flags=os.O_RDWR | os.O_NONBLOCK)
        self._serial_device = device_path

    def send_and_receive(self, command, show_raw, protocol) -> dict:
        full_command = protocol.get_full_command(command, show_raw)
        log.info(f'full command {full_command} for command {command}')

        response_line = bytes()
        usb0 = None
        try:
            usb0 = os.open(self._serial_device, os.O_RDWR | os.O_NONBLOCK)
        except Exception as e:
            log.debug("USB open error: {}".format(e))
            return command
        # Send the command to the open usb connection
        to_send = full_command
        try:
            log.debug(f'length of to_send: {len(to_send)}')
        except:  # noqa: E722
            import pdb
            pdb.set_trace()
        if len(to_send) <= 8:
            # Send all at once
            log.debug("1 chunk send")
            time.sleep(0.35)
            os.write(usb0, to_send)
        elif len(to_send) > 8 and len(to_send) < 11:
            log.debug("2 chunk send")
            time.sleep(0.35)
            os.write(usb0, to_send[:5])
            time.sleep(0.35)
            os.write(usb0, to_send[5:])
        else:
            while (len(to_send) > 0):
                log.debug("multiple chunk send")
                # Split the byte command into smaller chucks
                send, to_send = to_send[:8], to_send[8:]
                log.debug("send: {}, to_send: {}".format(send, to_send))
                time.sleep(0.35)
                os.write(usb0, send)
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
            if (bytes([13]) in response_line):
                # remove anything after the \r
                response_line = response_line[:response_line.find(bytes([13])) + 1]
                break
        log.debug('usb response was: %s', response_line)
        os.close(usb0)
        decoded_response = protocol.decode(response_line)
        # _response = response.decode('utf-8')
        log.debug(f'Decoded response {decoded_response}')
        return decoded_response
