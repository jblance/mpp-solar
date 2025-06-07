""" pyinstaller_runtime.py """
import os
import sys
import time
import subprocess
import logging
import shutil
import tempfile
import atexit

log = logging.getLogger(__name__)


def is_pyinstaller_bundle():
    # True if running in a PyInstaller bundle
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def has_been_spawned():
    val = os.environ.get("MPP_SOLAR_SPAWNED")
    log.info(f"has_been_spawned(): MPP_SOLAR_SPAWNED={val}")
    return val == "1"

def is_spawned_pyinstaller_process():
    return is_pyinstaller_bundle() and has_been_spawned()


def copy_essential_files():
    """
    Copy essential files from PyInstaller temp dir to a permanent location
    Returns the permanent directory path
    """
    if not is_pyinstaller_bundle():
        return None

    try:
        # Create a permanent directory for our files
        permanent_dir = tempfile.mkdtemp(prefix="mpp_solar_", suffix="_daemon")
        log.info(f"Created permanent directory: {permanent_dir}")

        # Copy the entire extracted directory to permanent location
        meipass_contents = os.listdir(sys._MEIPASS)
        for item in meipass_contents:
            src = os.path.join(sys._MEIPASS, item)
            dst = os.path.join(permanent_dir, item)

            if os.path.isdir(src):
                shutil.copytree(src, dst, symlinks=True)
            else:
                shutil.copy2(src, dst)

        # Make sure the main script is executable
        main_script = os.path.join(permanent_dir, 'mpp-solar')
        if os.path.exists(main_script):
            os.chmod(main_script, 0o755)

        return permanent_dir

    except Exception as e:
        log.error(f"Failed to copy essential files: {e}")
        return None


def setup_permanent_environment(permanent_dir):
    """Set up environment to use permanent directory instead of _MEIPASS"""
    if permanent_dir:
        # Update sys.path to use permanent directory
        if sys._MEIPASS in sys.path:
            sys.path.remove(sys._MEIPASS)
        sys.path.insert(0, permanent_dir)

        # Update _MEIPASS to point to permanent directory
        sys._MEIPASS = permanent_dir
        
        # Register cleanup for permanent directory
        atexit.register(cleanup_permanent_directory, permanent_dir)
        
        log.info(f"Environment updated to use permanent directory: {permanent_dir}")


def cleanup_permanent_directory(permanent_dir):
    """Clean up the permanent directory on exit"""
    try:
        if os.path.exists(permanent_dir):
            shutil.rmtree(permanent_dir)
            log.info(f"Cleaned up permanent directory: {permanent_dir}")
    except Exception as e:
        log.warning(f"Failed to clean up permanent directory {permanent_dir}: {e}")


def _log_runtime_context(label, log_func=None):
    if log_func is None:
        log_func = log.debug

    pid = os.getpid()
    ppid = os.getppid()
    try:
        pgid = os.getpgid(0)
        sid = os.getsid(0)
    except OSError:
        pgid = "unknown"
        sid = "unknown"

    is_leader = (pid == pgid)
    frozen = getattr(sys, 'frozen', False)
    meipass = getattr(sys, '_MEIPASS', 'N/A')
    spawned = os.environ.get("MPP_SOLAR_SPAWNED", "N/A")
    permanent_dir = os.environ.get("MPP_SOLAR_PERMANENT_DIR", "N/A")

    log_func(f"[{label}] Process Info: PID={pid}, PPID={ppid}, PGID={pgid}, SID={sid}, Leader={is_leader}")
    log_func(f"[{label}] Sys Info: sys.frozen={frozen}, _MEIPASS={meipass}")
    log_func(f"[{label}] Env Info: MPP_SOLAR_SPAWNED={spawned}, MPP_SOLAR_PERMANENT_DIR={permanent_dir}")
    log_func(f"[{label}] Current Working Dir: {os.getcwd()}")


def cleanup_bootstrap_pid_file(pid_file_path):
    """
    Clean up PID file created by bootstrap process
    """
    try:
        if os.path.exists(pid_file_path):
            # Check if the PID in the file is our bootstrap process
            with open(pid_file_path, 'r') as f:
                bootstrap_pid = int(f.read().strip())

            current_pid = os.getpid()

            if bootstrap_pid == current_pid:
                log.info(f"Removing bootstrap PID file {pid_file_path} (PID {bootstrap_pid})")
                os.remove(pid_file_path)
            else:
                log.debug(f"PID file contains different PID {bootstrap_pid}, not our bootstrap PID {current_pid}")

    except Exception as e:
        log.warning(f"Failed to cleanup bootstrap PID file {pid_file_path}: {e}")


def spawn_pyinstaller_subprocess(args):
    """
    Handles PyInstaller bootstrap-spawn logic to prevent premature termination
    of daemonized processes.
    Returns True if a subprocess is spawned and parent should exit.
    """
    _log_runtime_context("PR_PARENT_ENTRY", log.debug)
    if args.daemon and is_pyinstaller_bundle() and not has_been_spawned():
        log.warning("Running from PyInstaller — spawning subprocess to survive bootstrap parent")
        _log_runtime_context("PR_PARENT_BEFORE_FORK", log.info)

        # Clean up any PID file created by the bootstrap process
        pid_file_paths = []

        # Try to determine the PID file path that might have been created
        if hasattr(args, 'pid_file') and args.pid_file:
            pid_file_paths.append(args.pid_file)

        # Add common default locations
        if os.geteuid() == 0:  # Running as root
            pid_file_paths.extend(["/var/run/mpp-solar.pid", "/var/run/mppsolard.pid"])
        else:
            if 'XDG_RUNTIME_DIR' in os.environ:
                pid_file_paths.append(os.path.join(os.environ['XDG_RUNTIME_DIR'], "mpp-solar.pid"))
            pid_file_paths.append("/tmp/mpp-solar.pid")

        # Clean up bootstrap-created PID files
        for pid_file_path in pid_file_paths:
            cleanup_bootstrap_pid_file(pid_file_path)

        # Create permanent copy of extracted files
        permanent_dir = copy_essential_files()
        if not permanent_dir:
            log.critical("Failed to create permanent copy of files")
            return False

        new_env = os.environ.copy()
        new_env["MPP_SOLAR_SPAWNED"] = "1"
        new_env["MPP_SOLAR_PERMANENT_DIR"] = permanent_dir

        # NEW: Pass information about cleaned up PID files
        new_env["MPP_SOLAR_CLEANED_PID_FILES"] = ",".join(pid_file_paths)

        executable = os.path.join(permanent_dir, os.path.basename(sys.executable))
        if not os.path.exists(executable):
            executable = sys.executable

        cmd_args = sys.argv[1:]
        if "--daemon" not in cmd_args:
            cmd_args.append("--daemon")

        cmd = [executable] + cmd_args

        log.info(f"Launching child with cmd: {' '.join(cmd)}")
        log.debug(f"Spawning child subprocess: {cmd}")
        log.debug(f"Working directory: {permanent_dir}")
        _log_runtime_context("PR_PARENT_SPAWNING", log.warning)
        log.warning(f"[SPAWN] sys.argv: {sys.argv}")
        log.warning(f"[SPAWN] final cmd: {cmd}")
        log.warning(f"[SPAWN] is_pyinstaller_bundle: {is_pyinstaller_bundle()}")
        log.warning(f"[SPAWN] has_been_spawned: {has_been_spawned()}")
        log.warning(f"[SPAWN] args.daemon: {args.daemon}")
#         print("ENV:", dict(os.environ)) # troubleshooting

        try:
            proc = subprocess.Popen(
                cmd, 
                env=new_env, 
                cwd=permanent_dir,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )

            # Wait a bit to ensure child process starts successfully
            for i in range(10):
                if proc.poll() is not None:
                    if proc.returncode == 0:
                        log.info(f"Child process (PID: {proc.pid}) exited cleanly (expected for daemon mode and PyInstaller bootstrap).")
                    else:
                        log.error(f"Child process (PID: {proc.pid}) exited prematurely with code: {proc.returncode}")
                        log.info("Child ENV MPP_SOLAR_SPAWNED = %s", os.environ.get("MPP_SOLAR_SPAWNED"))
                        log.info("Child ENV MPP_SOLAR_PERMANENT_DIR = %s", os.environ.get("MPP_SOLAR_PERMANENT_DIR"))
                    cleanup_permanent_directory(permanent_dir)
                    return True
                time.sleep(0.5)

            log.info(f"Child process started successfully with PID: {proc.pid}. Parent exiting.")
            return True
            
        except Exception as e:
            log.critical(f"Failed to spawn subprocess: {e}", exc_info=True)
            cleanup_permanent_directory(permanent_dir)
            return False

    return False


def setup_spawned_environment():
    """
    Set up environment for spawned process to use permanent directory
    """
    _log_runtime_context("PR_SPAWNED_CHILD_SETUP_ENTRY", log.debug)
    if has_been_spawned() and is_pyinstaller_bundle():
        permanent_dir = os.environ.get("MPP_SOLAR_PERMANENT_DIR")
        if permanent_dir and os.path.exists(permanent_dir):
            setup_permanent_environment(permanent_dir)
            _log_runtime_context("PR_SPAWNED_CHILD_SETUP_COMPLETE", log.info)

            # Log information about cleaned PID files
            cleaned_files = os.environ.get("MPP_SOLAR_CLEANED_PID_FILES", "")
            if cleaned_files:
                log.info(f"Bootstrap process cleaned up PID files: {cleaned_files}")

            return True
        else:
            _log_runtime_context("PR_SPAWNED_CHILD_SETUP_EXIT - Spawned process but permanent directory not found: {permanent_dir}. Continuing without explicit permanent environment setup.", log.warning)
    return False

import os
import logging
log = logging.getLogger(__name__)

def is_stale_pyinstaller_pid(check_func_bundle, check_func_spawned):
    """
    Check if the PID file contains a stale PyInstaller bootstrap process PID
    :param check_func_bundle: function that returns True if PyInstaller bundle
    :param check_func_spawned: function that returns True if PyInstaller has spawned
    :return: bool
    """
    try:
        return check_func_bundle() and check_func_spawned()
    except Exception:
        return False

def handle_stale_pid(pid_file_path, check_bundle, check_spawned, check_existing):
    """
    Check for stale PID files and handle removal logic.
    Returns True if it is safe to continue, or False if a daemon is already running or error occurs.
    """
    if is_stale_pyinstaller_pid(check_bundle, check_spawned):
        log.info("Removing stale PyInstaller bootstrap PID file")
        try:
            os.remove(pid_file_path)
        except Exception as e:
            log.error(f"Failed to remove stale PID file: {e}")
            return False
    elif check_existing():
        log.error("Another daemon instance is already running")
        return False
    else:
        log.info("Removing stale PID file")
        try:
            os.remove(pid_file_path)
        except Exception as e:
            log.error(f"Failed to remove stale PID file: {e}")
            return False
    return True
