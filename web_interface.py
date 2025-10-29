#!/usr/bin/env python3
"""
MPP-Solar Web Interface
A simple web interface for monitoring and controlling MPP-Solar inverters
"""

import os
import sys
import json
import time
import logging
import glob
import re
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, redirect, url_for
import threading
import paho.mqtt.client as mqtt

# Add the mppsolar package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mppsolar'))

from mppsolar import get_device_class
from mppsolar.libs.mqttbroker_legacy import MqttBroker


def parse_prometheus_file_with_timestamp(file_path):
    """Parse a Prometheus file and extract metrics with file modification time as timestamp"""
    data = {}
    try:
        # Get file modification time as timestamp
        file_mtime = os.path.getmtime(file_path)
        timestamp = datetime.fromtimestamp(file_mtime).isoformat()
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Parse each metric line
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Parse Prometheus metric format: metric_name{labels} value
                if '{' in line and '}' in line:
                    metric_part = line.split('{')[0]
                    value_part = line.split('}')[1].strip()
                    
                    try:
                        value = float(value_part)
                        data[metric_part] = value
                    except ValueError:
                        continue
        
        # Add timestamp to the data
        if data:
            data['timestamp'] = timestamp
                        
    except Exception as e:
        logging.error(f"Error parsing Prometheus file {file_path}: {e}")
    
    return data

def load_historical_prometheus_data(prometheus_dir, max_entries=1000):
    load_historical_house_weather_data(prometheus_dir, max_entries_per_sensor=2100)
    """Load historical data from Prometheus files on startup"""
    global historical_data_store
    
    logging.info("Loading historical data from Prometheus files...")
    
    try:
        # Get all qpigs .prom files
        prom_files = glob.glob(os.path.join(prometheus_dir, "mpp-solar-inverter-qpigs*.prom"))
        
        # Sort by modification time (oldest first)
        prom_files.sort(key=lambda x: os.path.getmtime(x))
        
        # Take the last max_entries files
        prom_files = prom_files[-max_entries:] if len(prom_files) > max_entries else prom_files
        
        loaded_count = 0
        for file_path in prom_files:
            data = parse_prometheus_file_with_timestamp(file_path)
            if data and 'timestamp' in data:
                historical_data_store.append(data)
                loaded_count += 1
        
        logging.info(f"Loaded {loaded_count} historical entries from Prometheus files")
        if historical_data_store:
            logging.info(f"Historical data spans from {historical_data_store[0]['timestamp']} to {historical_data_store[-1]['timestamp']}")
                        
    except Exception as e:
        logging.error(f"Error loading historical Prometheus data: {e}")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Global variables
inverter_data = {}
last_update = None
device = None
historical_data_store = []
battery_data = {}  # Store battery cell data
house_data = {}  # Store house sensor data
weather_data = {}  # Store weather data
house_historical_data = {}  # Store historical house sensor data
weather_historical_data = {}  # Store historical weather data


def load_historical_house_weather_data(prometheus_dir, max_entries_per_sensor=500):
    """Load historical house and weather data from Prometheus files on startup"""
    global house_historical_data, weather_historical_data
    
    logging.info("Loading historical house and weather data from Prometheus files...")
    
    try:
        # House sensors: temperature, humidity, pressure
        house_sensors = ['temperature', 'humidity', 'pressure']
        for sensor in house_sensors:
            pattern = os.path.join(prometheus_dir, f"house-{sensor}-*.prom")
            prom_files = glob.glob(pattern)
            
            # Sort by modification time (oldest first)
            prom_files.sort(key=lambda x: os.path.getmtime(x))
            
            # Take the last max_entries files
            prom_files = prom_files[-max_entries_per_sensor:] if len(prom_files) > max_entries_per_sensor else prom_files
            
            house_historical_data[sensor] = []
            for file_path in prom_files:
                # Extract timestamp from filename: house-{sensor}-YYYYMMDD_HHMMSS.prom
                filename = os.path.basename(file_path)
                timestamp_str = filename.split('-')[-1].replace('.prom', '')
                try:
                    # Parse timestamp: 20251029_144910
                    timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                except:
                    # Fallback to file mtime
                    timestamp = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                # Read value from file
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            if line.startswith(f'house_{sensor}'):
                                # Parse: house_temperature{sensor="temperature"} 17.61
                                value = float(line.split()[-1])
                                house_historical_data[sensor].append({
                                    'timestamp': timestamp.isoformat(),
                                    'value': value
                                })
                                break
                except Exception as e:
                    logging.debug(f"Error parsing {file_path}: {e}")
                    continue
        
        # Weather sensors: temperature, humidity, pressure, wind_speed, wind_direction, rain
        weather_sensors = ['temperature', 'humidity', 'pressure', 'wind_speed', 'wind_direction', 'rain']
        for sensor in weather_sensors:
            pattern = os.path.join(prometheus_dir, f"weather-{sensor}-*.prom")
            prom_files = glob.glob(pattern)
            
            # Sort by modification time (oldest first)
            prom_files.sort(key=lambda x: os.path.getmtime(x))
            
            # Take the last max_entries files
            prom_files = prom_files[-max_entries_per_sensor:] if len(prom_files) > max_entries_per_sensor else prom_files
            
            weather_historical_data[sensor] = []
            for file_path in prom_files:
                # Extract timestamp from filename
                filename = os.path.basename(file_path)
                timestamp_str = filename.split('-')[-1].replace('.prom', '')
                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                except:
                    timestamp = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                # Read value from file
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            if line.startswith(f'weather_{sensor}'):
                                # Parse: weather_temperature{sensor="temperature"} 15.3
                                value = float(line.split()[-1])
                                weather_historical_data[sensor].append({
                                    'timestamp': timestamp.isoformat(),
                                    'value': value
                                })
                                break
                except Exception as e:
                    logging.debug(f"Error parsing {file_path}: {e}")
                    continue
        
        # Log summary
        house_count = sum(len(v) for v in house_historical_data.values())
        weather_count = sum(len(v) for v in weather_historical_data.values())
        logging.info(f"Loaded {house_count} house data points and {weather_count} weather data points")
        
    except Exception as e:
        logging.error(f"Error loading historical house/weather data: {e}")

def get_inverter_data():
    """Get data from the inverter - reads from Prometheus files written by daemon"""
    global inverter_data, last_update, device, historical_data_store
    
    try:
        # Read from Prometheus file (updated by daemon every 60 seconds)
        prom_file = "/home/constantine/mpp-solar/prometheus/mpp-solar-inverter-qpigs.prom"
        prom_data = {}
        
        with open(prom_file, 'r') as f:
            import re
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    match = re.match(r'([a-z_]+)\{([^}]+)\}\s+([\d.]+)', line)
                    if match:
                        metric_name = match.group(1)
                        value = float(match.group(3))
                        prom_data[metric_name] = value
        
        # Convert Prometheus format back to status format for compatibility
        status = {
            'Battery Voltage': [prom_data.get('mpp_solar_battery_voltage', 0), 'V'],
            'AC Output Voltage': [prom_data.get('mpp_solar_ac_output_voltage', 0), 'V'],
            'AC Input Voltage': [prom_data.get('mpp_solar_ac_input_voltage', 0), 'V'],
            'AC Output Active Power': [int(prom_data.get('mpp_solar_ac_output_active_power', 0)), 'W'],
            'AC Output Apparent Power': [int(prom_data.get('mpp_solar_ac_output_apparent_power', 0)), 'VA'],
            'AC Output Load': [int(prom_data.get('mpp_solar_ac_output_load', 0)), '%'],
            'Inverter Heat Sink Temperature': [int(prom_data.get('mpp_solar_inverter_heat_sink_temperature', 0)), '°C'],
            'Battery Charging Current': [int(prom_data.get('mpp_solar_battery_charging_current', 0)), 'A'],
            'Battery Discharge Current': [int(prom_data.get('mpp_solar_battery_discharge_current', 0)), 'A'],
            'Battery Capacity': [int(prom_data.get('mpp_solar_battery_capacity', 0)), '%'],
            'Is Charging On': [int(prom_data.get('mpp_solar_is_charging_on', 0)), 'bool'],
            'Is Switched On': [int(prom_data.get('mpp_solar_is_switched_on', 0)), 'bool'],
            'Is Load On': [int(prom_data.get('mpp_solar_is_load_on', 0)), 'bool'],
            'AC Output Frequency': [prom_data.get('mpp_solar_ac_output_frequency', 0), 'Hz'],
            'AC Input Frequency': [prom_data.get('mpp_solar_ac_input_frequency', 0), 'Hz'],
            'BUS Voltage': [int(prom_data.get('mpp_solar_bus_voltage', 0)), 'V'],
            'Battery Voltage from SCC': [prom_data.get('mpp_solar_battery_voltage_from_scc', 0), 'V'],
            'PV Input Voltage': [prom_data.get('mpp_solar_pv_input_voltage', 0), 'V'],
            'PV Input Current for Battery': [prom_data.get('mpp_solar_pv_input_current_for_battery', 0), 'A'],
            'PV Input Power': [int(prom_data.get('mpp_solar_pv_input_power', 0)), 'W'],
            'Is SCC Charging On': [int(prom_data.get('mpp_solar_is_scc_charging_on', 0)), 'bool'],
        }
        
        # For settings/mode/flags, query device only once at startup if needed
        if 'settings' not in inverter_data:
            if device is None:
                device_class = get_device_class("mppsolar")
                device = device_class(
                    name="inverter",
                    port="/dev/hidraw0",
                    protocol="pi30",
                    porttype="hidraw",
                    mqtt_broker=MqttBroker(config={"name": "localhost", "port": 1883})
                )
            settings = device.run_command(command="QPIRI")
            mode = device.run_command(command="QMOD")
            flags = device.run_command(command="QFLAG")
        else:
            settings = inverter_data.get('settings', {})
            mode = inverter_data.get('mode', {})
            flags = inverter_data.get('flags', {})
        
        inverter_data = {
            'status': status,
            'settings': settings,
            'mode': mode,
            'flags': flags,
            'timestamp': datetime.now().isoformat()
        }
        last_update = datetime.now()
        
        # Store historical data for charts
        if isinstance(status, dict) and 'Battery Voltage' in status:
            # Convert to Prometheus-like format for charts
            timestamp = datetime.now().isoformat()
            print(f"DEBUG: Storing historical data at {timestamp}")
            historical_entry = {
                'timestamp': timestamp,
                'mpp_solar_battery_voltage': status.get('Battery Voltage', [0])[0] if isinstance(status.get('Battery Voltage'), list) else 0,
                'mpp_solar_ac_output_voltage': status.get('AC Output Voltage', [0])[0] if isinstance(status.get('AC Output Voltage'), list) else 0,
                'mpp_solar_ac_input_voltage': status.get('AC Input Voltage', [0])[0] if isinstance(status.get('AC Input Voltage'), list) else 0,
                'mpp_solar_ac_output_active_power': status.get('AC Output Active Power', [0])[0] if isinstance(status.get('AC Output Active Power'), list) else 0,
                'mpp_solar_ac_output_apparent_power': status.get('AC Output Apparent Power', [0])[0] if isinstance(status.get('AC Output Apparent Power'), list) else 0,
                'mpp_solar_ac_output_load': status.get('AC Output Load', [0])[0] if isinstance(status.get('AC Output Load'), list) else 0,
                'mpp_solar_inverter_heat_sink_temperature': status.get('Inverter Heat Sink Temperature', [0])[0] if isinstance(status.get('Inverter Heat Sink Temperature'), list) else 0,
                'mpp_solar_battery_charging_current': status.get('Battery Charging Current', [0])[0] if isinstance(status.get('Battery Charging Current'), list) else 0,
                'mpp_solar_battery_discharge_current': status.get('Battery Discharge Current', [0])[0] if isinstance(status.get('Battery Discharge Current'), list) else 0,
                'mpp_solar_is_charging_on': status.get('Is Charging On', [0])[0] if isinstance(status.get('Is Charging On'), list) else 0,
                'mpp_solar_is_switched_on': status.get('Is Switched On', [0])[0] if isinstance(status.get('Is Switched On'), list) else 0,
                'mpp_solar_is_load_on': status.get('Is Load On', [0])[0] if isinstance(status.get('Is Load On'), list) else 0,
                'mpp_solar_battery_capacity': status.get('Battery Capacity', [0])[0] if isinstance(status.get('Battery Capacity'), list) else 0
            }
            
            # Add to historical store (keep last 1000 entries)
            historical_data_store.append(historical_entry)
            if len(historical_data_store) > 1000:
                historical_data_store.pop(0)
        
    except Exception as e:
        logging.error(f"Error getting inverter data: {e}")
        inverter_data = {'error': str(e)}

def parse_prometheus_file(file_path):
    """Parse a Prometheus file and extract metrics with timestamps"""
    data = {}
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Try to extract timestamp from filename first (format: mpp-solar-inverter-qpigs-YYYYMMDD_HHMMSS.prom)
        timestamp = None
        filename = os.path.basename(file_path)
        if '-qpigs-' in filename and '.prom' in filename:
            try:
                # Extract timestamp from filename like: mpp-solar-inverter-qpigs-20250825_221548.prom
                timestamp_str = filename.split('-qpigs-')[1].replace('.prom', '')
                if '_' in timestamp_str:
                    date_part, time_part = timestamp_str.split('_')
                    timestamp = datetime.strptime(f"{date_part}_{time_part}", "%Y%m%d_%H%M%S")
            except (ValueError, IndexError):
                pass
        
        # Fall back to file modification time if filename parsing fails
        if timestamp is None:
            file_mtime = os.path.getmtime(file_path)
            timestamp = datetime.fromtimestamp(file_mtime)
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Parse Prometheus metric format: metric_name{labels} value
                if '{' in line and '}' in line:
                    # Extract metric name, labels, and value
                    metric_part = line.split('{')[0]
                    labels_part = line.split('{')[1].split('}')[0]
                    value_part = line.split('}')[1].strip()
                    
                    try:
                        value = float(value_part)
                        data[metric_part] = {
                            'value': value,
                            'timestamp': timestamp.isoformat(),
                            'labels': labels_part
                        }
                    except ValueError:
                        continue
                        
    except Exception as e:
        logging.error(f"Error parsing Prometheus file {file_path}: {e}")
    
    return data

def update_data_thread():
    """Background thread to update inverter data every 30 seconds"""
    while True:
        try:
            get_inverter_data()
            logging.info("Updated inverter data from Prometheus files")
        except Exception as e:
            logging.error(f"Error in update thread: {e}")
        time.sleep(30)  # Update every 30 seconds

def get_historical_data(hours=24):
    """Get historical data from in-memory store for the last N hours"""
    global historical_data_store
    
    try:
        # Get current time and cutoff time
        now = datetime.now()
        cutoff_time = now - timedelta(hours=hours)
        
        # Transform data from list of entries to metric-keyed dictionary
        # Input format: [{timestamp: 'X', metric1: val1, metric2: val2}, ...]
        # Output format: {metric1: [{timestamp: 'X', value: val1}, ...], metric2: [...]}
        historical_data = {}
        
        for entry in historical_data_store:
            try:
                entry_time = datetime.fromisoformat(entry['timestamp'])
                if entry_time >= cutoff_time:
                    timestamp = entry['timestamp']
                    # Process each metric in the entry (skip timestamp itself)
                    for key, value in entry.items():
                        if key != 'timestamp':
                            if key not in historical_data:
                                historical_data[key] = []
                            historical_data[key].append({
                                'timestamp': timestamp,
                                'value': value
                            })
            except (KeyError, ValueError) as e:
                logging.error(f"Error processing historical entry: {e}")
                continue
        
        return historical_data
            
    except Exception as e:
        logging.error(f"Error getting historical data: {e}")
        return {}

# Background thread removed - using daemon for data collection

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/lcars')
def dashboard_lcars():
    """LCARS themed dashboard page"""
    return render_template('dashboard_lcars.html')

@app.route('/charts')
def charts():
    """Charts page with line graphs"""
    return render_template('charts.html')

@app.route('/charts/lcars')
def charts_lcars():
    """Charts page with Star Trek LCARS theme"""
    return render_template('charts_lcars.html')

@app.route('/api/data')
def api_data():
    """API endpoint to get current data"""
    return jsonify(inverter_data)

@app.route('/api/historical')
def api_historical():
    """API endpoint to get historical data"""
    hours = request.args.get('hours', 24, type=int)
    data = get_historical_data(hours)
    return jsonify(data)

@app.route('/api/historical/all')
def api_historical_all():
    """API endpoint for all available historical data"""
    data = get_historical_data(hours=8760)  # 1 year
    return jsonify(data)

@app.route('/api/command', methods=['POST'])
def api_command():
    """API endpoint to execute commands"""
    try:
        command = request.json.get('command')
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        if device is None:
            return jsonify({'error': 'Device not initialized'}), 500
        
        result = device.run_command(command=command)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh')
def api_refresh():
    """API endpoint to manually refresh data"""
    get_inverter_data()
    return jsonify({'status': 'Data refreshed', 'timestamp': last_update.isoformat() if last_update else None})

@app.route('/house')
def house_dashboard():
    """House monitoring dashboard"""
    return render_template('house.html')

@app.route('/api/house')
def api_house():
    """API endpoint to get house sensor data"""
    return jsonify(house_data)

@app.route('/api/weather')
def api_weather():
    """API endpoint to get weather data"""
    return jsonify(weather_data)


@app.route('/api/house_historical')
def api_house_historical():
    """Return historical house and weather data"""
    global house_historical_data, weather_historical_data
    
    # Combine house and weather data with clear naming
    result = {
        'house_temperature': house_historical_data.get('temperature', []),
        'house_humidity': house_historical_data.get('humidity', []),
        'house_pressure': house_historical_data.get('pressure', []),
        'weather_temperature': weather_historical_data.get('temperature', []),
        'weather_humidity': weather_historical_data.get('humidity', []),
        'weather_pressure': weather_historical_data.get('pressure', []),
        'weather_wind_speed': weather_historical_data.get('wind_speed', []),
        'weather_wind_direction': weather_historical_data.get('wind_direction', []),
        'weather_rain': weather_historical_data.get('rain', [])
    }
    
    return jsonify(result)

@app.route('/battery')
def battery_dashboard():
    """Battery monitoring dashboard"""
    return render_template('battery.html')

@app.route('/api/battery')
def api_battery():
    """API endpoint to get battery cell data"""
    return jsonify(battery_data)

def on_mqtt_connect(client, userdata, flags, rc):
    """Callback for when the MQTT client connects"""
    if rc == 0:
        logging.info("Connected to MQTT broker")
        client.subscribe("battery/#")
        client.subscribe("house/#")
        client.subscribe("weather/#")
        logging.info("Subscribed to battery/#, house/# and weather/# topics")
    else:
        logging.error(f"Failed to connect to MQTT broker: {rc}")

def on_mqtt_message(client, userdata, msg):
    """Callback for when an MQTT message is received"""
    global battery_data, house_data, weather_data
    try:
        # Parse topic: battery/status/bank/cell
        parts = msg.topic.split('/')
        
        if len(parts) == 4 and parts[0] == 'battery' and parts[1] == 'status':
            bank = int(parts[2])
            cell = int(parts[3])
            data = json.loads(msg.payload.decode('utf-8'))

            # Store in hierarchical structure
            if bank not in battery_data:
                battery_data[bank] = {}
            battery_data[bank][cell] = {
                **data,
                'timestamp': datetime.now().isoformat()
            }
        
        # Handle house sensor data: house/sensor_name
        elif len(parts) == 2 and parts[0] == 'house':
            sensor_name = parts[1]
            try:
                value = float(msg.payload.decode('utf-8'))
                house_data[sensor_name] = value
                house_data[f'{sensor_name}_time'] = datetime.now().isoformat()
                logging.info(f"Received house data: {sensor_name} = {value}")
                
                # Write to Prometheus file
                write_house_prometheus(sensor_name, value)
            except ValueError:
                logging.error(f"Invalid value for house sensor {sensor_name}: {msg.payload}")

        # Handle weather data: weather/sensor_name
        elif len(parts) == 2 and parts[0] == 'weather':
            sensor_name = parts[1]
            try:
                payload_str = msg.payload.decode('utf-8')
                # Try to convert to float, but accept strings too
                try:
                    value = float(payload_str)
                except ValueError:
                    value = payload_str  # Keep as string (e.g., "Partly Cloudy")
                
                weather_data[sensor_name] = value
                weather_data[f'{sensor_name}_time'] = datetime.now().isoformat()
                logging.info(f"Received weather data: {sensor_name} = {value}")
                
                # Write to Prometheus file (only for numeric values)
                if isinstance(value, (int, float)):
                    write_weather_prometheus(sensor_name, value)
            except Exception as e:
                logging.error(f"Error processing weather sensor {sensor_name}: {e}")

    except Exception as e:
        logging.error(f"Error processing MQTT message {msg.topic}: {e}")

def write_house_prometheus(sensor_name, value):
    """Write house sensor data to Prometheus format file"""
    try:
        import os
        prom_dir = "/home/constantine/mpp-solar/prometheus"
        
        # Ensure directory exists
        os.makedirs(prom_dir, exist_ok=True)
        
        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Write to timestamped file (like inverter does)
        timestamped_file = os.path.join(prom_dir, f"house-{sensor_name}-{timestamp}.prom")
        
        # Also write to a current file (like mpp-solar-inverter-qpigs.prom)
        current_file = os.path.join(prom_dir, "house-sensors.prom")
        
        # Prometheus format metric line
        metric_line = f'house_{sensor_name}{{sensor="{sensor_name}"}} {value}\n'
        
        # Write timestamped file
        with open(timestamped_file, 'w') as f:
            f.write(f'machine_role{{role="house_sensors"}} 1\n')
            f.write(metric_line)
        
        # Update current file (read existing, update this metric, write back)
        existing_metrics = {}
        if os.path.exists(current_file):
            with open(current_file, 'r') as f:
                for line in f:
                    if line.startswith('house_'):
                        # Parse: house_temperature{sensor="temperature"} 25.0
                        match = re.match(r'(house_\w+)\{[^}]+\}\s+([\d.]+)', line)
                        if match:
                            existing_metrics[match.group(1)] = line
        
        # Update with new value
        existing_metrics[f'house_{sensor_name}'] = metric_line
        
        # Write updated current file
        with open(current_file, 'w') as f:
            f.write(f'machine_role{{role="house_sensors"}} 1\n')
            for metric in sorted(existing_metrics.keys()):
                f.write(existing_metrics[metric])
        
        logging.debug(f"Wrote house data to Prometheus files: {sensor_name} = {value}")
        
    except Exception as e:
        logging.error(f"Error writing house Prometheus data: {e}")

def write_weather_prometheus(sensor_name, value):
    """Write weather data to Prometheus format file"""
    try:
        import os
        prom_dir = "/home/constantine/mpp-solar/prometheus"
        
        # Ensure directory exists
        os.makedirs(prom_dir, exist_ok=True)
        
        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Write to timestamped file
        timestamped_file = os.path.join(prom_dir, f"weather-{sensor_name}-{timestamp}.prom")
        
        # Also write to a current file
        current_file = os.path.join(prom_dir, "weather-data.prom")
        
        # Prometheus format metric line
        metric_line = f'weather_{sensor_name}{{sensor="{sensor_name}"}} {value}\n'
        
        # Write timestamped file
        with open(timestamped_file, 'w') as f:
            f.write(f'machine_role{{role="weather_data"}} 1\n')
            f.write(metric_line)
        
        # Update current file (read existing, update this metric, write back)
        existing_metrics = {}
        if os.path.exists(current_file):
            with open(current_file, 'r') as f:
                for line in f:
                    if line.startswith('weather_'):
                        match = re.match(r'(weather_\w+)\{[^}]+\}\s+([\d.\-]+)', line)
                        if match:
                            existing_metrics[match.group(1)] = line
        
        # Update with new value
        existing_metrics[f'weather_{sensor_name}'] = metric_line
        
        # Write updated current file
        with open(current_file, 'w') as f:
            f.write(f'machine_role{{role="weather_data"}} 1\n')
            for metric in sorted(existing_metrics.keys()):
                f.write(existing_metrics[metric])
        
        logging.debug(f"Wrote weather data to Prometheus files: {sensor_name} = {value}")
        
    except Exception as e:
        logging.error(f"Error writing weather Prometheus data: {e}")

def start_mqtt_subscriber():
    """Start MQTT subscriber in background thread"""
    try:
        # Use CallbackAPIVersion to avoid deprecation warnings
        import paho.mqtt.client as mqtt_lib
        mqtt_client = mqtt_lib.Client(client_id="mpp_solar_web", protocol=mqtt_lib.MQTTv311)
        mqtt_client.username_pw_set("mqttuser", "mqtt123")
        mqtt_client.on_connect = on_mqtt_connect
        mqtt_client.on_message = on_mqtt_message
        mqtt_client.enable_logger(logging.getLogger())

        logging.info("Connecting to MQTT broker at 127.0.0.1:1883")
        mqtt_client.connect("127.0.0.1", 1883, 60)
        mqtt_client.loop_forever()
    except Exception as e:
        logging.error(f"Error starting MQTT subscriber: {e}", exc_info=True)

if __name__ == '__main__':
    # Get initial data
    # Load historical data from Prometheus files
    prometheus_dir = "/home/constantine/mpp-solar/prometheus"
    load_historical_prometheus_data(prometheus_dir, max_entries=1000)
    
    load_historical_house_weather_data(prometheus_dir, max_entries_per_sensor=2100)
    get_inverter_data()
    
    # Load configuration from web.yaml
    import yaml
    try:
        with open('web.yaml', 'r') as f:
            config = yaml.safe_load(f)
        host = config.get('host', '0.0.0.0')
        port = config.get('port', 5000)
        log_level = config.get('log_level', 'info')
    except FileNotFoundError:
        host = '0.0.0.0'
        port = 5000
        log_level = 'info'
    
    # Set up logging
    logging.basicConfig(level=getattr(logging, log_level.upper()))

    # Start data update thread
    data_thread = threading.Thread(target=update_data_thread, daemon=True)
    data_thread.start()
    logging.info("Started data update thread")

        # Start MQTT subscriber thread
    mqtt_thread = threading.Thread(target=start_mqtt_subscriber, daemon=True)
    mqtt_thread.start()
    logging.info("Started MQTT subscriber thread")

    print(f"Starting MPP-Solar Web Interface on {host}:{port}")
    print(f"Access the interface at: http://{host}:{port}")

    app.run(host=host, port=port, debug=False)
