""" daemon.py """
import os
import logging
from enum import Enum, auto
from time import time

# Set-up logger
log = logging.getLogger("daemon")

def setup_daemon_logging(log_file="/var/log/mpp-solar.log"):
    """Setup logging for daemon mode"""
    try:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)

        # Setup file logging
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.WARNING)

        # Setup formatter
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(module)s:%(funcName)s@%(lineno)d: %(message)s'
        )
        file_handler.setFormatter(formatter)

        # Get root logger and add handler
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)

        return True
    except Exception as e:
        print(f"Failed to setup daemon logging: {e}")
        return False


def daemonize():
    """
    Properly daemonize the process (Unix double-fork)
    Enhanced for PyInstaller compatibility
    This should ONLY be called when using DaemonType.DISABLED
    """
    import sys
    import logging

    log = logging.getLogger("daemon")
    pid = os.getpid()
    ppid = os.getppid()
    log.info(f"[DAEMONIZE] Before fork PID: {pid}, PPID: {ppid}")

    # Import PyInstaller runtime functions safely
    try:
        from mppsolar.daemon.pyinstaller_runtime import is_pyinstaller_bundle, has_been_spawned
    except ImportError:
        # Fallback if module not available
        def is_pyinstaller_bundle():
            return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
        def has_been_spawned():
            return os.environ.get("MPP_SOLAR_SPAWNED") == "1"

    # Special handling for PyInstaller spawned processes
    if is_pyinstaller_bundle() and has_been_spawned():
        log.info("[DAEMONIZE] Running in spawned PyInstaller process - using modified daemonization")

        # We're already in a subprocess, so we can do a simpler daemonization
        # Just do a single fork and session setup
        try:
            pid = os.fork()
            if pid > 0:
                log.info(f"[DAEMONIZE] Fork successful, parent exiting. Child PID: {pid}")
                sys.exit(0)
        except OSError as e:
            log.error(f"Fork failed in spawned PyInstaller process: {e}")
            sys.exit(1)

        # Set up daemon environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Redirect standard file descriptors
        _redirect_std_descriptors()
        log.info(f"[DAEMONIZE] PyInstaller daemon process ready. PID: {os.getpid()}")
        return

    # Standard daemonization for non-PyInstaller or direct execution
    log.info("[DAEMONIZE] Performing standard double-fork daemonization")

    # First fork
    try:
        pid = os.fork()
        if pid > 0:
            log.info(f"[DAEMONIZE] First fork successful, parent exiting. Child PID: {pid}")
            sys.exit(0)
    except OSError as e:
        log.error(f"First fork failed: {e}")
        sys.exit(1)

    # Decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            log.info(f"[DAEMONIZE] Second fork successful, intermediate parent exiting. Child PID: {pid}")
            sys.exit(0)
    except OSError as e:
        log.error(f"Second fork failed: {e}")
        sys.exit(1)

    # Redirect standard file descriptors
    _redirect_std_descriptors()
    log.info(f"[DAEMONIZE] Daemon process forked successfully. PID: {os.getpid()}")


def _redirect_std_descriptors():
    """Helper function to redirect standard file descriptors to /dev/null"""
    import sys

    sys.stdout.flush()
    sys.stderr.flush()

    try:
        with open('/dev/null', 'r') as si:
            os.dup2(si.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+') as so:
            os.dup2(so.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+') as se:
            os.dup2(se.fileno(), sys.stderr.fileno())
    except Exception as e:
        # If redirection fails, log the error but continue
        # (logging might not work after redirection anyway)
        pass


class Daemon:
    """ abstraction to support different daemon approaches / solutions """
    def __str__(self):
        return f"Daemon name: {self.__class__.__name__}"

    def initialize(self):
        """ Daemon initialization activities """
        log.debug("Base Daemon initialized")
        self._notify(self._Notification.READY)
        self._lastNotify = time()

    def get_watchdog_path(self):
        """Return the path for the watchdog file, derived from the PID file path."""
        return self.pid_file_path.replace(".pid", ".watchdog")

    def watchdog(self):
        log.debug("Base Daemon watchdog ping")
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

    def _get_effective_pid(self):
        """Return the PID to use for tracking this daemon.
        For PyInstaller parent processes, return os.getppid().
        For normal or spawned PyInstaller processes, return os.getpid().
        Place holder"""
        from mppsolar.daemon.pyinstaller_runtime import is_pyinstaller_bundle, is_spawned_pyinstaller_process
        if is_pyinstaller_bundle() and not is_spawned_pyinstaller_process():
            return os.getpid()
        return os.getpid()


    def log(self, message=None):
        # Print log message
        if message is not None:
            self._journal(message)
    
    # These methods should be overridden by subclasses
    def _notify(self, notification, message=None):
        pass
    
    def _journal(self, message):
        pass