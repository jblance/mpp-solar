# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MPP-Solar is a Python package for communicating with solar inverters, Battery Management Systems (BMS), and power monitoring devices. It supports MPP-Solar inverters (PI series), JK BMS, Daly BMS, and Victron VE Direct devices.

**Version:** 0.16.57
**Python:** 3.11+ required (minimum 3.10 for >=0.16.0)
**Breaking Change:** Command separator changed from `,` to `#` in v0.16.0

## Development Commands

### Testing
```bash
# Run all tests
make test

# Run unit tests only
make unit-tests

# Run integration tests only
make integration-tests

# Using pytest directly
pytest tests/unit/
pytest tests/integration/
pytest -v  # verbose mode
```

### Running the Application
```bash
# Basic command execution
mpp-solar -p /dev/hidraw0 -P pi30 --porttype hidraw -c QPIGS

# Multiple commands (note: separator is # not ,)
mpp-solar -p /dev/hidraw0 -P pi30 --porttype hidraw -c "QPIGS#QPIRI#QMOD"

# Run daemon mode
mpp-solar -C mpp-solar.conf --daemon

# Debug mode
mpp-solar -p /dev/hidraw0 -P pi30 --porttype hidraw -c QPIGS -D

# Start web interface
python web_interface.py
```

### Build & Release
```bash
# Build for PyPI
make pypi

# Upload to PyPI
make pypi-upload

# Tag a release
make git-tag-release

# Docker
make docker-up
```

### Code Style
- Black formatter with line length 149
- Run: `black --line-length 149 mppsolar/`

## Architecture

### Core Layers

1. **I/O Layer** (`mppsolar/inout/`)
   - Handles physical communication: serial, USB HID, Bluetooth, MQTT, sockets
   - Key files: `serialio.py`, `hidrawio.py`, `jkbleio.py`, `mqttio.py`

2. **Protocol Layer** (`mppsolar/protocols/`)
   - Defines command structures, CRC algorithms, response parsing
   - PI series: `pi30.py` (most common), `pi16.py`, `pi17.py`, `pi18.py`, `pi41.py`
   - JK BMS: `jk02.py`, `jk04.py`, `jkserial.py`
   - Others: `daly.py` (Daly BMS), `ved.py` (Victron)
   - All inherit from `abstractprotocol.py`

3. **Device Layer** (`mppsolar/devices/`)
   - Orchestrates I/O + Protocol with error handling and retry logic
   - `device.py`: AbstractDevice with 3-attempt retry (1s, 2s, 3s backoff)
   - Implements special commands: `list_commands`, `get_status`, `get_settings`

4. **Output Layer** (`mppsolar/outputs/`)
   - Routes data to various destinations
   - `screen.py`, `json.py`, `prometheus.py`, `prom_file.py`
   - MQTT variants: `mqtt.py`, `hass_mqtt.py`, `json_mqtt.py`
   - Storage: `postgres.py`, `mongo.py`

5. **Daemon** (`mppsolar/daemon/`)
   - Continuous monitoring service with systemd/OpenRC support
   - Config-driven execution with scheduling

6. **Web Interface** (`web_interface.py`)
   - Flask app with REST API and dashboards
   - In-memory store (1000 data points ~8.3 hours)
   - Historical data from Prometheus files
   - Multiple UI themes: standard, LCARS (Star Trek)

### Data Flow
```
Hardware → I/O Port → Protocol Parser → Device (retry logic) → Output Processor → Destination
```

## Key Implementation Details

### Device Communication Pattern

The `AbstractDevice` class (`mppsolar/devices/device.py:269 lines`) provides:
- **Validation:** Protocol, port, and command checking before execution
- **Retry Logic:** Up to 3 attempts with progressive backoff
- **Echo Detection:** Filters out command echoes in responses
- **Error Classification:** Distinguishes between transient and permanent errors

When adding protocol support, always work through this device layer - do not bypass retry logic.

### Command Separator

**CRITICAL:** Use `#` not `,` for multiple commands (breaking change in v0.16.0):
```bash
# Correct
mpp-solar -c "QPIGS#QPIRI#QMOD"

# Wrong (old syntax)
mpp-solar -c "QPIGS,QPIRI,QMOD"
```

### Protocol Implementation

Each protocol defines:
- Command structures with CRC algorithms
- Response parsing and decoding logic
- Status vs settings command categorization
- Default/ID commands for device identification

Example protocol files to reference:
- `mppsolar/protocols/pi30.py` - Most common MPP-Solar protocol
- `mppsolar/protocols/jk04.py` - JK BMS example with binary protocol

### Configuration System

Config file structure (`mpp-solar.conf`):
```ini
[SETUP]
pause = 60  # seconds between iterations
mqtt_broker = localhost
mqtt_port = 1883

[device_section_name]
type = mppsolar
protocol = pi30
port = /dev/hidraw0
porttype = hidraw
command = QPIGS
outputs = screen,json,prom_file
prom_output_dir = /path/to/prometheus
```

Multiple device sections supported - each runs in parallel in daemon mode.

### Web Interface Architecture

**API Endpoints:**
- `/api/data` - Current device status
- `/api/historical` - Historical data from Prometheus files
- `/api/historical/all` - All historical data
- `/api/command` - Execute device command (POST)
- `/api/refresh` - Manual data refresh

**Routes:**
- `/` - Standard Bootstrap dashboard
- `/lcars` - LCARS (Star Trek) themed dashboard
- `/charts` - Historical charts
- `/charts/lcars` - LCARS themed charts

**Data Management:**
- In-memory circular buffer (1000 entries)
- 30-second collection interval
- Reads `.prom` files from daemon for history

### MQTT Integration

The codebase uses a centralized MQTT manager (`mppsolar/libs/mqtt_manager.py`):
- Connection pooling (reuses connections per broker)
- Threaded publish queue with exponential backoff
- Command authorization via regex patterns
- Automatic reconnection with 5s → 300s backoff

Output options:
- `mqtt` - Basic MQTT publishing
- `hass_mqtt` - Home Assistant auto-discovery with device classes
- `json_mqtt` - JSON formatted MQTT messages

### Prometheus Output

File output (`mppsolar/outputs/prom_file.py`) features:
- Atomic writes (temp file → rename)
- Hard-linked backups (zero-copy)
- Automatic rotation (keeps last 10 backups)
- Prometheus format compatible with Grafana

## Common Development Scenarios

### Adding a New Protocol

1. Create file in `mppsolar/protocols/` (e.g., `mynewprotocol.py`)
2. Inherit from `AbstractProtocol`
3. Define command dictionary with CRC and response parsing
4. Register in `mppsolar/protocols/__init__.py`
5. Add tests in `tests/integration/test_protocol_*.py`

### Adding a New Output Format

1. Create file in `mppsolar/outputs/` (e.g., `myoutput.py`)
2. Inherit from `BaseOutput`
3. Implement `output(data, tag=None, mqtt_broker=None)` method
4. Register in `mppsolar/outputs/__init__.py`

### Testing Device Communication

```bash
# List available devices
ls -la /dev/ttyUSB* /dev/hidraw*

# Check USB device info
lsusb

# Test basic command with debug
mpp-solar -p /dev/hidraw0 -P pi30 --porttype hidraw -c QID -D

# Test without actual device (test mode)
mpp-solar -p test -P pi30 -c QPIGS
```

### Daemon Service Management

```bash
# Check status
sudo systemctl status mpp-solar-daemon
sudo systemctl status mpp-solar-web

# View logs
sudo journalctl -u mpp-solar-daemon -f
tail -f web_interface.log

# Restart services
sudo systemctl restart mpp-solar-daemon
sudo systemctl restart mpp-solar-web
```

### Device Permissions Setup

```bash
# Add user to dialout group (for serial ports)
sudo usermod -a -G dialout $USER

# Create udev rule for USB device (example)
# First, find vendor/product ID with: lsusb
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0665", ATTRS{idProduct}=="5161", MODE="0666"' | \
  sudo tee /etc/udev/rules.d/99-mpp-solar.rules

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## File Structure Quick Reference

```
mppsolar/
├── __init__.py          # Main entry point (680+ lines with CLI argument parsing)
├── devices/             # Device orchestration with retry logic
│   ├── device.py        # AbstractDevice (269 lines)
│   ├── mppsolar.py
│   └── jkbms.py
├── protocols/           # 28+ protocol implementations
│   ├── abstractprotocol.py
│   ├── pi30.py          # Most common MPP-Solar
│   ├── jk04.py
│   └── ...
├── inout/               # I/O communication handlers
│   ├── serialio.py
│   ├── hidrawio.py
│   ├── jkbleio.py       # Bluetooth for JK BMS
│   └── ...
├── outputs/             # Data output processors
│   ├── prometheus.py
│   ├── prom_file.py     # File output with atomic writes
│   ├── mqtt.py
│   ├── hass_mqtt.py     # Home Assistant integration
│   └── ...
├── daemon/              # Background service support
│   ├── daemon.py
│   └── daemon_systemd.py
└── libs/
    └── mqtt_manager.py  # Centralized MQTT management

web_interface.py         # Flask web app (265 lines)
templates/               # Web UI templates
tests/
├── unit/
└── integration/
```

## Important Notes for Development

1. **Port Types Matter:** Different devices require different port types:
   - `hidraw` for USB HID devices (most MPP-Solar inverters)
   - `serial` for RS232/USB serial
   - `jkble` for Bluetooth JK BMS
   - `test` for testing without hardware

2. **Protocol Selection:** Use `-P` flag to specify protocol:
   - `pi30` - Most common for MPP-Solar/Voltronic
   - `jk04` - JK BMS via Bluetooth
   - `daly` - Daly BMS
   - Run `mpp-solar -P help` to list all protocols

3. **Output Chaining:** Multiple outputs can be specified:
   ```bash
   outputs = screen,json,prom_file,hass_mqtt
   ```

4. **Error Handling:** The device layer handles retries automatically. If you see commands failing after 3 attempts, it's likely:
   - Wrong port or porttype
   - Wrong protocol
   - Hardware connection issue
   - Permission problem

5. **Configuration Templates:** Never commit actual config files. Use templates:
   - `mpp-solar.conf.template`
   - `web.yaml.template`
   - `manage_daemon.sh.template`

6. **Web Interface Data:** The web interface maintains an in-memory store and reads historical data from Prometheus files. If historical data is missing, check:
   - Daemon is running with `prom_file` output
   - `prom_output_dir` is correctly configured
   - Files exist in the output directory

7. **Bluetooth BLE (JK BMS):** Requires `bluepy` package:
   ```bash
   pip install mppsolar[ble]
   ```

## Troubleshooting

### Common Issues

**"Could not open port"**
- Check device exists: `ls -la /dev/hidraw* /dev/ttyUSB*`
- Check permissions: Add user to `dialout` group
- Verify porttype matches device

**"No response from device"**
- Enable debug mode: `-D` flag
- Verify protocol matches device
- Check physical connection
- Try different baud rate (default 2400)

**"Web interface shows no data"**
- Check daemon is running: `systemctl status mpp-solar-daemon`
- Verify daemon config includes `prom_file` output
- Check Prometheus output directory exists and has `.prom` files

**"MQTT not publishing"**
- Verify MQTT broker is running: `ss -tlnp | grep 1883`
- Test with mosquitto_sub: `mosquitto_sub -h localhost -t '#' -v`
- Check daemon config has MQTT output enabled
- Review logs for connection errors

## Additional Documentation

- `README.md` - Installation and basic usage
- `SETUP_GUIDE.md` - Detailed installation instructions
- `WEB_INTERFACE_README.md` - Web UI documentation
- `DAEMON_README.md` - Daemon configuration guide
- `CHARTS_README.md` - Charts feature documentation
- `LCARS_COMPLETE_README.md` - LCARS theme documentation
- `docs/` directory - Protocol specs, troubleshooting, hardware compatibility

## Links

- Repository: https://github.com/jblance/mpp-solar
- Wiki: https://github.com/jblance/mpp-solar/wiki
- PyPI: https://pypi.org/project/mppsolar/
- Docker Hub: https://hub.docker.com/r/jblance/mppsolar
