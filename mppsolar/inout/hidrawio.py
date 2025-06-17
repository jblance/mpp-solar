# shamelessly stolen from ccrisan https://github.com/qtoggle/qtoggleserver-mppsolar/blob/master/qtoggleserver/mppsolar/io.py
# Added better error handling principals 2025 Corey DeLasaux <cordelster@gmail.com>
import logging
import os
import time
import errno

from .baseio import BaseIO
from ..helpers import get_kwargs

log = logging.getLogger(__name__)


class HIDRawIO(BaseIO):
    """
    Handles HIDRAW serial communications.
    Purpose: Added better error handling and progressive backoff.
    """
    def __init__(self, device_path: str, timeout: float = 5.0, max_retries: int = 3) -> None:
        self._device = device_path
        self._timeout = timeout
        self._max_retries = max_retries

    def send_and_receive(self, *args, **kwargs) -> dict:
        full_command = get_kwargs(kwargs, "full_command")
        
        for attempt in range(self._max_retries):
            try:
                return self._attempt_communication(full_command)
            except (TimeoutError, OSError) as e:
                log.warning(f"Communication attempt {attempt + 1} failed: {e}")
                if attempt == self._max_retries - 1:
                    # Last attempt failed, return error
                    error_msg = f"Communication failed after {self._max_retries} attempts: {e}"
                    log.error(error_msg)
                    return {"ERROR": [error_msg, ""]}
                # Wait before retry
                time.sleep(0.5 * (attempt + 1))  # Progressive backoff
        
        # This shouldn't be reached, but just in case
        return {"ERROR": ["Unexpected error in communication retry loop", ""]}

    def _attempt_communication(self, full_command: bytes) -> dict:
        """Single attempt at communication with the device"""
        response_line = bytes()
        usb0 = None
        
        try:
            # Open device
            usb0 = os.open(self._device, os.O_RDWR | os.O_NONBLOCK)
            log.debug(f"Opened device: {self._device}")
            
            # Send command
            self._send_command(usb0, full_command)
            
            # Receive response
            response_line = self._receive_response(usb0)
            
            if not response_line:
                raise TimeoutError("No response received from device")
                
            log.debug("usb response was: %s", response_line)
            return response_line
            
        except OSError as e:
            if e.errno == errno.ENOENT:
                error_msg = f"Device not found: {self._device}"
            elif e.errno == errno.EACCES:
                error_msg = f"Permission denied accessing device: {self._device}"
            elif e.errno == errno.EBUSY:
                error_msg = f"Device busy: {self._device}"
            else:
                error_msg = f"USB device error: {e}"
            log.error(error_msg)
            raise OSError(error_msg) from e
            
        except TimeoutError as e:
            log.error(f"Communication timeout: {e}")
            raise
            
        except Exception as e:
            error_msg = f"Unexpected error during communication: {e}"
            log.error(error_msg)
            raise OSError(error_msg) from e
            
        finally:
            # Always close the device if it was opened
            if usb0 is not None:
                try:
                    os.close(usb0)
                    log.debug("Closed USB device")
                except Exception as e:
                    log.warning(f"Error closing USB device: {e}")

    def _send_command(self, usb_fd: int, full_command: bytes) -> None:
        """Send command to the USB device"""
        cmd_len = len(full_command)
        log.debug(f"Sending command of length: {cmd_len}")
        
        try:
            if cmd_len <= 8:
                # Send all at once
                log.debug("Sending full_command in one shot")
                time.sleep(0.05)
                os.write(usb_fd, full_command)
            else:
                # Send in 8-byte chunks
                log.debug("Sending command in multiple chunks")
                chunks = [full_command[i:i + 8] for i in range(0, cmd_len, 8)]
                for chunk in chunks:
                    # Pad chunk to 8 bytes
                    if len(chunk) < 8:
                        padding = 8 - len(chunk)
                        chunk += b'\x00' * padding
                    log.debug("Sending chunk: %s", chunk)
                    time.sleep(0.05)
                    os.write(usb_fd, chunk)
                    
            time.sleep(0.25)  # Wait for device to process
            
        except OSError as e:
            raise OSError(f"Failed to send command: {e}") from e

    def _receive_response(self, usb_fd: int) -> bytes:
        """Receive response from the USB device with timeout handling"""
        response_line = bytes()
        start_time = time.time()
        read_attempts = 0
        max_read_attempts = 100
        
        log.debug(f"Starting to read response (timeout: {self._timeout}s)")
        
        while read_attempts < max_read_attempts:
            # Check for overall timeout
            if time.time() - start_time > self._timeout:
                raise TimeoutError(f"Overall timeout ({self._timeout}s) exceeded while reading response")
            
            try:
                time.sleep(0.15)
                r = os.read(usb_fd, 256)
                if r:  # Only add if we got data
                    response_line += r
                    log.debug(f"Read {len(r)} bytes, total: {len(response_line)}")
                
                # Check if we have a complete response (ends with \r)
                if bytes([13]) in response_line:
                    # Remove anything after the \r
                    response_line = response_line[:response_line.find(bytes([13])) + 1]
                    log.debug("Complete response received")
                    break
                    
            except OSError as e:
                if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                    # No data available, this is expected with non-blocking I/O
                    log.debug("No data available (EAGAIN/EWOULDBLOCK)")
                elif e.errno == errno.ETIMEDOUT or e.errno == 110:  # 110 is ETIMEDOUT on some systems
                    raise TimeoutError(f"Read operation timed out: {e}") from e
                else:
                    log.debug(f"USB read error: {e}")
                    # For other errors, we might want to continue trying
                    
            read_attempts += 1
        
        if read_attempts >= max_read_attempts:
            raise TimeoutError(f"Maximum read attempts ({max_read_attempts}) exceeded")
            
        if not response_line:
            raise TimeoutError("No response received from device")
            
        return response_line
