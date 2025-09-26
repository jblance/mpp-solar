# MPP-Solar Web Interface

A modern, responsive web interface for monitoring and controlling MPP-Solar inverters.

## Features

- **Real-time Monitoring**: Live display of inverter status, battery voltage, AC output, temperature, and more
- **Command Interface**: Execute any MPP-Solar command directly from the web interface
- **Auto-refresh**: Data automatically updates every 30 seconds
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **REST API**: JSON API endpoints for integration with other systems
- **Modern UI**: Clean, professional interface using Bootstrap 5

## Quick Start

### 1. Start the Web Interface

```bash
# Using the management script
./manage_web.sh start

# Or manually
source venv/bin/activate
python web_interface.py
```

### 2. Access the Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

### 3. Check Status

```bash
./manage_web.sh status
```

## Configuration

The web interface uses the `web.yaml` configuration file:

```yaml
host: "0.0.0.0"    # Listen on all interfaces
port: 5000         # Port number
log_level: "info"  # Logging level
```

## Management Commands

```bash
# Start the web interface
./manage_web.sh start

# Stop the web interface
./manage_web.sh stop

# Restart the web interface
./manage_web.sh restart

# Check if it's running
./manage_web.sh status

# View logs
./manage_web.sh logs

# Install as systemd service (optional)
./manage_web.sh install-service
```

## API Endpoints

### GET /api/data
Returns current inverter data in JSON format.

**Response:**
```json
{
  "status": {
    "battery_voltage": 48.0,
    "ac_output_voltage": 120.1,
    "ac_output_active_power": 0,
    "inverter_heat_sink_temperature": 36
  },
  "settings": {
    "battery_type": "User",
    "output_source_priority": "Solar first"
  },
  "mode": {
    "device_mode": "Battery"
  },
  "flags": {
    "buzzer": "enabled",
    "lcd_backlight": "enabled"
  },
  "timestamp": "2025-08-25T21:46:00.123456"
}
```

### POST /api/command
Execute a command on the inverter.

**Request:**
```json
{
  "command": "QPIGS"
}
```

**Response:**
```json
{
  "_command": "QPIGS",
  "_command_description": "General Status Parameters inquiry",
  "battery_voltage": 48.0,
  "ac_output_voltage": 120.1
}
```

### GET /api/refresh
Manually refresh the data from the inverter.

**Response:**
```json
{
  "status": "Data refreshed",
  "timestamp": "2025-08-25T21:46:00.123456"
}
```

## Dashboard Features

### Main Metrics
- **Battery Voltage**: Current battery voltage in volts
- **AC Output Voltage**: Current AC output voltage
- **Output Power**: Current power output in watts
- **Temperature**: Inverter heat sink temperature

### Status Panel
Displays all current status parameters from the inverter including:
- AC input/output voltages and frequencies
- Battery charging/discharging currents
- PV input data
- System flags and warnings

### Settings Panel
Shows current device settings including:
- Battery type and voltage settings
- Charging parameters
- Output priorities
- System configuration

### Command Interface
- **Manual Commands**: Type any MPP-Solar command directly
- **Quick Commands**: Dropdown with common commands
- **Command Results**: JSON display of command responses

## Common Commands

| Command | Description |
|---------|-------------|
| `QPIGS` | General Status Parameters |
| `QPIRI` | Current Settings |
| `QMOD` | Device Mode |
| `QFLAG` | Flag Status |
| `QID` | Device Serial Number |
| `QPIWS` | Warning Status |
| `QDI` | Default Settings |

## Installation as System Service

To run the web interface as a system service:

```bash
# Install the service
./manage_web.sh install-service

# Start the service
sudo systemctl start mpp-solar-web

# Enable auto-start on boot
sudo systemctl enable mpp-solar-web

# Check status
sudo systemctl status mpp-solar-web
```

## Troubleshooting

### Web Interface Won't Start
1. Check if the virtual environment is activated
2. Verify all dependencies are installed: `pip install flask pyyaml`
3. Check the log file: `./manage_web.sh logs`

### No Data Displayed
1. Verify the inverter is connected and accessible
2. Check device permissions: `ls -la /dev/YOUR_DEVICE`
3. Test direct communication: `mpp-solar -p /dev/YOUR_DEVICE -P YOUR_PROTOCOL --porttype YOUR_PORTTYPE -c QPIGS`

### Permission Denied
1. Ensure the hidraw device has correct permissions
2. Check if the udev rules are loaded: `sudo udevadm control --reload-rules`

## Security Notes

- The web interface runs on `0.0.0.0:5000` by default (accessible from any IP)
- For production use, consider:
  - Using a reverse proxy (nginx, Apache)
  - Adding authentication
  - Restricting access to local network only
  - Using HTTPS

## Integration Examples

### Home Assistant
Add to your `configuration.yaml`:
```yaml
rest:
  - resource: http://localhost:5000/api/data
    scan_interval: 30
    sensors:
      - name: "Battery Voltage"
        value_template: "{{ value_json.status.battery_voltage }}"
        unit_of_measurement: "V"
```

### Grafana
Use the API endpoints as data sources for Grafana dashboards.

### Custom Scripts
```bash
# Get current battery voltage
curl -s http://localhost:5000/api/data | jq '.status.battery_voltage'

# Execute a command
curl -X POST http://localhost:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "QPIGS"}'
```

## Support

For issues with the web interface, check:
1. The log file: `./manage_web.sh logs`
2. MPP-Solar documentation: https://github.com/jblance/mpp-solar
3. Flask documentation: https://flask.palletsprojects.com/
