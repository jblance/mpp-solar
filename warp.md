# MPP Solar Monitoring System - Warp Documentation

## Project Overview
This is an mmp-solar monitoring system running on a Raspberry Pi with Debian GNU/Linux. The system monitors solar inverter data via USB communication and exports metrics to various outputs including Prometheus, JSON, and screen display.

## System Architecture

### Hardware Setup
- **Platform**: Raspberry Pi running Debian GNU/Linux (bookworm)
- **Inverter Connection**: USB-to-Serial adapter (Cypress 0665:5161)
- **Interface**: HID Raw device (`/dev/hidraw0`)
- **Protocol**: PI30 (standard MPP Solar protocol)

### Software Components
- **Main Application**: mpp-solar daemon
- **Python Environment**: Virtual environment in `./venv/`
- **Configuration**: `mpp-solar.conf`
- **Logging**: `mpp-solar.log` and `web_interface.log`
- **Metrics Output**: Prometheus files in `./prometheus/`

## Configuration Files

### Main Config: `mpp-solar.conf`
```ini
[SETUP]
pause = 60
mqtt_broker = localhost
mqtt_port = 1883
log_file = /home/constantine/mpp-solar/mpp-solar.log

[inverter]
protocol = pi30
type = mppsolar
port = /dev/hidraw0
porttype = hidraw
baud = 2400
command = QPIGS
tag = inverter
outputs = screen,json,prom_file
prom_output_dir = /home/constantine/mpp-solar/prometheus
dev = main_inverter
```

## USB Device Information

### Current USB Device Detection
```
Bus 001 Device 003: ID 0665:5161 Cypress Semiconductor USB to Serial
- Interface Class: Human Interface Device (HID)
- Interface: /dev/hidraw0
- Endpoint: 0x81 EP 1 IN (Interrupt, 8 bytes, 12ms interval)
- Protocol: USB HID v1.11
```

### Device Path Structure
```
/devices/platform/scb/fd500000.pcie/pci0000:00/0000:00:00.0/0000:01:00.0/usb1/1-1/1-1.2/1-1.2:1.0/0003:0665:5161.0001/hidraw/hidraw0
```

## Operation Commands

### Start Daemon
```bash
cd /home/constantine/mpp-solar
./venv/bin/mpp-solar -C mpp-solar.conf --daemon
```

### Manual Testing
```bash
# Test single command
./venv/bin/mpp-solar -p /dev/hidraw0 -P pi30 -c QPIGS

# Debug mode
./venv/bin/mpp-solar -p /dev/hidraw0 -P pi30 -D -c QPIRI
```

### Check Status
```bash
# Check running processes
ps aux | grep mpp-solar

# Check recent logs
tail -f mpp-solar.log

# Check prometheus output
ls -la prometheus/
```

## Troubleshooting

### Common Issues

#### 1. Communication Timeouts
**Symptoms**: 
- "Overall timeout (5.0s) exceeded while reading response"
- "No data available (EAGAIN/EWOULDBLOCK)"

**Causes**:
- Inverter not powered on
- USB cable disconnected
- Inverter not in communication mode
- Wrong cable type (needs data cable, not charging cable)

**Diagnostic Commands**:
```bash
# Check USB device presence
lsusb | grep 0665:5161

# Check HID device info
udevadm info /dev/hidraw0

# Test device accessibility
python3 -c "
with open('/dev/hidraw0', 'rb+') as f:
    print('Device accessible')
"

# Check recent USB activity
dmesg | grep -i "usb\|hid" | tail -10
```

#### 2. Permission Issues
**Fix**:
```bash
# Check permissions
ls -la /dev/hidraw0

# If needed, add user to dialout group
sudo usermod -a -G dialout $USER
```

### Protocol Details

#### PI30 Protocol Commands
- `QPIGS` - Get inverter general status
- `QPIRI` - Get inverter rating information
- Commands are sent with CRC checksum
- Response timeout: 5 seconds with 3 retry attempts

#### Communication Flow
1. Calculate CRC for command (e.g., QPIGS → CRC: 0xf8 0x54)
2. Send full command: `QPIGS\xf8T\r`
3. Wait for response with 150ms polling intervals
4. Retry up to 3 times on timeout

## File Structure
```
/home/constantine/mpp-solar/
├── mpp-solar.conf              # Main configuration
├── mpp-solar.log              # Application logs (14MB+)
├── web_interface.log          # Web interface logs (44MB+)
├── venv/                      # Python virtual environment
├── prometheus/                # Metrics output directory
├── mppsolar/                  # Source code
├── docs/                      # Documentation
├── templates/                 # Configuration templates
└── manage_daemon.sh          # Daemon management script
```

## Monitoring & Metrics

### Prometheus Output
- Location: `./prometheus/mpp-solar-inverter-.prom`
- Updates every 60 seconds (configurable via `pause` setting)
- Metrics format: Prometheus exposition format

### Log Files
- **mpp-solar.log**: Main application logs with communication details
- **web_interface.log**: Web interface access logs
- Log rotation recommended for large deployments

## Hardware Requirements

### Supported USB-to-Serial Adapters
- Cypress Semiconductor USB to Serial (0665:5161) ✓ Detected
- Must support HID Raw communication
- Driver: `hid-generic`

### Inverter Compatibility
- MPP Solar inverters with PI30 protocol
- USB communication cable required
- Inverter must be in communication-ready state

## Development & Debugging

### Python Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # if available

# Run tests
python -m pytest tests/  # if test suite exists
```

### Debug Mode Features
- Detailed communication logging
- Protocol command tracing
- USB device interaction monitoring
- CRC calculation verification

## System Integration

### Service Management
- Manual daemon mode (no systemd service currently configured)
- PID file location: `/var/run/mpp-solar.pid` or `/tmp/mpp-solar.pid`
- Process management via `manage_daemon.sh`

### Network Integration
- MQTT broker: localhost:1883 (configurable)
- UDP port: 5555 (for data export)
- Prometheus push gateway support available
- Web interface on separate process

---

**Last Updated**: 2025-09-16  
**System**: Debian GNU/Linux on Raspberry Pi  
**mpp-solar Version**: 0.16.57-dev  
**Python Version**: 3.11.2
