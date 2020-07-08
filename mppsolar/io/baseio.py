# shamelessly stolen from ccrisan https://github.com/qtoggle/qtoggleserver-mppsolar/blob/master/qtoggleserver/mppsolar/io.py
import abc
import logging
# from time import sleep
log = logging.getLogger('powermon')


class BaseIO(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def send_and_receive(self, command, show_raw, protocol) -> dict:
        full_command = protocol.get_full_command(command, show_raw)
        log.info(f'full command {full_command} for command {command}')
        # Send the full command via the communications port
        self.write(full_command)
        # Get the response from the communications port
        response = self.read(10)
        decoded_response = protocol.decode(response)
        # _response = response.decode('utf-8')
        log.debug(f'Raw response {response}')
        log.debug(f'Decoded response {decoded_response}')
        return decoded_response
