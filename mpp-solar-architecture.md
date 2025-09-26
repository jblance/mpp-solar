# MPP-Solar Project Architecture

## System Architecture Diagram

```mermaid
graph TB
    %% Hardware Layer
    subgraph "Hardware Layer"
        INV[MPP-Solar Inverter]
        USB[USB HIDRAW Device<br/>/dev/hidraw0]
        INV -.->|PI30 Protocol| USB
    end

    %% Communication Layer
    subgraph "Communication Layer"
        MPPSOLAR[mppsolar Library<br/>Python Package]
        HIDRAW[HIDRAW I/O<br/>Low-level USB]
        USB --> HIDRAW
        HIDRAW --> MPPSOLAR
    end

    %% Application Layer
    subgraph "Application Layer"
        subgraph "Web Interface"
            WEB[Flask Web Server<br/>web_interface.py]
            API[REST API Endpoints<br/>/api/data, /api/historical, /api/command]
            THREAD[Background Thread<br/>30s Data Collection]
        end
        
        subgraph "Daemon Service"
            DAEMON[MPP-Solar Daemon<br/>mpp-solar --daemon]
            CONFIG[Configuration<br/>mpp-solar.conf]
        end
    end

    %% Data Storage Layer
    subgraph "Data Storage Layer"
        MEMORY[In-Memory Store<br/>1000 entries ~8.3 hours]
        PROM[Prometheus Files<br/>Time-series data]
        LOGS[Log Files<br/>mpp-solar.log]
    end

    %% Frontend Layer
    subgraph "Frontend Layer"
        subgraph "Web UI"
            DASH[Dashboard<br/>Real-time Monitoring]
            CHARTS[Charts Page<br/>Historical Visualization]
            CMD[Command Interface<br/>Direct Control]
        end
        
        subgraph "UI Technologies"
            HTML[HTML5/CSS3]
            BOOT[Bootstrap 5]
            CHARTJS[Chart.js]
            JS[JavaScript ES6+]
        end
    end

    %% Data Flow Connections
    MPPSOLAR --> WEB
    MPPSOLAR --> DAEMON
    WEB --> THREAD
    THREAD --> MEMORY
    DAEMON --> PROM
    DAEMON --> LOGS
    CONFIG --> DAEMON
    
    WEB --> API
    API --> DASH
    API --> CHARTS
    API --> CMD
    
    DASH --> HTML
    CHARTS --> CHARTJS
    CMD --> JS
    HTML --> BOOT
    CHARTS --> JS

    %% Data Retrieval
    MEMORY -.->|Historical Data| API
    PROM -.->|Historical Data| API

    %% Styling
    classDef hardware fill:#e1f5fe
    classDef communication fill:#f3e5f5
    classDef application fill:#e8f5e8
    classDef storage fill:#fff3e0
    classDef frontend fill:#fce4ec
    classDef ui fill:#f1f8e9

    class INV,USB hardware
    class MPPSOLAR,HIDRAW communication
    class WEB,API,THREAD,DAEMON,CONFIG application
    class MEMORY,PROM,LOGS storage
    class DASH,CHARTS,CMD frontend
    class HTML,BOOT,CHARTJS,JS ui
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant INV as MPP-Solar Inverter
    participant USB as USB HIDRAW
    participant WEB as Web Interface
    participant DAEMON as Daemon Service
    participant MEM as In-Memory Store
    participant PROM as Prometheus Files
    participant UI as Web UI
    participant USER as User

    %% Real-time Data Collection
    loop Every 30 seconds
        WEB->>USB: QPIGS Command
        USB->>INV: Request Status
        INV->>USB: Status Response
        USB->>WEB: Data
        WEB->>MEM: Store Data
    end

    %% Historical Data Collection
    loop Every 60 seconds
        DAEMON->>USB: QPIGS Command
        USB->>INV: Request Status
        INV->>USB: Status Response
        USB->>DAEMON: Data
        DAEMON->>PROM: Write Prometheus File
    end

    %% User Interaction
    USER->>UI: Access Dashboard
    UI->>WEB: GET /api/data
    WEB->>MEM: Retrieve Latest Data
    MEM->>WEB: Return Data
    WEB->>UI: JSON Response
    UI->>USER: Display Real-time Data

    %% Historical Data Viewing
    USER->>UI: View Charts
    UI->>WEB: GET /api/historical?hours=24
    WEB->>MEM: Get In-Memory Data
    WEB->>PROM: Get Prometheus Data
    MEM->>WEB: Return Data
    PROM->>WEB: Return Data
    WEB->>UI: Combined Historical Data
    UI->>USER: Display Charts

    %% Command Execution
    USER->>UI: Send Command
    UI->>WEB: POST /api/command
    WEB->>USB: Execute Command
    USB->>INV: Send Command
    INV->>USB: Command Response
    USB->>WEB: Response
    WEB->>UI: Command Result
    UI->>USER: Display Result
```

## Technology Stack Diagram

```mermaid
graph LR
    subgraph "Backend Technologies"
        PY[Python 3]
        FLASK[Flask Web Framework]
        MPPSOLAR[mppsolar Library]
        HIDRAW[HIDRAW Protocol]
        PROM[Prometheus Format]
        THREAD[Threading]
    end

    subgraph "Frontend Technologies"
        HTML[HTML5/CSS3]
        BOOT[Bootstrap 5]
        CHARTJS[Chart.js]
        JS[JavaScript ES6+]
        FA[Font Awesome]
        DATE[Date-fns]
    end

    subgraph "Communication Protocols"
        USB[USB HIDRAW]
        PI30[PI30 Protocol]
        REST[REST API]
        JSON[JSON]
        MQTT[MQTT Optional]
    end

    subgraph "Data Storage"
        MEM[In-Memory Store]
        FILE[Prometheus Files]
        LOG[Log Files]
        CONF[Configuration Files]
    end

    subgraph "System Services"
        SYSTEMD[systemd Service]
        SCRIPT[Management Scripts]
        DAEMON[Background Daemon]
    end

    %% Connections
    PY --> FLASK
    PY --> MPPSOLAR
    PY --> THREAD
    MPPSOLAR --> HIDRAW
    HIDRAW --> USB
    USB --> PI30
    
    FLASK --> REST
    REST --> JSON
    
    HTML --> BOOT
    HTML --> CHARTJS
    HTML --> JS
    HTML --> FA
    CHARTJS --> DATE
    
    FLASK --> MEM
    DAEMON --> FILE
    DAEMON --> LOG
    DAEMON --> CONF
    
    SYSTEMD --> DAEMON
    SCRIPT --> SYSTEMD

    %% Styling
    classDef backend fill:#e3f2fd
    classDef frontend fill:#f3e5f5
    classDef protocol fill:#e8f5e8
    classDef storage fill:#fff3e0
    classDef system fill:#fce4ec

    class PY,FLASK,MPPSOLAR,HIDRAW,PROM,THREAD backend
    class HTML,BOOT,CHARTJS,JS,FA,DATE frontend
    class USB,PI30,REST,JSON,MQTT protocol
    class MEM,FILE,LOG,CONF storage
    class SYSTEMD,SCRIPT,DAEMON system
```

## Component Interaction Diagram

```mermaid
graph TD
    subgraph "User Interface Layer"
        DASH[Dashboard Page<br/>Real-time Monitoring]
        CHARTS[Charts Page<br/>Historical Data]
        CMD[Command Interface<br/>Direct Control]
    end

    subgraph "API Layer"
        DATA_API[/api/data<br/>Current Status]
        HIST_API[/api/historical<br/>Historical Data]
        CMD_API[/api/command<br/>Command Execution]
    end

    subgraph "Business Logic Layer"
        GET_DATA[get_inverter_data<br/>Data Collection]
        GET_HIST[get_historical_data<br/>Data Retrieval]
        UPDATE_THREAD[update_data_thread<br/>Background Collection]
    end

    subgraph "Data Access Layer"
        DEVICE[Device Interface<br/>mppsolar Library]
        MEM_STORE[historical_data_store<br/>In-Memory Cache]
        PROM_FILES[Prometheus Files<br/>Persistent Storage]
    end

    subgraph "Hardware Layer"
        HIDRAW_DEV[HIDRAW Device<br/>/dev/hidraw0]
        INVERTER[MPP-Solar Inverter<br/>PI30 Protocol]
    end

    %% User Interactions
    DASH --> DATA_API
    CHARTS --> HIST_API
    CMD --> CMD_API

    %% API to Business Logic
    DATA_API --> GET_DATA
    HIST_API --> GET_HIST
    CMD_API --> DEVICE

    %% Business Logic to Data Access
    GET_DATA --> DEVICE
    GET_DATA --> MEM_STORE
    GET_HIST --> MEM_STORE
    GET_HIST --> PROM_FILES
    UPDATE_THREAD --> GET_DATA

    %% Data Access to Hardware
    DEVICE --> HIDRAW_DEV
    HIDRAW_DEV --> INVERTER

    %% Background Processes
    UPDATE_THREAD -.->|Every 30s| GET_DATA
    DAEMON_PROC[Daemon Process] -.->|Every 60s| DEVICE
    DAEMON_PROC -.->|Write| PROM_FILES

    %% Styling
    classDef ui fill:#e1f5fe
    classDef api fill:#f3e5f5
    classDef logic fill:#e8f5e8
    classDef data fill:#fff3e0
    classDef hardware fill:#fce4ec

    class DASH,CHARTS,CMD ui
    class DATA_API,HIST_API,CMD_API api
    class GET_DATA,GET_HIST,UPDATE_THREAD logic
    class DEVICE,MEM_STORE,PROM_FILES data
    class HIDRAW_DEV,INVERTER hardware
```
