import logging

from .device import AbstractDevice


log = logging.getLogger("MPP-Solar")


class mppsolar(AbstractDevice):
    def __init__(self, *args, **kwargs) -> None:
        self._classname = "mppsolar"
        super().__init__(*args, **kwargs)
