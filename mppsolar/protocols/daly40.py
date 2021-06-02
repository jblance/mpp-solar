import logging

from .daly import daly

# from .pi30 import COMMANDS

log = logging.getLogger("daly40")

# (AAA BBB CCC DDD EEE
# (000 001 002 003 004


startFlag = bytes.fromhex("A5")


class daly40(daly):
    """
    DALY - Daly40 BMS protocol handler
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"DALY40"
        self.module_address = bytes.fromhex("40")
