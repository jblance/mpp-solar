# MPP-Solar Setup Guide

This guide will help you set up the MPP-Solar monitoring system with your own configuration.

## 🔧 **Initial Setup**

### **1. Clone the Repository**
```bash
git clone https://github.com/thedini/mpp-solar.git
cd mpp-solar
```

### **2. Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### **3. Configure the System**

#### **A. Copy Template Files**
```bash
cp mpp-solar.conf.template mpp-solar.conf
cp web.yaml.template web.yaml
cp mpp-solar-daemon.service.template mpp-solar-daemon.service
cp mpp-solar-web.service.template mpp-solar-web.service
cp manage_daemon.sh.template manage_daemon.sh
cp manage_web.sh.template manage_web.sh
cp web_interface.py.template web_interface.py
```

#### **B. Edit Configuration Files**

**Edit `mpp-solar.conf`:**
- Replace `/path/to/your/mpp-solar` with your actual installation path
- Update `log_file` path
- Update `prom_output_dir` path
- Set `protocol` to your inverter's protocol (e.g., `pi30`, `pi16`, etc.)
- Set `port` to your device path (e.g., `/dev/hidraw0`, `/dev/ttyUSB0`, etc.)
- Set `porttype` to your port type (e.g., `hidraw`, `serial`, etc.)
- Set `baud` to your device's baud rate (e.g., `2400`, `9600`, etc.)
- Set `command` to the commands you want to run (e.g., `QPIGS`, `QPIGS#QPIRI`, etc.)
- Set `tag` and `dev` to your preferred identifiers
- Adjust other settings as needed

**Edit `web.yaml`:**
- Change `host` if needed (default: "0.0.0.0")
- Change `port` if needed (default: 5000)
- Adjust `log_level` if needed (default: "info")

**Edit `mpp-solar-daemon.service`:**
- Replace `YOUR_USERNAME` with your actual username
- Replace `/path/to/your/mpp-solar` with your actual installation path
- Replace `/dev/YOUR_DEVICE` with your actual device path

**Edit `mpp-solar-web.service`:**
- Replace `YOUR_USERNAME` with your actual username
- Replace `/path/to/your/mpp-solar` with your actual installation path

**Edit `manage_daemon.sh`:**
- Replace `/path/to/your/mpp-solar` with your actual installation path
- Replace `/dev/YOUR_DEVICE` with your actual device path
- Replace `YOUR_PROTOCOL` and `YOUR_PORTTYPE` with your actual values

**Edit `manage_web.sh`:**
- Replace `/path/to/your/mpp-solar` with your actual installation path

**Edit `web_interface.py`:**
- Replace `/path/to/your/mpp-solar` with your actual installation path
- Replace `/dev/YOUR_DEVICE` with your actual device path
- Replace `YOUR_PROTOCOL` and `YOUR_PORTTYPE` with your actual values
- Replace `YOUR_COMMANDS` with your actual commands

### **4. Set Up Systemd Services**

#### **A. Copy Service Files**
```bash
sudo cp mpp-solar-daemon.service /etc/systemd/system/
sudo cp mpp-solar-web.service /etc/systemd/system/
```

**Note:** The service files should already be configured with your specific paths and settings.

#### **C. Enable and Start Services**
```bash
sudo systemctl daemon-reload
sudo systemctl enable mpp-solar-daemon
sudo systemctl enable mpp-solar-web
sudo systemctl start mpp-solar-daemon
sudo systemctl start mpp-solar-web
```

### **5. Set Up Device Permissions**

#### **A. Add User to Dialout Group**
```bash
sudo usermod -a -G dialout $USER
```

#### **B. Create Udev Rule**

**First, find your device IDs:**
```bash
lsusb
# Look for your MPP-Solar device and note the Vendor:Product IDs
# Example: Bus 001 Device 003: ID 0665:5161 Cypress Semiconductor USB to Serial
```

Create `/etc/udev/rules.d/99-mpp-solar.rules`:
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="YOUR_VENDOR_ID", ATTRS{idProduct}=="YOUR_PRODUCT_ID", MODE="0666"
```

#### **C. Reload Udev Rules**
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### **6. Create Required Directories**
```bash
mkdir -p prometheus
```

## 🌐 **Access the Web Interface**

### **Standard Dashboard**
- URL: `http://localhost:5000`
- Features: Real-time monitoring, command interface

### **LCARS Dashboard (Star Trek Theme)**
- URL: `http://localhost:5000/lcars`
- Features: Futuristic LCARS interface

### **Charts Interface**
- URL: `http://localhost:5000/charts`
- Features: Historical data visualization

### **LCARS Charts**
- URL: `http://localhost:5000/charts/lcars`
- Features: LCARS-themed historical data

## 🔍 **Troubleshooting**

### **Check Service Status**
```bash
sudo systemctl status mpp-solar-daemon
sudo systemctl status mpp-solar-web
```

### **View Logs**
```bash
sudo journalctl -u mpp-solar-daemon -f
sudo journalctl -u mpp-solar-web -f
```

### **Check Device Permissions**
```bash
ls -la /dev/YOUR_DEVICE
groups $USER
```

### **Test Device Communication**
```bash
source venv/bin/activate
mpp-solar -p /dev/YOUR_DEVICE -P YOUR_PROTOCOL --porttype YOUR_PORTTYPE -c QID
```

## 📁 **File Structure**

```
mpp-solar/
├── venv/                    # Virtual environment
├── mpp-solar.conf          # Main configuration (create from template)
├── web.yaml                # Web interface config (create from template)
├── prometheus/             # Prometheus data directory
├── templates/              # Web interface templates
├── manage_daemon.sh        # Daemon management script
├── manage_web.sh           # Web interface management script
└── README files            # Documentation
```

## 🔒 **Security Notes**

- **Never commit** your actual `mpp-solar.conf` or `web.yaml` files
- **Never commit** log files or Prometheus data
- **Use templates** for configuration files
- **Update paths** in service files to match your system
- **Set proper permissions** for device access

## 🚀 **Next Steps**

1. **Test the system** with your MPP-Solar inverter
2. **Customize the interface** as needed
3. **Set up monitoring** for production use
4. **Configure alerts** if needed

For more information, see the individual README files:
- `README.md` - Main documentation
- `DAEMON_README.md` - Daemon setup details
- `CHARTS_README.md` - Charts interface guide
- `LCARS_COMPLETE_README.md` - LCARS theme guide
