# House Page Data Loading Diagnosis

## Current Situation

Your system is working correctly! Here's what's happening:

### Timeline:
- **11:11-11:13**: Last historical data points loaded from Prometheus files
- **11:15**: Web server restarted (loaded files created before 11:15)
- **11:26-11:31**: New Prometheus files being created (NOT loaded yet)
- **Current**: Live data is being fetched every 30 seconds via `/api/house` and `/api/weather`

### Why It Looks Like Data Stopped:

The **historical data** loaded from server shows points up to 11:11-11:13 because:
1. Server was restarted at 11:15
2. It loaded Prometheus files that existed at that time
3. New files created after 11:15 haven't been loaded into server memory

However, **live data IS updating** every 30 seconds via MQTT!

## Verify Live Updates Are Working

### In Browser Console (F12):

```javascript
// Check how many points are currently loaded
console.log('Indoor temp points:', indoorTempHistory.length);
console.log('Outdoor temp points:', outdoorTempHistory.length);

// Check the last few timestamps
if (indoorTempHistory.length > 0) {
    const last5 = indoorTempHistory.slice(-5);
    console.log('Last 5 indoor temp points:');
    last5.forEach(p => console.log(`  ${p.x.toLocaleTimeString()}: ${p.y}°C`));
}

// Watch for new data being added
setInterval(() => {
    console.log(`[${new Date().toLocaleTimeString()}] Points: ${indoorTempHistory.length}`);
}, 10000); // Log every 10 seconds
```

### Check Live API:

```bash
# Run this multiple times, 30 seconds apart
curl -s http://localhost:5000/api/house | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"Temp: {d['temperature']}°C at {d['temperature_time']}\")"

# Wait 30 seconds and run again - timestamp should update
```

## Solutions

### Option 1: Restart Server (Loads Latest Files)
```bash
cd /home/constantine/mpp-solar
./manage_web.sh restart
```

After restart:
- Historical data will include files up to 11:31
- Live updates continue every 30 seconds
- Charts will show more complete history

### Option 2: Just Wait (Live Updates Working)
- Charts ARE updating with new live data every 30 seconds
- Historical gap (11:11 to 11:15) will remain until restart
- This is normal behavior - historical data loaded once on startup

### Option 3: Implement Auto-Reload (Future Enhancement)
Add periodic reloading of historical data (every 5-10 minutes) so new Prometheus files are picked up without restart.

## What's Actually Happening Now

✅ **MQTT data arriving**: Every ~5 minutes
✅ **Live API updating**: Data from 11:26-11:31 available
✅ **Frontend fetching**: Every 30 seconds via `fetchData()`
✅ **Charts updating**: New points being added to history
✅ **Prometheus files**: Being created (11:31 was latest)

❌ **Server memory**: Only has historical files from before 11:15
❌ **Chart gap**: Historical data stops at 11:11, live data starts at 11:26

## Recommended Action

**Restart the web server** to load the latest historical files:

```bash
cd /home/constantine/mpp-solar
./manage_web.sh restart

# Then reload /house page in browser
```

You'll see:
- Historical data up to 11:31
- Live data continuing to update
- No more gaps!

## Check If It's Really Updating

Open /house page and run in console:

```javascript
// Before page reload, check last point
const before = indoorTempHistory[indoorTempHistory.length - 1];
console.log('Before:', before);

// Wait 60 seconds...

// After fetch cycles, check again
const after = indoorTempHistory[indoorTempHistory.length - 1];
console.log('After:', after);

// If timestamps are different, it's working!
console.log('Updated?', before.x !== after.x);
```

## Expected Behavior

**On page load:**
- Historical data: From server (up to time of last restart)
- Shown immediately

**Every 30 seconds after:**
- Live data: From `/api/house` and `/api/weather`
- Added to charts
- Saved to localStorage

**Result:**
- Continuous data stream
- May have gaps from server restarts
- Restart server to fill gaps with new Prometheus files
