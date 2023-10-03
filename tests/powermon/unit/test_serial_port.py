from unittest import TestCase
from unittest.mock import patch, Mock
from powermon.ports.serialport import SerialPort
from powermon.commands.command import Command
from powermon.protocols.pi30max import pi30max

class test_serial_port(TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.port = None

    # Given
    def setUp(self):
        self.port = SerialPort(path=None, baud=None, protocol=pi30max())

    def test_is_connected_when_port_is_open(self):
        """
        Test if isConnected() method return True if serialPort is not None and is_open is True
        """
        # When: serialPort.is_open == True
        with patch.object(self.port, 'serialPort', Mock(is_open = True)):
            #Then: isConnected() == True
            self.assertTrue(self.port.isConnected())

    def test_is_connected_when_port_not_open(self):
        """
        Test if isConnected() method return True if serialPort is not None and is_open is False
        """
        #When: serialPort.is_open == False
        with patch.object(self.port, 'serialPort', Mock(is_open = False)):
            #Then: isConnected() == False
            self.assertFalse(self.port.isConnected())

    def test_is_connected_when_port_is_none(self):
        """
        Test if isConnected() method return False if serialPort is None
        """
        #When: serialPort == None
        #Then: isConnected() == False
        self.assertFalse(self.port.isConnected())

    def test_if_connection_is_open_before_run_command_if_port_not_open(self):
        """
        Port should open connection if not connected before run command
        """
        #Given:
        self.command = Mock(
                        spec=Command, 
                        code="QPIRI",
                        outputs = [Mock()],
                        dueToRun = Mock(return_value=True)
                    )
        #When: 
        #   isConnected() == False
        #
        with patch.object(self.port, 'serialPort', Mock(is_open = False)):
            #Then: connect() called in run_command()
            with patch.object(self.port, 'connect') as connectMock:
                self.port.run_command(self.command)   
                connectMock.assert_called_once()
    
    def test_if_port_not_reconnecting_when_already_open(self):
        """
        Port should not reconnect if already connected
        """
        #Given:
        self.command = Mock(
                        spec=Command, 
                        code="QPIRI",
                        outputs = [Mock()],
                        dueToRun = Mock(return_value=True)
                    )
        #When: 
        #   isConnected() == True
        #   
        with patch.object(self.port, 'serialPort', Mock(is_open = True)):    
            #Then: connect() called in run_command()
            with patch.object(self.port, 'connect') as connectMock:
                self.port.run_command(self.command)   
                connectMock.assert_not_called()