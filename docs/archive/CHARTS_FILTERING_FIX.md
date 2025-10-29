# Charts Page Time Filtering Fix

## Problem
The /charts page was stuck showing a 24-hour window regardless of the selected time range filter.

## Root Cause
Two issues were found:

1. **Aggressive Fallback Logic**: The code would fallback to `/api/historical/all` (all data) if fewer than 3 data points were returned, even when the filtered data was valid.

2. **No Client-Side Filtering**: The `getChartData()` function didn't filter data by time on the client side, so even when the correct amount of data was fetched, it would display all of it.

## Changes Made

### 1. Added Client-Side Time Filtering

**Before:**
```javascript
function getChartData(metricName) {
    if (!historicalData[metricName]) return [];
    
    return historicalData[metricName].map(item => ({
        x: new Date(item.timestamp),
        y: item.value
    }));
}
```

**After:**
```javascript
function getChartData(metricName) {
    if (!historicalData[metricName]) return [];
    
    // Get selected time range
    const hours = parseInt(document.getElementById('timeRange').value);
    const now = new Date();
    const cutoffTime = new Date(now.getTime() - (hours * 60 * 60 * 1000));
    
    // Filter and map data
    return historicalData[metricName]
        .map(item => ({
            x: new Date(item.timestamp),
            y: item.value
        }))
        .filter(item => item.x >= cutoffTime);
}
```

### 2. Fixed Fallback Logic

**Before:**
```javascript
// If filtered endpoint returns insufficient data, fallback to all data
if (hours < 168 && dataPoints < 3) {
    console.log(`Insufficient data for ${hours}h filter (${dataPoints} points), falling back to all data`);
    return fetch('/api/historical/all').then(response => response.json());
}
```

**After:**
```javascript
// Only fallback to all data if we have NO data at all
if (dataPoints === 0) {
    console.log(`No data returned for ${hours}h filter, falling back to all data`);
    return fetch('/api/historical/all').then(response => response.json());
}
```

## How It Works Now

1. **User selects time range** (1h, 2h, 4h, 8h, 12h, 24h, 7d)
2. **Frontend fetches** from `/api/historical?hours=X`
3. **Server filters** data to last X hours
4. **Frontend receives** filtered data
5. **Client-side applies additional filtering** to ensure exact time window
6. **Charts update** with correctly filtered data

## Testing

### Test All Time Ranges:

1. Open /charts page
2. Try each time range option:
   - **1 hour** - Should show last hour only
   - **2 hours** - Should show last 2 hours
   - **4 hours** - Should show last 4 hours  
   - **8 hours** - Should show last 8 hours
   - **12 hours** - Should show last 12 hours
   - **24 hours** - Should show last 24 hours
   - **7 days (168h)** - Should show last 7 days

3. **Check in browser console:**
   - Open DevTools (F12)
   - Select different time ranges
   - Watch network requests
   - Verify correct endpoint is called

### Verify Filtering Works:

In browser console after selecting 1 hour:
```javascript
// Check first chart's data
const firstMetric = Object.keys(historicalData)[0];
const data = historicalData[firstMetric];
console.log('Total points:', data.length);

const filtered = getChartData(firstMetric);
console.log('Filtered points:', filtered.length);

// Check time span
if (filtered.length > 0) {
    const oldest = new Date(filtered[0].x);
    const newest = new Date(filtered[filtered.length - 1].x);
    const hoursDiff = (newest - oldest) / (1000 * 60 * 60);
    console.log('Time span (hours):', hoursDiff.toFixed(2));
}
```

## Benefits

✅ **Accurate Time Filtering**: Charts now show exactly the selected time range
✅ **Server + Client Filtering**: Double-layer ensures correctness
✅ **Smart Fallback**: Only uses all data when absolutely no data is available
✅ **Better UX**: Time range selector works as expected

## Files Modified

- `templates/charts.html` - Fixed `getChartData()` and fallback logic

## No Server Restart Required

This is a pure frontend fix - just hard refresh your browser:
- **Chrome/Firefox/Edge**: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
- **Or**: Clear browser cache and reload

## Rollback

If issues occur:
```bash
cd /home/constantine/mpp-solar
git checkout templates/charts.html
# Or restore from backup if it exists
cp templates/charts.html.backup templates/charts.html
```

## Notes

- The 7-day view still uses `/api/historical/all` endpoint (by design)
- Client-side filtering provides an extra safety layer
- This fix is compatible with all existing server-side filtering
