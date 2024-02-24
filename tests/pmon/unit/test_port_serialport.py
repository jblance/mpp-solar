""" test_serial_port.py """
import asyncio
from unittest import TestCase
from unittest.mock import Mock, patch

from powermon.commands.command import Command
from powermon.ports.serialport import SerialPort
from powermon.protocols.pi30max import PI30MAX


class TestSerialPort(TestCase):
    """ unit tests for the serial port object and functionality """
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.port = None
        self.command = None

    # Given
    def setUp(self):
        self.port = SerialPort(path='/dev/tty0', baud=None, protocol=PI30MAX(), identifier=None)

    def test_is_connected_when_port_is_open(self):
        """
        Test if is_connected() method return True if serial_port is not None and is_open is True
        """
        # When: serial_port.is_open == True
        with patch.object(self.port, 'serial_port', Mock(is_open=True)):
            # Then: is_connected() == True
            self.assertTrue(self.port.is_connected())

    def test_is_connected_when_port_not_open(self):
        """
        Test if is_connected() method return True if serial_port is not None and is_open is False
        """
        # When: serial_port.is_open == False
        with patch.object(self.port, 'serial_port', Mock(is_open=False)):
            # Then: isConnected() == False
            self.assertFalse(self.port.is_connected())

    def test_is_connected_when_port_is_none(self):
        """
        Test if is_connected() method return False if serial_port is None
        """
        # When: serial_port == None
        # Then: is_connected() == False
        self.assertFalse(self.port.is_connected())

    # def test_if_connection_is_open_before_run_command_if_port_not_open(self):
    #     """
    #     Port should open connection if not connected before run command
    #     """
    #     # Given:
    #     self.command = Mock(
    #         spec=Command,
    #         code="QPIRI",
    #         outputs=[Mock()],
    #         dueToRun=Mock(return_value=True),
    #         full_command="QPIRI"
    #     )
    #     # When:
    #     #   is_connected() == False
    #     #
    #     with patch.object(self.port, 'serial_port', Mock(is_open=False)):
    #         # Then: connect() called in run_command()
    #         with patch.object(self.port, 'connect') as connect_mock:
    #             self.port.run_command(self.command)
    #             connect_mock.assert_called()

    def test_if_port_not_reconnecting_when_already_open(self):
        """
        Port should not reconnect if already connected
        """
        # Given:
        self.command = Mock(
            spec=Command,
            code="QPIRI",
            outputs=[Mock()],
            dueToRun=Mock(return_value=True),
            full_command="QPIRI"
        )
        # When:
        #   is_connected() == True
        #
        with patch.object(self.port, 'serial_port', Mock(is_open=True)):
            # Then: connect() called in run_command()
            with patch.object(self.port, 'connect') as connect_mock:
                asyncio.run(self.port.run_command(self.command))
                connect_mock.assert_not_called()
