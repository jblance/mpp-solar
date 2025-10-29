# Prometheus Data Export to CSV

## Export Complete! ✅

### File Location
**Path:** `/home/constantine/prometheus_export.csv`
**Size:** 6.3 MB

### Data Summary
- **Total rows:** 41,469 (including header)
- **Date range:** August 25, 2025 to October 29, 2025
- **Columns:** 41 total (timestamp + 40 metrics)
- **Source files processed:** 44,725 Prometheus files

### Data Sources
- **House sensors:** 776 files (temperature, humidity, pressure)
- **Weather sensors:** 3,563 files (temperature, humidity, pressure, wind, rain)
- **Inverter sensors:** 40,386 files (voltage, power, frequency, etc.)

### Metrics Included

#### House Sensors (3 metrics)
- `house_humidity` - Indoor humidity (%)
- `house_pressure` - Indoor pressure (hPa)
- `house_temperature` - Indoor temperature (°C)

#### Weather Sensors (6 metrics)
- `weather_humidity` - Outdoor humidity (%)
- `weather_pressure` - Outdoor pressure (hPa)
- `weather_temperature` - Outdoor temperature (°C)
- `weather_wind_speed` - Wind speed (m/s)
- `weather_wind_direction` - Wind direction (degrees)
- `weather_rain` - Rain amount (mm)

#### Inverter Sensors (30+ metrics)
- AC input/output voltage
- AC input/output frequency
- Active/apparent power
- Battery voltage/current
- Battery charging/discharging current
- Load percentage
- PV input current/voltage
- Temperature readings
- Device status codes
- And more...

### CSV Format

**Header row:**
```
timestamp,house_humidity,house_pressure,house_temperature,...
```

**Data rows:**
```
2025-10-29T11:49:00,42.5,968.2,18.3,...
```

- Timestamp in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- Missing values are empty (not zero)
- All numeric values are floats

### Usage Examples

#### Open in Excel/LibreOffice
Simply double-click the file or import as CSV:
- Delimiter: comma (,)
- Encoding: UTF-8
- First row contains headers

#### Python Analysis
```python
import pandas as pd

# Load the CSV
df = pd.read_csv('/home/constantine/prometheus_export.csv', 
                  parse_dates=['timestamp'])

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# Show summary statistics
print(df.describe())

# Plot temperature over time
df[['house_temperature', 'weather_temperature']].plot()

# Filter by date range
oct_data = df['2025-10-01':'2025-10-31']

# Check data availability
print(df.notna().sum())  # Count non-missing values per column
```

#### Analysis Tips
```python
# Resample to hourly averages
hourly = df.resample('1H').mean()

# Calculate daily min/max
daily_stats = df.resample('1D').agg(['min', 'max', 'mean'])

# Find correlations
correlations = df.corr()

# Export specific columns
df[['house_temperature', 'weather_temperature']].to_csv('temps.csv')
```

### Re-export Data

To re-export (e.g., after collecting more data):
```bash
cd /home/constantine
python3 export_prometheus_to_csv.py
```

This will overwrite the existing CSV with updated data.

### Data Gaps

Not all metrics are present at all timestamps:
- House sensors: Updated every ~5 minutes
- Weather sensors: Updated every ~5 minutes
- Inverter sensors: Updated every ~1 minute

Use pandas `.fillna()` or `.interpolate()` to handle missing values if needed.

### File Size Considerations

Current export: **6.3 MB** (41,469 rows × 41 columns)

If the file gets too large:
1. **Filter by date range** - Modify the export script to limit date range
2. **Select specific metrics** - Export only needed columns
3. **Compress the file:** `gzip prometheus_export.csv` (reduces to ~1-2 MB)
4. **Split into multiple files** - One per month or sensor type

### Backup

The export script can be run anytime without affecting the original Prometheus files. The source data remains in:
```
/home/constantine/mpp-solar/prometheus/
```

### Automation

To export automatically (e.g., daily):
```bash
# Add to crontab
0 2 * * * cd /home/constantine && python3 export_prometheus_to_csv.py
```

This exports all data daily at 2 AM.

### Troubleshooting

**Script location:** `/home/constantine/export_prometheus_to_csv.py`

**Re-run manually:**
```bash
python3 /home/constantine/export_prometheus_to_csv.py
```

**Check progress:**
The script prints progress every 100 files processed.

**Verify output:**
```bash
# Check file size
ls -lh /home/constantine/prometheus_export.csv

# Count rows
wc -l /home/constantine/prometheus_export.csv

# View first few rows
head -5 /home/constantine/prometheus_export.csv

# View last few rows
tail -5 /home/constantine/prometheus_export.csv
```

## Summary

✅ **Export complete:** 6.3 MB CSV file in home directory
✅ **Data span:** Aug 25 - Oct 29, 2025 (2+ months)
✅ **Metrics:** 40 different sensor readings
✅ **Format:** Ready for Excel, Python, R, or any data analysis tool
✅ **Re-runnable:** Script can be run again anytime

Your complete sensor history is now available in a single CSV file!
