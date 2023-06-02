import logging
from enum import Enum, auto
from time import time

from strenum import LowercaseStrEnum

# Set-up logger
log = logging.getLogger("daemon")


class dummyNotification(Enum):
    READY = auto()
    STATUS = auto()
    STOPPING = auto()
    WATCHDOG = auto()


class DaemonType(LowercaseStrEnum):
    DISABLED = auto()
    SYSTEMD = auto()


class Daemon:
    def __str__(self):
        if not self.enabled:
            return "Daemon DISABLED"
        return f"Daemon name: {self.type}"

    @classmethod
    def fromConfig(cls, config={}):
        log.debug(f"daemon config: {config}")

        if config is None:
            _type = DaemonType.DISABLED
            keepalive = 0
            enabled = False
            log.debug("daemon not configured, disabling")
        if config is not None:
            enabled = True
            _type = config.get("type", None)
            keepalive = config.get("keepalive", 60)
            log.debug(f"got daemon: {_type=}, {keepalive=}")

        return cls(_type=_type, keepalive=keepalive, enabled=enabled)

    def __init__(self, _type, keepalive, enabled):

        self.enabled = enabled
        self.type = _type
        self.keepalive = keepalive
        log.debug(f"got daemon type: {self.type}, keepalive: {self.keepalive}")

        match self.type:
            case DaemonType.SYSTEMD:
                try:
                    from cysystemd import journal
                    from cysystemd.daemon import Notification, notify

                    self._notify = notify
                    self._journal = journal.write
                    self._Notification = Notification
                except ModuleNotFoundError as e:
                    print(
                        f"error: {e}, try 'pip install cysystemd' (which may need 'apt install build-essential libsystemd-dev'), see https://pypi.org/project/cysystemd/ for further info"
                    )
                    exit(1)
            case _:
                self._notify = self._dummyNotify
                self._journal = self._dummyNotify
                self._Notification = dummyNotification
        self.notify(f"got daemon type: {self.type}, keepalive: {self.keepalive}")

    def initialize(self, *args, **kwargs):
        if self.enabled:
            # Send READY=1
            self._notify(self._Notification.READY)
            self._lastNotify = time()

    def watchdog(self, *args, **kwargs):
        if self.enabled:
            elapsed = time() - self._lastNotify
            if (elapsed) > self.keepalive:
                self._notify(self._Notification.WATCHDOG)
                self._lastNotify = time()
                self._journal(f"Daemon notify at {self._lastNotify}")

    def notify(self, *args, **kwargs):
        if not self.enabled:
            return
        # Send status
        if args:
            status = args[0]
        else:
            status = "OK"
        self._notify(self._Notification.STATUS, status)

    def stop(self, *args, **kwargs):
        if self.enabled:
            # Send stopping
            self._notify(self._Notification.STOPPING)

    def log(self, *args, **kwargs):
        if self.enabled:
            # Print log message
            if args:
                self._journal(args[0])

    def _dummyNotify(self, *args, **kwargs):
        # Print log message
        # if args:
        #     print(args[0])
        return
