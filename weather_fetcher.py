#!/usr/bin/env python3
"""
Weather data fetcher for Open-Meteo API
Fetches weather data and publishes to MQTT
"""

import requests
import time
import logging
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuration
LOCATION = {
    'latitude': 43.7776,
    'longitude': -72.8145,
    'name': 'Pittsfield, Vermont'
}

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_USERNAME = "mqttuser"
MQTT_PASSWORD = "mqtt123"

# Open-Meteo API endpoint
API_URL = "https://api.open-meteo.com/v1/forecast"

# Fetch interval (seconds) - 10 minutes
FETCH_INTERVAL = 600

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/constantine/mpp-solar/weather_fetcher.log'),
        logging.StreamHandler()
    ]
)


def decode_weather_code(code):
    """Decode WMO weather code to description"""
    codes = {
        0: 'Clear', 1: 'Mainly Clear', 2: 'Partly Cloudy', 3: 'Overcast',
        45: 'Foggy', 48: 'Foggy',
        51: 'Light Drizzle', 53: 'Drizzle', 55: 'Heavy Drizzle',
        61: 'Light Rain', 63: 'Rain', 65: 'Heavy Rain',
        71: 'Light Snow', 73: 'Snow', 75: 'Heavy Snow',
        77: 'Snow Grains',
        80: 'Light Showers', 81: 'Showers', 82: 'Heavy Showers',
        85: 'Light Snow Showers', 86: 'Snow Showers',
        95: 'Thunderstorm', 96: 'Thunderstorm with Hail', 99: 'Severe Thunderstorm'
    }
    return codes.get(code, 'Unknown')

def fetch_weather_data():
    """Fetch current weather data from Open-Meteo API"""
    try:
        params = {
            'latitude': LOCATION['latitude'],
            'longitude': LOCATION['longitude'],
            'current': 'temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,wind_direction_10m,pressure_msl,weather_code',
            'temperature_unit': 'celsius',
            'wind_speed_unit': 'ms',
            'precipitation_unit': 'mm'
        }
        
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data.get('current', {})
        
        weather_data = {
            'temperature': current.get('temperature_2m'),
            'humidity': current.get('relative_humidity_2m'),
            'wind_speed': current.get('wind_speed_10m'),
            'wind_direction': current.get('wind_direction_10m'),
            'rain': current.get('precipitation', 0),
            'pressure': current.get('pressure_msl'),
            'condition': decode_weather_code(current.get('weather_code', 0))
        }
        
        logging.info(f"Fetched weather data: Temp={weather_data['temperature']}°C, "
                    f"Humidity={weather_data['humidity']}%, "
                    f"Wind={weather_data['wind_speed']}m/s, "
                    f"Rain={weather_data['rain']}mm")
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def publish_to_mqtt(weather_data):
    """Publish weather data to MQTT broker"""
    try:
        client = mqtt.Client(client_id="weather_fetcher")
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        for key, value in weather_data.items():
            if value is not None:
                topic = f"weather/{key}"
                client.publish(topic, str(value))
                logging.debug(f"Published {topic}: {value}")
        
        client.disconnect()
        logging.info("Published weather data to MQTT")
        return True
        
    except Exception as e:
        logging.error(f"Error publishing to MQTT: {e}")
        return False

def main():
    """Main loop"""
    logging.info(f"Weather Fetcher started for {LOCATION['name']}")
    logging.info(f"Location: {LOCATION['latitude']}, {LOCATION['longitude']}")
    logging.info(f"Fetch interval: {FETCH_INTERVAL} seconds ({FETCH_INTERVAL/60} minutes)")
    
    while True:
        try:
            weather_data = fetch_weather_data()
            
            if weather_data:
                publish_to_mqtt(weather_data)
            else:
                logging.warning("No weather data fetched, skipping MQTT publish")
            
            # Wait for next fetch
            logging.info(f"Next fetch in {FETCH_INTERVAL/60} minutes...")
            time.sleep(FETCH_INTERVAL)
            
        except KeyboardInterrupt:
            logging.info("Weather fetcher stopped by user")
            break
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    main()
