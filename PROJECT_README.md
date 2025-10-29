# MPP-Solar Monitoring System

This is a customized implementation of the mpp-solar package with added web interface, house monitoring, and weather integration.

## Features

### Core Monitoring
- Real-time inverter/battery monitoring via MPP-Solar protocol
- Prometheus metrics collection and storage
- Historical data archival and retrieval

### Web Interface
- **Dashboard** (`/`): Main inverter metrics and status
- **Charts** (`/charts`): Historical data visualization with time range filtering
- **House** (`/house`): Real-time house sensor data (temperature, humidity, pressure)
- **Battery** (`/battery`): Detailed battery metrics
- **LCARS Theme**: Alternative UI theme (`/lcars`, `/charts/lcars`)

### Data Collection
- **MPP-Solar Daemon**: Continuous inverter data collection
- **Weather Fetcher**: Periodic weather data from OpenWeatherMap
- **House Sensors**: Temperature, humidity, pressure via MQTT

### Data Management
- Prometheus file-based metrics storage
- Automatic data rotation and archival
- CSV export capability for analysis
- Local storage for user preferences

## Quick Start

1. **Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

2. **Configure Services**
   ```bash
   cp mpp-solar.conf.template mpp-solar.conf
   cp web.yaml.template web.yaml
   # Edit configuration files with your settings
   ```

3. **Start Services**
   ```bash
   sudo systemctl start mpp-solar-daemon
   sudo systemctl start mpp-solar-web
   ```

4. **Access Web Interface**
   - Open http://localhost:5000

## Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)**: Detailed installation and configuration
- **[CHANGELOG.md](CHANGELOG.md)**: Recent changes and improvements
- **[docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)**: Complete documentation index
- **[PROMETHEUS_EXPORT_README.md](PROMETHEUS_EXPORT_README.md)**: CSV export utility
- **[ZEROTIER_README.md](ZEROTIER_README.md)**: Network monitoring setup

## Utilities

### Prometheus Export
```bash
python3 export_prometheus_to_csv.py
```

### System Management
```bash
# Located in utils/
./utils/reboot.sh              # System reboot
./utils/log-boot.sh            # Boot logging
./utils/zerotier-health-check.sh  # Network monitoring
./utils/zt-status.sh           # ZeroTier status
```

## Project Structure

```
mpp-solar/
├── mppsolar/              # Core library
├── templates/             # Flask templates
│   ├── dashboard.html
│   ├── charts.html
│   ├── house.html
│   └── battery.html
├── docs/                  # Documentation
│   ├── archive/           # Development notes
│   ├── IMPLEMENTATION_PLAN.md
│   └── PROGRESS.md
├── utils/                 # Utility scripts
├── prometheus/            # Metrics storage
├── tests/                 # Test suite
├── web_interface.py       # Flask application
├── weather_fetcher.py     # Weather service
└── load_prometheus_history.py  # Historical data loader
```

## Services

### mpp-solar-daemon
- Queries inverter at regular intervals
- Writes metrics to Prometheus format files
- Handles device communication errors

### mpp-solar-web
- Flask web server on port 5000
- REST API for metrics retrieval
- Real-time data updates via AJAX

### weather_fetcher
- Fetches weather data from OpenWeatherMap
- Updates every 15 minutes
- Stores in Prometheus format

## Troubleshooting

```bash
# Check service status
sudo systemctl status mpp-solar-daemon
sudo systemctl status mpp-solar-web

# View logs
sudo journalctl -u mpp-solar-daemon -f
sudo journalctl -u mpp-solar-web -f
tail -f web_interface.log
tail -f weather_fetcher.log

# Test device connection
mpp-solar -p /dev/hidraw0 -P PI30 --porttype SERIAL -c QID
```

## Contributing

See upstream project: https://github.com/jblance/mpp-solar

## License

See LICENSE file in repository.
