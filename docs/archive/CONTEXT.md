# MPP-Solar Monitoring System - Context File

## 🎯 Purpose of This File

This document serves as the **entry point** for understanding the MPP-Solar Monitoring System. If you're starting a new AI session, experiencing context loss, or trying to understand the project from scratch, **start here**.

## 📊 Project Status

**Status**: ✅ **FULLY OPERATIONAL**  
**Last Updated**: October 28, 2025  
**Version**: 1.0 (Production)  
**Location**: `/home/constantine/mpp-solar/`

## 🔍 Quick Summary

The MPP-Solar Monitoring System is a comprehensive solar inverter monitoring platform that:
- Monitors an MPP-Solar inverter via USB HIDRAW interface
- Collects house environmental sensor data via MQTT
- Fetches and displays weather data from Open-Meteo API
- Provides multiple web dashboards (standard and LCARS themed)
- Stores metrics in Prometheus format
- Offers RESTful API for programmatic access

**Key Technologies**: Python 3.11+, Flask, MQTT (Mosquitto), mppsolar library, systemd services

## 📚 Essential Documentation

### Start Here for Fresh Setup
1. **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Comprehensive project plan
   - Complete system architecture
   - All phases and objectives
   - Technical implementation details
   - Configuration examples
   - Success criteria

2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Step-by-step installation
   - Initial setup commands
   - Configuration file templates
   - Service installation
   - Device permissions
   - Troubleshooting

### Current State Documentation
3. **[PROGRESS.md](PROGRESS.md)** - Current state and history
   - Completed phases (all 6 phases ✅)
   - Running services status
   - Known issues and technical debt
   - Deviations from plan
   - Future enhancements

### Architecture and Design
4. **[mpp-solar-architecture.md](mpp-solar-architecture.md)** - System architecture
   - Mermaid diagrams (architecture, data flow, components)
   - Technology stack details
   - Component interactions

### Component-Specific Guides
5. **[DAEMON_README.md](DAEMON_README.md)** - Daemon service details
6. **[WEB_INTERFACE_README.md](WEB_INTERFACE_README.md)** - Web interface guide
7. **[HOUSE_MQTT_SETUP.md](HOUSE_MQTT_SETUP.md)** - House sensor setup
8. **[CHARTS_README.md](CHARTS_README.md)** - Charts functionality
9. **[LCARS_COMPLETE_README.md](LCARS_COMPLETE_README.md)** - LCARS theme guide

### Main Project Documentation
10. **[README.md](README.md)** - mpp-solar package documentation

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                          │
│  Web Dashboard | LCARS Dashboard | Charts | House Sensors | API │
│     :5000/          :5000/lcars    :5000/charts  :5000/house    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     FLASK WEB APPLICATION                       │
│         web_interface.py (Background thread: 30s updates)       │
│    In-Memory Store (1000 entries) | MQTT Client | REST API     │
└─────────────────────────────────────────────────────────────────┘
         ↓                    ↓                     ↓
┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  MPP-Solar      │  │  MQTT Broker     │  │  Weather Fetcher │
│  Daemon Service │  │  (Mosquitto)     │  │  Service         │
│  (60s interval) │  │  localhost:1883  │  │  (10min interval)│
└─────────────────┘  └──────────────────┘  └──────────────────┘
         ↓                    ↓                     ↓
┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  USB HIDRAW     │  │  House Sensors   │  │  Open-Meteo API  │
│  /dev/hidraw0   │  │  (MQTT topics)   │  │  (Weather data)  │
│  PI30 @ 2400    │  │  house/#         │  │  43.7776,-72.8145│
└─────────────────┘  └──────────────────┘  └──────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE                               │
│  Prometheus Files (/prometheus/) | Logs | In-Memory Cache      │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Current Configuration

### Hardware
- **Device**: MPP-Solar Inverter
- **Connection**: USB HIDRAW `/dev/hidraw0`
- **Protocol**: PI30
- **Baud Rate**: 2400
- **USB IDs**: Vendor 0665, Product 5161

### Services
- **mpp-solar-daemon.service**: ✅ Active, queries inverter every 60s
- **weather-fetcher.service**: ✅ Active, fetches weather every 10 min
- **mosquitto.service**: ✅ Active, MQTT broker on localhost:1883
- **mpp-solar-web.service**: ⚠️ Not enabled (manual start preferred)

### Network Access
- **Web Interface**: http://192.168.1.134:5000
- **MQTT Broker**: localhost:1883 (mqttuser/mqtt123)
- **No external access** (localhost-only for security)

### File Locations
```
/home/constantine/mpp-solar/
├── venv/                          # Python virtual environment
├── web_interface.py               # Main Flask application
├── weather_fetcher.py             # Weather data collector
├── mpp-solar.conf                 # Daemon configuration
├── web.yaml                       # Web interface config
├── prometheus/                    # Metrics storage
├── templates/                     # HTML templates
├── static/                        # CSS/JS/images
└── [documentation files]          # This and other docs
```

### Key Configuration Files
- **mpp-solar.conf**: Daemon settings (query interval, device path, outputs)
- **web.yaml**: Web server settings (host, port, log level)
- **weather_fetcher.py**: Weather API config (location, MQTT settings)
- **/etc/udev/rules.d/99-mpp-solar.rules**: USB device permissions
- **/etc/systemd/system/*.service**: Service definitions

## 🚀 Quick Start Commands

### Check System Status
```bash
# Check all services
systemctl status mpp-solar-daemon weather-fetcher mosquitto

# Check web interface (if running as service)
systemctl status mpp-solar-web

# View logs
sudo journalctl -u mpp-solar-daemon -f
tail -f /home/constantine/mpp-solar/weather_fetcher.log
```

### Start Web Interface Manually
```bash
cd /home/constantine/mpp-solar
source venv/bin/activate
python web_interface.py
# Access at http://192.168.1.134:5000
```

### Manage Services
```bash
# Using management scripts
./manage_daemon.sh status   # Check daemon
./manage_web.sh status       # Check web interface

# Direct systemd commands
sudo systemctl start mpp-solar-daemon
sudo systemctl stop mpp-solar-daemon
sudo systemctl restart mpp-solar-daemon
```

### Test MQTT
```bash
# Publish test house sensor data
mosquitto_pub -h 192.168.1.134 -p 1883 -u mqttuser -P mqtt123 \
  -t house/temperature -m "25.0"

# Subscribe to all house topics
mosquitto_sub -h 192.168.1.134 -p 1883 -u mqttuser -P mqtt123 \
  -t "house/#" -v
```

## 🎯 Next Steps for AI Agent

When resuming work on this project after context reset:

1. **Read this file first** - Orient yourself with the project
2. **Read [PROGRESS.md](PROGRESS.md)** - Understand current state and completed work
3. **Read [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Get detailed technical specs
4. **Check relevant component documentation** - Based on what you need to work on

### If Starting Fresh Rebuild
Follow this sequence:
1. Read [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) completely
2. Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) step-by-step
3. Refer to component-specific READMEs as needed
4. Use [PROGRESS.md](PROGRESS.md) to understand deviations and known issues

### If Debugging Issues
1. Check [PROGRESS.md](PROGRESS.md) - Known Issues section
2. Review relevant component README (daemon, web, MQTT)
3. Check service logs: `sudo journalctl -u [service-name] -n 50`
4. Test device connectivity: `./manage_daemon.sh check-device`

### If Adding Features
1. Review [PROGRESS.md](PROGRESS.md) - Future Enhancements section
2. Study [mpp-solar-architecture.md](mpp-solar-architecture.md)
3. Check [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for design patterns
4. Update documentation after changes

## 📋 Project Completion Checklist

All phases are complete ✅:
- [x] Phase 1: Core Infrastructure
- [x] Phase 2: Web Interface
- [x] Phase 3: MQTT Integration
- [x] Phase 4: Weather Data Automation
- [x] Phase 5: Enhanced UI/UX
- [x] Phase 6: Documentation

System is **production-ready** and **fully operational**.

## ⚠️ Known Limitations

1. **In-memory storage**: Limited to ~8.3 hours (1000 entries)
2. **No web authentication**: Open access on local network
3. **MQTT stability**: Occasional disconnections (auto-reconnects)
4. **Hardcoded paths**: Requires editing for deployment to different systems
5. **Battery page**: Placeholder for future JK BMS integration

See [PROGRESS.md](PROGRESS.md) for detailed issue tracking and planned fixes.

## 🔐 Security Notes

- **Web interface**: No authentication (localhost/LAN only)
- **MQTT broker**: Basic auth (mqttuser/mqtt123), localhost-only
- **USB device**: Requires udev rule for non-root access
- **Services**: Run as user `constantine` (not root)

For production deployment, consider:
- Adding web authentication (Flask-Login)
- Implementing TLS/SSL for MQTT and web
- Network firewall rules
- Stronger MQTT credentials

## 📞 Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Web interface won't start | Check venv activated, device permissions |
| No inverter data | Check daemon service, device connection |
| No house/weather data | Check MQTT broker, check weather service |
| Charts not loading | Check browser console, verify API endpoints |
| Service won't start | Check logs: `sudo journalctl -u [service]` |
| Permission denied | Check udev rules, dialout group membership |

Full troubleshooting in [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting).

## 📈 Performance Metrics

- **CPU Usage**: <1% (all services combined)
- **Memory Usage**: ~100MB total
- **Disk I/O**: <1MB/day (Prometheus files)
- **Network**: Negligible (local only)
- **Web Response**: <100ms for API calls
- **Update Frequency**: 30s (web), 60s (daemon), 600s (weather)

## 🔄 Maintenance Schedule

- **Daily**: Check web interface accessibility
- **Weekly**: Review service logs for errors
- **Monthly**: Verify Prometheus file disk usage, update documentation
- **Quarterly**: Update Python dependencies
- **Annually**: System review and planning

## 📝 Development History

- **Aug 25, 2025**: Project initiated, core infrastructure completed
- **Aug 26, 2025**: Web interface operational
- **Sep 16-30, 2025**: MQTT integration completed
- **Oct 7, 2025**: UI enhancements finalized
- **Oct 26, 2025**: Weather automation deployed
- **Oct 28, 2025**: Comprehensive documentation completed

**Total Development Time**: ~2 months  
**Current Version**: 1.0 (Production)

## 🎓 Technology Stack Summary

**Backend**:
- Python 3.11+ (programming language)
- Flask 3.1.2 (web framework)
- mppsolar (inverter communication library)
- paho-mqtt 1.6.1 (MQTT client)
- requests (HTTP client)

**Frontend**:
- HTML5/CSS3
- Bootstrap 5 (responsive framework)
- Chart.js (data visualization)
- JavaScript ES6+
- Font Awesome (icons)

**Infrastructure**:
- Debian Linux
- systemd (service management)
- Mosquitto (MQTT broker)
- USB HIDRAW (hardware interface)

**Data Storage**:
- In-memory circular buffer (1000 entries)
- Prometheus format files (.prom)
- Log files (.log)

## 🌐 API Endpoints Reference

```
GET  /                      # Main dashboard
GET  /lcars                 # LCARS themed dashboard
GET  /charts                # Historical charts
GET  /charts/lcars          # LCARS themed charts
GET  /house                 # House sensors dashboard
GET  /battery               # Battery monitoring (placeholder)

GET  /api/data              # Current inverter data (JSON)
GET  /api/historical        # Historical data (query: hours)
POST /api/command           # Execute inverter command
GET  /api/refresh           # Force data refresh
GET  /api/house             # House sensor data (JSON)
```

## 📧 MQTT Topics Reference

### House Sensors (Subscribe)
- `house/temperature` - House temperature in °C or °F
- `house/humidity` - House humidity percentage
- `house/pressure` - Barometric pressure
- `house/{sensor_name}` - Any custom sensor

### Weather Data (Subscribe)
- `weather/temperature` - External temperature
- `weather/humidity` - External humidity
- `weather/wind_speed` - Wind speed
- `weather/wind_direction` - Wind direction
- `weather/rain` - Precipitation
- `weather/pressure` - Atmospheric pressure

### Battery Data (Reserved for future)
- `battery/#` - Battery cell data from JK BMS

## 💡 Pro Tips

1. **Context Recovery**: Always read this file + PROGRESS.md + IMPLEMENTATION_PLAN.md
2. **Debugging**: Check service logs first, then device connectivity
3. **Configuration Changes**: Update both the file and the documentation
4. **Adding Sensors**: Just publish to MQTT topic `house/{name}`, auto-detected
5. **Backup**: Copy `/home/constantine/mpp-solar/` excluding `venv/` and `prometheus/`
6. **Dependencies**: Always use virtual environment: `source venv/bin/activate`

## 🎯 Critical Files to Backup

Priority 1 (Configuration):
- `mpp-solar.conf`
- `web.yaml`
- `weather_fetcher.py`
- `/etc/udev/rules.d/99-mpp-solar.rules`
- `/etc/systemd/system/mpp-solar-*.service`
- `/etc/systemd/system/weather-fetcher.service`

Priority 2 (Application):
- `web_interface.py`
- `templates/*.html`
- `static/*` (if customized)

Priority 3 (Documentation):
- All *.md files
- `docs/` directory

**Do NOT backup**:
- `venv/` (recreate with requirements)
- `prometheus/` (historical data, large)
- `__pycache__/` (generated files)

## ✅ Verification Commands

After context reset or system changes, verify:

```bash
# 1. Check services are running
systemctl status mpp-solar-daemon weather-fetcher mosquitto

# 2. Verify device access
ls -la /dev/hidraw0
groups constantine | grep dialout

# 3. Test inverter communication
source /home/constantine/mpp-solar/venv/bin/activate
cd /home/constantine/mpp-solar
python -c "from mppsolar import get_device_class; \
  device = get_device_class('mppsolar')('hidraw', '/dev/hidraw0', 2400); \
  print(device.run_command('QID'))"

# 4. Check web interface
curl -s http://localhost:5000/api/data | python -m json.tool

# 5. Test MQTT
mosquitto_pub -h localhost -p 1883 -u mqttuser -P mqtt123 \
  -t test/topic -m "test"
```

All should complete without errors if system is healthy.

## 📖 Reading Order for New AI Session

**Minimum Context** (Quick tasks):
1. CONTEXT.md (this file)
2. PROGRESS.md (current state)

**Full Context** (Development work):
1. CONTEXT.md (this file)
2. PROGRESS.md (current state)
3. IMPLEMENTATION_PLAN.md (detailed specs)
4. Component-specific README (as needed)

**Fresh Rebuild**:
1. CONTEXT.md (this file)
2. IMPLEMENTATION_PLAN.md (full plan)
3. SETUP_GUIDE.md (step-by-step)
4. mpp-solar-architecture.md (architecture)
5. PROGRESS.md (known issues)

---

**Last Updated**: October 28, 2025  
**Maintainer**: constantine  
**System Location**: /home/constantine/mpp-solar/  
**Documentation Standard**: Following claude_rob.md methodology
