# CLAUDE.md - Quick Reference Guide

This file provides quick reference commands and common tasks for Claude Code when working with this repository.

**For detailed context and architecture, see:**
- `CONTEXT.md` - Start here for full project understanding
- `IMPLEMENTATION_PLAN.md` - Deep technical architecture
- `PROGRESS.md` - Development history and current status

## Quick Project Facts

**Version:** 0.16.57
**Python:** 3.11+ required (minimum 3.10 for >=0.16.0)
**Breaking Change:** Command separator changed from `,` to `#` in v0.16.0

**Architecture:** Hardware → I/O Port → Protocol Parser → Device (retry logic) → Output → Destination

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

## Architecture Overview

**Five Core Layers:**
1. **I/O** (`mppsolar/inout/`) - Physical communication (serial, USB HID, Bluetooth, MQTT)
2. **Protocol** (`mppsolar/protocols/`) - Command structures, CRC, response parsing (28+ protocols)
3. **Device** (`mppsolar/devices/`) - Retry logic (3 attempts, 1s/2s/3s backoff), validation
4. **Output** (`mppsolar/outputs/`) - Data routing (MQTT, Prometheus, databases, Home Assistant)
5. **Daemon** (`mppsolar/daemon/`) - Background service, config-driven multi-device support

**Web Interface:** Flask app (`web_interface.py`) with REST API, SSE, and historical charts

**See `IMPLEMENTATION_PLAN.md` for detailed architecture and design decisions.**

## Critical Information

### Command Separator (Breaking Change!)

**CRITICAL:** Use `#` not `,` for multiple commands (changed in v0.16.0):
```bash
# Correct
mpp-solar -c "QPIGS#QPIRI#QMOD"

# Wrong (old syntax)
mpp-solar -c "QPIGS,QPIRI,QMOD"
```

### Key Files

- `mppsolar/devices/device.py:269` - AbstractDevice with retry logic (always use this layer)
- `mppsolar/protocols/pi30.py` - Most common protocol (reference for new protocols)
- `mppsolar/protocols/jk04.py` - Binary protocol example
- `mppsolar/libs/mqtt_manager.py` - MQTT connection pooling
- `web_interface.py:265` - Flask web app

### Configuration Quick Reference

Daemon config (`mpp-solar.conf`):
```ini
[SETUP]
pause = 60  # seconds between device polls

[device_name]
type = mppsolar
protocol = pi30
port = /dev/hidraw0
porttype = hidraw
command = QPIGS
outputs = screen,json,prom_file,hass_mqtt
```

**Port Types:** `hidraw`, `serial`, `jkble`, `test`
**Common Protocols:** `pi30` (MPP-Solar), `jk04` (JK BMS), `daly` (Daly BMS)
**Popular Outputs:** `screen`, `json`, `prom_file`, `hass_mqtt`, `json_mqtt`

### Web API Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Standard dashboard |
| `/lcars` | GET | LCARS themed dashboard |
| `/api/data` | GET | Current status (JSON) |
| `/api/historical` | GET | Historical data |
| `/api/command` | POST | Execute command |

**Data:** In-memory (1000 points ~8.3hrs) + Prometheus files for history

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

## Directory Structure

```
mppsolar/
├── __init__.py          # CLI entry point (680+ lines)
├── devices/             # Device layer (retry logic)
├── protocols/           # 28+ protocol implementations
├── inout/               # I/O handlers (serial, USB, BLE, MQTT)
├── outputs/             # Output processors (screen, JSON, MQTT, Prometheus, databases)
├── daemon/              # Background service
└── libs/mqtt_manager.py # MQTT connection pooling

web_interface.py         # Flask web app (265 lines)
tests/                   # Unit + integration tests
```

## Development Notes

**Port Types:** `hidraw` (USB HID), `serial` (RS232), `jkble` (Bluetooth), `test` (no hardware)

**Protocol Selection:** Use `-P` flag - `pi30` (MPP-Solar), `jk04` (JK BMS), `daly` (Daly BMS)
- Run `mpp-solar -P help` to list all available protocols

**Output Chaining:** Specify multiple outputs: `outputs = screen,json,prom_file,hass_mqtt`

**Retry Logic:** Device layer auto-retries (3 attempts). Failures after retries usually mean:
- Wrong port/porttype/protocol
- Hardware issue
- Permission problem

**Config Templates:** Never commit actual configs - use `.template` files

**BLE Support:** `pip install mppsolar[ble]` for Bluetooth devices

**Always use AbstractDevice layer** - Don't bypass retry logic when adding protocols

## Troubleshooting Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| "Could not open port" | Check device exists, add user to `dialout` group, verify porttype |
| "No response" | Use `-D` debug flag, verify protocol, check connection |
| "Web shows no data" | Ensure daemon running with `prom_file` output, check output directory |
| "MQTT not publishing" | Verify broker running (`ss -tlnp \| grep 1883`), check daemon config |

**Debug Mode:** Add `-D` flag to any command for detailed output

## Documentation Index

**Context & Architecture:**
- `CONTEXT.md` - AI assistant entry point (start here!)
- `IMPLEMENTATION_PLAN.md` - Technical architecture deep-dive
- `PROGRESS.md` - Development history and status
- This file (`CLAUDE.md`) - Quick reference

**User Documentation:**
- `README.md` - Installation and basic usage
- `SETUP_GUIDE.md` - Detailed installation
- `WEB_INTERFACE_README.md` - Web UI guide
- `DAEMON_README.md` - Daemon configuration
- `CHARTS_README.md` - Charts feature
- `LCARS_COMPLETE_README.md` - LCARS theme
- `docs/` - Protocol specs, hardware compatibility

**Links:**
- GitHub: https://github.com/jblance/mpp-solar
- PyPI: https://pypi.org/project/mppsolar/
- Wiki: https://github.com/jblance/mpp-solar/wiki
