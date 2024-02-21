import asyncio
from unittest import TestCase
from unittest.mock import Mock

from powermon import Device
from powermon.commands.command import Command
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.ports import SerialPort
from powermon.protocols.pi30 import PI30


class DeviceTest(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.port = None
        self.device = None

    def setUp(self) -> None:
        self.port = Mock(spec=SerialPort, protocol=PI30())
        self.device = Device(name="Test Device", port=self.port)

    def test_if_output_processed_in_success_run(self):
        """
        Test if output process called in success command run
        """

        # Add command into command list with dueToRun=True to emulate running command
        output = Mock(spec=AbstractOutput)
        self.device.add_command(Mock(spec=Command, code="Q1", outputs=[output], dueToRun=Mock(return_value=True)))

        # Run main device loop. Expecting positive result
        # self.assertTrue(self.device.run())
        asyncio.run(self.device.run())
        output.process.assert_called()
