import logging

from .device import AbstractDevice
from ..io.jkbleio import JkBleIO

log = logging.getLogger("MPP-Solar")


class jkbms(AbstractDevice):
    def __init__(self, *args, **kwargs) -> None:
        self._classname = "jkbms"
        super().__init__(*args, **kwargs)
