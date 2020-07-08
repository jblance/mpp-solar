import logging

from .device import AbstractDevice

log = logging.getLogger('MPP-Solar')


def getVal(_dict, key, ind=None):
    if key not in _dict:
        return ""
    if ind is None:
        return _dict[key]
    else:
        return _dict[key][ind]


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

        # TODO: implement
        response = self._port.send_and_receive(command, show_raw, self._protocol)
        log.debug(f'Send and Receive Response {response}')
        return response

    def get_status(self, show_raw):
        pass

    def get_settings(self, show_raw):
        """
        Query inverter for all current settings
        """
        # serial_number = self.getSerialNumber()
        default_settings = self.run_command("QDI")
        current_settings = self.run_commmand("QPIRI")
        flag_settings = self.run_command("QFLAG")

        settings = {}
        # {"Battery Bulk Charge Voltage": {"unit": "V", "default": 56.4, "value": 57.4}}

        for item in current_settings.keys():
            key = '{}'.format(item).replace(" ", "_")
            settings[key] = {"value": getVal(current_settings, key, 0),
                             "unit": getVal(current_settings, key, 1),
                             "default": getVal(default_settings, key, 0)}
        for key in flag_settings:
            _key = '{}'.format(key).replace(" ", "_")
            if _key in settings:
                settings[_key]['value'] = getVal(flag_settings, key, 0)
            else:
                settings[_key] = {'value': getVal(flag_settings, key, 0), "unit": "", "default": ""}
        return settings
