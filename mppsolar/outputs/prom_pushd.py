import logging
import socket

try:
    import requests
except ImportError:
    print("You are missing dependencies in order to be able to use that output.")
    print("To install them, use this command:")
    print("    python -m pip install 'mppsolar[push]'")
    requests = None

from .prom import prom
from ..helpers import get_kwargs

log = logging.getLogger("prom")


class prom_pushd(prom):
    push_url = ""
    job = "mppsolar"  # static default

    def __str__(self):
        return "Pushes Prometheus exposition format directly to VictoiaMetrics (Not Gateway)"

    def output(self, *args, **kwargs):
        log.debug(f"RAW kwargs: {kwargs}")
        self.push_url = kwargs.get("push_url")
        self.job = kwargs.get("job", "mppsolar")
        # Fully ignore provided instance, always sanitize from hostname
        self.instance = socket.gethostname().split('.')[0]

        log.debug(f"Forced instance to short hostname: {self.instance}")
        return super().output(*args, **kwargs)

    def handle_output(self, content: str) -> None:
        if not requests:
            return

        headers = {'Content-Type': 'text/plain'}
        target_url = f"{self.push_url}/metrics/job/{self.job}/instance/{self.instance}"

        try:
            with requests.post(target_url, data=content, headers=headers, timeout=(2,10)) as req:
                log.debug(f"POST'ed data to PushGateway {target_url!r}: status_code={req.status_code}")
        except requests.RequestException as e:
            log.error(f"Failed to push to PushGateway: {e}")

    
