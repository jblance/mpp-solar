# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New `/house` page with real-time house sensor data (temperature, humidity, pressure)
- Weather data integration with OpenWeatherMap API
- Weather fetcher service (`weather_fetcher.py`) for periodic weather updates
- Battery monitoring page with detailed battery metrics
- Historical data loading from Prometheus archives
- Time range filtering (24h, 7d, 30d, All) for charts and data views
- Local storage persistence for user preferences (time range, data retention)
- MQTT support for house sensor data
- Prometheus export to CSV utility (`export_prometheus_to_csv.py`)
- ZeroTier network health monitoring scripts
- Comprehensive documentation in `docs/` directory

### Fixed
- Weather Condition field not showing values on `/house` page
- Chart filtering issues with date ranges
- Historical data loading from archived Prometheus files
- MQTT data retention and display issues
- Time synchronization between different data sources

### Changed
- Organized project documentation into `docs/` and `docs/archive/`
- Consolidated utility scripts into `utils/` directory
- Improved web interface with better error handling
- Enhanced chart rendering with proper time range support

### Improved
- Web interface performance with debounced updates
- Data persistence using browser localStorage
- Error handling and logging across all services
- Prometheus file management and rotation

## Project Structure

```
mpp-solar/
├── mppsolar/          # Core library
├── templates/         # Web interface templates
├── docs/              # Documentation
│   └── archive/       # Development notes
├── utils/             # Utility scripts
├── prometheus/        # Prometheus metric storage
└── tests/             # Test suite
```

## Services

- **mpp-solar-daemon**: Main inverter monitoring service
- **mpp-solar-web**: Web interface (Flask)
- **weather_fetcher**: Weather data collection service

## Documentation

See `docs/DOCUMENTATION_INDEX.md` for a complete guide to all documentation files.
