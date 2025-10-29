# Complete System Rebuild Guide

## Prerequisites

Before starting, ensure you have:
- Debian Linux system (or compatible distribution)
- Python 3.11 or higher installed
- Root/sudo access
- MPP-Solar inverter connected via USB
- Internet connection for package installation

## Step-by-Step Rebuild Process

### 1. System Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3 python3-pip python3-venv git usbutils mosquitto mosquitto-clients

# Install build dependencies
sudo apt install -y build-essential python3-dev libusb-1.0-0-dev
```

### 2. Clone Repository

```bash
cd ~
git clone https://github.com/jblance/mpp-solar.git
cd mpp-solar
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
pip install flask paho-mqtt requests pyyaml
```

### 4. Identify USB Device

```bash
# Find your MPP-Solar inverter USB device
lsusb
# Look for output like: Bus 001 Device 003: ID 0665:5161

# Find the hidraw device
ls -la /dev/hidraw*
# Usually /dev/hidraw0
```

### 5. Configure USB Permissions

```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Create udev rule (replace VENDOR_ID and PRODUCT_ID with your values)
sudo tee /etc/udev/rules.d/99-mpp-solar.rules << 'UDEV'
SUBSYSTEM=="usb", ATTRS{idVendor}=="0665", ATTRS{idProduct}=="5161", MODE="0666"
UDEV

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Log out and back in for group membership to take effect
```

### 6. Configure Daemon

Create `mpp-solar.conf`:

```ini
[SETUP]
pause = 60
mqtt_broker = localhost
mqtt_port = 1883
log_file = /home/YOUR_USERNAME/mpp-solar/mpp-solar.log

[inverter]
protocol = pi30
type = mppsolar
port = /dev/hidraw0
porttype = hidraw
baud = 2400
command = QPIGS
tag = inverter
outputs = screen,json,prom_file
prom_output_dir = /home/YOUR_USERNAME/mpp-solar/prometheus
dev = main_inverter
```

**Replace** `/home/YOUR_USERNAME/` with your actual home directory path.

### 7. Configure Web Interface

Create `web.yaml`:

```yaml
host: "0.0.0.0"
port: 5000
log_level: "info"
```

### 8. Test Device Communication

```bash
source venv/bin/activate
cd ~/mpp-solar

# Test basic communication
mpp-solar -p /dev/hidraw0 -P pi30 --porttype hidraw -c QID
# Should return device serial number

# Test status query
mpp-solar -p /dev/hidraw0 -P pi30 --porttype hidraw -c QPIGS
# Should return inverter status data
```

### 9. Create Management Scripts

Create `manage_daemon.sh`:

```bash
#!/bin/bash
INSTALL_DIR="/home/YOUR_USERNAME/mpp-solar"
VENV_DIR="$INSTALL_DIR/venv"
SERVICE_NAME="mpp-solar-daemon"

case "$1" in
    start)
        sudo systemctl start $SERVICE_NAME
        ;;
    stop)
        sudo systemctl stop $SERVICE_NAME
        ;;
    restart)
        sudo systemctl restart $SERVICE_NAME
        ;;
    status)
        sudo systemctl status $SERVICE_NAME
        ;;
    logs)
        sudo journalctl -u $SERVICE_NAME -f
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
```

Create `manage_web.sh` (similar structure).

Make executable:
```bash
chmod +x manage_daemon.sh manage_web.sh
```

### 10. Create Systemd Services

Create `/etc/systemd/system/mpp-solar-daemon.service`:

```ini
[Unit]
Description=MPP-Solar Inverter Monitoring Daemon
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/mpp-solar
ExecStart=/home/YOUR_USERNAME/mpp-solar/venv/bin/mpp-solar -c /home/YOUR_USERNAME/mpp-solar/mpp-solar.conf --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mpp-solar-daemon
sudo systemctl start mpp-solar-daemon
sudo systemctl status mpp-solar-daemon
```

### 11. Configure MQTT Broker

```bash
# Create MQTT user
sudo mosquitto_passwd -c /etc/mosquitto/passwd mqttuser
# Enter password: mqtt123 (or your chosen password)

# Configure Mosquitto
sudo tee /etc/mosquitto/conf.d/default.conf << 'MQTTCONF'
listener 1883 127.0.0.1
allow_anonymous false
password_file /etc/mosquitto/passwd
MQTTCONF

# Restart Mosquitto
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto

# Test MQTT
mosquitto_pub -h localhost -p 1883 -u mqttuser -P mqtt123 -t test/topic -m "test"
```

### 12. Create Weather Fetcher

Copy the existing `weather_fetcher.py` or create with your location settings:

```python
LOCATION = {
    'latitude': YOUR_LATITUDE,
    'longitude': YOUR_LONGITUDE,
    'name': 'Your Location'
}
```

Create `/etc/systemd/system/weather-fetcher.service`:

```ini
[Unit]
Description=Weather Data Fetcher for MPP-Solar
After=network.target mosquitto.service

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/mpp-solar
ExecStart=/home/YOUR_USERNAME/mpp-solar/venv/bin/python /home/YOUR_USERNAME/mpp-solar/weather_fetcher.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable weather-fetcher
sudo systemctl start weather-fetcher
sudo systemctl status weather-fetcher
```

### 13. Deploy Web Interface

```bash
cd ~/mpp-solar
source venv/bin/activate

# Test web interface manually
python web_interface.py
# Access at http://YOUR_IP:5000

# Press Ctrl+C to stop, then optionally create web service
```

### 14. Verify Installation

```bash
# Check all services are running
systemctl status mpp-solar-daemon weather-fetcher mosquitto

# Check Prometheus files are being created
ls -la ~/mpp-solar/prometheus/

# Check logs
tail -f ~/mpp-solar/mpp-solar.log
tail -f ~/mpp-solar/weather_fetcher.log

# Test web interface
curl -s http://localhost:5000/api/data | python -m json.tool

# Test MQTT house sensors
mosquitto_pub -h localhost -p 1883 -u mqttuser -P mqtt123 \
  -t house/temperature -m "22.5"
```

### 15. Access Dashboards

Open browser and navigate to:
- Main dashboard: `http://YOUR_IP:5000`
- LCARS dashboard: `http://YOUR_IP:5000/lcars`
- Charts: `http://YOUR_IP:5000/charts`
- House sensors: `http://YOUR_IP:5000/house`

## Configuration Checklist

- [ ] Python 3.11+ installed
- [ ] System packages installed (mosquitto, git, etc.)
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] USB device identified
- [ ] udev rules created
- [ ] User added to dialout group
- [ ] mpp-solar.conf configured
- [ ] web.yaml configured
- [ ] Device communication tested
- [ ] mpp-solar-daemon.service created and running
- [ ] mosquitto configured with authentication
- [ ] weather_fetcher.py configured
- [ ] weather-fetcher.service created and running
- [ ] web_interface.py tested
- [ ] All services verified running
- [ ] Web dashboards accessible

## Troubleshooting

### Device Not Found
```bash
# Check USB connection
lsusb | grep -i "0665:5161"

# Check hidraw device
ls -la /dev/hidraw*

# Check permissions
groups $USER | grep dialout
```

### Service Won't Start
```bash
# Check logs
sudo journalctl -u mpp-solar-daemon -n 50
sudo journalctl -u weather-fetcher -n 50

# Check configuration
cat ~/mpp-solar/mpp-solar.conf
```

### No Web Access
```bash
# Check if process is running
ps aux | grep web_interface

# Check port is listening
sudo netstat -tlnp | grep 5000

# Check firewall
sudo ufw status
```

### MQTT Issues
```bash
# Check mosquitto is running
sudo systemctl status mosquitto

# Test connection
mosquitto_sub -h localhost -p 1883 -u mqttuser -P mqtt123 -t "#" -v

# Check logs
sudo journalctl -u mosquitto -n 50
```

## Post-Installation

### Regular Maintenance
- Check service status weekly: `systemctl status mpp-solar-daemon weather-fetcher`
- Review logs monthly: `journalctl -u mpp-solar-daemon --since "1 month ago"`
- Update dependencies quarterly: `pip install --upgrade -r requirements.txt`
- Backup configuration files regularly

### Monitoring
- CPU usage should be <1%
- Memory usage should be <100MB total
- Disk usage for prometheus/ directory grows slowly (<1MB/day)

### Backups
Priority files to backup:
- `mpp-solar.conf`
- `web.yaml`
- `weather_fetcher.py`
- `/etc/udev/rules.d/99-mpp-solar.rules`
- `/etc/systemd/system/mpp-solar-*.service`
- `/etc/systemd/system/weather-fetcher.service`
- All documentation files (*.md)

## Success Criteria

Your system is successfully rebuilt when:
- ✅ All three services are running (mpp-solar-daemon, weather-fetcher, mosquitto)
- ✅ Prometheus files are being generated in ~/mpp-solar/prometheus/
- ✅ Web interface is accessible and shows inverter data
- ✅ Charts display historical data
- ✅ House sensors dashboard receives MQTT data
- ✅ Weather data is updating every 10 minutes
- ✅ All dashboards (standard and LCARS) are functional

## Reference Documentation

For detailed information, refer to:
- **CONTEXT.md** - Entry point and quick reference
- **IMPLEMENTATION_PLAN.md** - Complete technical specification
- **PROGRESS.md** - Current state and known issues
- **SETUP_GUIDE.md** - Original setup guide
- **mpp-solar-architecture.md** - System architecture diagrams

---

**Last Updated**: October 28, 2025
**Documentation Standard**: claude_rob.md methodology
