import logging

from .prom import prom
from ..helpers import get_kwargs

log = logging.getLogger("prom")


class prom_file(prom):
    prom_output_dir = ""

    def __str__(self):
        return "pushes Node exporter Prometheus format to PushGateway"

    def output(self, *args, **kwargs):
        # We override the method only to get the PushGateway URL from the config
        self.prom_output_dir = kwargs["prom_output_dir"]
        self.cmd = get_kwargs(kwargs, "data").get("_command", "").lower()

        return super().output(*args, **kwargs)

    def handle_output(self, content: str) -> None:
        file_path = f"{self.prom_output_dir.rstrip('/')}/mpp-solar-{self.cmd}.prom"
        with open(file_path, "w") as f:
            f.write(content)
