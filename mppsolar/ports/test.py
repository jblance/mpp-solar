# shamelessly stolen from ccrisan https://github.com/qtoggle/qtoggleserver-mppsolar/blob/master/qtoggleserver/mppsolar/io.py
import logging

# import random
# import re

from .port import Port

# from ..helpers import get_kwargs

log = logging.getLogger("Test")


class test(Port):
    def __init__(self, *args, **kwargs) -> None:
        self._test_data = b"(230.0 50.0 0030 42.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 0 0 1 0 54.0 0 1 000\x9E\x60\r"
        # self._counter = 0
        # self._device = get_kwargs(kwargs, "device_path")
        print("asadf", *args, **kwargs)

    def send_and_receive(self, *args, **kwargs) -> dict:
        # full_command = get_kwargs(kwargs, "full_command")
        # command_defn = get_kwargs(kwargs, "command_defn")

        # if command_defn is not None:
        #     # Have test data defined, so use that
        #     number_of_test_responses = len(command_defn["test_responses"])
        #     # have we specified which test response to use?
        #     check = re.match("test(\d+)", self._device, flags=re.IGNORECASE)  # noqa: W605
        #     if check:
        #         # use the specified response if that one exists
        #         try:
        #             desired_test_response = int(check.group(1))
        #         except ValueError:
        #             desired_test_response = 0
        #         if desired_test_response < number_of_test_responses:
        #             self._test_data = command_defn["test_responses"][desired_test_response]
        #         else:
        #             log.warn(
        #                 f"Test response requested: {desired_test_response} exceeds highest id available (IDs start at 0): {number_of_test_responses-1}, returning random one"
        #             )
        #             self._test_data = command_defn["test_responses"][
        #                 random.randrange(number_of_test_responses)
        #             ]
        #     else:
        #         # just use a random test response
        #         self._test_data = command_defn["test_responses"][
        #             random.randrange(number_of_test_responses)
        #         ]
        # else:
        #     # No test responses defined
        #     log.warn("Testing a command with no test responses defined")
        response = self._test_data
        log.debug(f"Raw response {response}")
        return response
