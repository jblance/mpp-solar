# !/usr/bin/python3
import os
import logging
import time
import sys
from argparse import ArgumentParser
from platform import python_version

from mppsolar.version import __version__  # noqa: F401

from mppsolar.helpers import get_device_class

from mppsolar.daemon.pyinstaller_runtime import (
    spawn_pyinstaller_subprocess,
    is_pyinstaller_bundle,
    has_been_spawned,
    is_spawned_pyinstaller_process,
  )
from mppsolar.daemon import get_daemon, detect_daemon_type
from mppsolar.daemon import DaemonType
from mppsolar.daemon.daemon import (
    setup_daemon_logging,
    daemonize,
)
from mppsolar.libs.mqttbroker_legacy import MqttBroker
from mppsolar.libs.mqtt_manager import mqtt_manager
from mppsolar.outputs import get_outputs, list_outputs
from mppsolar.protocols import list_protocols

# Set-up logger
log = logging.getLogger("")
FORMAT = "%(asctime)-15s:%(levelname)s:%(module)s:%(funcName)s@%(lineno)d: %(message)s"
logging.basicConfig(format=FORMAT)




def main():
    description = f"Solar Device Command Utility, version: {__version__}, python version: {python_version()}"
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-n",
        "--name",
        help="Specifies the device name - used to differentiate different devices",
        default="unnamed",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Specifies the device communications port (/dev/ttyUSB0 [default], /dev/hidraw0, test, ...)",
        default="/dev/ttyUSB0",
    )
    parser.add_argument(
        "--porttype",
        help="overrides the device communications port type",
        default=None,
    )
    parser.add_argument(
        "--dev",
        help="Device identifier for prometheus output labeling for complex installations (default: None)",
        default=None,
    )
    if parser.prog == "jkbms":
        parser.add_argument(
            "-P",
            "--protocol",
            nargs="?",
            const="help",
            help="Specifies the device command and response protocol, (default: JK04)",
            default="JK04",
        )
    else:
        parser.add_argument(
            "-P",
            "--protocol",
            nargs="?",
            const="help",
            help="Specifies the device command and response protocol, (default: PI30)",
            default="PI30",
        )
    parser.add_argument(
        "-T",
        "--tag",
        help="Override the command name and use this instead (for mqtt and influx type output processors)",
    )
    parser.add_argument(
        "-b",
        "--baud",
        type=int,
        help="Baud rate for serial communications (default: 2400)",
        default=2400,
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        help="Specifies the output processor(s) to use [comma separated if multiple] (screen [default]) leave blank to give list",
        const="help",
        default="screen",
    )
    parser.add_argument(
        "--keepcase",
        action="store_true",
        help="Do not convert the field names to lowercase",
    )
    parser.add_argument(
        "--filter",
        help="Specifies the filter to reduce the output - only those fields that match will be output (uses re.search)",
        default=None,
    )
    parser.add_argument(
        "--exclfilter",
        help="Specifies the filter to reduce the output - any fields that match will be excluded from the output (uses re.search)",
        default=None,
    )
    parser.add_argument(
        "-q",
        "--mqttbroker",
        help="Specifies the mqtt broker to publish to if using a mqtt output (localhost [default], hostname, ip.add.re.ss ...)",
        default="localhost",
    )
    parser.add_argument(
        "--mqttport",
        type=int,
        help="Specifies the mqtt broker port if needed (default: 1883)",
        default=1883,
    )
    parser.add_argument(
        "--mqtttopic",
        help="provides an override topic (or prefix) for mqtt messages (default: None)",
        default=None,
    )
    parser.add_argument(
        "--mqttuser",
        help="Specifies the username to use for authenticated mqtt broker publishing",
        default=None,
    )
    parser.add_argument(
        "--mqttpass",
        help="Specifies the password to use for authenticated mqtt broker publishing",
        default=None,
    )
    parser.add_argument(
        "--udpport",
        type=int,
        help="Specifies the UDP port if needed (default: 5555)",
        default="5555",
    )
    parser.add_argument(
        "--postgres_url",
        help="PostgresSQL connection url, example postgresql://user:password@server:5432/postgres",
    )
    parser.add_argument(
        "--mongo_url",
        help="Mongo connection url, example mongodb://user:password@ip:port/admindb",
    )
    parser.add_argument(
        "--mongo_db",
        help="Mongo db name (default: mppsolar)",
        default="mppsolar",
    )
    parser.add_argument(
        "--pushurl",
        help=(
            "Any server used to send data to (PushGateway for Prometheus, for instance), "
            "(default: http://localhost:9091/metrics/job/pushgateway)"
        ),
        default="http://localhost:9091/metrics/job/pushgateway",
    )
    parser.add_argument(
        "--prom_output_dir",
        help=(
            "Output directory where Prometheus metrics are written as .prom files"
            "(default: /var/lib/node_exporter)"
        ),
        default="/var/lib/node_exporter",
    )
    parser.add_argument(
        "-c",
        "--command",
        nargs="?",
        const="help",
        help="Command to run; or list of hash separated commands to run",
    )
    if parser.prog == "jkbms":
        parser.add_argument(
            "-C",
            "--configfile",
            nargs="?",
            help="Full location of config file (default None, /etc/jkbms/jkbms.conf if -C supplied)",
            const="/etc/jkbms/jkbms.conf",
            default=None,
        )
    else:
        parser.add_argument(
            "-C",
            "--configfile",
            nargs="?",
            help="Full location of config file (default None, /etc/mpp-solar/mpp-solar.conf if -C supplied)",
            const="/etc/mpp-solar/mpp-solar.conf",
            default=None,
        )
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--getstatus", action="store_true", help="Get Inverter Status")
    parser.add_argument("--getsettings", action="store_true", help="Get Inverter Settings")
    parser.add_argument("--getDeviceId", action="store_true", help="Generate Device ID")

    parser.add_argument("-v", "--version", action="store_true", help="Display the version")
    parser.add_argument("--getVersion", action="store_true", help="Output the software version via the supplied output")
    parser.add_argument(
        "-D",
        "--debug",
        action="store_true",
        help="Enable Debug and above (i.e. all) messages",
    )
    parser.add_argument(
        "--pidfile",
        help="Specifies the PID file location for daemon mode (default: /var/run/mpp-solar.pid, /tmp/mpp-solar.pid for PyInstaller)",
        default=None,
    )
    parser.add_argument(
        "--daemon-stop", 
        action="store_true", 
        help="Stop a running daemon (requires --pidfile if using non-default location)"
    )
    parser.add_argument("-I", "--info", action="store_true", help="Enable Info and above level messages")

    args = parser.parse_args()
    prog_name = parser.prog
    if prog_name is None:
        prog_name = "mpp-solar"
    s_prog_name = prog_name.replace("-", "")
    log_file_path = "/var/log/mpp-solar.log"


    # logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    # Turn on debug if needed
    if args.debug:
        log.setLevel(logging.DEBUG)
    elif args.info:
        log.setLevel(logging.INFO)
    else:
        # set default log level
        log.setLevel(logging.WARNING)


    # Display version if asked
    log.info(description)
    if args.version:
        print(description)
        return None

    def execute_device_command(device_name: str, command: str):
        """Execute a command on a specific device and return results"""
        log.info(f"Executing command '{command}' on device '{device_name}'")

        # Find the device in our commands list
        for _device, _command, _tag, _outputs, filter, excl_filter, dev in _commands:
            if _device._name == device_name:
                try:
                    result = _device.run_command(command=command)
                    return {"result": result, "command": command, "timestamp": time.time()}
                except Exception as e:
                    raise Exception(f"Command execution failed: {str(e)}")

        raise Exception(f"Device '{device_name}' not found")

    # List available protocols if asked
    if args.protocol == "help":
        op = get_outputs("screen")[0]
        op.output(data=list_protocols())
        return None

    # List outputs if asked
    if args.output == "help":
        keep_case = True
        op = get_outputs("screen")[0]
        op.output(data=list_outputs())
        # print("Available output modules:")
        # for result in results:
        #    print(result)
        return None

    # mqttbroker:
    #     name: null
    #     port: 1883
    #     user: null
    #     pass: null
    # Handle daemon setup and stop requests

    #### Extra Logging
    def log_process_info(label, log_func=None):
        """Log detailed process information for debugging"""
        if log_func is None:
            log_func = print

        pid = os.getpid()
        ppid = os.getppid()

        # Get process group and session info
        try:
            pgid = os.getpgid(0)
            sid = os.getsid(0)
        except:
            pgid = "unknown"
            sid = "unknown"

        # Check if we're the process group leader
        is_leader = (pid == pgid)

        log_func(f"[{label}] PID: {pid}, PPID: {ppid}, PGID: {pgid}, SID: {sid}, Leader: {is_leader}")

        # Log command line that started this process
        try:
            with open(f'/proc/{pid}/cmdline', 'r') as f:
                cmdline = f.read().replace('\0', ' ').strip()
            log_func(f"[{label}] Command: {cmdline}")
        except:
            log_func(f"[{label}] Command: {' '.join(sys.argv)}")

    def log_debug_context(label, args):
        log.debug(f"[{label}] sys.argv = {sys.argv}")
        log.debug(f"[{label}] args.daemon = {args.daemon}")
        log.debug(f"[{label}] args.debug = {args.debug}")

    if args.debug:
        if is_spawned_pyinstaller_process():
            log_debug_context("CHILD", args)
        elif is_pyinstaller_bundle():
            log_debug_context("PARENT", args)
        else:
            log_debug_context("SYSTEM", args)


    def setup_daemon_if_requested(args, log_file_path="/var/log/mpp-solar.log"):
        if args.daemon:
            os.environ["MPP_SOLAR_DAEMON"] = "1"
            log.info("Daemon mode requested")

            try:
                daemon_type = detect_daemon_type()
                log.info(f"Detected daemon type: {daemon_type}")
            except Exception as e:
                log.warning(f"Failed to detect daemon type: {e}, falling back to OpenRC")
                daemon_type = DaemonType.OPENRC

            daemon = get_daemon(daemontype=daemon_type)

            if hasattr(daemon, 'set_pid_file_path') and args.pidfile:
                daemon.set_pid_file_path(args.pidfile)
                log.info(f"Using custom PID file: {args.pidfile}")
            elif hasattr(daemon, 'pid_file_path'):
                daemon.pid_file_path = "/tmp/mpp-solar.pid" if os.geteuid() != 0 else "/var/run/mpp-solar.pid"
                log.info(f"Using default PID file: {daemon.pid_file_path}")

            daemon.keepalive = 60

            # Only call daemonize() for DISABLED daemon type (manual daemonization)
            # OpenRC, systemd, and other init systems handle daemonization themselves
            if daemon_type == DaemonType.DISABLED:
                log.info("Using DISABLED daemon type - performing manual daemonization...")
                try:
                    daemonize()
                    log.info("Daemonized successfully")
                    # Re-setup logging for the daemonized process
                    if not setup_daemon_logging(log_file_path):
                        sys.stderr.write("CRITICAL: Failed to setup file logging for daemon. Check permissions.\n")
                    else:
                        log.info("Daemon file logging successfully re-initialized.")
                except Exception as e:
                    log.error(f"Failed to daemonize process: {e}")
                    log.info("Continuing in foreground mode")
            else:
                log.info(f"Using {daemon_type.name} daemon type - init system will handle process management")
                # For OpenRC/systemd, we still need to setup file logging since we're running as daemon
                if not setup_daemon_logging(log_file_path):
                    log.warning("Failed to setup file logging for daemon. Check permissions.")
                else:
                    log.info("Daemon file logging setup successful.")

            return daemon
        else:
            log.info("Daemon mode NOT requested. Using DISABLED daemon.")
            daemon = get_daemon(daemontype=DaemonType.DISABLED)
            return daemon

    # --- Optional PyInstaller bootstrap cleanup ---
    # To enable single-process daemon spawn logic (avoids PyInstaller parent):
    #################################################################
#     if spawn_pyinstaller_subprocess(args):
#       sys.exit(0)
# 
#     from daemon.pyinstaller_runtime import setup_spawned_environment
#     setup_spawned_environment()
    #################################################################

    # Handle daemon stop request
    if args.daemon_stop:
        pid_file_path = args.pidfile
        if pid_file_path is None:
            # Use default based on environment
            if os.geteuid() != 0:  # Non-root check
                pid_file_path = "/tmp/mpp-solar.pid"
            else:
                pid_file_path = "/var/run/mpp-solar.pid"

        log.info(f"Attempting to stop daemon using PID file: {pid_file_path}")

        try:
            daemon_type = detect_daemon_type()
            daemon_class = get_daemon(daemontype=daemon_type).__class__
            if hasattr(daemon_class, 'stop_daemon'):
                success = daemon_class.stop_daemon(pid_file_path)
                if success:
                    print("Daemon stopped successfully")
                else:
                    print("Failed to stop daemon")
                sys.exit(0 if success else 1)
            else:
                print("Daemon stop functionality not available for this daemon type")
                sys.exit(1)
        except Exception as e:
            print(f"Error stopping daemon: {e}")
            sys.exit(1)


    # mqttbroker setup
    mqtt_broker = MqttBroker(
        config={
            "name": args.mqttbroker,
            "port": args.mqttport,
            "user": args.mqttuser,
            "pass": args.mqttpass,
        }
    )
    mqtt_broker.set("results_topic", (args.mqtttopic if args.mqtttopic is not None else prog_name))
    log.debug(mqtt_broker)
    udp_port = args.udpport
    log.debug(f"udp port {udp_port}")
    postgres_url = args.postgres_url
    log.debug(f"Using Postgres {postgres_url}")
    mongo_url = args.mongo_url
    mongo_db = args.mongo_db
    log.debug(f"Using Mongo {mongo_url} with {mongo_db}")
    ##
    filter = args.filter
    excl_filter = args.exclfilter
    keep_case = args.keepcase
    mqtt_topic = args.mqtttopic
    push_url = args.pushurl
    prom_output_dir = args.prom_output_dir
    dev = args.dev

    _commands = []


    # If config file specified, process
    if args.configfile:
        import configparser

        log.debug(f"args.configfile is true: {args.configfile}")
        config = configparser.ConfigParser()
        try:
            config.read(args.configfile)
        except configparser.DuplicateSectionError as e:
            log.error(f"Config File '{args.configfile}' has duplicate sections")
            log.error(e)
            exit(1)
        sections = config.sections()
        # Check setup section exists
        if "SETUP" not in config:
            log.error(f"Config File '{args.configfile}'  is missing the required 'SETUP' section or does not exist")
            exit(1)
        # Process setup section
        pause = config["SETUP"].getint("pause", fallback=60)
        # Overide mqtt_broker settings
        mqtt_broker.update("name", config["SETUP"].get("mqtt_broker", fallback=None))
        mqtt_broker.update("port", config["SETUP"].getint("mqtt_port", fallback=None))
        mqtt_broker.update("username", config["SETUP"].get("mqtt_user", fallback=None))
        mqtt_broker.update("password", config["SETUP"].get("mqtt_pass", fallback=None))
        log_file_path = config["SETUP"].get("log_file", fallback="/var/log/mpp-solar.log")
        sections.remove("SETUP")

        # Track device configurations for MQTT command setup
        # Process 'command' sections
        for section in sections:
            name = section
            protocol = config[section].get("protocol", fallback=None)
            _type = config[section].get("type", fallback="mppsolar")
            port = config[section].get("port", fallback="/dev/ttyUSB0")
            baud = config[section].get("baud", fallback=2400)
            _command = config[section].get("command")
            tag = config[section].get("tag")
            outputs = config[section].get("outputs", fallback="screen")
            porttype = config[section].get("porttype", fallback=None)
            filter = config[section].get("filter", fallback=None)
            excl_filter = config[section].get("exclfilter", fallback=None)
            udp_port = config[section].get("udpport", fallback=None)
            postgres_url = config[section].get("postgres_url", fallback=None)
            mongo_url = config[section].get("mongo_url", fallback=None)
            mongo_db = config[section].get("mongo_db", fallback=None)
            push_url = config[section].get("push_url", fallback=push_url)
            prom_output_dir = config[section].get("prom_output_dir", fallback=prom_output_dir)
            mqtt_topic = config[section].get("mqtt_topic", fallback=mqtt_topic)
            section_dev = config[section].get("dev", fallback=None)
            mqtt_allowed_cmds = config[section].get("mqtt_allowed_cmds", fallback="")
            #
            device_class = get_device_class(_type)
            log.debug(f"device_class {device_class}")
            # The device class __init__ will instantiate the port communications and protocol classes
            device = device_class(
                name=name,
                port=port,
                protocol=protocol,
                outputs=outputs,
                baud=baud,
                porttype=porttype,
                mqtt_broker=mqtt_broker,
                udp_port=udp_port,
                postgres_url=postgres_url,
                mongo_url=mongo_url,
                mongo_db=mongo_db,
                push_url=push_url,
                prom_output_dir=prom_output_dir,
            )
            # build array of commands
            commands = _command.split("#")

            # Setup MQTT commands if configured
            if mqtt_allowed_cmds and mqtt_broker.enabled:
                allowed_cmd_list = [cmd.strip() for cmd in mqtt_allowed_cmds.split(",") if cmd.strip()]
                log.info(f"Setting up MQTT commands for device '{name}': {allowed_cmd_list}")
                mqtt_broker.setup_device_commands(
                    device_name=name, allowed_commands=allowed_cmd_list, command_callback=execute_device_command
                )

            for command in commands:
                _commands.append((device, command, tag, outputs, filter, excl_filter, section_dev))
            log.debug(f"Commands from config file {_commands}")
            log.debug(f"[DAEMON LOOP INIT] args.daemon={args.daemon}, pause={pause}, commands={_commands}")
            if args.daemon:
                print(f"Config file: {args.configfile}")
                print(f"Config setting - pause: {pause}")
                # print(f"Config setting - mqtt_broker: {mqtt_broker}, port: {mqtt_port}")
                print(f"Config setting - command sections found: {len(sections)}")
            else:
                log.info(f"Config file: {args.configfile}")
                log.info(f"Config setting - pause: {pause}")
                # log.info(f"Config setting - mqtt_broker: {mqtt_broker}, port: {mqtt_port}")
                log.info(f"Config setting - command sections found: {len(sections)}")

    else:
        # No configfile specified
        # create instance of device (supplying port + protocol types)
        log.info(
            f'Creating device "{args.name}" (type: "{s_prog_name}") on port "{args.port} (porttype={args.porttype})" using protocol "{args.protocol}"'
        )
        device_class = get_device_class(s_prog_name)
        log.debug(f"device_class {device_class}")
        # The device class __init__ will instantiate the port communications and protocol classes
        device = device_class(
            name=args.name,
            port=args.port,
            protocol=args.protocol,
            baud=args.baud,
            porttype=args.porttype,
            mqtt_broker=mqtt_broker,
            udp_port=udp_port,
            mongo_url=mongo_url,
            mongo_db=mongo_db,
            push_url=push_url,
            prom_output_dir=prom_output_dir,
        )

        # determine whether to run command or call helper function
        commands = []
        if args.command == "help":
            keep_case = True
            commands.append("list_commands")
        elif args.getstatus:
            # use get_status helper
            commands.append("get_status")
        elif args.getsettings:
            # use get_settings helper
            commands.append("get_settings")
        elif args.getDeviceId:
            # use get_settings helper
            commands.append("get_device_id")
        elif args.getVersion:
            # use get_version helper
            commands.append("get_version")
        elif args.command is None:
            # run the command
            commands.append("")
        else:
            commands = args.command.split("#")

        outputs = args.output
        for command in commands:
            if args.tag:
                tag = args.tag
            else:
                tag = command
            _commands.append((device, command, tag, outputs, filter, excl_filter, dev))
        log.debug(f"Commands {_commands}")


    # ------------------------
    # Daemon setup and logging
    # ------------------------
    daemon = setup_daemon_if_requested(args, log_file_path=log_file_path)
    log.info(daemon)
    DAEMON_MODE = args.daemon
    # Notify systemd/init
    daemon.initialize()
    log_process_info("AFTER_DAEMON_INITIALIZE", log.info)

    # Start MQTT manager
    mqtt_manager.start_all()
    daemon.notify("Service Initializing ...")
    log_process_info("AFTER_DAEMON_NOTIFY", log.info)


    while True:
        # Loop through the configured commands
        if not args.daemon:
            log.info(f"Looping {len(_commands)} commands")
        for _device, _command, _tag, _outputs, filter, excl_filter, dev in _commands:
            # for item in mppUtilArray:
            # Tell systemd watchdog we are still alive
            daemon.watchdog()
            daemon.notify(f"Getting results from device: {_device} for command: {_command}, tag: {_tag}, outputs: {_outputs}")
            log.info(f"Getting results from device: {_device} for command: {_command}, tag: {_tag}, outputs: {_outputs}")
            results = _device.run_command(command=_command)
            log.debug(f"results: {results}")
            # send to output processor(s)
            outputs = get_outputs(_outputs)
            for op in outputs:
                # maybe include the command and what the command is im the output
                # eg QDI run, Display Inverter Default Settings
                log.debug(f"Using output filter: {filter}")
                op.output(
                    data=results.copy(),
                    tag=_tag,
                    name=_device._name,
                    mqtt_broker=mqtt_broker,
                    udp_port=udp_port,
                    postgres_url=postgres_url,
                    mongo_url=mongo_url,
                    mongo_db=mongo_db,
                    push_url=push_url,
                    prom_output_dir=prom_output_dir,
                    # mqtt_port=mqtt_port,
                    # mqtt_user=mqtt_user,
                    # mqtt_pass=mqtt_pass,
                    mqtt_topic=mqtt_topic,
                    filter=filter,
                    excl_filter=excl_filter,
                    keep_case=keep_case,
                    dev=dev,  # ADD: Pass dev parameter to output
                )
        try:
                # Tell systemd watchdog we are still alive
#            if args.daemon:
            if DAEMON_MODE:
                daemon.watchdog()
                print(f"Sleeping for {pause} sec")
                time.sleep(pause)
            else:
                # Dont loop unless running as daemon
                log.debug("Not daemon, so not looping")
                break
        except Exception as e:
            log.error(f"[LOOP ERROR] Exception in daemon loop: {e}", exc_info=True)
            time.sleep(5)  # Prevent tight loop in case of recurring errors
    mqtt_manager.stop_all()


if __name__ == "__main__":
    main()

