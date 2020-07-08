import logging

log = logging.getLogger('powermon')


class screen():
    def __init__(self, *args, **kwargs) -> None:
        log.info('Using output processor: print')
        log.debug(f'processor.print __init__ kwargs {kwargs}')
        _data = kwargs['results']
        if _data is None:
            return
        print(f"{'Parameter':<30}\t{'Value':<15} Unit")
        for key in _data:
            value = _data[key][0]
            unit = _data[key][1]
            print(f'{key:<30}\t{value:<15}\t{unit:<4}')
