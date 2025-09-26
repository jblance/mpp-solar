# MPP-Solar Charts - Historical Data Visualization

The MPP-Solar web interface now includes an advanced charts page that displays interactive line graphs of your inverter's historical performance data.

## Features

### 📊 **Interactive Line Graphs**
- **Real-time Data**: Live updates from your inverter
- **Historical Data**: View trends over time using data from the daemon
- **Multiple Time Ranges**: 1 hour to 1 week of historical data
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### 📈 **Chart Categories**

#### 1. **Voltage Charts**
- Battery Voltage (V)
- AC Output Voltage (V)
- AC Input Voltage (V)

#### 2. **Power Charts**
- AC Output Active Power (W)
- AC Output Apparent Power (VA)
- AC Output Load (%)

#### 3. **Temperature Charts**
- Inverter Heat Sink Temperature (°C)

#### 4. **Current Charts**
- Battery Charging Current (A)
- Battery Discharge Current (A)

#### 5. **Status Charts**
- Is Charging On (boolean)
- Is Switched On (boolean)
- Is Load On (boolean)

### 🎛️ **Interactive Features**
- **Time Range Selector**: Choose from 1 hour to 1 week of data
- **Tab Navigation**: Switch between different chart categories
- **Hover Tooltips**: Detailed information on data points
- **Auto-refresh**: Charts update every 5 minutes
- **Manual Refresh**: Click refresh button for immediate updates

## Accessing the Charts

### From the Dashboard
1. Open the web interface: `http://localhost:5000`
2. Click the **"Charts"** button in the top-right corner
3. Or navigate directly to: `http://localhost:5000/charts`

### Direct URL
```
http://localhost:5000/charts
```

## How It Works

### Data Sources
The charts page uses two data sources:

1. **Real-time Data**: From the `/api/data` endpoint
2. **Historical Data**: From the `/api/historical` endpoint (reads Prometheus files)

### Data Collection
- **Daemon Service**: Collects data every 15 minutes and stores in Prometheus files
- **Web Interface**: Reads historical data from Prometheus files
- **Time Stamps**: Uses file modification times as data timestamps

### Chart Updates
- **Initial Load**: Loads data when page opens
- **Auto-refresh**: Updates every 5 minutes
- **Manual Refresh**: Click refresh button
- **Time Range Change**: Automatically reloads data when time range changes

## API Endpoints

### Historical Data API
```
GET /api/historical?hours=24
```

**Parameters:**
- `hours` (optional): Number of hours to look back (default: 24)

**Response:**
```json
{
  "mpp_solar_battery_voltage": [
    {
      "value": 48.0,
      "timestamp": "2025-08-25T21:54:02.062975",
      "labels": "inverter=\"inverter\",device=\"main_inverter\",cmd=\"QPIGS\""
    }
  ],
  "mpp_solar_ac_output_voltage": [
    {
      "value": 120.1,
      "timestamp": "2025-08-25T21:54:02.062975",
      "labels": "inverter=\"inverter\",device=\"main_inverter\",cmd=\"QPIGS\""
    }
  ]
}
```

## Data Summary

The charts page includes a data summary section that shows:
- **Current Values**: Latest readings for each metric
- **Average Values**: Mean values over the selected time range
- **Min/Max Values**: Range of values over the selected time range

### Summary Metrics
- Battery Voltage
- AC Output Voltage
- Output Power
- Temperature
- Load Percentage
- Charging Current

## Configuration

### Time Ranges Available
- 1 Hour
- 6 Hours
- 12 Hours
- 24 Hours (default)
- 48 Hours
- 1 Week (168 hours)

### Chart Configuration
- **Responsive**: Automatically adjusts to screen size
- **Interactive**: Hover for detailed information
- **Color-coded**: Different colors for each metric
- **Time-axis**: Proper time formatting and scaling

## Integration with Daemon

The charts feature works seamlessly with the MPP-Solar daemon:

1. **Daemon collects data** every 15 minutes
2. **Stores in Prometheus files** in `/path/to/your/mpp-solar/prometheus/`
3. **Charts read historical data** from these files
4. **Real-time updates** from the web interface API

### Required Setup
- Daemon service running: `./manage_daemon.sh status`
- Prometheus files being created: `ls -la prometheus/`
- Web interface running: `./manage_web.sh status`

## Troubleshooting

### No Charts Displaying
1. **Check daemon status**:
   ```bash
   ./manage_daemon.sh status
   ```

2. **Verify Prometheus files exist**:
   ```bash
   ls -la prometheus/
   ```

3. **Check web interface logs**:
   ```bash
   ./manage_web.sh logs
   ```

4. **Test historical API**:
   ```bash
   curl "http://localhost:5000/api/historical?hours=24"
   ```

### Charts Not Updating
1. **Check if daemon is collecting data**:
   ```bash
   tail -f mpp-solar.log
   ```

2. **Verify file permissions**:
   ```bash
   ls -la prometheus/
   ```

3. **Restart web interface**:
   ```bash
   ./manage_web.sh restart
   ```

### Performance Issues
- **Large time ranges** (1 week) may load slowly
- **Many data points** can affect chart rendering
- **Browser memory** usage increases with more data

## Browser Compatibility

### Supported Browsers
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

### Requirements
- JavaScript enabled
- Modern browser (ES6+ support)
- Chart.js library loads from CDN

## Customization

### Adding New Charts
To add new chart types:

1. **Add new tab** in `templates/charts.html`
2. **Create chart canvas** with unique ID
3. **Initialize chart** in JavaScript
4. **Map data** from historical API response

### Modifying Chart Colors
Edit the `borderColor` and `backgroundColor` properties in the chart initialization:

```javascript
{
    label: 'Battery Voltage (V)',
    borderColor: '#ffc107',
    backgroundColor: 'rgba(255, 193, 7, 0.1)',
    data: []
}
```

### Changing Time Formats
Modify the time display formats in the chart configuration:

```javascript
time: {
    displayFormats: {
        hour: 'HH:mm',
        minute: 'HH:mm',
        second: 'HH:mm:ss'
    }
}
```

## Data Export

### Exporting Chart Data
You can export the historical data via the API:

```bash
# Export last 24 hours as JSON
curl "http://localhost:5000/api/historical?hours=24" > data_24h.json

# Export last week as JSON
curl "http://localhost:5000/api/historical?hours=168" > data_week.json
```

### Using with External Tools
The historical data API can be used with:
- **Grafana**: As a data source
- **Excel**: Import JSON data
- **Python**: Parse with pandas
- **Custom scripts**: Process the JSON response

## Security Notes

- Charts page is accessible to anyone with access to the web interface
- Historical data contains sensitive system information
- Consider implementing authentication for production use
- Data is stored locally on your system

## Support

For issues with the charts feature:
1. Check the web interface logs: `./manage_web.sh logs`
2. Verify daemon is running: `./manage_daemon.sh status`
3. Test API endpoints manually
4. Check browser console for JavaScript errors
5. Ensure Prometheus files are being created

## Future Enhancements

Potential improvements:
- **Export charts as images**
- **Custom date range selection**
- **Multiple device support**
- **Alert thresholds on charts**
- **Data aggregation (hourly/daily averages)**
- **Zoom and pan functionality**
- **Chart annotations**
