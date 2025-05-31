""" daemon.py """
import logging
from enum import Enum
from time import time
from mppsolar.daemon.daemon import Daemon

# Set-up logger
log = logging.getLogger("daemon-dummy")


class DummyNotification(Enum):
    READY = "READY"
    STATUS = "STATUS"
    STOPPING = "STOPPING"
    WATCHDOG = "WATCHDOG"


class DaemonDummy(Daemon):
    """ """
    def __str__(self):
        return "Daemon DISABLED"

    def __init__(self):
        self._notify = self._dummyNotify
        self._journal = self._dummyNotify
        self._Notification = DummyNotification
        self.keepalive = 60
        # self.notify(f"got daemon type: {self.type}, keepalive: {self.keepalive}")

    def _dummyNotify(self, *args, **kwargs):
        log.debug(f"DaemonDummy notified: args={args}, kwargs={kwargs}")
        # Print log message
        # if args:
        #     print(args[0])
        return

