from mppsolar.helpers import get_kwargs
import logging
import importlib

# from time import sleep
log = logging.getLogger("formatter")


def format_data(*args, **kwargs):

    formatter = get_kwargs(kwargs, "formatter")

    log.info(f"attempting to create output processor: {formatter}")
    try:
        _module = importlib.import_module("mppsolar.sender.formats." + formatter, ".")
        _class = getattr(_module, formatter)
    except ModuleNotFoundError as e:
        # perhaps raise a Powermon exception here??
        # maybe warn and keep going, only error if no outputs found?
        log.critical(f"No module found for formatter processor {formatter} Error: {e}")
        return

    return _class.output(**kwargs)
