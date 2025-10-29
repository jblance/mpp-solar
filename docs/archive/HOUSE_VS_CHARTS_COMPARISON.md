# /house vs /charts Page Comparison

## How /charts Works (Reference Implementation)

### Initialization
```javascript
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();     // Create Chart objects
    updateChartData();      // Fetch from /api/historical and update
    // Set up event listeners and intervals
});
```

### Data Flow
1. Page loads → waits for DOM ready
2. `initializeCharts()` → creates Chart.js objects with empty data
3. `updateChartData()` → fetches from `/api/historical?hours=X`
4. Data returned → stored in `historicalData` variable
5. `updateCharts()` → populates charts with `getChartData(metric)`
6. Charts display immediately with server-stored historical data

## How /house Now Works (After Fixes)

### Initialization
```javascript
document.addEventListener('DOMContentLoaded', function() {
    initCharts();              // Create Chart objects
    loadFromLocalStorage();    // Load saved data + update display
    loadHistoricalData();      // No-op (no server API for house data)
    fetchData();               // Fetch live data from /api/house & /api/weather
    // Set up event listeners and intervals
});
```

### Data Flow
1. Page loads → waits for DOM ready ✅
2. `initCharts()` → creates Chart.js objects with empty data ✅
3. `loadFromLocalStorage()` → loads from browser storage ✅
   - If data exists → populates history arrays ✅
   - Calls `updateChartsDisplay()` → charts show data immediately ✅
4. `fetchData()` → gets current data every 30 seconds ✅
5. `updateCharts()` → adds new points + saves to localStorage ✅

## Key Differences

### Data Source
- **/charts**: Server database (`/api/historical`) - persistent across all sessions
- **/house**: Browser localStorage - persistent per browser only

### Historical Data
- **/charts**: Loads months of data from server
- **/house**: Loads up to 100 data points from localStorage (max ~50 minutes)

### Server API
- **/charts**: `/api/historical?hours=X` returns historical inverter data
- **/house**: No historical API - `/api/house` and `/api/weather` return only current values

## Changes Made to /house

### 1. DOMContentLoaded Wrapper ✅
```javascript
// OLD: Ran immediately (charts might not be ready)
initCharts();

// NEW: Waits for DOM (like /charts)
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
});
```

### 2. localStorage Functions ✅
```javascript
loadFromLocalStorage()  // Load + update display
saveToLocalStorage()    // Save after each update
```

### 3. Display Update Function ✅
```javascript
updateChartsDisplay()   // Refresh charts from history arrays
```

### 4. Debug Logging ✅
Comprehensive console logging with `[localStorage]` and `[updateChartsDisplay]` tags

## Testing Checklist

### Initial Test (First Visit)
1. ✅ Open /house page
2. ✅ Console shows: `[localStorage] No saved data found`
3. ✅ Charts start empty
4. ✅ After 30s: New data point appears
5. ✅ After 2-3 minutes: Charts show growing line

### Reload Test (Persistence)
1. ✅ Wait 2-3 minutes on /house
2. ✅ Reload page (Ctrl+R or F5)
3. ✅ Console shows: `[localStorage] Found saved data: {indoorTemp: X, ...}`
4. ✅ Console shows: `[localStorage] Loaded X historical data points`
5. ✅ Console shows: `[updateChartsDisplay] ✓ Charts updated successfully`
6. ✅ Charts immediately show previous data

### Time Range Test
1. ✅ Change time range selector (1h, 2h, 4h, 8h, 12h, 24h)
2. ✅ Console shows: `[updateChartsDisplay] Filtering data for X hour range`
3. ✅ Charts update to show selected time range

## Browser Console Commands

### Check if data exists:
```javascript
localStorage.getItem('houseChartData')
```

### View saved data:
```javascript
JSON.parse(localStorage.getItem('houseChartData'))
```

### Clear data (start fresh):
```javascript
localStorage.removeItem('houseChartData');
location.reload();
```

### Check data point count:
```javascript
const data = JSON.parse(localStorage.getItem('houseChartData'));
console.log({
    indoorTemp: data?.indoorTemp?.length || 0,
    outdoorTemp: data?.outdoorTemp?.length || 0,
    indoorHum: data?.indoorHum?.length || 0,
    outdoorHum: data?.outdoorHum?.length || 0
});
```

## Expected Console Output

### On Page Load (with saved data):
```
[localStorage] Checking for saved data...
[localStorage] Found saved data: {indoorTemp: 15, outdoorTemp: 15, ...}
[localStorage] Loaded 15 historical data points
[localStorage] Charts exist, updating display...
[updateChartsDisplay] Filtering data for 1 hour range
[updateChartsDisplay] History arrays: {indoorTemp: 15, outdoorTemp: 15, ...}
[updateChartsDisplay] Filtered to: {indoorTemp: 15, outdoorTemp: 15, ...}
[updateChartsDisplay] ✓ Charts updated successfully
```

### On Page Load (no saved data):
```
[localStorage] Checking for saved data...
[localStorage] No saved data found (first visit or cleared)
```

### After fetchData() updates:
```
// (no console output from updateCharts by default)
// Data is added and saved silently every 30 seconds
```

## Why /house Can't Work Exactly Like /charts

1. **No Server API**: There's no `/api/house_historical` endpoint
2. **Real-time Only**: `/api/house` and `/api/weather` return only current values
3. **MQTT-based**: Data comes from MQTT topics, not stored in database
4. **Client-side Storage**: localStorage is limited to ~5-10MB per domain

## Future Enhancement: Server-side Storage

To make /house work exactly like /charts:

1. Create database table for house/weather sensors
2. Add `/api/house_historical?hours=X` endpoint
3. Store MQTT data in database (like inverter data)
4. Load from server on page load
5. Keep localStorage as fallback/cache

## Summary

✅ **What's Fixed:**
- DOMContentLoaded wrapper ensures proper initialization
- localStorage persistence works correctly
- Charts display loaded data immediately
- Debug logging helps troubleshoot issues

⚠️ **Limitations:**
- Max ~100 data points (~50 minutes at 30s intervals)
- Data doesn't persist across browsers/devices
- No long-term historical view like /charts

✅ **Current Behavior:**
- First visit: Charts fill as data arrives
- Subsequent visits: Charts show previous data immediately
- Works like /charts within localStorage constraints
