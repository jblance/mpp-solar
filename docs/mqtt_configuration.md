# MQTT Manager System

## Overview

The new MQTT system provides a threaded, centralized manager for all MQTT connections with support for bidirectional communication. Key features:

- **Single connection per broker**: Multiple devices can share the same MQTT broker connection
- **Bidirectional communication**: Devices can receive and respond(acknowledge) to commands via MQTT (json reponse).
- **Thread-safe**: All operations are handled in separate threads with proper synchronization
- **Automatic reconnection**: Built-in reconnection logic with exponential backoff
- **Legacy compatibility**: Existing code continues to work without changes (WORK In PROGRESS)
- **Proper qos levels**: Broker retention possible for commands if the sender set it, default for cmd_response. All outputs are still qos 0
- **Broker retention ready**: automatically sends cmd_response with retention and qos 1, login with hostname plus a hash ID (using host, user, port)
  to allow sending commands with qos 1/2 plus retention. Creates a readable client ID format: mppsolar_{hostname}_{hash}
- **MQTT default wildcards**: are allowed.
- **Allowed command list**: per device (regex supported).
- Lagacy MQTT configuration in SETUP plus per device override (multiple broker support).


## Configuration

### MQTT Basic Setup Section
You may  still setup mqtt options here, though any of the values per device will take precedence.
```
[SETUP]
pause=10
mqtt_broker=192.168.10.134
mqtt_port=1883
mqtt_user=mqttuser
mqtt_pass=mqttpass
```

### Device Section with MQTT Commands
```
[Inverter_1]
port=/dev/hidraw0
protocol=PI30m045
command=QPGS0#QPIGS
outputs=hassd_mqtt2
mqtt_allowed_cmds=POP0[0-2],PCP*,MCHGC{0-1}[0-6][0-2]
# Optional: override broker settings for this device
mqtt_broker=192.168.1.100
mqtt_port=1884
```

## Command Structure

### Command Topic Pattern where hostname is mpp-solars host (FQDN) short name.
Commands are received on: `{hostname}/{device_name}/cmd`

Example: `myserver/Inverter_1/cmd`

### Response Topic Pattern
Responses are sent on: `{hostname}/{device_name}/cmd_response`

Example: `myserver/Inverter_1/cmd_response`

### Command Format
Send plain text commands to the command topic:
```
POP02
```
### MQTT wildcards are allowed for devices:
MQTT supports two types of wildcards: + (single-level) and # (multi-level).

### Response Format
Responses are JSON formatted:
```json
{
  "result": {
    "_command": "POP02",
     "_command_description": "Set Device Output Source Priority",
      "raw_response": [
        "(ACK9 \r",
         ""
      ],
       "POP": [
         "ACK",
          ""
        ]
  },
  "command": "POP02",
  "timestamp": 1750305720.956817
}