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
    """
    import logging
    from mppsolar.daemon.pyinstaller_runtime import is_pyinstaller_bundle, has_been_spawned

    log = logging.getLogger("daemon")
    pid = os.getpid()
    ppid = os.getppid()
    log.info(f"[DAEMONIZE] Before fork PID: {pid}, PPID: {ppid}")

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
        sys.stdout.flush()
        sys.stderr.flush()
        try:
            with open('/dev/null', 'r') as si: # Disable only while testing.
                os.dup2(si.fileno(), sys.stdin.fileno())
            with open('/dev/null', 'a+') as so:
                os.dup2(so.fileno(), sys.stdout.fileno())
            with open('/dev/null', 'a+') as se:
                os.dup2(se.fileno(), sys.stderr.fileno())
            log.info("[DAEMONIZE] Standard I/O redirected to /dev/null.") # This log won't appear on console
        except Exception as e:
            pass # Keep original pass here, as the log might not work yet
        log.info(f"[DAEMONIZE] PyInstaller daemon process ready. PID: {os.getpid()}")
        return

    # Standard daemonization for non-PyInstaller or direct execution
    try:
        pid = os.fork()
        if pid > 0:
            log.info(f"[DAEMONIZE] First fork successful, parent exiting. Child PID: {pid}")
            sys.exit(0)
    except OSError as e:
        log.error(f"First fork failed: {e}")
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            log.info(f"[DAEMONIZE] Second fork successful, intermediate parent exiting. Child PID: {pid}")
            sys.exit(0)
    except OSError as e:
        log.error(f"Second fork failed: {e}")
        sys.exit(1)

    # Redirect standard file descriptors to /dev/null
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as si:  # Disabled while testing pyinstaller code
        os.dup2(si.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a+') as so:
        os.dup2(so.fileno(), sys.stdout.fileno())
    with open('/dev/null', 'a+') as se:
        os.dup2(se.fileno(), sys.stderr.fileno())

    log.info(f"[DAEMONIZE] Daemon process forked successfully. PID: {os.getpid()}")



class Daemon:
    """ abstraction to support different daemon approaches / solutions """
    def __str__(self):
        return f"Daemon name: {self.__class__.__name__}"

    def initialize(self):
        """ Daemon initialization activities """
        log.debug("Base Daemon initialized")
        self._notify(self._Notification.READY)
        self._lastNotify = time()

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
        """
        from mppsolar.daemon.pyinstaller_runtime import is_pyinstaller_bundle, is_spawned_pyinstaller_process
        if is_pyinstaller_bundle() and not is_spawned_pyinstaller_process():
            return os.getppid()
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