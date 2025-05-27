""" daemon_openrc.py """
import logging
import os
import signal
import sys
from enum import Enum
from pathlib import Path
from time import time

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

from mppsolar.daemon.daemon import Daemon

# Set-up logger
log = logging.getLogger("daemon_openrc")


class OpenRCNotification(Enum):
    READY = "READY"
    STATUS = "STATUS"
    STOPPING = "STOPPING"
    WATCHDOG = "WATCHDOG"

class DaemonOpenRC(Daemon):
    """ OpenRC daemon implementation with signal handling and PID management """
    
    def __str__(self):
        return "Daemon OpenRC"
    
    def __init__(self):
        self._notify = self._openrc_notify
        self._journal = self._journal
        self._Notification = OpenRCNotification
        self.keepalive = 60
        self._lastNotify = time()
        self._pid_file = None
        self._running = True
        
        # Default PID file location - can be overridden
        self.pid_file_path = "/var/run/mpp-solar.pid"
        
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Optional: Handle SIGHUP for config reload
        signal.signal(signal.SIGHUP, self._sighup_handler)
    
    def _signal_handler(self, signum, frame):
        """ Handle SIGTERM and SIGINT for clean shutdown """
        log.info(f"Received signal {signum}, initiating clean shutdown...")
        self._running = False
        self.stop()
        self._cleanup_pid_file()
        sys.exit(0)
    
    def _sighup_handler(self, signum, frame):
        """ Handle SIGHUP for potential config reload """
        log.info("Received SIGHUP - config reload not implemented yet")
        # Future: implement config reload functionality
    
    def _create_pid_file(self):
        """ Create PID file with current process ID """
        try:
            # Ensure directory exists
            pid_dir = Path(self.pid_file_path).parent
            pid_dir.mkdir(parents=True, exist_ok=True)
            
            # Create PID file exclusively (fail if exists)
            with open(self.pid_file_path, 'x') as pid_file:
                pid_file.write(str(os.getpid()))
            log.info(f"Created PID file: {self.pid_file_path}")
            return True
        except FileExistsError:
            log.error(f"PID file {self.pid_file_path} already exists - daemon may already be running")
            return False
        except Exception as e:
            log.error(f"Failed to create PID file {self.pid_file_path}: {e}")
            return False
    
    def _cleanup_pid_file(self):
        """ Remove PID file on shutdown """
        try:
            if os.path.exists(self.pid_file_path):
                os.remove(self.pid_file_path)
                log.info(f"Removed PID file: {self.pid_file_path}")
        except Exception as e:
            log.error(f"Failed to remove PID file {self.pid_file_path}: {e}")
    
    def _check_existing_daemon(self):
        """ Check if daemon is already running """
        if not os.path.exists(self.pid_file_path):
            return False
        
        try:
            with open(self.pid_file_path, 'r') as pid_file:
                pid = int(pid_file.read().strip())
            
            if HAS_PSUTIL:
                # Use psutil to check if process exists and is our daemon
                try:
                    process = psutil.Process(pid)
                    if process.is_running():
                        log.warning(f"Daemon already running with PID {pid}")
                        return True
                except psutil.NoSuchProcess:
                    log.info(f"Stale PID file found, removing: {self.pid_file_path}")
                    os.remove(self.pid_file_path)
                    return False
            else:
                # Fallback: check if PID exists in /proc (Linux-specific)
                if os.path.exists(f"/proc/{pid}"):
                    log.warning(f"Daemon may already be running with PID {pid}")
                    return True
                else:
                    log.info(f"Stale PID file found, removing: {self.pid_file_path}")
                    os.remove(self.pid_file_path)
                    return False
                    
        except (ValueError, FileNotFoundError) as e:
            log.error(f"Invalid PID file {self.pid_file_path}: {e}")
            return False
        
        return False
    
    def initialize(self):
        """ Initialize daemon - create PID file and set up """
        log.info("Initializing OpenRC daemon...")
        
        # Check if daemon is already running
        if self._check_existing_daemon():
            log.error("Daemon is already running. Exiting.")
            sys.exit(1)
        
        # Create PID file
        if not self._create_pid_file():
            log.error("Failed to create PID file. Exiting.")
            sys.exit(1)
        
        # Call parent initialization
        super().initialize()
        log.info("OpenRC daemon initialized successfully")
    
    def _openrc_notify(self, notification, message=None):
        """ Internal notification method """
        if message:
            log.info(f"Daemon notification: {notification} - {message}")
        else:
            log.info(f"Daemon notification: {notification}")
    
    def _openrc_journal(self, message):
        """ Internal journal method - just log """
        log.info(f"Daemon journal: {message}")
    
    def watchdog(self):
        """ Watchdog function - just log activity """
        elapsed = time() - self._lastNotify
        if elapsed > self.keepalive:
            self._lastNotify = time()
            log.debug(f"Daemon watchdog at {self._lastNotify}")
    
    def notify(self, status="OK"):
        """ Send notification - just log for OpenRC """
        log.info(f"Daemon status: {status}")
    
    def stop(self):
        """ Stop daemon gracefully """
        log.info("Stopping OpenRC daemon...")
        self._running = False
    
    def is_running(self):
        """ Check if daemon should continue running """
        return self._running
    
    @staticmethod
    def stop_daemon(pid_file_path="/var/run/mpp-solar.pid"):
        """ Static method to stop a running daemon """
        if not os.path.exists(pid_file_path):
            print(f"PID file {pid_file_path} not found - daemon may not be running")
            return False
        
        try:
            with open(pid_file_path, 'r') as pid_file:
                pid = int(pid_file.read().strip())
            
            print(f"Stopping daemon with PID {pid}")
            
            # Send SIGTERM first
            os.kill(pid, signal.SIGTERM)
            
            if HAS_PSUTIL:
                try:
                    process = psutil.Process(pid)
                    # Wait up to 10 seconds for graceful shutdown
                    process.wait(timeout=10)
                    print("Daemon stopped gracefully")
                except psutil.TimeoutExpired:
                    print("Daemon didn't stop gracefully, sending SIGKILL")
                    process.kill()
                except psutil.NoSuchProcess:
                    print("Daemon already stopped")
            else:
                # Fallback: just send SIGKILL after a delay
                import time
                time.sleep(2)
                try:
                    os.kill(pid, signal.SIGKILL)
                    print("Sent SIGKILL to daemon")
                except ProcessLookupError:
                    print("Daemon already stopped")
            
            # Clean up PID file
            if os.path.exists(pid_file_path):
                os.remove(pid_file_path)
                print(f"Removed PID file: {pid_file_path}")
            
            return True
            
        except (ValueError, FileNotFoundError, ProcessLookupError) as e:
            print(f"Error stopping daemon: {e}")
            return False
    
    def _notify(self, notification, message=None):
        """ Internal notification method """
        if message:
            log.info(f"Daemon notification: {notification.name} - {message}")
        else:
            log.info(f"Daemon notification: {notification.name}")
    
    def _journal(self, message):
        """ Internal journal method - just log """
        log.info(f"Daemon journal: {message}")
    
    # Define notification enum locally since it's not in parent
    class _Notification:
        class NotificationType:
            def __init__(self, name):
                self.name = name
        
        READY = NotificationType("READY")
        WATCHDOG = NotificationType("WATCHDOG")
        STATUS = NotificationType("STATUS")
        STOPPING = NotificationType("STOPPING")

