# House Monitoring MQTT Setup

## Overview
The house monitoring page is now set up and ready to receive sensor data via MQTT.

## Access the House Monitoring Page
**URL:** http://192.168.1.134:5000/house

## MQTT Configuration for Your Remote Sensor Host

### Connection Settings
- **MQTT Broker Host:** `192.168.1.134`
- **MQTT Broker Port:** `1883`
- **Username:** `mqttuser`
- **Password:** `mqtt123`

### Topic Structure
Send sensor data to the following topics:

- **Temperature:** `house/temperature`
- **Humidity:** `house/humidity`
- **Pressure:** `house/pressure`

### Message Format
Send the sensor value as a plain number (float). Examples:

```bash
# Temperature in Celsius
mosquitto_pub -h 192.168.1.134 -p 1883 -u mqttuser -P mqtt123 -t house/temperature -m "23.5"

# Humidity in %
mosquitto_pub -h 192.168.1.134 -p 1883 -u mqttuser -P mqtt123 -t house/humidity -m "65.2"

# Pressure in hPa
mosquitto_pub -h 192.168.1.134 -p 1883 -u mqttuser -P mqtt123 -t house/pressure -m "1013.25"
```

## Python Example
```python
import paho.mqtt.client as mqtt
import time

# MQTT Configuration
MQTT_BROKER = "192.168.1.134"
MQTT_PORT = 1883
MQTT_USERNAME = "mqttuser"
MQTT_PASSWORD = "mqtt123"

# Create MQTT client
client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Send sensor data
def send_sensor_data(temperature, humidity, pressure):
    client.publish("house/temperature", str(temperature))
    client.publish("house/humidity", str(humidity))
    client.publish("house/pressure", str(pressure))
    print(f"Sent: T={temperature}°C, H={humidity}%, P={pressure}hPa")

# Example usage
while True:
    # Replace with your actual sensor readings
    temp = 23.5
    hum = 65.2
    pres = 1013.25
    
    send_sensor_data(temp, hum, pres)
    time.sleep(60)  # Send every 60 seconds
```

## ESP32/Arduino Example
```cpp
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "192.168.1.134";
const char* mqtt_user = "mqttuser";
const char* mqtt_password = "mqtt123";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  client.setServer(mqtt_server, 1883);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("Connected to MQTT");
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Read your sensors here
  float temperature = 23.5;  // Replace with actual reading
  float humidity = 65.2;     // Replace with actual reading
  float pressure = 1013.25;  // Replace with actual reading
  
  // Publish to MQTT
  client.publish("house/temperature", String(temperature).c_str());
  client.publish("house/humidity", String(humidity).c_str());
  client.publish("house/pressure", String(pressure).c_str());
  
  delay(60000);  // Wait 60 seconds
}
```

## Adding More Sensors
To add additional sensors, simply publish to new topics under `house/`:

```bash
house/co2          # CO2 level in ppm
house/light        # Light level in lux
house/motion       # Motion detected (0 or 1)
house/door         # Door state (0=closed, 1=open)
```

The web page will need to be updated to display these new sensors, but the MQTT backend will automatically receive and store them.

## Testing
Test the connection from your remote host:

```bash
# Install mosquitto clients
sudo apt-get install mosquitto-clients

# Test publishing
mosquitto_pub -h 192.168.1.134 -p 1883 -u mqttuser -P mqtt123 -t house/temperature -m "25.0"

# You should see the value appear on http://192.168.1.134:5000/house
```

## Troubleshooting
1. **Cannot connect to MQTT:** Check firewall on 192.168.1.134 allows port 1883
2. **Authentication failed:** Verify username=mqttuser and password=mqtt123
3. **Data not appearing:** Check the web interface logs at `/home/constantine/mpp-solar/web_interface.log`

## Viewing Logs
```bash
tail -f /home/constantine/mpp-solar/web_interface.log
```
