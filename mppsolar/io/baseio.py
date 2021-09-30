from abc import ABC, abstractmethod
import logging

# from time import sleep
log = logging.getLogger("BaseIO")


class BaseIO(ABC):
    @abstractmethod
    def send_and_receive(self, *args, **kwargs) -> dict:
        raise NotImplementedError
