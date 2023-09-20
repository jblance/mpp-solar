from unittest import TestCase
from unittest.mock import Mock
from powermon import Device
from powermon.ports import SerialPort
from powermon.commands.command import Command
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.protocols.pi30max import pi30max

class DeviceTest(TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.port = None
        self.device = None

    def setUp(self) -> None:
        self.port = Mock(spec=SerialPort, protocol = pi30max())
        self.device = Device(name="Test Device", port=self.port)

    def test_if_port_connect_before_run_command(self):
        """
        Test if connect() method on port is called inside runLoop() before run command
        """

        # Add command into command list with dueToRun=True to emulate running command
        self.device.add_command(
            Mock(
                spec=Command, 
                code="QPIRI",
                outputs = [Mock(spec=AbstractOutput)],
                dueToRun = Mock(return_value=True)
                )
            )
        #Pretend that port is disconnected
        self.port.isConnected.side_effect = [False, True]
    
        #Run main device loop. Expecting positive result
        self.assertTrue(self.device.runLoop())

        #Check that port connection has been checked
        self.port.isConnected.assert_called()
        #Check if port connection been established
        self.port.connect.assert_called()
        
    def test_if_port_is_not_connected(self):
        """
        Test if connect() method on port is called inside runLoop() but connection is not established
        """
        # Add command into command list with dueToRun=True to emulate running command
        self.device.add_command(
            Mock(
                spec=Command, 
                code="QPIRI",
                outputs = [Mock(spec=AbstractOutput)],
                dueToRun = Mock(return_value=True)
                )
            )
        #Pretend that port is disconnected
        self.port.isConnected.side_effect = [False, False]
    
        #Run main device loop. Expecting negative result due to closed port
        self.assertFalse(self.device.runLoop())

        #Check that port connection has been checked
        self.port.isConnected.assert_called()
        #Check if port connect method has been called
        self.port.connect.assert_called()