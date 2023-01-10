import logging
import socket
import time

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger("remoteSocketIO")


class remoteSocketIO(BaseIO):
    def __init__(self, *args, **kwargs) -> None:
        self._remote_ip = get_kwargs(kwargs, "remote_ip")
        self._remote_port = get_kwargs(kwargs, "remote_port")

    def send_and_receive(self, *args, **kwargs) -> dict:
        full_command = get_kwargs(kwargs, "full_command")
        response_line = None
        log.debug(f"host ip: {self._remote_ip}, host port: {self._remote_port}")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self._remote_ip, self._remote_port))
                log.debug("Executing command via remoteserialio...")
                s.send(full_command)
                time.sleep(0.1)  # give serial port time to receive the data
                response_line = s.recv(1024)
                # response_line = s.read_until(b"\r")
                log.debug("socket response was: %s", response_line)
                return response_line
        except Exception as e:
            log.warning(f"socket read error: {e}")
        log.info("Command execution failed")
        return {"ERROR": ["Socket command execution failed", ""]}
