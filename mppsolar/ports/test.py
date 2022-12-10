import logging
import random

from ..helpers import get_kwargs
from .port import Port

# import re


log = logging.getLogger("Test")


class test(Port):
    def __init__(self, *args, **kwargs) -> None:
        # self._test_data = None
        # self._counter = 0
        # self._device = get_kwargs(kwargs, "device_path")
        log.debug("test port", *args, **kwargs)

    def send_and_receive(self, *args, **kwargs) -> dict:
        # full_command = get_kwargs(kwargs, "full_command")
        command_defn = get_kwargs(kwargs, "command_defn")

        if command_defn is not None:
            # Have test data defined, so use that
            number_of_test_responses = len(command_defn["test_responses"])
            self._test_data = command_defn["test_responses"][
                random.randrange(number_of_test_responses)
            ]
        else:
            # No test responses defined
            log.warn("Testing a command with no test responses defined")
            self._test_data = None
        response = self._test_data
        log.debug(f"Raw response {response}")
        return response
