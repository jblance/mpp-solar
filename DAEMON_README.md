# MPP-Solar Daemon Service Setup

This guide explains how to set up the MPP-Solar daemon to run automatically on system startup and log data every 15 minutes.

## Overview

The MPP-Solar daemon service:
- Runs automatically on system boot
- Monitors your inverter every 15 minutes (900 seconds)
- Logs data to multiple formats (screen, JSON, Prometheus files)
- Restarts automatically if it crashes
- Provides comprehensive logging and monitoring

## Quick Setup

### 1. Install the Daemon Service

```bash
./manage_daemon.sh install
```

This will:
- Copy the service file to systemd
- Enable the service to start on boot
- Set up proper permissions and paths

### 2. Start the Daemon

```bash
./manage_daemon.sh start
```

### 3. Verify It's Running

```bash
./manage_daemon.sh status
```

## Configuration

The daemon uses the `mpp-solar.conf` configuration file:

```ini
[SETUP]
pause = 900                    # 15 minutes between readings
mqtt_broker = localhost        # MQTT broker (optional)
mqtt_port = 1883              # MQTT port
log_file = /path/to/your/mpp-solar/mpp-solar.log

[inverter]
protocol = YOUR_PROTOCOL      # MPP-Solar protocol
type = mppsolar              # Device type
port = /dev/YOUR_DEVICE      # Device port
porttype = YOUR_PORTTYPE     # Port type
baud = YOUR_BAUD_RATE        # Baud rate
command = YOUR_COMMANDS      # Commands to run
tag = YOUR_TAG               # Device tag
outputs = screen,json,prom_file  # Output formats
prom_output_dir = /path/to/your/mpp-solar/prometheus
dev = YOUR_DEVICE_ID         # Device identifier
```

## Management Commands

### Service Management

```bash
# Start the daemon
./manage_daemon.sh start

# Stop the daemon
./manage_daemon.sh stop

# Restart the daemon
./manage_daemon.sh restart

# Check status
./manage_daemon.sh status

# View logs (follow mode)
./manage_daemon.sh logs

# Enable auto-start on boot
./manage_daemon.sh enable

# Disable auto-start on boot
./manage_daemon.sh disable
```

### Installation

```bash
# Install and enable the service
./manage_daemon.sh install

# Remove the service
./manage_daemon.sh uninstall
```

### Troubleshooting

```bash
# Test device connectivity
./manage_daemon.sh check-device

# Test configuration
./manage_daemon.sh test-config
```

## Data Output

The daemon creates several types of output:

### 1. Screen Output
Real-time display of inverter data in the terminal.

### 2. JSON Output
Structured data in JSON format for easy parsing.

### 3. Prometheus Files
Metrics files in Prometheus format for monitoring systems:

```
/path/to/your/mpp-solar/prometheus/
├── mpp-solar-inverter-qpigs.prom    # General status
├── mpp-solar-inverter-qpiri.prom    # Current settings
├── mpp-solar-inverter-qmod.prom     # Device mode
└── mpp-solar-inverter-qflag.prom    # Flag status
```

### 4. Log File
Detailed logs at `/path/to/your/mpp-solar/mpp-solar.log`

## Prometheus Integration

The daemon creates Prometheus-compatible metrics files. You can:

### 1. Use with Node Exporter
Configure Node Exporter to read the prometheus directory:

```yaml
# In node_exporter config
textfile:
  directory: /path/to/your/mpp-solar/prometheus
```

### 2. Use with Prometheus Server
Add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'mpp-solar'
    static_configs:
      - targets: ['localhost:9100']
    file_sd_configs:
      - files:
        - '/path/to/your/mpp-solar/prometheus/*.prom'
```

### 3. Example Metrics
```
mpp_solar_battery_voltage{inverter="inverter",device="main_inverter",cmd="QPIGS"} 48.0
mpp_solar_ac_output_voltage{inverter="inverter",device="main_inverter",cmd="QPIGS"} 120.1
mpp_solar_inverter_heat_sink_temperature{inverter="inverter",device="main_inverter",cmd="QPIGS"} 35
```

## Monitoring and Alerts

### Check Service Status
```bash
# Systemd status
sudo systemctl status mpp-solar-daemon

# Service logs
sudo journalctl -u mpp-solar-daemon -f

# Check if data is being collected
ls -la /path/to/your/mpp-solar/prometheus/
```

### Set Up Alerts
You can set up alerts based on the Prometheus metrics:

```yaml
# Example Prometheus alert rules
groups:
  - name: mpp-solar
    rules:
      - alert: BatteryVoltageLow
        expr: mpp_solar_battery_voltage < 45
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Battery voltage is low"
          
      - alert: InverterTemperatureHigh
        expr: mpp_solar_inverter_heat_sink_temperature > 50
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Inverter temperature is high"
```

## Troubleshooting

### Service Won't Start
1. Check device permissions:
   ```bash
   ls -la /dev/YOUR_DEVICE
   ```

2. Test device connectivity:
   ```bash
   ./manage_daemon.sh check-device
   ```

3. Check service logs:
   ```bash
   sudo journalctl -u mpp-solar-daemon -n 50
   ```

### No Data Being Collected
1. Verify the service is running:
   ```bash
   ./manage_daemon.sh status
   ```

2. Check the log file:
   ```bash
   tail -f /path/to/your/mpp-solar/prometheus/mpp-solar.log
   ```

3. Test the configuration:
   ```bash
   ./manage_daemon.sh test-config
   ```

### Permission Issues
1. Ensure udev rules are loaded:
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

2. Check device permissions:
   ```bash
   ls -la /dev/YOUR_DEVICE
   ```

## Integration with Web Interface

The daemon and web interface can run simultaneously:

1. **Daemon**: Collects data every 15 minutes and stores in Prometheus files
2. **Web Interface**: Provides real-time access and manual control

Both services can be managed independently:
- Daemon: `./manage_daemon.sh`
- Web Interface: `./manage_web.sh`

## System Requirements

- Python 3.11+
- Virtual environment with mpp-solar installed
- Access to `/dev/YOUR_DEVICE` device
- systemd (for service management)

## Security Considerations

- The service runs as your user account
- Device access is restricted to `/dev/YOUR_DEVICE`
- Logs are stored in user directory
- No network exposure by default

## Performance

- Low CPU usage (typically <1%)
- Minimal memory footprint (~10-20MB)
- Data collection every 15 minutes
- Automatic restart on failure

## Support

For issues with the daemon service:
1. Check the service logs: `./manage_daemon.sh logs`
2. Test device connectivity: `./manage_daemon.sh check-device`
3. Review the configuration file: `mpp-solar.conf`
4. Check systemd logs: `sudo journalctl -u mpp-solar-daemon`
