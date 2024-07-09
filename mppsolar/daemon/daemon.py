""" daemon.py """
import logging
from enum import Enum, auto
from time import time

# Set-up logger
log = logging.getLogger("daemon")

class Daemon:
    """ abstraction to support different daemon approaches / solutions """
    def __str__(self):
        return f"Daemon name: {self.type}"

    def initialize(self):
        """ Daemon initialization activities """
        self._notify(self._Notification.READY)
        self._lastNotify = time()

    def watchdog(self):
        elapsed = time() - self._lastNotify
        if (elapsed) > self.keepalive:
            self._notify(self._Notification.WATCHDOG)
            self._lastNotify = time()
            self._journal(f"Daemon notify at {self._lastNotify}")

    def notify(self, status="OK"):
        # Send status
        self._notify(self._Notification.STATUS, status)

    def stop(self):
        # Send stopping
        self._notify(self._Notification.STOPPING)

    def log(self, message=None):
        # Print log message
        if message is not None:
            self._journal(message)
