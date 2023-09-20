from unittest import TestCase
from unittest.mock import patch, Mock
from powermon.ports.serialport import SerialPort

class test_serial_port(TestCase):

    def test_is_connected_true(self):
        """
        Test if isConnected() method return True if serialPort is not None
        """
        port = SerialPort(path=None, baud=None, protocol=None)
        with patch.object(port, 'serialPort', Mock()):
            
            self.assertTrue(port.isConnected())

    def test_is_connected_false(self):
        """
        Test if isConnected() method return False if serialPort is None
        """
        port = SerialPort(path=None, baud=None,protocol=None)

        self.assertFalse(port.isConnected())
   
