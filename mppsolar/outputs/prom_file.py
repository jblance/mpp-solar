import logging
import os
import tempfile
import atexit

from .prom import prom
from ..helpers import get_kwargs, is_daemon_mode

log = logging.getLogger("prom")


class prom_file(prom):
    prom_output_dir = ""
    # Class variable to track all created files for cleanup
    _created_files = set()
    _cleanup_registered = False

    def __str__(self):
        return "Node exporter Prometheus format to files for NodeExporter consumption"

    @classmethod
    def _register_cleanup(cls):
        """Register cleanup function once"""
        if not cls._cleanup_registered:
            atexit.register(cls._cleanup_all_files)
            cls._cleanup_registered = True

    @classmethod
    def _cleanup_all_files(cls):
        log.info("Cleaning up prometheus files...")
        removed = 0
        for file_path in cls._created_files.copy():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    removed += 1
                    log.debug(f"Removed prometheus file: {file_path}")
                cls._created_files.discard(file_path)
            except Exception as e:
                log.warning(f"Failed to remove prometheus file {file_path}: {e}")
        log.info(f"Cleanup complete, {removed} prometheus files removed.")

    @classmethod
    def cleanup_file(cls, file_path):
        """Remove a specific file and track it for cleanup"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                log.debug(f"Removed prometheus file: {file_path}")
            cls._created_files.discard(file_path)
        except Exception as e:
            log.warning(f"Failed to remove prometheus file {file_path}: {e}")

    def output(self, *args, **kwargs):
        # We override the method only to get the PushGateway URL from the config
        self.prom_output_dir = kwargs["prom_output_dir"]
        self.cmd = get_kwargs(kwargs, "data").get("_command", "").lower()
        self.name = get_kwargs(kwargs, "name")


        return super().output(*args, **kwargs)

    def handle_output(self, content: str) -> None:
        if self.name != "unnamed":
            self.filename = "{0}-{1}".format(self.name, self.cmd)
        else:
            self.filename = self.cmd

        file_path = f"{self.prom_output_dir.rstrip('/')}/mpp-solar-{self.filename}.prom"

        # Ensure output directory exists
        os.makedirs(self.prom_output_dir, exist_ok=True)

        try:
            # Create temporary file in the same directory as the target file
            # This ensures atomic move works (same filesystem)
            temp_fd, temp_path = tempfile.mkstemp(
                suffix='.tmp',
                prefix=f'mpp-solar-{self.filename}_',
                dir=self.prom_output_dir
            )

            try:
                # Write content to temporary file
                with os.fdopen(temp_fd, 'w') as temp_file:
                    temp_file.write(content)
                    temp_file.flush()
                    os.fsync(temp_file.fileno())  # Force write to disk
                    os.chmod(temp_path, 0o744)

                # Atomically move temp file to final location
                os.rename(temp_path, file_path)

                # Track these files for cleanup if daemon
                log.debug(f"is_daemon_mode(): {is_daemon_mode()}")
                if is_daemon_mode():
                    prom_file._created_files.add(file_path)
                    prom_file._register_cleanup()
                    log.debug(f"DAEMON_MODE - Registering PROM files for cleanup on exit.")

                log.debug(f"Successfully wrote prometheus file: {file_path}")

            except Exception as e:
                # Clean up temp file if something went wrong
                try:
                    os.unlink(temp_path)
                except:
                    pass
                raise e

        except Exception as e:
            log.error(f"Failed to write prometheus file {file_path}: {e}")
            raise
