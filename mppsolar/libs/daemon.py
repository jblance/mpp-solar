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
    WATCHDOG = auto()


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
                from cysystemd import journal

                self._notify = notify
                self._journal = journal.write
                self._Notification = Notification
            except ModuleNotFoundError as e:
                print(
                    f"error: {e}, try 'pip install cysystemd' (which may need 'apt install build-essential libsystemd-dev'), see https://pypi.org/project/cysystemd/ for further info"
                )
                exit(1)
        else:
            self._notify = self._dummyNotify
            self._journal = self._dummyNotify
            self._Notification = dummyNotification
        self.notify(f"got daemon type: {self.type}, keepalive: {self.keepalive}")

    def initialize(self, *args, **kwargs):
        # Send READY=1
        self._notify(self._Notification.READY)
        self._lastNotify = time()

    def watchdog(self, *args, **kwargs):
        elapsed = time() - self._lastNotify
        if (elapsed) > self.keepalive:
            self._notify(self._Notification.WATCHDOG)
            self._lastNotify = time()
            self._journal(f"Daemon notify at {self._lastNotify}")

    def notify(self, *args, **kwargs):
        # Send status
        if args:
            status = args[0]
        else:
            status = "OK"
        self._notify(self._Notification.STATUS, status)

    def stop(self, *args, **kwargs):
        # Send stopping
        self._notify(self._Notification.STOPPING)

    def log(self, *args, **kwargs):
        # Print log message
        if args:
            self._journal(args[0])

    def _dummyNotify(self, *args, **kwargs):
        # Print log message
        # if args:
        #     print(args[0])
        pass
