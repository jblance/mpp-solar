# MPP-Solar Daemon with Configurable PID File

## Usage Examples

### Basic daemon operation (uses default PID file location):
```bash
# Start daemon
mpp-solar --daemon -C /etc/mpp-solar/mpp-solar.conf

# Stop daemon
mpp-solar --daemon-stop
```

### Custom PID file location and naming:
```bash
# Start daemon with custom PID file
mpp-solar --daemon --pidfile /home/user/solar/mpp-solar.pid -C /etc/mpp-solar/mpp-solar.conf

# Stop daemon using custom PID file
mpp-solar --daemon-stop --pidfile /home/user/solar/mpp-solar.pid
```

### For non-root users:
```bash
# Start daemon (automatically uses /tmp or XDG_RUNTIME_DIR)
mpp-solar --daemon --pidfile ~/.config/mpp-solar.pid -C ~/mpp-solar.conf

# Stop daemon
mpp-solar --daemon-stop --pidfile ~/.config/mpp-solar.pid
```

### For PyInstaller distributions:
```bash
# The daemon will automatically detect PyInstaller and use appropriate defaults
./mpp-solar --daemon --pidfile ./mpp-solar.pid -C ./config/mpp-solar.conf

# Stop PyInstaller daemon
./mpp-solar --daemon-stop --pidfile ./mpp-solar.pid
```

### Docker containers:
```bash
# Use a mounted volume for persistent PID file
docker run -v /host/path:/app/data your-mpp-solar-image \
  --daemon --pidfile /app/data/mpp-solar.pid -C /app/config/mpp-solar.conf
```

## Default PID File Locations

The daemon automatically chooses appropriate default locations:

- **Root user**: `/var/run/mpp-solar.pid`
- **Non-root user with XDG_RUNTIME_DIR**: `$XDG_RUNTIME_DIR/mpp-solar.pid`
- **Non-root user without XDG_RUNTIME_DIR**: `/tmp/mpp-solar.pid`
- **PyInstaller bundle**: `/tmp/mpp-solar.pid` (can be overridden)

## Benefits of Configurable PID File

1. **Multi-instance support**: Run multiple daemon instances with different configurations
2. **Permission flexibility**: Use locations where the user has write access
3. **Container-friendly**: Easy to mount volumes for persistent PID files
4. **Development**: Use local directories during development/testing
5. **System integration**: Integrate with existing system management tools

## Advanced Examples

### Multiple daemon instances:
```bash
# Start first instance for battery monitoring
mpp-solar --daemon --pidfile /var/run/mpp-solar-battery.pid \
  -C /etc/mpp-solar/battery.conf

# Start second instance for inverter monitoring  
mpp-solar --daemon --pidfile /var/run/mpp-solar-inverter.pid \
  -C /etc/mpp-solar/inverter.conf
```

### Systemd service integration:
```ini
[Unit]
Description=MPP Solar Monitor
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/bin/mpp-solar --daemon --pidfile /var/run/mpp-solar.pid -C /etc/mpp-solar/mpp-solar.conf
ExecStop=/usr/local/bin/mpp-solar --daemon-stop --pidfile /var/run/mpp-solar.pid
PIDFile=/var/run/mpp-solar.pid
Restart=always
User=mpp-solar
Group=mpp-solar

[Install]
WantedBy=multi-user.target
```

### OpenRC service integration:
```bash
#!/sbin/openrc-run

name="MPP-Solar Daemon"
command="/usr/bin/mpp-solar"
command_args="-C /etc/mpp-solar/mpp-solar.conf --daemon"
pidfile="/run/mpp-solar.pid"
command_background="yes"

supervisor="supervise-daemon"
directory="/"
respawn_delay=5
respawn_max=0  # 0 means unlimited restarts
output_log="/var/log/mpp-solar.log"
error_log="/var/log/mpp-solar.err"

depend() {
    need localmount
    after networking
    use logger
}

start_pre() {
    checkpath --directory --mode 0755 /run
    checkpath --file --mode 0644 "$output_log"
    checkpath --file --mode 0644 "$error_log"
}
```