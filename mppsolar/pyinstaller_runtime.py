
import os
import sys
import time
import subprocess
import logging

log = logging.getLogger(__name__)


def is_pyinstaller_bundle():
    # True if running in a PyInstaller bundle
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def has_been_spawned():
    val = os.environ.get("MPP_SOLAR_SPAWNED")
    log.warning(f"has_been_spawned(): MPP_SOLAR_SPAWNED={val}")
    return val == "1"


def spawn_pyinstaller_subprocess(args):
    """
    Handles PyInstaller bootstrap-spawn logic to prevent premature termination
    of daemonized processes.
    Returns True if a subprocess is spawned and parent should exit.
    """
    if args.daemon and is_pyinstaller_bundle() and not has_been_spawned():
        log.warning("Running from PyInstaller — spawning subprocess to survive bootstrap parent")

        new_env = os.environ.copy()
        new_env["MPP_SOLAR_SPAWNED"] = "1"

        filtered_args = [arg for arg in sys.argv[1:] if arg != "--daemon"]
        cmd = [sys.executable] + filtered_args + ["--daemon"]

        log.debug(f"Spawning child subprocess: {cmd}")
        proc = subprocess.Popen(cmd, env=new_env, start_new_session=True)

        for _ in range(10):
            if proc.poll() is not None:
                log.error("Child process exited too soon!")
                return True
            time.sleep(0.5)

        log.debug("Child process started successfully; exiting parent")
        return True

    return False
