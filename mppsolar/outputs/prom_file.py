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
        self.name = get_kwargs(kwargs, "name")

        return super().output(*args, **kwargs)

    def handle_output(self, content: str) -> None:
        if self.name != "unnamed":
            self.filename = "{0}-{1}".format(self.name, self.cmd)
        else:
            self.filename = self.cmd
            
        file_path = f"{self.prom_output_dir.rstrip('/')}/mpp-solar-{self.filename}.prom"
        with open(file_path, "w") as f:
            f.write(content)
