import logging
from enum import Enum, auto
from time import time

from ..helpers import get_kwargs

# Set-up logger
log = logging.getLogger("daemon")


class dummyNotification(Enum):
    READY = auto()
    STATUS = auto()
    STOPPING = auto()


class Daemon:
    def __str__(self):
        return f"Daemon name: {self.type}"

    def __init__(self, *args, **kwargs):

        config = get_kwargs(kwargs, "config", {})

        daemon_config = config.get("daemon")
        if daemon_config is None:
            self.type = None
            self.keepalive = 60
        if daemon_config is not None:
            self.type = daemon_config.get("type", None)
            self.keepalive = daemon_config.get("keepalive", 60)

        log.info(f"got daemon type: {self.type}, keepalive: {self.keepalive}")

        if self.type == "systemd":
            try:
                from cysystemd.daemon import Notification, notify

                self._notify = notify
                self._Notification = Notification
            except ModuleNotFoundError as e:
                print(
                    f"error: {e}, try 'pip install cysystemd' (which may need 'apt install build-essential libsystemd-dev'), see https://pypi.org/project/cysystemd/ for further info"
                )
                exit(1)
        else:
            self._notify = self._dummyNotify
            self._Notification = dummyNotification

    def initialize(self, *args, **kwargs):
        # Send READY=1
        self._notify(self._Notification.READY)
        self._lastNotify = time()

    def notify(self, *args, **kwargs):
        if (time() - self._lastNotify) > self.keepalive:
            # Send status
            if args:
                status = args[0]
            else:
                status = "OK"
            self._notify(self._Notification.STATUS, status)
            self._lastNotify = time()

    def stop(self, *args, **kwargs):
        # Send stopping
        self._notify(self._Notification.STOPPING)

    def _dummyNotify(self, *args, **kwargs):
        pass
