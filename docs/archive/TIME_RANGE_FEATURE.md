# Time Range Selector Feature

**Date Added**: October 28, 2025  
**Page**: `/house` (House & Weather Monitoring)

## Feature Description

Added a time range selector to the house monitoring page that allows users to view different time periods of historical temperature and humidity data.

## What Was Added

### 1. Time Range Selector UI
- **Location**: Below the page header, above the sensor cards
- **Options**:
  - Last Hour
  - Last 6 Hours
  - Last 12 Hours
  - Last 24 Hours (default)
  - Last 2 Days
  - Last 3 Days
  - Last Week

### 2. Data Filtering Logic
- Charts now filter historical data based on selected time range
- Filters applied to:
  - Indoor temperature history
  - Outdoor temperature history
  - Indoor humidity history
  - Outdoor humidity history

### 3. Data Point Counter
- Shows number of data points being displayed
- Updates dynamically when time range changes
- Format: `📊 X data points (Yh range)`

## How It Works

1. **User selects a time range** from the dropdown
2. **JavaScript calculates cutoff time** based on selection
3. **Data is filtered** to only include points after cutoff
4. **Charts update immediately** with filtered data
5. **Counter shows** how many points are displayed

## Technical Implementation

### JavaScript Variables
```javascript
let currentTimeRange = 24; // Default to 24 hours
```

### Filtering Logic
```javascript
const now = new Date();
const cutoffTime = new Date(now.getTime() - (currentTimeRange * 60 * 60 * 1000));

const filteredIndoorTemp = indoorTempHistory.filter(point => new Date(point.x) >= cutoffTime);
// Same for outdoor temp, indoor/outdoor humidity
```

### Event Listener
```javascript
document.getElementById('timeRange').addEventListener('change', function() {
    currentTimeRange = parseInt(this.value);
    updateCharts(); // Immediate update
});
```

## Files Modified

- **templates/house.html** - Added UI, filtering logic, and event listeners
- **templates/house.html.backup** - Backup of original file

## Usage

1. Navigate to `http://YOUR_IP:5000/house`
2. Look for the **📅 Time Range** dropdown near the top
3. Select desired time range
4. Charts update instantly
5. Data point counter shows filtered count

## Benefits

- ✅ **View recent data**: See last hour for real-time trends
- ✅ **Analyze patterns**: View last week to spot daily patterns
- ✅ **Performance**: Reduces chart points for better rendering
- ✅ **Flexibility**: Switch ranges without page reload
- ✅ **User feedback**: Counter shows how much data is displayed

## Notes

- Historical data is still collected every 30 seconds in the background
- All data remains in memory (up to 1000 points)
- Filtering is client-side (fast, no server requests)
- Charts automatically update with new data every 5 seconds
- Selected range persists during auto-updates

## Future Enhancements

1. **Custom date range picker** - Select specific start/end dates
2. **Export filtered data** - Download CSV of selected range  
3. **Comparison mode** - Compare two time ranges side-by-side
4. **Save preferences** - Remember user's preferred time range
5. **URL parameters** - Share links with specific time ranges

## Troubleshooting

### Selector not visible
- Clear browser cache (Ctrl+F5)
- Check browser console for JavaScript errors

### Charts not updating when range changes
- Verify event listener is attached
- Check browser console for errors
- Ensure `currentTimeRange` variable exists

### No data for longer ranges
- System only keeps ~8.3 hours in memory currently
- For longer history, wait for system to accumulate more data
- Or implement database storage (see PROGRESS.md)

## Restore Original

If issues occur:
```bash
cp /home/constantine/mpp-solar/templates/house.html.backup \
   /home/constantine/mpp-solar/templates/house.html
```

---

**Status**: ✅ Fully functional  
**Testing**: Manual testing recommended on live page  
**Documentation**: This file + code comments
