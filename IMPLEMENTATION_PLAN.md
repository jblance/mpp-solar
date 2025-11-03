# MPP-Solar Implementation Plan

## Project Overview

MPP-Solar is a comprehensive Python framework for communicating with solar inverters, Battery Management Systems, and power monitoring devices. The architecture is designed for extensibility, reliability, and multiple deployment modes.

**Design Philosophy:**
- Protocol-agnostic core with pluggable protocol implementations
- Robust retry logic for unreliable hardware connections
- Multiple output formats for diverse integration needs
- Zero-configuration outputs where possible (e.g., Home Assistant auto-discovery)

## Architecture Design

### 1. Core Layer Architecture

The system is built on five distinct layers, each with specific responsibilities:

#### 1.1 I/O Layer (`mppsolar/inout/`)

**Purpose:** Abstract physical communication methods into a uniform interface.

**Key Implementations:**
- `serialio.py` - RS232/USB serial (configurable baud rates, typically 2400/9600)
- `hidrawio.py` - USB HID devices (most MPP-Solar inverters)
- `jkbleio.py` - Bluetooth Low Energy (JK BMS specific)
- `mqttio.py` - MQTT command/response pattern
- `socketio.py` - TCP/UDP socket communication
- `testio.py` - Mock I/O for testing without hardware

**Design Pattern:** All I/O classes inherit from an abstract base that provides:
- `send_and_receive(data, timeout)` - Core communication method
- Connection management (open, close, is_connected)
- Timeout handling with configurable durations

**Technical Details:**
- USB HID uses direct file I/O on `/dev/hidraw*` devices
- Serial uses pyserial with 8N1 configuration (8 data bits, no parity, 1 stop bit)
- Bluetooth uses bluepy library with notification-based response handling
- All implementations return raw bytes for protocol layer processing

#### 1.2 Protocol Layer (`mppsolar/protocols/`)

**Purpose:** Define command structures, checksum algorithms, and response parsing for each device type.

**Base Class:** `abstractprotocol.py`
- Defines command dictionary structure
- Provides CRC/checksum algorithm registry
- Implements response parsing framework
- Categorizes commands (status vs settings vs special)

**Protocol Structure:**
```python
{
    "command_code": {
        "name": "command_name",
        "description": "Human readable description",
        "help": "Usage instructions",
        "type": "status|settings|query",
        "response": [
            ["field_name", field_length, "unit", decoder_function],
            # ... more fields
        ],
        "test_responses": [b"sample_response"],
        "regex": "validation_regex"
    }
}
```

**Key Protocol Implementations:**

1. **PI30 Protocol** (`pi30.py`) - Most Common MPP-Solar/Voltronic
   - CRC algorithm: CRC-XMODEM with specific polynomial
   - Commands wrapped with `(COMMAND\r` + CRC bytes
   - Response format: `(field1 field2 ... fieldN<CRC>\r`
   - Echo detection: Filters command echo from response
   - ~50+ commands defined (QPIGS, QPIRI, QMOD, POP*, PF, etc.)

2. **JK04 Protocol** (`jk04.py`) - JK BMS Bluetooth
   - Binary protocol with start/end markers
   - Commands: 0x55 0xAA 0xEB 0x90 <command_byte>
   - Response parsing: Fixed-length binary fields
   - Cell voltage array parsing (up to 24 cells)
   - Temperature sensor array handling

3. **Daly BMS** (`daly.py`)
   - Start byte: 0xA5
   - Address byte + command byte structure
   - Length-prefixed responses
   - Checksum: Simple sum modulo 256

4. **Victron VE Direct** (`ved.py`)
   - Text-based protocol with checksums
   - Newline-delimited key-value pairs
   - Checksum validation on each block

**Design Decisions:**
- Protocols are stateless (no internal state between commands)
- Response parsing returns structured dictionaries
- All numeric values decoded to appropriate Python types
- Units preserved in metadata for display formatting
- Test responses embedded for CI/CD validation

#### 1.3 Device Layer (`mppsolar/devices/`)

**Purpose:** Orchestrate I/O and Protocol with intelligent error handling and retry logic.

**Core Class:** `AbstractDevice` (`device.py`, 269 lines)

**Retry Logic Implementation:**
```python
def run_command(command):
    max_retries = 3
    backoff_delays = [1, 2, 3]  # seconds

    for attempt in range(max_retries):
        try:
            # Validate command exists in protocol
            if not protocol.has_command(command):
                return error_response

            # Build command bytes
            command_bytes = protocol.build_command(command)

            # Send via I/O layer
            response_bytes = io_port.send_and_receive(command_bytes)

            # Filter command echo
            clean_response = remove_echo(response_bytes, command_bytes)

            # Parse with protocol
            result = protocol.parse_response(command, clean_response)

            if result.is_valid():
                return result

        except TransientError as e:
            if attempt < max_retries - 1:
                time.sleep(backoff_delays[attempt])
                continue
            raise

        except PermanentError as e:
            # Don't retry on config errors, invalid commands, etc.
            raise immediately
```

**Special Commands:**
- `list_commands` - Enumerate all available commands for the protocol
- `get_status` - Execute all status-type commands
- `get_settings` - Execute all settings-type commands

**Validation:**
- Protocol existence check
- Port availability verification
- Command validity check before sending
- Response format validation

**Why This Matters:** Hardware communication is inherently unreliable. USB devices can have transmission errors, Bluetooth can disconnect, serial buffers can overflow. The device layer shields the rest of the application from these transient failures.

#### 1.4 Output Layer (`mppsolar/outputs/`)

**Purpose:** Route processed data to various destinations with format-specific transformations.

**Base Class:** `BaseOutput`
- Abstract `output(data, tag, mqtt_broker)` method
- Output-specific configuration via kwargs
- Filtering capabilities (include/exclude fields)

**Output Implementations:**

1. **Screen Output** (`screen.py`)
   - Human-readable formatting with units
   - Table layout with aligned columns
   - Color coding for critical values (optional)

2. **JSON Output** (`json.py`)
   - Pretty-printed JSON to stdout
   - Timestamp injection
   - Nested structure for complex responses

3. **Prometheus Outputs**
   - `prometheus.py` - Direct push gateway integration
   - `prom_file.py` - File-based exposition format

   **File Output Details:**
   - Atomic writes: temp file → rename (prevents partial reads)
   - Hard-linked backups (zero-copy, keeps last 10)
   - Format: `# TYPE` declarations + `metric{labels} value timestamp`
   - Rotation logic: `file.prom` + `file.prom.bak.N`

4. **MQTT Outputs**
   - `mqtt.py` - Basic topic publishing
   - `json_mqtt.py` - JSON formatted messages
   - `hass_mqtt.py` - Home Assistant auto-discovery

   **Home Assistant Integration:**
   - Auto-discovery topics: `homeassistant/sensor/{device_id}/{field}/config`
   - Device class mapping (battery, voltage, current, power, energy, temperature)
   - State topics: `{base_topic}/{device_id}/{field}/state`
   - Unique IDs for entity registry
   - Device metadata (manufacturer, model, sw_version)

5. **Database Outputs**
   - `postgres.py` - PostgreSQL with automatic table creation
   - `mongo.py` - MongoDB document insertion
   - Schema inference from data types

**MQTT Manager Architecture** (`mppsolar/libs/mqtt_manager.py`):

```python
class MQTTManager:
    # Connection pooling
    _connections = {}  # broker_key -> client instance

    def get_client(broker, port, username, password):
        # Reuse existing connection or create new
        # Thread-safe with locks

    # Publish queue with retries
    def publish(topic, payload, qos=0, retain=False):
        # Threaded queue for non-blocking publishes
        # Exponential backoff on failures (5s → 10s → 20s ... → 300s max)
        # Automatic reconnection logic

    # Command authorization
    def is_command_authorized(command, allowed_patterns):
        # Regex-based whitelist checking
        # Prevents unauthorized device control
```

**Design Decisions:**
- Outputs are independent and can fail without affecting others
- All outputs receive the same structured data dictionary
- MQTT connections are pooled and reused across outputs
- File outputs use atomic writes to prevent corruption
- Database schemas are auto-created for zero-config deployment

#### 1.5 Daemon Layer (`mppsolar/daemon/`)

**Purpose:** Enable continuous monitoring with configuration-driven execution.

**Components:**
- `daemon.py` - Core daemon logic with scheduling
- `daemon_systemd.py` - Systemd service integration

**Configuration-Driven Execution:**
```ini
[SETUP]
pause = 60  # Seconds between poll cycles
mqtt_broker = localhost
mqtt_port = 1883

[inverter_1]
type = mppsolar
protocol = pi30
port = /dev/hidraw0
porttype = hidraw
command = QPIGS
outputs = screen,json,prom_file,hass_mqtt
prom_output_dir = /var/lib/prometheus

[battery_1]
type = jkbms
protocol = jk04
port = XX:XX:XX:XX:XX:XX
porttype = jkble
command = getCellData
outputs = hass_mqtt
```

**Execution Model:**
- Each config section = one device
- All devices polled in parallel (separate threads)
- Each device respects the global `pause` interval
- Failures logged but don't stop other devices
- Graceful shutdown on SIGTERM/SIGINT

**Systemd Integration:**
- Type=notify for ready notification
- Restart=always for automatic recovery
- Nice=-5 for higher priority (optional)
- User/Group permissions for device access

### 2. Web Interface Architecture

**File:** `web_interface.py` (265 lines)

**Technology Stack:**
- Flask web framework
- REST API + Server-Sent Events (SSE)
- Bootstrap UI + custom LCARS theme
- Chart.js for historical visualization

**Data Management:**

1. **In-Memory Store:**
   ```python
   data_store = {
       "current": {},  # Latest device data
       "historical": deque(maxlen=1000)  # Circular buffer
   }
   ```
   - 1000 data points at 30-second intervals = ~8.3 hours
   - Automatic eviction of old data
   - Thread-safe with locks

2. **Historical Data Loading:**
   - Reads `.prom` files from daemon output directory
   - Parses Prometheus format into time-series data
   - Caches parsed data (invalidated on file mtime change)
   - Supports date range filtering

**API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/data` | GET | Current device status (JSON) |
| `/api/historical` | GET | Historical data (optional date range) |
| `/api/historical/all` | GET | All historical data |
| `/api/command` | POST | Execute device command |
| `/api/refresh` | POST | Force data refresh |
| `/stream` | GET | SSE for real-time updates |

**UI Routes:**

| Route | Purpose |
|-------|---------|
| `/` | Standard Bootstrap dashboard |
| `/lcars` | LCARS (Star Trek) themed dashboard |
| `/charts` | Historical charts |
| `/charts/lcars` | LCARS themed charts |

**Security Considerations:**
- Command execution requires POST (CSRF protection available)
- No authentication by default (designed for local network)
- Can be proxied behind nginx with auth

**Performance Optimization:**
- SSE for push updates (no polling overhead)
- Historical data cached and incrementally updated
- Static assets served with caching headers
- Prometheus file parsing only on mtime change

### 3. Cross-Cutting Concerns

#### 3.1 Error Handling Strategy

**Error Classification:**

1. **Configuration Errors** (permanent)
   - Invalid protocol name
   - Non-existent port
   - Malformed config file
   - Action: Fail fast with clear error message

2. **Transient Errors** (retryable)
   - USB device temporarily unavailable
   - Bluetooth connection dropped
   - CRC mismatch on response
   - Action: Retry with backoff

3. **Command Errors** (immediate)
   - Unknown command for protocol
   - Invalid command format
   - Action: Return error response, no retry

**Logging Levels:**
- DEBUG: Raw bytes sent/received, protocol parsing details
- INFO: Command execution, successful responses
- WARNING: Retries, recoverable errors
- ERROR: Failed commands after retries, config errors
- CRITICAL: Daemon shutdown, unrecoverable errors

#### 3.2 Testing Strategy

**Unit Tests** (`tests/unit/`):
- Protocol parsing with known good responses
- CRC algorithm validation
- Output formatting
- Mock I/O for device tests

**Integration Tests** (`tests/integration/`):
- End-to-end command execution with test port
- Multi-protocol support verification
- Output chaining tests
- Config file parsing

**Test Fixtures:**
- Sample responses embedded in protocol definitions
- Mock devices with predictable responses
- Config file templates for various scenarios

**CI/CD:**
- GitHub Actions on push/PR
- Test matrix: Python 3.10, 3.11, 3.12
- Coverage reporting
- Linting with black, flake8

#### 3.3 Backwards Compatibility

**Version 0.16.0 Breaking Changes:**
- Command separator: `,` → `#`
- Minimum Python: 3.8 → 3.10

**Mitigation:**
- Clear documentation in README, CHANGELOG
- Version detection logic for automated tools
- Deprecation warnings in 0.15.x series

**Protocol Versioning:**
- Each protocol is versioned independently
- New protocol versions can be added without breaking existing ones
- Protocol aliases for common variations

#### 3.4 Performance Characteristics

**Typical Latencies:**
- USB HID command: 50-200ms
- Serial command: 100-500ms
- Bluetooth command: 200-1000ms
- MQTT publish: 1-10ms (async)
- Prometheus file write: 5-20ms

**Resource Usage:**
- Daemon (1 device): ~20MB RAM, <1% CPU
- Web interface: ~30MB RAM, <1% CPU idle, ~5% during chart rendering
- Disk: ~1MB per day per device (Prometheus files)

**Scalability:**
- Tested with 10+ devices in parallel
- MQTT connection pooling prevents broker exhaustion
- File I/O atomic writes prevent corruption under concurrent access

## Implementation Phases

### Phase 1: Core Framework (Completed)
- ✅ I/O layer abstraction
- ✅ Protocol framework
- ✅ Device orchestration with retry logic
- ✅ Basic outputs (screen, JSON)
- ✅ PI30 protocol implementation

### Phase 2: Extended Protocol Support (Completed)
- ✅ JK BMS (jk02, jk04, jkserial)
- ✅ Daly BMS
- ✅ Victron VE Direct
- ✅ Additional PI variants (pi16, pi17, pi18, pi41)

### Phase 3: Integration Outputs (Completed)
- ✅ MQTT support
- ✅ Prometheus integration
- ✅ Home Assistant auto-discovery
- ✅ Database outputs (PostgreSQL, MongoDB)

### Phase 4: Daemon & Web Interface (Completed)
- ✅ Background daemon service
- ✅ Systemd/OpenRC integration
- ✅ Web interface with REST API
- ✅ Real-time monitoring with SSE
- ✅ Historical data visualization
- ✅ LCARS theme

### Phase 5: Ongoing Maintenance
- 🔄 New protocol additions as needed
- 🔄 Bug fixes and stability improvements
- 🔄 Performance optimizations
- 🔄 Community feature requests

## Success Criteria

### Technical Criteria
- ✅ Support 20+ device protocols
- ✅ <1% failed command rate under normal conditions
- ✅ <100ms overhead from framework (excluding hardware latency)
- ✅ Zero data loss in Prometheus file output
- ✅ 95%+ test coverage on core modules

### Usability Criteria
- ✅ Zero-config Home Assistant integration
- ✅ Single-command installation via pip
- ✅ CLI tool with intuitive arguments
- ✅ Web interface accessible without technical knowledge
- ✅ Comprehensive documentation with examples

### Reliability Criteria
- ✅ Daemon runs continuously for weeks without restart
- ✅ Automatic recovery from transient hardware failures
- ✅ Graceful degradation when outputs fail
- ✅ Clear error messages for troubleshooting

## Design Decisions & Rationale

### Why Multiple Output Formats?

Users deploy in diverse environments:
- Home Assistant users need auto-discovery
- Grafana users need Prometheus format
- Custom scripts need JSON
- Quick checks need screen output

Chaining outputs lets one daemon serve multiple needs simultaneously.

### Why File-Based Prometheus Output?

Push Gateway has limitations:
- Single point of failure
- Network dependency
- Difficult to debug

File-based output:
- Works offline
- Easy to inspect
- Prometheus scrapes directly
- Atomic writes prevent corruption

### Why Device-Layer Retry Logic?

Hardware communication is unreliable:
- USB devices can NAK randomly
- Bluetooth has RF interference
- Serial buffers overflow

Retry at device layer (not protocol or I/O):
- Protocol doesn't know about transient failures
- I/O layer too low-level for backoff logic
- Device layer has context for intelligent retry

### Why Connection Pooling for MQTT?

Without pooling:
- Each output creates a connection
- Broker limits connections per client
- Connection churn causes delays

With pooling:
- Single connection per broker
- Shared across all outputs
- Reduced broker load
- Faster publishes

## Future Enhancement Opportunities

### Short Term
- [ ] YAML config format (in addition to INI)
- [ ] Websocket API for web interface
- [ ] Configurable retry behavior per device
- [ ] Output filtering expressions

### Medium Term
- [ ] Plugin system for custom protocols
- [ ] Distributed deployment support (multiple daemons)
- [ ] Historical data export (CSV, Excel)
- [ ] Alert/notification system

### Long Term
- [ ] Machine learning for anomaly detection
- [ ] Predictive maintenance alerts
- [ ] Cloud sync for multi-site deployments
- [ ] Mobile app

---

**Document Version:** 1.0
**Last Updated:** 2025-10-30
