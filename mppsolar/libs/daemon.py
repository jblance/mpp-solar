""" daemon.py """
import logging
from enum import Enum, auto
from time import time

#from pydantic import BaseModel
# from strenum import LowercaseStrEnum

# Set-up logger
log = logging.getLogger("daemon")


class dummyNotification(Enum):
    READY = "READY"
    STATUS = "STATUS"
    STOPPING = "STOPPING"
    WATCHDOG = "WATCHDOG"


class DaemonType(Enum):
    """ Daemon types implemented """
    DISABLED = "disabled"
    SYSTEMD = "systemd"


class Daemon:
    """ abstraction to support different daemon approaches / solutions """
    def __str__(self):
        if not self.enabled:
            return "Daemon DISABLED"
        return f"Daemon name: {self.type}"

    def __init__(self, _type=DaemonType.SYSTEMD, keepalive=60, enabled=False):

        self.enabled = enabled
        self.type = _type
        self.keepalive = keepalive
        log.debug(f"got daemon type: {self.type}, keepalive: {self.keepalive}")

        match self.type:
            case DaemonType.SYSTEMD:
                # TODO: this should probably be separate classes / objects
                try:
                    from cysystemd import journal
                    from cysystemd.daemon import Notification, notify

                    self._notify = notify
                    self._journal = journal.write
                    self._Notification = Notification
                except ModuleNotFoundError as exception:
                    print(
                        f"error: {exception}, try 'pip install cysystemd' (which may need 'apt install build-essential libsystemd-dev'), see https://pypi.org/project/cysystemd/ for further info"
                    )
                    exit(1)
            case _:
                self._notify = self._dummyNotify
                self._journal = self._dummyNotify
                self._Notification = dummyNotification
        self.notify(f"got daemon type: {self.type}, keepalive: {self.keepalive}")

    def initialize(self):
        """ Daemon initialization activities """
        if self.enabled:
            # Send READY=1
            self._notify(self._Notification.READY)
            self._lastNotify = time()

    def watchdog(self):
        if self.enabled:
            elapsed = time() - self._lastNotify
            if (elapsed) > self.keepalive:
                self._notify(self._Notification.WATCHDOG)
                self._lastNotify = time()
                self._journal(f"Daemon notify at {self._lastNotify}")

    def notify(self, status="OK"):
        if not self.enabled:
            return
        # Send status
        self._notify(self._Notification.STATUS, status)

    def stop(self):
        if self.enabled:
            # Send stopping
            self._notify(self._Notification.STOPPING)

    def log(self, message=None):
        if self.enabled:
            # Print log message
            if message is not None:
                self._journal(message)

    def _dummyNotify(self, *args, **kwargs):
        # Print log message
        # if args:
        #     print(args[0])
        return
