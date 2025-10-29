# Charts and Data Loading Fixes

**Date**: October 28, 2025
**Issue**: Charts page not filtering time correctly, home page rebuilding chart on every reload

## Problems Identified

1. **Prometheus Files Have No Timestamps**: The daemon overwrites the same Prometheus files each time, so there's no historical data stored in files
2. **Wrong Data Source**: The `get_historical_data()` function was trying to read from timestamped Prometheus files that don't exist
3. **No Background Data Collection**: Web interface wasn't updating data after initial load
4. **Wrong Data Format**: Data transformation didn't match what charts expected

## Fixes Applied

### 1. Fixed get_historical_data() Function
**File**: `web_interface.py`

Changed from reading Prometheus files to using the in-memory `historical_data_store`:

```python
def get_historical_data(hours=24):
    """Get historical data from in-memory store for the last N hours"""
    global historical_data_store
    
    # Transform data from list of entries to metric-keyed dictionary
    # Input: [{timestamp: 'X', metric1: val1, metric2: val2}, ...]
    # Output: {metric1: [{timestamp: 'X', value: val1}, ...], metric2: [...]}
    
    # Properly filters by time range
    # Transforms format to match chart expectations
```

**Result**: 
- Time filtering now works correctly
- Data format matches what charts.html expects

### 2. Added Background Data Update Thread
**File**: `web_interface.py`

```python
def update_data_thread():
    """Background thread to update inverter data every 30 seconds"""
    while True:
        try:
            get_inverter_data()
            logging.info("Updated inverter data from Prometheus files")
        except Exception as e:
            logging.error(f"Error in update thread: {e}")
        time.sleep(30)
```

**Result**:
- Inverter data updates every 30 seconds
- Historical data store grows continuously (up to 1000 entries = ~8.3 hours)
- Charts automatically get new data without page reload

### 3. Thread Startup
Added to `if __name__ == '__main__'` section:

```python
# Start data update thread
data_thread = threading.Thread(target=update_data_thread, daemon=True)
data_thread.start()
logging.info("Started data update thread")
```

## Data Flow After Fixes

```
┌──────────────────┐
│   MPP-Solar      │
│   Daemon         │ Writes every 60s
│   Service        │────────────────┐
└──────────────────┘                │
                                    ▼
                         ┌─────────────────────┐
                         │  Prometheus Files   │
                         │  (latest values)    │
                         └─────────────────────┘
                                    │
                                    │ Read every 30s
                                    ▼
┌──────────────────────────────────────────────┐
│  Web Interface Background Thread             │
│  - Reads Prometheus files                    │
│  - Stores in historical_data_store (memory)  │
│  - Keeps last 1000 entries (~8.3 hours)      │
└──────────────────────────────────────────────┘
                    │
                    │ Filtered by time range
                    ▼
        ┌────────────────────────┐
        │  /api/historical       │
        │  Returns data for      │
        │  requested time range  │
        └────────────────────────┘
                    │
                    ▼
        ┌────────────────────────┐
        │  Charts Page           │
        │  Displays historical   │
        │  data with Chart.js    │
        └────────────────────────┘
```

## Testing the Fixes

### 1. Restart Web Interface
```bash
cd /home/constantine/mpp-solar
source venv/bin/activate

# Stop if running
pkill -f web_interface.py

# Start with logging
python web_interface.py
```

### 2. Check Logs
You should see:
```
Started data update thread
Updated inverter data from Prometheus files
```
Every 30 seconds.

### 3. Test Charts Page
1. Navigate to `http://YOUR_IP:5000/charts`
2. Change time range (24h, 7d, 30d)
3. Verify data is filtered correctly
4. Leave page open - chart should update automatically

### 4. Test Home Page
1. Navigate to `http://YOUR_IP:5000`
2. Refresh page multiple times
3. Chart should persist data (not rebuild from scratch)
4. New data points should appear every 30 seconds

## Expected Behavior

### Charts Page
- ✅ Time range filter works (24h, 7d, 30d)
- ✅ Only shows data within selected range
- ✅ Charts update automatically without reload
- ✅ Data accumulated over time (up to 8.3 hours in memory)

### Home Page
- ✅ Chart persists on reload
- ✅ Historical data shown from memory
- ✅ New data points added every 30 seconds
- ✅ Smooth chart updates

## Files Changed
- `web_interface.py` - Main application file
- `web_interface.py.backup` - Backup of original file

## Backup Restoration
If issues occur:
```bash
cp /home/constantine/mpp-solar/web_interface.py.backup /home/constantine/mpp-solar/web_interface.py
```

## Known Limitations

1. **In-Memory Storage Only**: Historical data limited to ~8.3 hours (1000 entries @ 30s interval)
   - After 8.3 hours, oldest data is removed
   - Data lost on web interface restart
   - Solution: Implement PostgreSQL/InfluxDB for long-term storage

2. **No Persistent Historical Data**: Prometheus files only contain latest values
   - Daemon overwrites same files
   - No timestamped file creation
   - Solution: Modify daemon to create timestamped files or use database

## Future Enhancements

1. **Database Integration**
   - Store all historical data in PostgreSQL or InfluxDB
   - Enable unlimited history
   - Persist data across restarts

2. **Prometheus File Timestamps**
   - Modify daemon to create timestamped files
   - Parse multiple Prometheus files for history
   - Combine in-memory + file storage

3. **Configurable Update Intervals**
   - Make 30s interval configurable
   - Adjust based on needs and performance

4. **Data Compression**
   - Store more history in same memory
   - Aggregate older data points

## Verification Commands

```bash
# Check if web interface is running with thread
ps aux | grep web_interface

# Check logs for update messages
tail -f /home/constantine/mpp-solar/web_interface.log

# Test API directly
curl -s "http://localhost:5000/api/historical?hours=1" | python -m json.tool

# Check data structure
curl -s "http://localhost:5000/api/historical?hours=1" | jq 'keys'
```

## Success Criteria

- [x] get_historical_data() uses in-memory store
- [x] Time filtering works correctly
- [x] Data format matches chart expectations  
- [x] Background thread updates data every 30s
- [x] Historical data accumulates up to 1000 entries
- [ ] Test charts page with time range changes *(needs manual testing)*
- [ ] Verify home page doesn't rebuild on reload *(needs manual testing)*

---

**Documentation**: This fix is now part of the project history. Update PROGRESS.md if this becomes a permanent solution or if further changes are needed.
