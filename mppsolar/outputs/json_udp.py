import json as js
import logging
import re
import socket

from . import to_json
from .baseoutput import baseoutput
from ..helpers import get_kwargs

log = logging.getLogger("json_udp")


class json_udp(baseoutput):
    def __str__(self):
        return "outputs all the results to tcp UDP datagram packet in JSON format"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def output(self, *args, **kwargs):
        data = get_kwargs(kwargs, "data")
        tag = get_kwargs(kwargs, "tag")
        keep_case = get_kwargs(kwargs, "keep_case")
        udp_port = get_kwargs(kwargs, "udp_port", "5555")
        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        msgs = []
        # Remove command and _command_description
        cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)
        if tag is None:
            tag = cmd
        output = to_json(data, keep_case, excl_filter, filter)

        payload = js.dumps(output)
        log.debug(payload)
        msgs.append(payload)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP datagram
        for msg in msgs:
            count = sock.sendto(bytes(msg, "utf-8"), ("localhost", int(udp_port)))
        log.debug(f"Udp sent response {count}")
        return msgs
