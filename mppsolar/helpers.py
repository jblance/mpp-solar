#!/usr/bin/env python3
import os
import sys
import logging
import importlib

log = logging.getLogger("helpers")


def get_kwargs(kwargs, key, default=None):
    return kwargs.get(key) or default


def key_wanted(key, filter=None, excl_filter=None):
    # remove any specifically excluded keys
    if excl_filter is not None and excl_filter.search(key):
        # log.debug(f"key_wanted: key {key} matches excl_filter {excl_filter} so key excluded")
        return False
    if filter is None:
        # log.debug(
        #    f"key_wanted: No filter and key {key} not excluded by excl_filter {excl_filter} so key wanted"
        # )
        return True
    elif filter.search(key):
        # log.debug(
        #    f"key_wanted: key {key} matches filter {filter} and not excl_filter {excl_filter} so key wanted"
        # )
        return True
    else:
        # log.debug(f"key_wanted: key {key} does not match filter {filter} so key excluded")
        return False


def get_value(_list, _index):
    """
    get the value from _list or return None if _index is out of bounds
    """
    # print(_list, len(_list))
    if _index >= len(_list):
        return None
    return _list[_index]


def get_resp_defn(key, defns):
    """
    look for a definition for the supplied key
    """
    # print(key, defns)
    if not key:
        return None
    if type(key) is bytes:
        try:
            key = key.decode("utf-8")
        except UnicodeDecodeError:
            log.info(f"key decode error for {key}")
    for defn in defns:
        if key == defn[0]:
            # print(key, defn)
            return defn
    # did not find definition for this key
    log.info(f"No defn found for {key} key")
    return [key, key, "", ""]


def get_device_class(device_type=None):
    """
    Take a device type string
    attempt to find and instantiate the corresponding module
    return class if found, otherwise return None
    """
    if device_type is None:
        return None
    device_type = device_type.lower()
    try:
        device_module = importlib.import_module("mppsolar.devices." + device_type, ".")
    except ModuleNotFoundError as e:
        # perhaps raise a mppsolar exception here??
        log.critical(f"Error loading device {device_type}: {e}")
        return None
    device_class = getattr(device_module, device_type)
    return device_class


def getMaxLen(data, index=0):
    _maxLen = 0
    for item in data:
        if type(item) == list:
            item = item[index]
        if type(item) == float or type(item) == int:
            item = str(item)
        if len(item) > _maxLen:
            _maxLen = len(item)
    return _maxLen

def get_max_response_length(data, index=0):
    return getMaxLen(data, index)

def pad(text, length):
    if type(text) == float or type(text) == int:
        text = str(text)
    if len(text) > length:
        return text
    return text.ljust(length, " ")

class CRC_XModem:
    def __init__(self, poly=0x1021, initial=0x0000):
        self.poly = poly
        self.initial = initial
        self.table = self.generate_crc_table()

    def generate_crc_table(self):
        table = [0] * 256
        for i in range(256):
            crc = i << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ self.poly
                else:
                    crc = crc << 1
            table[i] = crc & 0xFFFF
        return table

    def compute_crc(self, data):
        crc = self.initial
        for byte in data:
            crc = ((crc << 8) & 0xFFFF) ^ self.table[(crc >> 8) ^ byte]
        return crc

    def crc_hex(self, data):
        crc = self.compute_crc(data)
        return format(crc, '04x').upper()

def log_pyinstaller_context():
    """
    Log context info if running inside a PyInstaller bundle.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        log.info("Running from PyInstaller bundle. An initial loader process may appear in pstree.")
        log.debug(f"PyInstaller context: sys.executable={sys.executable}, _MEIPASS={sys._MEIPASS}")


def daemonize():
    """
    Properly daemonize the process (Unix double-fork)
    Enhanced for PyInstaller compatibility
    """
    import logging
    from mppsolar.daemon.pyinstaller_runtime import is_pyinstaller_bundle, has_been_spawned

    log = logging.getLogger("helpers")
    pid = os.getpid()
    ppid = os.getppid()
    log.info(f"[DAEMONIZE] Before fork PID: {pid}, PPID: {ppid}")

    # Special handling for PyInstaller spawned processes
    if is_pyinstaller_bundle() and has_been_spawned():
        log.info("[DAEMONIZE] Running in spawned PyInstaller process - using modified daemonization")
        
        # We're already in a subprocess, so we can do a simpler daemonization
        # Just do a single fork and session setup
        try:
            pid = os.fork()
            if pid > 0:
                log.info(f"[DAEMONIZE] Fork successful, parent exiting. Child PID: {pid}")
                sys.exit(0)
        except OSError as e:
            log.error(f"Fork failed in spawned PyInstaller process: {e}")
            sys.exit(1)

        # Set up daemon environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
        
        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        try:
            with open('/dev/null', 'r') as si: # Disable only while testing.
                os.dup2(si.fileno(), sys.stdin.fileno())
            with open('/dev/null', 'a+') as so:
                os.dup2(so.fileno(), sys.stdout.fileno())
            with open('/dev/null', 'a+') as se:
                os.dup2(se.fileno(), sys.stderr.fileno())
            log.info("[DAEMONIZE] Standard I/O redirected to /dev/null.") # This log won't appear on console
        except Exception as e:
            pass # Keep original pass here, as the log might not work yet
        log.info(f"[DAEMONIZE] PyInstaller daemon process ready. PID: {os.getpid()}")
        return

    # Standard daemonization for non-PyInstaller or direct execution
    try:
        pid = os.fork()
        if pid > 0:
            log.info(f"[DAEMONIZE] First fork successful, parent exiting. Child PID: {pid}")
            sys.exit(0)
    except OSError as e:
        log.error(f"First fork failed: {e}")
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            log.info(f"[DAEMONIZE] Second fork successful, intermediate parent exiting. Child PID: {pid}")
            sys.exit(0)
    except OSError as e:
        log.error(f"Second fork failed: {e}")
        sys.exit(1)

    # Redirect standard file descriptors to /dev/null
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as si:  # Disabled while testing pyinstaller code
        os.dup2(si.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a+') as so:
        os.dup2(so.fileno(), sys.stdout.fileno())
    with open('/dev/null', 'a+') as se:
        os.dup2(se.fileno(), sys.stderr.fileno())

    log.info(f"[DAEMONIZE] Daemon process forked successfully. PID: {os.getpid()}")


def has_been_spawned():
    val = os.environ.get("MPP_SOLAR_SPAWNED")
    log.info(f"has_been_spawned(): MPP_SOLAR_SPAWNED={val}")
    return val == "1"


def setup_daemon_logging(log_file="/var/log/mpp-solar.log"):
    """Setup logging for daemon mode"""
    try:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)

        # Setup file logging
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Setup formatter
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(module)s:%(funcName)s@%(lineno)d: %(message)s'
        )
        file_handler.setFormatter(formatter)

        # Get root logger and add handler
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)

        return True
    except Exception as e:
        print(f"Failed to setup daemon logging: {e}")
        return False

