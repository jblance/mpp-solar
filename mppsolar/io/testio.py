# shamelessly stolen from ccrisan https://github.com/qtoggle/qtoggleserver-mppsolar/blob/master/qtoggleserver/mppsolar/io.py
import logging
import random

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger("MPP-Solar")


class TestIO(BaseIO):
    def __init__(self, *args, **kwargs) -> None:
        self._test_data = b"(230.0 50.0 0030 42.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 0 0 1 0 54.0 0 1 000\x9E\x60\r"
        self._counter = 0

    def send_and_receive(self, *args, **kwargs) -> dict:
        full_command = get_kwargs(kwargs, "full_command")
        command_defn = get_kwargs(kwargs, "command_defn")
        if command_defn is not None:
            self._test_data = command_defn["test_responses"][
                random.randrange(len(command_defn["test_responses"]))
            ]
        response = self._test_data
        # response = b"(PI30\x9a\x0b\r"
        log.debug(f"Raw response {response}")
        return response
