""" abstractport.py """
import logging
from abc import ABC, abstractmethod

from powermon.commands.result import Result
from powermon.protocols.abstractprotocol import AbstractProtocol
from powermon.commands.command import Command


log = logging.getLogger("Port")


class AbstractPort(ABC):
    """
    model for all ports
    """

    @classmethod
    @abstractmethod
    def from_config(cls, config=None):
        """ build port object from config dict """
        raise NotImplementedError

    def __init__(self, protocol: AbstractProtocol):
        self.protocol: AbstractProtocol = protocol

    def connect(self) -> int:  # QUESTION: what does the int signify? 0 success, 1? fail, others???
        """ default port connect function """
        log.debug("Port connect not implemented")
        return 0

    def disconnect(self) -> None:
        """ default port disconnect function """
        log.debug("Port disconnect not implemented")

    def is_connected(self):
        """ default is_connected function """
        log.debug("Port is_connected not implemented")
        return True

    @abstractmethod
    def send_and_receive(self, command: Command) -> Result:
        """ main worker function for port objects, specific to each port type """
        raise NotImplementedError

    @abstractmethod
    def to_dto(self):
        """ convert port object to data transfer object """
        raise NotImplementedError

    def get_protocol(self) -> AbstractProtocol:
        """ return the protocol associated with this port """
        return self.protocol

    def run_command(self, command: Command) -> Result:
        """ run_command takes a command object, runs the command and returns a result object (replaces process_command) """
        log.debug("Command %s", command)

        # open port if it is closed
        if not self.is_connected():
            self.connect()
        # FIXME: what if still not connected....
        # ??

        # update run times
        command.touch()
        # update full_command - expand any template / add crc etc
        # updates every run incase something has changed
        command.set_full_command(self.get_protocol().get_full_command(command.code))

        # run the command via the 'send_and_receive port function
        result = self.send_and_receive(command)
        log.debug("after send_and_receive: %s", result)
        return result
