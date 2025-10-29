# MPP-Solar Monitoring System - Implementation Plan

## Project Overview

The MPP-Solar Monitoring System is a comprehensive solar inverter monitoring and control platform that integrates:
- **MPP-Solar inverter monitoring** via USB HIDRAW interface
- **House sensor data collection** via MQTT (temperature, humidity, pressure)
- **Weather data integration** from Open-Meteo API
- **Web-based dashboards** for real-time monitoring and historical visualization
- **Multiple UI themes** including standard Bootstrap and LCARS (Star Trek themed) interfaces
- **Data persistence** using Prometheus format files and in-memory storage
- **RESTful API** for programmatic access and third-party integration

### System Architecture
The system consists of several interconnected components:
1. **Hardware Layer**: MPP-Solar inverter connected via USB HIDRAW device
2. **Data Collection Layer**: Daemon service, weather fetcher, MQTT broker
3. **Application Layer**: Flask web server with background data collection threads
4. **Storage Layer**: In-memory store, Prometheus files, log files
5. **Presentation Layer**: Web UI with multiple dashboard views and charts

## Objectives and Milestones

### Phase 1: Core Infrastructure ✅ COMPLETED
**Objective**: Establish base MPP-Solar monitoring capabilities
- Install and configure mpp-solar Python package
- Set up USB HIDRAW device communication
- Configure inverter protocol (PI30) and communication parameters
- Create systemd service for daemon-based data collection
- Implement Prometheus file format output for metrics

**Success Criteria**:
- Daemon successfully queries inverter every 60 seconds
- Prometheus files generated in correct format
- Service auto-starts on system boot
- Data includes: battery voltage, AC output, power, temperature

### Phase 2: Web Interface ✅ COMPLETED
**Objective**: Provide real-time web-based monitoring
- Flask web application with RESTful API endpoints
- Real-time dashboard showing current inverter status
- Command interface for direct inverter control
- Historical data visualization using Chart.js
- Background thread for continuous data collection (30s interval)
- In-memory data store (1000 entries, ~8.3 hours of data)

**Success Criteria**:
- Web interface accessible at http://IP:5000
- Dashboard updates automatically every 30 seconds
- Historical charts display data from past 24+ hours
- Users can execute commands and see responses
- API endpoints return valid JSON data

### Phase 3: MQTT Integration ✅ COMPLETED
**Objective**: Enable external sensor data integration
- Install and configure Mosquitto MQTT broker
- Implement MQTT client in web_interface.py
- Subscribe to house/# and weather/# topics
- Parse and store sensor data in global dictionaries
- Create dedicated house sensors dashboard
- Generate Prometheus files for house sensors

**Success Criteria**:
- MQTT broker running on localhost:1883
- Web interface successfully connects to MQTT broker
- House sensor data received and displayed
- Weather data received and displayed
- House dashboard accessible at /house
- Prometheus files generated for house metrics

### Phase 4: Weather Data Automation ✅ COMPLETED
**Objective**: Automate external weather data collection
- Create weather_fetcher.py script
- Integrate with Open-Meteo API (free, no API key required)
- Publish weather data to MQTT every 10 minutes
- Create systemd service for weather fetcher
- Configure location-specific weather data (Pittsfield, VT)

**Success Criteria**:
- Weather fetcher service runs continuously
- Weather data published to MQTT topics
- Data includes: temperature, humidity, wind, rain, pressure
- Service auto-starts on boot and restarts on failure
- Weather data visible in house dashboard

### Phase 5: Enhanced UI/UX ✅ COMPLETED
**Objective**: Provide multiple interface themes and improved visualization
- LCARS themed dashboard (Star Trek UI)
- LCARS themed charts interface
- Battery monitoring page (for future JK BMS integration)
- Responsive design for mobile/tablet access
- Multiple chart types (line, area, bar)
- Date range selectors for historical data

**Success Criteria**:
- LCARS dashboard accessible at /lcars
- LCARS charts accessible at /charts/lcars
- Standard charts accessible at /charts
- Battery page accessible at /battery
- All interfaces responsive on mobile devices
- Charts properly render 24h, 7d, 30d data ranges

## Technical Implementation Details

### Hardware Configuration
```
Device: MPP-Solar Inverter
Connection: USB HIDRAW (/dev/hidraw0)
Protocol: PI30
Baud Rate: 2400
Port Type: hidraw
Vendor ID: 0665
Product ID: 5161
```

### Software Stack
**Backend**:
- Python 3.11+
- Flask 3.1.2 (web framework)
- mppsolar library (inverter communication)
- paho-mqtt 1.6.1 (MQTT client)
- requests (HTTP client for weather API)

**Frontend**:
- HTML5/CSS3
- Bootstrap 5 (responsive framework)
- Chart.js (data visualization)
- JavaScript ES6+ (interactivity)
- Font Awesome (icons)
- date-fns (date manipulation)

**Services**:
- Mosquitto MQTT Broker
- systemd services (mpp-solar-daemon, weather-fetcher, mpp-solar-web)

### File Structure
```
/home/constantine/mpp-solar/
├── venv/                          # Python virtual environment
├── mppsolar/                      # mpp-solar library source
├── templates/                     # Flask HTML templates
│   ├── dashboard.html            # Main dashboard
│   ├── dashboard_lcars.html      # LCARS themed dashboard
│   ├── charts.html               # Standard charts
│   ├── charts_lcars.html         # LCARS charts
│   ├── house.html                # House sensors dashboard
│   └── battery.html              # Battery monitoring
├── static/                        # Static assets (CSS, JS, images)
├── prometheus/                    # Prometheus format metrics files
├── docs/                          # Additional documentation
├── web_interface.py               # Main Flask application
├── weather_fetcher.py             # Weather data collector
├── mpp-solar.conf                 # Daemon configuration
├── web.yaml                       # Web interface configuration
├── manage_daemon.sh               # Daemon management script
├── manage_web.sh                  # Web interface management script
├── mpp-solar-daemon.service       # systemd service (daemon)
├── mpp-solar-web.service          # systemd service (web)
├── weather-fetcher.service        # systemd service (weather)
└── [documentation files]          # Various README and guide files
```

### Configuration Files

#### mpp-solar.conf
```ini
[SETUP]
pause = 60                    # Query interval (seconds)
mqtt_broker = localhost
mqtt_port = 1883
log_file = /home/constantine/mpp-solar/mpp-solar.log

[inverter]
protocol = pi30
type = mppsolar
port = /dev/hidraw0
porttype = hidraw
baud = 2400
command = QPIGS              # Query general status
tag = inverter
outputs = screen,json,prom_file
prom_output_dir = /home/constantine/mpp-solar/prometheus
dev = main_inverter
```

#### web.yaml
```yaml
host: "0.0.0.0"              # Listen on all interfaces
port: 5000
log_level: "info"
```

#### weather_fetcher.py (Configuration Section)
```python
LOCATION = {
    'latitude': 43.7776,
    'longitude': -72.8145,
    'name': 'Pittsfield, Vermont'
}
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_USERNAME = "mqttuser"
MQTT_PASSWORD = "mqtt123"
FETCH_INTERVAL = 600          # 10 minutes
```

### Data Flow

#### Inverter Data Collection
1. **Daemon Service** (every 60s):
   - Executes QPIGS command via USB HIDRAW
   - Receives status data from inverter
   - Writes to Prometheus files in /prometheus/
   - Logs to mpp-solar.log

2. **Web Interface** (every 30s):
   - Background thread reads Prometheus files
   - Parses metrics into structured data
   - Stores in in-memory circular buffer (1000 entries)
   - Updates inverter_data global variable

#### House Sensor Data Flow
1. External sensor device publishes to MQTT:
   - Topic format: `house/{sensor_name}`
   - Payload: Float value (e.g., "23.5")
2. Web interface MQTT client receives message
3. Stores in house_data dictionary with timestamp
4. Writes to Prometheus file for persistence
5. Displayed on /house dashboard

#### Weather Data Flow
1. Weather fetcher service (every 10 minutes):
   - Queries Open-Meteo API
   - Receives current weather data
   - Publishes to MQTT topics (weather/*)
2. Web interface receives via MQTT
3. Stores in weather_data dictionary
4. Displayed on house dashboard

### API Endpoints

```
GET  /                      # Main dashboard
GET  /lcars                 # LCARS themed dashboard
GET  /charts                # Historical charts
GET  /charts/lcars          # LCARS themed charts
GET  /house                 # House sensors dashboard
GET  /battery               # Battery monitoring page

GET  /api/data              # Current inverter data (JSON)
GET  /api/historical        # Historical data (query params: hours)
POST /api/command           # Execute inverter command
GET  /api/refresh           # Force data refresh
GET  /api/house             # House sensor data (JSON)
```

### systemd Services

#### mpp-solar-daemon.service
- Runs mpp-solar in daemon mode
- Queries inverter every 60 seconds
- Writes Prometheus files
- Auto-restarts on failure
- Starts after USB devices are available

#### weather-fetcher.service
- Runs weather_fetcher.py
- Fetches weather every 10 minutes
- Publishes to MQTT
- Auto-restarts on failure
- Starts after network and MQTT broker

#### mpp-solar-web.service (optional)
- Runs Flask web interface as service
- Enables auto-start on boot
- Manages web server lifecycle

### Security Configuration

#### Device Permissions
- udev rule: `/etc/udev/rules.d/99-mpp-solar.rules`
- Sets USB device permissions (MODE="0666")
- Allows non-root access to HIDRAW device

#### User Groups
- User added to `dialout` group for serial/USB access

#### MQTT Security
- Basic authentication (mqttuser/mqtt123)
- Localhost-only broker (no external access)
- Can be enhanced with TLS/SSL for production

## Development Cycles

### Cycle 1: Base System Setup ✅
- Install Debian Linux
- Install Python 3.11+
- Clone mpp-solar repository
- Create virtual environment
- Install mpp-solar package
- Configure USB device permissions

### Cycle 2: Daemon Configuration ✅
- Create mpp-solar.conf from template
- Configure inverter communication parameters
- Test device connectivity
- Set up systemd service
- Verify Prometheus file generation

### Cycle 3: Web Interface Development ✅
- Develop Flask application structure
- Implement API endpoints
- Create dashboard HTML templates
- Integrate Chart.js for visualization
- Implement background data collection thread
- Set up in-memory data storage

### Cycle 4: MQTT Integration ✅
- Install Mosquitto broker
- Configure MQTT authentication
- Implement MQTT client in web_interface.py
- Create house sensor data handlers
- Develop house dashboard template
- Test with manual MQTT publishes

### Cycle 5: Weather Automation ✅
- Develop weather_fetcher.py script
- Integrate Open-Meteo API
- Implement MQTT publishing
- Create systemd service
- Configure location settings
- Test and verify data flow

### Cycle 6: UI Enhancements ✅
- Design LCARS theme CSS
- Create LCARS dashboard template
- Develop LCARS charts interface
- Implement responsive design
- Add multiple chart types
- Create battery monitoring page

### Cycle 7: Documentation and Refinement ✅
- Write README files for each component
- Create setup guides
- Document architecture
- Write troubleshooting guides
- Create management scripts
- Document MQTT topics and formats

## Criteria for Success

### System Requirements
- [ ] System runs on Debian Linux
- [ ] Python 3.11+ installed
- [ ] All dependencies installed in virtual environment
- [ ] USB device accessible and configured

### Daemon Service
- [ ] mpp-solar-daemon.service enabled and running
- [ ] Inverter queried every 60 seconds
- [ ] Prometheus files generated correctly
- [ ] Service auto-restarts on failure
- [ ] Logs written to mpp-solar.log

### Web Interface
- [ ] Flask application accessible on port 5000
- [ ] Dashboard shows real-time data
- [ ] Data updates every 30 seconds
- [ ] Command interface functional
- [ ] Historical charts display correctly
- [ ] API endpoints return valid JSON

### MQTT System
- [ ] Mosquitto broker running on localhost:1883
- [ ] Authentication configured
- [ ] Web interface connects to broker
- [ ] House sensor data received and displayed
- [ ] Weather data received and displayed

### Weather Service
- [ ] weather-fetcher.service running
- [ ] Weather data fetched every 10 minutes
- [ ] Data published to MQTT correctly
- [ ] Service auto-restarts on failure

### User Interface
- [ ] Multiple dashboard themes available
- [ ] Responsive design works on mobile
- [ ] Charts render correctly
- [ ] All pages accessible and functional
- [ ] Navigation works properly

### Documentation
- [ ] Setup guide complete and accurate
- [ ] Architecture documented
- [ ] API endpoints documented
- [ ] Troubleshooting guide available
- [ ] Configuration examples provided
- [ ] CONTEXT.md provides full system overview

## Known Limitations and Future Enhancements

### Current Limitations
1. In-memory storage limited to ~8.3 hours (1000 entries)
2. No long-term historical database (only Prometheus files)
3. No authentication on web interface
4. MQTT authentication is basic (username/password only)
5. No alerting/notification system
6. Battery monitoring page placeholder (awaits JK BMS integration)

### Planned Enhancements
1. PostgreSQL or InfluxDB for long-term data storage
2. User authentication and role-based access control
3. Email/SMS alerting for critical events
4. Mobile app development
5. JK BMS integration for battery cell monitoring
6. Grafana dashboards integration
7. Prometheus server integration
8. Additional sensor types (solar panels, battery bank)
9. Energy production/consumption analytics
10. Export data to CSV/Excel
