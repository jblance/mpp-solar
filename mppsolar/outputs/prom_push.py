import logging

import requests

from .prom import prom
from ..helpers import get_kwargs

log = logging.getLogger("prom")


class prom_push(prom):
    push_url = ""

    def __str__(self):
        return "pushes Node exporter Prometheus format to PushGateway"

    def output(self, *args, **kwargs):
        # We override the method only to get the PushGateway URL from the config
        self.push_url = kwargs["push_url"]

        return super().output(*args, **kwargs)

    def handle_output(self, content: str) -> None:
        with requests.post(self.push_url, data=content) as req:
            log.debug(f"POST'ed data to PushGateway {self.push_url!r}: {req=}")
    