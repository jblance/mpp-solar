# import importlib
import logging
from abc import ABC

from mppsolar.version import __version__  # noqa: F401
from mppsolar.helpers import get_kwargs
from mppsolar.inout import get_port
from mppsolar.protocols import get_protocol

PORT_TYPE_UNKNOWN = 0
PORT_TYPE_TEST = 1
PORT_TYPE_USB = 2
PORT_TYPE_ESP32 = 4
PORT_TYPE_SERIAL = 8
PORT_TYPE_JKBLE = 16
PORT_TYPE_MQTT = 32
PORT_TYPE_VSERIAL = 64
PORT_TYPE_DALYSERIAL = 128

log = logging.getLogger("device")


class AbstractDevice(ABC):
    """
    Abstract device class with improved error handling
    """

    def __init__(self, *args, **kwargs):
        log.debug(f"__init__ args {args}")
        log.debug(f"__init__ kwargs {kwargs}")
        self._name = get_kwargs(kwargs, "name")
        self._port = get_port(**kwargs)
        self._protocol = get_protocol(get_kwargs(kwargs, "protocol"))
        log.debug(f"__init__ name {self._name}, port {self._port}, protocol {self._protocol}")

    def __str__(self):
        """
        Build a printable representation of this class
        """
        return f"{self._classname} device - name: {self._name}, port: {self._port}, protocol: {self._protocol}"

    def run_command(self, command) -> dict:
        """
        Generic method for running a 'raw' command with improved error handling
        """
        log.info(f"Running command {command}")

        # Pre-flight checks
        if self._protocol is None:
            error_msg = "Attempted to run command with no protocol defined"
            log.error(error_msg)
            return {"ERROR": [error_msg, ""]}
            
        if self._port is None:
            error_msg = f"No communications port defined - unable to run command {command}"
            log.error(error_msg)
            return {"ERROR": [error_msg, ""]}

        # Handle special commands
        if command == "list_commands":
            return self._protocol.list_commands()
        if command == "get_status":
            return self.get_status()
        if command == "get_settings":
            return self.get_settings()
        if command == "get_device_id":
            return self._get_device_id()
        if command == "get_version":
            return self.get_version()

        # Use default command if none specified
        if not command:
            command = self._protocol.DEFAULT_COMMAND

        try:
            # Get the full command
            full_command = self._protocol.get_full_command(command)
            log.info(f"Full command {full_command} for command {command}")
            
            if full_command is None:
                error_msg = f"Full command not found for {command} in protocol {self._protocol._protocol_id}"
                log.error(error_msg)
                return {"ERROR": [error_msg, ""]}

            # Send command and receive data with error handling
            raw_response = self._send_command_with_retry(command, full_command)
            
            # Check if we got an error response
            if isinstance(raw_response, dict) and "ERROR" in raw_response:
                return raw_response
                
            log.debug(f"Send and Receive Response {raw_response}")

            # Handle specific response patterns
            if raw_response == full_command:
                error_msg = f"Inverter returned the command string for {command} - the inverter didn't recognise this command"
                log.warning(error_msg)
                return {"ERROR": [error_msg, ""]}

            # Decode response
            try:
                decoded_response = self._protocol.decode(raw_response, command)
                log.info(f"Decoded response {decoded_response}")
                return decoded_response
                
            except Exception as e:
                error_msg = f"Failed to decode response for command {command}: {e}"
                log.error(error_msg)
                return {"ERROR": [error_msg, ""]}

        except Exception as e:
            error_msg = f"Unexpected error running command {command}: {e}"
            log.error(error_msg, exc_info=True)
            return {"ERROR": [error_msg, ""]}

    def _send_command_with_retry(self, command: str, full_command: bytes, max_retries: int = 3) -> dict:
        """
        Send command with retry logic and comprehensive error handling
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                log.debug(f"Command attempt {attempt + 1}/{max_retries} for {command}")
                
                raw_response = self._port.send_and_receive(
                    command=command,
                    full_command=full_command,
                    protocol=self._protocol,
                    command_defn=self._protocol.get_command_defn(command),
                )
                
                # If we get a valid response, return it
                if raw_response is not None:
                    return raw_response
                    
            except Exception as e:
                last_error = e
                log.warning(f"Command attempt {attempt + 1} failed: {e}")
                
                # If this is the last attempt, don't sleep
                if attempt < max_retries - 1:
                    # Progressive backoff: wait longer between retries
                    import time
                    wait_time = 1.0 * (attempt + 1)
                    log.debug(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
        
        # All attempts failed
        error_msg = f"Command {command} failed after {max_retries} attempts. Last error: {last_error}"
        log.error(error_msg)
        return {"ERROR": [error_msg, ""]}

    def get_status(self) -> dict:
        """
        Run all the commands that are defined as status from the protocol definition
        """
        data = {}
        failed_commands = []
        
        for command in self._protocol.STATUS_COMMANDS:
            try:
                result = self.run_command(command)
                if isinstance(result, dict) and "ERROR" in result:
                    failed_commands.append(command)
                    log.warning(f"Status command {command} failed: {result['ERROR']}")
                else:
                    data.update(result)
            except Exception as e:
                failed_commands.append(command)
                log.error(f"Exception running status command {command}: {e}")
        
        # Add a summary of failed commands if any
        if failed_commands:
            data["_failed_status_commands"] = [", ".join(failed_commands), ""]
            
        return data

    def get_settings(self) -> dict:
        """
        Run all the commands that are defined as settings from the protocol definition
        """
        data = {}
        failed_commands = []
        
        for command in self._protocol.SETTINGS_COMMANDS:
            try:
                result = self.run_command(command)
                if isinstance(result, dict) and "ERROR" in result:
                    failed_commands.append(command)
                    log.warning(f"Settings command {command} failed: {result['ERROR']}")
                else:
                    data.update(result)
            except Exception as e:
                failed_commands.append(command)
                log.error(f"Exception running settings command {command}: {e}")
        
        # Add a summary of failed commands if any
        if failed_commands:
            data["_failed_settings_commands"] = [", ".join(failed_commands), ""]
            
        return data

    def _get_device_id(self) -> dict:
        """
        Try to work out the 'id' for this device with error handling
        """
        try:
            _id = ""
            if self._protocol.ID_COMMANDS:
                for line in self._protocol.ID_COMMANDS:
                    if isinstance(line, tuple):
                        command = line[0]
                    else:
                        command = line
                        
                    result = self.run_command(command)
                    
                    # Check if command failed
                    if isinstance(result, dict) and "ERROR" in result:
                        log.warning(f"ID command {command} failed: {result['ERROR']}")
                        continue
                    
                    if isinstance(line, tuple):
                        key = line[1]
                    else:
                        key = list(result).pop()

                    try:
                        value = result[key][0]
                        if not _id:
                            _id = f"{value}"
                        else:
                            _id = f"{_id}:{value}"
                    except (KeyError, IndexError, TypeError) as e:
                        log.warning(f"Failed to extract device ID from command {command}: {e}")
                        continue
                        
                log.info(f"DeviceId: {_id}")
                return {
                    "_command": "Get Device ID", 
                    "_command_description": "Generate a device id", 
                    "DeviceID": [_id if _id else "Unable to determine device ID", ""]
                }
            else:
                return {
                    "_command": "Get Device ID",
                    "_command_description": "Generate a device id",
                    "DeviceID": ["getDeviceId not supported for this protocol", ""],
                }
        except Exception as e:
            error_msg = f"Error getting device ID: {e}"
            log.error(error_msg)
            return {
                "_command": "Get Device ID",
                "_command_description": "Generate a device id",
                "DeviceID": [error_msg, ""],
            }

    def get_version(self) -> dict:
        """
        Get the software version
        """
        return {
            "_command": "Get Version",
            "_command_description": "Output the mpp-solar software version",
            "MPP-Solar Software Version": [__version__, ""],
        }
