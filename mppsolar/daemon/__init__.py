from enum import Enum, auto

class DaemonType(Enum):
    """ Daemon types implemented """
    DISABLED = "disabled"
    SYSTEMD = "systemd"

def get_daemon(daemontype):
    match daemontype:
        case DaemonType.DISABLED:
            from .daemon_disabled import DaemonDummy as daemon
            return daemon()
        case DaemonType.SYSTEMD:
            from .daemon_systemd import DaemonSystemd as daemon
            return daemon()
        case _:
            raise Exception(f"unknown daemontype {daemontype}")