#!/usr/bin/env python3
""" Optional daemon_cli.py - CLI utility for managing mpp-solar daemon """

import argparse
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to import mppsolar modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from mppsolar.daemon import DaemonType, get_daemon, detect_daemon_type
from mppsolar.daemon.daemon_openrc import DaemonOpenRC

def start_daemon(args):
    """ Start the daemon """
    print("Starting mpp-solar daemon...")
    
    # Determine daemon type
    if args.daemon_type:
        daemon_type = DaemonType(args.daemon_type)
    else:
        daemon_type = detect_daemon_type()
    
    print(f"Using daemon type: {daemon_type.value}")
    
    # If OpenRC and fork requested, fork the process
    if daemon_type == DaemonType.OPENRC and args.fork:
        pid = os.fork()
        if pid > 0:
            print(f"Daemon forked with PID {pid}")
            sys.exit(0)
        # Child process continues
    
    # Import and run main with daemon flag
    from mppsolar import main as mpp_main
    
    # Modify sys.argv to include daemon flag and config
    original_argv = sys.argv.copy()
    sys.argv = ['mpp-solar', '--daemon']
    
    if args.config:
        sys.argv.extend(['-C', args.config])
    
    # Add any additional arguments
    if args.debug:
        sys.argv.append('--debug')
    elif args.info:
        sys.argv.append('--info')
    
    try:
        mpp_main()
    except KeyboardInterrupt:
        print("\nDaemon stopped by user")
    except Exception as e:
        print(f"Daemon error: {e}")
        sys.exit(1)
    finally:
        sys.argv = original_argv

def stop_daemon(args):
    """ Stop the daemon """
    print("Stopping mpp-solar daemon...")
    
    pid_file = args.pid_file or "/var/run/mpp-solar.pid"
    
    if DaemonOpenRC.stop_daemon(pid_file):
        print("Daemon stopped successfully")
    else:
        print("Failed to stop daemon")
        sys.exit(1)

def status_daemon(args):
    """ Check daemon status """
    pid_file = args.pid_file or "/var/run/mpp-solar.pid"
    
    if not os.path.exists(pid_file):
        print("Daemon is not running (no PID file found)")
        return
    
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process exists
        try:
            import psutil
            process = psutil.Process(pid)
            if process.is_running():
                print(f"Daemon is running with PID {pid}")
                print(f"Command: {' '.join(process.cmdline())}")
                print(f"Started: {process.create_time()}")
            else:
                print(f"PID file exists but process {pid} is not running")
        except ImportError:
            # Fallback without psutil
            if os.path.exists(f"/proc/{pid}"):
                print(f"Daemon appears to be running with PID {pid}")
            else:
                print(f"PID file exists but process {pid} is not running")
                
    except (ValueError, FileNotFoundError) as e:
        print(f"Invalid PID file: {e}")

def main():
    parser = argparse.ArgumentParser(description="mpp-solar daemon management utility")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start the daemon')
    start_parser.add_argument('--fork', action='store_true', 
                             help='Fork the process (for OpenRC daemon)')
    start_parser.add_argument('--daemon-type', choices=['disabled', 'systemd', 'openrc'],
                             help='Force specific daemon type')
    start_parser.add_argument('-C', '--config', 
                             help='Configuration file path')
    start_parser.add_argument('--debug', action='store_true',
                             help='Enable debug logging')
    start_parser.add_argument('--info', action='store_true',
                             help='Enable info logging')
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', help='Stop the daemon')
    stop_parser.add_argument('--pid-file', 
                           help='PID file path (default: /var/run/mpp-solar.pid)')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check daemon status')
    status_parser.add_argument('--pid-file',
                              help='PID file path (default: /var/run/mpp-solar.pid)')
    
    # Restart command
    restart_parser = subparsers.add_parser('restart', help='Restart the daemon')
    restart_parser.add_argument('--fork', action='store_true',
                               help='Fork the process (for OpenRC daemon)')
    restart_parser.add_argument('--daemon-type', choices=['disabled', 'systemd', 'openrc'],
                               help='Force specific daemon type')
    restart_parser.add_argument('-C', '--config',
                               help='Configuration file path')
    restart_parser.add_argument('--pid-file',
                               help='PID file path (default: /var/run/mpp-solar.pid)')
    restart_parser.add_argument('--debug', action='store_true',
                               help='Enable debug logging')
    restart_parser.add_argument('--info', action='store_true',
                               help='Enable info logging')
    
    args = parser.parse_args()
    
    if args.command == 'start':
        start_daemon(args)
    elif args.command == 'stop':
        stop_daemon(args)
    elif args.command == 'status':
        status_daemon(args)
    elif args.command == 'restart':
        print("Restarting daemon...")
        stop_daemon(args)
        import time
        time.sleep(2)  # Brief pause between stop and start
        start_daemon(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

