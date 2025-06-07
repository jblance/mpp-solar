""" daemon_openrc.py - Fixed version for PyInstaller compatibility """
import logging
import os
from mppsolar.daemon.pyinstaller_runtime import handle_stale_pid
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
        import logging
        log = logging.getLogger("daemon_openrc")
    
        pid = os.getpid()
        ppid = os.getppid()
        log.info(f"[OPENRC_INIT] Creating OpenRC daemon: PID={pid}, PPID={ppid}")
    
        self._Notification = OpenRCNotification
        self.keepalive = 60
        self._lastNotify = time.time()
        self._pid_file = None
        self._running = True
        self._pid_file_created = False  # NEW: Track if we created the PID file

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

    def _check_existing_daemon(self):
        """Check if daemon with PID from file is actually running"""
        try:
            with open(self.pid_file_path, 'r') as pid_file:
                content = pid_file.read().strip()
                if not content:
                    log.warning("PID file is empty")
                    return False

                pid = int(content)
                current_pid = os.getpid()

                # If the PID in the file is our current PID, that's fine
                if pid == current_pid:
                    log.info(f"PID file contains our own PID {pid}, continuing")
                    return False

                log.debug(f"Checking if PID {pid} is running...")

                if HAS_PSUTIL:
                    # Use psutil if available for more reliable process checking
                    try:
                        process = psutil.Process(pid)
                        if process.is_running():
                            # Additional check - is it actually our process name?
                            try:
                                process_name = process.name()
                                cmdline = ' '.join(process.cmdline())
                                log.info(f"Process {pid} is running: {process_name}")
                                log.debug(f"Process {pid} cmdline: {cmdline}")

                                # Check if it's likely our own process (mpp-solar related)
                                if 'mpp-solar' in process_name or 'mpp-solar' in cmdline:
                                    return True
                                else:
                                    log.warning(f"Process {pid} exists but doesn't appear to be mpp-solar")
                                    return False
                            except (psutil.AccessDenied, psutil.ZombieProcess):
                                # If we can't get process details, assume it's running
                                return True
                        else:
                            log.info(f"Process {pid} is not running")
                            return False
                    except psutil.NoSuchProcess:
                        log.info(f"No process found with PID {pid}")
                        return False
                else:
                    # Fallback to os.kill method
                    try:
                        # Send signal 0 to check if process exists without killing it
                        os.kill(pid, 0)
                        log.info(f"Process {pid} exists and is running")
                        return True
                    except OSError:
                        log.info(f"No process found with PID {pid}")
                        return False

        except (ValueError, FileNotFoundError, PermissionError) as e:
            log.warning(f"Could not check existing daemon: {e}")
            return False

    def _safe_import_pyinstaller_runtime(self):
        """
        Safely import PyInstaller runtime functions with fallback
        Returns tuple: (is_pyinstaller_bundle_func, has_been_spawned_func)
        """
        try:
            from mppsolar.daemon.pyinstaller_runtime import is_pyinstaller_bundle, has_been_spawned
            return is_pyinstaller_bundle, has_been_spawned
        except ImportError:
            log.debug("Could not import pyinstaller_runtime, using fallback functions")
            # Fallback functions that return safe defaults
            def fallback_is_pyinstaller_bundle():
                return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

            def fallback_has_been_spawned():
                return os.environ.get("MPP_SOLAR_SPAWNED") == "1"

            return fallback_is_pyinstaller_bundle, fallback_has_been_spawned

    

            if not os.path.exists(self.pid_file_path):
                return False

            with open(self.pid_file_path, 'r') as pid_file:
                content = pid_file.read().strip()
                if not content:
                    return False

                old_pid = int(content)
                current_pid = os.getpid()

                if old_pid == current_pid:
                    return False

                # Check if the old PID is still running
                if HAS_PSUTIL:
                    try:
                        process = psutil.Process(old_pid)
                        if process.is_running():
                            cmdline = ' '.join(process.cmdline())
                            # If it's a PyInstaller bootstrap process, it's likely stale
                            if 'mpp-solar' in cmdline and process.ppid() != os.getppid():
                                log.info(f"Detected potential stale PyInstaller bootstrap PID {old_pid}")
                                return True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        # Process doesn't exist, definitely stale
                        return True
                else:
                    # Fallback: if we can't signal the process, assume it's stale
                    try:
                        os.kill(old_pid, 0)
                        return False  # Process exists
                    except OSError:
                        return True  # Process doesn't exist, stale

        except Exception as e:
            log.debug(f"Error checking for stale PyInstaller PID: {e}")

        return False

    def _create_pid_file(self):
        """ Create PID file with current process ID """
        pid = self._get_effective_pid()
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

                # Special handling for PyInstaller stale PIDs
                if not handle_stale_pid(
                    self.pid_file_path,
                    *self._safe_import_pyinstaller_runtime(),
                    self._check_existing_daemon,
                ):
                    return False
                elif self._check_existing_daemon():
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
                self._pid_file_created = True  # NEW: Mark that we created it

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
        # Only clean up if we created the PID file
        if not self._pid_file_created:
            log.debug("Skipping PID file cleanup - we didn't create it")
            return
            
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
                except (ValueError, FileNotFoundError):
                    # File doesn't exist or has invalid content, try to remove anyway
                    os.remove(self.pid_file_path)
                    log.info(f"Removed PID file: {self.pid_file_path}")
        except Exception as e:
            log.error(f"Failed to remove PID file {self.pid_file_path}: {e}")
        #----- clean up watchdog file ----#
        watchdog_path = self.get_watchdog_path()
        if os.path.exists(watchdog_path):
            try:
                os.remove(watchdog_path)
                log.info(f"Removed watchdog file: {watchdog_path}")
            except Exception as e:
                log.warning(f"Failed to remove watchdog file: {e}")

    def initialize(self):
        """Initialize daemon and create PID file"""
        log.info("Initializing OpenRC daemon...")

        pid = os.getpid()
        ppid = os.getppid()
        log.info(f"[OPENRC_INITIALIZE] Before PID file creation: PID={pid}, PPID={ppid}")

        # Create PID file
        if not self._create_pid_file():
            log.error("Failed to create PID file, daemon cannot start")
            sys.exit(1)
        log.info(f"[OPENRC_INITIALIZE] After PID file creation: PID={pid}, PPID={ppid}")

        # Call parent initialization
        super().initialize()
        log.info("OpenRC daemon initialized successfully")

    def stop(self):
        """Stop daemon and clean up"""
        log.info("Stopping OpenRC daemon...")
        self._running = False
        super().stop()

    def is_running(self):
        """Check if daemon should continue running"""
        return self._running

    @classmethod
    def stop_daemon(cls, pid_file_path):
        """Class method to stop a running daemon by PID file"""
        log.info(f"Attempting to stop daemon using PID file: {pid_file_path}")

        try:
            if not os.path.exists(pid_file_path):
                log.error(f"PID file not found: {pid_file_path}")
                return False

            with open(pid_file_path, 'r') as pid_file:
                content = pid_file.read().strip()
                if not content:
                    log.error("PID file is empty")
                    return False

                pid = int(content)
                log.info(f"Found PID {pid} in file, attempting to terminate...")

                # Check if process exists before trying to kill it
                try:
                    os.kill(pid, 0)  # Signal 0 just checks if process exists
                except OSError:
                    log.warning(f"Process {pid} not found, removing stale PID file")
                    try:
                        os.remove(pid_file_path)
                    except:
                        pass
                    return True  # Consider this success since daemon isn't running

                # Try graceful shutdown first (SIGTERM)
                try:
                    log.info(f"Sending SIGTERM to PID {pid}")
                    os.kill(pid, signal.SIGTERM)

                    # Wait a bit for graceful shutdown
                    for i in range(10):  # Wait up to 10 seconds
                        time.sleep(1)
                        try:
                            os.kill(pid, 0)  # Check if still running
                        except OSError:
                            # Process has terminated
                            log.info(f"Process {pid} terminated gracefully")
                            # Clean up PID file if it still exists
                            if os.path.exists(pid_file_path):
                                try:
                                    os.remove(pid_file_path)
                                    log.info(f"Removed PID file: {pid_file_path}")
                                except:
                                    pass
                            return True

                    # If still running, try SIGKILL
                    log.warning(f"Process {pid} didn't respond to SIGTERM, sending SIGKILL")
                    os.kill(pid, signal.SIGKILL)

                    # Wait for force kill
                    for i in range(5):  # Wait up to 5 seconds
                        time.sleep(1)
                        try:
                            os.kill(pid, 0)  # Check if still running
                        except OSError:
                            # Process has terminated
                            log.info(f"Process {pid} terminated forcefully")
                            # Clean up PID file
                            if os.path.exists(pid_file_path):
                                try:
                                    os.remove(pid_file_path)
                                    log.info(f"Removed PID file: {pid_file_path}")
                                except:
                                    pass
                            return True

                    log.error(f"Failed to terminate process {pid}")
                    return False

                except OSError as e:
                    log.error(f"Failed to send signal to process {pid}: {e}")
                    return False

        except (ValueError, FileNotFoundError, PermissionError) as e:
            log.error(f"Error stopping daemon: {e}")
            return False
            
            
    def watchdog(self):
        """OpenRC watchdog heartbeat"""
        now = time.time()
        time_since_last = now - self._lastNotify
        self._lastNotify = now

        log.debug(f"[WATCHDOG] Ping at {time.strftime('%Y-%m-%d %H:%M:%S')} (Δ {time_since_last:.2f}s)")

        # Use PID-derived watchdog path
        watchdog_path = self.get_watchdog_path()

        try:
            with open(watchdog_path, "w") as f:
                f.write(f"watchdog ping: {int(now)}\n")
        except Exception as e:
            log.warning(f"Watchdog write failed: {e}")


    def _notify(self, notification, message=None):
        """Handle daemon notifications"""
        if message:
            log.info(f"Daemon notification: {notification.value} - {message}")
        else:
            log.debug(f"Daemon notification: {notification.value}")

    def _journal(self, message):
        """Log message to system journal (or regular log)"""
        log.info(message)