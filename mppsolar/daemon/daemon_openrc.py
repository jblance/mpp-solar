""" daemon_openrc.py """
import logging
import os
import signal
import sys
import time
import atexit
from enum import Enum
from pathlib import Path

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
    """ OpenRC daemon implementation with signal handling and configurable PID management """
    
    def __str__(self):
        return f"Daemon OpenRC (PID file: {self.pid_file_path})"
    
    def __init__(self, pid_file_path=None):
        self._notify = self._openrc_notify
        self._journal = self._openrc_journal
        self._Notification = OpenRCNotification
        self.keepalive = 60
        self._lastNotify = time.time()
        self._pid_file = None
        self._running = True
        
        # Set PID file location with smart defaults
        if pid_file_path:
            self.pid_file_path = pid_file_path
        else:
            # Auto-determine based on permissions and environment
            if os.geteuid() == 0:  # Running as root
                self.pid_file_path = "/var/run/mpp-solar.pid"
            else:  # Non-root user
                # Try user-specific locations
                if 'XDG_RUNTIME_DIR' in os.environ:
                    self.pid_file_path = os.path.join(os.environ['XDG_RUNTIME_DIR'], "mpp-solar.pid")
                else:
                    self.pid_file_path = "/tmp/mpp-solar.pid"
        
        log.info(f"PID file will be created at: {self.pid_file_path}")
        
        # Register cleanup function to run on exit
        atexit.register(self._cleanup_pid_file)
        
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Optional: Handle SIGHUP for config reload
        signal.signal(signal.SIGHUP, self._sighup_handler)
    
    def set_pid_file_path(self, path):
        """Allow external setting of PID file path"""
        old_path = self.pid_file_path
        self.pid_file_path = path
        log.info(f"PID file path changed from {old_path} to {self.pid_file_path}")
    
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
        pid = os.getpid()
        log.info(f"Creating PID file {self.pid_file_path} with PID {pid}")
        
        try:
            # Ensure directory exists and is writable
            pid_dir = Path(self.pid_file_path).parent
            pid_dir.mkdir(parents=True, exist_ok=True)
            log.debug(f"PID directory ensured: {pid_dir}")
            
            # Check directory permissions
            if not os.access(pid_dir, os.W_OK):
                log.error(f"No write permission for PID directory: {pid_dir}")
                return False
            
            # Check if file already exists and handle appropriately
            if os.path.exists(self.pid_file_path):
                log.warning(f"PID file {self.pid_file_path} already exists, checking if daemon is running...")
                if self._check_existing_daemon():
                    log.error("Another daemon instance is already running")
                    return False
                else:
                    log.info("Removing stale PID file")
                    try:
                        os.remove(self.pid_file_path)
                    except Exception as e:
                        log.error(f"Failed to remove stale PID file: {e}")
                        return False
            
            # Create PID file with explicit write and flush
            try:
                # Use atomic write operation where possible
                temp_pid_file = f"{self.pid_file_path}.tmp"
                
                with open(temp_pid_file, 'w') as pid_file:
                    pid_file.write(str(pid))
                    pid_file.flush()  # Ensure data is written to disk
                    os.fsync(pid_file.fileno())  # Force kernel to write to disk
                
                # Atomically move temp file to final location
                os.rename(temp_pid_file, self.pid_file_path)
                
                log.info(f"Successfully created PID file: {self.pid_file_path} with PID {pid}")
                
                # Verify the file was written correctly
                with open(self.pid_file_path, 'r') as verify_file:
                    written_pid = verify_file.read().strip()
                    if written_pid != str(pid):
                        log.error(f"PID file verification failed: expected {pid}, got '{written_pid}'")
                        return False
                    log.debug(f"PID file verification successful: {written_pid}")
                
                return True
                
            except Exception as e:
                log.error(f"Failed to write to PID file {self.pid_file_path}: {e}")
                # Clean up temporary file if it exists
                temp_pid_file = f"{self.pid_file_path}.tmp"
                if os.path.exists(temp_pid_file):
                    try:
                        os.remove(temp_pid_file)
                    except:
                        pass
                return False
                
        except Exception as e:
            log.error(f"Failed to create PID file {self.pid_file_path}: {e}")
            return False
    
    def _cleanup_pid_file(self):
        """ Remove PID file on shutdown """
        try:
            if os.path.exists(self.pid_file_path):
                # Verify it's our PID before removing
                try:
                    with open(self.pid_file_path, 'r') as pid_file:
                        content = pid_file.read().strip()
                        if content and int(content) == os.getpid():
                            os.remove(self.pid_file_path)
                            log.info(f"Removed PID file: {self.pid_file_path}")
                        else:
                            log.warning(f"PID file contains different PID ({content}), not removing")
                except ValueError:
                    log.warning(f"PID file contains invalid data, removing anyway")
                    os.remove(self.pid_file_path)
        except Exception as e:
            log.error(f"Failed to remove PID file {self.pid_file_path}: {e}")
    
    def _check_existing_daemon(self):
        """ Check if daemon is already running """
        if not os.path.exists(self.pid_file_path):
            return False
        
        try:
            with open(self.pid_file_path, 'r') as pid_file:
                content = pid_file.read().strip()
                if not content:
                    log.warning(f"Empty PID file found: {self.pid_file_path}")
                    return False
                
                pid = int(content)
                log.debug(f"Found PID {pid} in PID file")
            
            if HAS_PSUTIL:
                # Use psutil to check if process exists and is our daemon
                try:
                    process = psutil.Process(pid)
                    if process.is_running():
                        # Additional check: verify it's actually our process
                        cmdline = ' '.join(process.cmdline())
                        if 'mpp-solar' in cmdline or 'mppsolar' in cmdline:
                            log.warning(f"Daemon already running with PID {pid}")
                            return True
                        else:
                            log.info(f"PID {pid} exists but is not our daemon process")
                            return False
                except psutil.NoSuchProcess:
                    log.info(f"Stale PID file found (process {pid} doesn't exist), removing: {self.pid_file_path}")
                    try:
                        os.remove(self.pid_file_path)
                    except:
                        pass
                    return False
            else:
                # Fallback: check if PID exists in /proc (Linux-specific)
                if os.path.exists(f"/proc/{pid}"):
                    log.warning(f"Daemon may already be running with PID {pid}")
                    return True
                else:
                    log.info(f"Stale PID file found (no /proc/{pid}), removing: {self.pid_file_path}")
                    try:
                        os.remove(self.pid_file_path)
                    except:
                        pass
                    return False
                    
        except (ValueError, FileNotFoundError) as e:
            log.error(f"Invalid PID file {self.pid_file_path}: {e}")
            # Remove invalid PID file
            try:
                os.remove(self.pid_file_path)
                log.info("Removed invalid PID file")
            except:
                pass
            return False
        
        return False
    
    def initialize(self):
        """ Initialize daemon - create PID file and set up """
        log.info("Initializing OpenRC daemon...")
        log.info(f"Current process PID: {os.getpid()}")
        log.info(f"PID file location: {self.pid_file_path}")
        
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
        elapsed = time.time() - self._lastNotify
        if elapsed > self.keepalive:
            self._lastNotify = time.time()
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
    def stop_daemon(pid_file_path):
        """ Static method to stop a running daemon """
        if not os.path.exists(pid_file_path):
            print(f"PID file {pid_file_path} not found - daemon may not be running")
            return False
        
        try:
            with open(pid_file_path, 'r') as pid_file:
                content = pid_file.read().strip()
                if not content:
                    print(f"Empty PID file found: {pid_file_path}")
                    os.remove(pid_file_path)
                    return False
                
                pid = int(content)
            
            print(f"Stopping daemon with PID {pid}")
            
            # Send SIGTERM first
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                print("Process not found - daemon may have already stopped")
                # Clean up PID file
                try:
                    os.remove(pid_file_path)
                    print(f"Removed stale PID file: {pid_file_path}")
                except:
                    pass
                return True
            
            if HAS_PSUTIL:
                try:
                    process = psutil.Process(pid)
                    # Wait up to 10 seconds for graceful shutdown
                    process.wait(timeout=10)
                    print("Daemon stopped gracefully")
                except psutil.TimeoutExpired:
                    print("Daemon didn't stop gracefully, sending SIGKILL")
                    try:
                        process.kill()
                        print("Sent SIGKILL to daemon")
                    except psutil.NoSuchProcess:
                        print("Process already gone")
                except psutil.NoSuchProcess:
                    print("Daemon already stopped")
            else:
                # Fallback: just send SIGKILL after a delay
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