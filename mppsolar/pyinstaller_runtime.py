#!/usr/bin/env python3
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




def spawn_pyinstaller_subprocess(args):
    """
    Handles PyInstaller bootstrap-spawn logic to prevent premature termination
    of daemonized processes.
    Returns True if a subprocess is spawned and parent should exit.
    """
    if args.daemon and is_pyinstaller_bundle() and not has_been_spawned():
        log.warning("Running from PyInstaller — spawning subprocess to survive bootstrap parent")

        # Create permanent copy of extracted files
        permanent_dir = copy_essential_files()
        if not permanent_dir:
            log.error("Failed to create permanent copy of files")
            return False

        new_env = os.environ.copy()
        new_env["MPP_SOLAR_SPAWNED"] = "1"
        new_env["MPP_SOLAR_PERMANENT_DIR"] = permanent_dir
        executable = os.path.join(permanent_dir, os.path.basename(sys.executable))
        if not os.path.exists(executable):
            executable = sys.executable

#         cmd = [executable] + sys.argv[1:]
        cmd = [executable] + [arg for arg in sys.argv[1:] if arg != "--daemon"] + ["--daemon"]

        log.info(f"Launching child with cmd: {' '.join(cmd)}")
        log.debug(f"Spawning child subprocess: {cmd}")
        log.debug(f"Working directory: {permanent_dir}")
        
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
                        log.info("Child process daemonized and exited cleanly (expected for daemon mode)")
                    else:
                        log.error(f"Child process exited prematurely with code: {proc.returncode}")
                    cleanup_permanent_directory(permanent_dir)
                    return True
                time.sleep(0.5)

            log.info(f"Child process started successfully with PID: {proc.pid}")
            log.info("Parent process exiting - child will continue as daemon")
            return True
            
        except Exception as e:
            log.error(f"Failed to spawn subprocess: {e}")
            cleanup_permanent_directory(permanent_dir)
            return False

    return False


def setup_spawned_environment():
    """
    Set up environment for spawned process to use permanent directory
    """
    if has_been_spawned() and is_pyinstaller_bundle():
        permanent_dir = os.environ.get("MPP_SOLAR_PERMANENT_DIR")
        if permanent_dir and os.path.exists(permanent_dir):
            setup_permanent_environment(permanent_dir)
            log.info("Spawned process environment configured")
            return True
        else:
            log.warning("Spawned process but permanent directory not found")
    return False
