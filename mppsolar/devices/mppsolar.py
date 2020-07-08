import logging

from .device import AbstractDevice

log = logging.getLogger('powermon')


class mppsolar(AbstractDevice):
    def __init__(self, *args, **kwargs) -> None:
        self._name = kwargs['name']
        self.set_port(port=kwargs['port'])
        self.set_protocol(protocol=kwargs['protocol'])
        log.debug(f'mppsolar __init__ name {self._name}, port {self._port}, protocol {self._protocol}')
        log.debug(f'mppsolar __init__ args {args}')
        log.debug(f'mppsolar __init__ kwargs {kwargs}')

    def run_command(self, command, show_raw=False) -> dict:
        '''
        mpp-solar specific method of running a 'raw' command, e.g. QPI or PI
        '''
        log.info(f'Running command {command}')
        # TODO: implement protocol self determiniation??
        if self._protocol is None:
            log.error('Attempted to run command with no protocol defined')
            return {'ERROR': ['Attempted to run command with no protocol defined', '']}
        if self._port is None:
            log.error(f'No communications port defined - unable to run command {command}')
            return {'ERROR': [f'No communications port defined - unable to run command {command}', '']}

        response = self._port.send_and_receive(command, show_raw, self._protocol)
        log.debug(f'Send and Receive Response {response}')
        return response
