# Chart Fixes Implementation Plan

## Project Overview

This plan addresses three critical issues affecting the MPP-Solar web interface charts functionality:

1. **Issue #1**: `/charts` page always reloads all data on server reload (no client-side caching)
2. **Issue #2**: `/charts` time range filtering doesn't work properly due to fallback mechanism
3. **Issue #3**: `/house` page displays updated data in top boxes but doesn't render charts properly

All fixes will maintain compatibility with existing data flow, preserve Prometheus file-based data storage, and ensure graceful degradation.

## Current Architecture Analysis

### Data Flow
```
Prometheus Files → Web Interface Startup → In-Memory Store (historical_data_store)
                                         ↓
                                    API Endpoints → Frontend Charts
```

### Key Components
- **Backend**: `web_interface.py`
  - `load_historical_prometheus_data()` (lines 61-91): Loads inverter data on startup
  - `load_historical_house_weather_data()` (lines 108-199): Loads house/weather data
  - `get_historical_data()` (lines 365-401): Returns filtered time-range data
  - `/api/historical` endpoint (lines 430-435): Serves inverter historical data
  - `/api/house_historical` endpoint (lines 482-500): Serves house/weather data

- **Frontend**:
  - `templates/charts.html`: Inverter charts page (~823 lines)
  - `templates/house.html`: House/weather charts page (~743 lines)

### Problem Analysis

#### Issue #1: No Client-Side Caching
**Location**: `templates/charts.html`
**Current Behavior**:
- Every page load fetches data via `/api/historical?hours=24`
- No browser caching headers
- No localStorage/sessionStorage persistence
- Lines 607-616: Fallback mechanism fetches ALL data if filtered result is empty

**Impact**:
- Slow page loads
- Unnecessary server load
- Poor UX on page refresh

#### Issue #2: Time Range Filtering Broken
**Location**: `templates/charts.html` lines 607-616
**Current Code**:
```javascript
if (dataPoints === 0) {
    console.log(`No data returned for ${hours}h filter, falling back to all data`);
    return fetch('/api/historical/all')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        });
}
```

**Problem**:
- Selecting "1 hour" can show days of data
- User expectation: see 1 hour of data OR "no data available" message
- Actual behavior: silently falls back to ALL data

#### Issue #3: House Page Chart Rendering
**Location**: `templates/house.html`
**Current Behavior**:
- Top boxes update correctly (live MQTT data)
- Charts don't populate with historical data from server
- Race condition suspected: charts may not be initialized when `loadHistoricalData()` runs

**Analysis**:
- Line 718: `initCharts()` called in DOMContentLoaded
- Line 726: `loadHistoricalData()` called immediately after
- Both are async but not properly sequenced
- Console logging shows data loads but charts don't update

## Objectives and Milestones

### Milestone 1: Fix /charts Time Range Filtering (Issue #2)
**Priority**: HIGH (breaks user expectations)
**Branch**: `fix/charts-time-range-filtering`
**Success Criteria**:
- ✅ Selecting "1 hour" shows ONLY last 1 hour of data
- ✅ If no data available for range, show clear message
- ✅ Remove automatic fallback to all data
- ✅ Add user option to manually request "all available data"
- ✅ Test all time ranges: 1h, 6h, 12h, 24h, 48h, 168h

### Milestone 2: Fix /house Page Chart Rendering (Issue #3)
**Priority**: HIGH (charts completely broken)
**Branch**: `fix/house-chart-rendering`
**Success Criteria**:
- ✅ Charts populate with historical data on page load
- ✅ Charts update when new live data arrives
- ✅ Time range selector works correctly
- ✅ No race conditions between chart init and data load
- ✅ Proper error handling if API fails

### Milestone 3: Add Client-Side Caching (Issue #1)
**Priority**: MEDIUM (performance optimization)
**Branch**: `feature/charts-client-caching`
**Success Criteria**:
- ✅ Page reload uses cached data if less than 5 minutes old
- ✅ Manual refresh bypasses cache
- ✅ Cache invalidates on time range change
- ✅ Cache includes metadata (timestamp, range)
- ✅ Graceful fallback if cache corrupted
- ✅ Storage size limits respected (max 5MB)

## Technical Implementation Details

### Fix #1: Time Range Filtering (Issue #2)

**Files to Modify**:
- `templates/charts.html`

**Changes**:
1. **Remove fallback mechanism** (lines 607-616):
   ```javascript
   // DELETE THIS:
   if (dataPoints === 0) {
       console.log(`No data returned for ${hours}h filter, falling back to all data`);
       return fetch('/api/historical/all')...
   }
   ```

2. **Add proper empty state handling**:
   ```javascript
   if (dataPoints === 0) {
       console.log(`No data available for ${hours}h time range`);
       dataSummaryDiv.innerHTML = `
           <div class="alert alert-info d-flex align-items-center justify-content-between">
               <div>
                   <i class="fas fa-info-circle me-2"></i>
                   <strong>No data available for selected time range.</strong>
                   <br>
                   <small>Try selecting a longer time range or wait for data to be collected.</small>
               </div>
               <button class="btn btn-sm btn-primary" id="loadAllDataBtn">
                   <i class="fas fa-database"></i> Load All Available Data
               </button>
           </div>
       `;

       // Add event listener for manual "load all" button
       document.getElementById('loadAllDataBtn')?.addEventListener('click', () => {
           fetch('/api/historical/all')
               .then(response => response.json())
               .then(data => {
                   historicalData = data;
                   updateCharts();
                   updateDataSummary();
               });
       });
       return;
   }
   ```

3. **Update getChartData() to respect time range** (line 740-755):
   - Already correct - client-side filtering working properly
   - Just needs the fallback removed

**Testing Plan**:
1. Set time range to 1 hour with no recent data → should show "no data" message
2. Click "Load All Available Data" → should populate charts with all data
3. Change time range back to 24 hours → should re-filter existing data
4. Verify all time ranges work correctly

### Fix #2: House Page Chart Rendering (Issue #3)

**Files to Modify**:
- `templates/house.html`

**Root Cause**:
The issue is a timing/sequencing problem in the initialization flow:
```javascript
// Current code (line 718-738)
document.addEventListener('DOMContentLoaded', function() {
    initCharts();                  // Creates chart objects
    loadFromLocalStorage();        // Tries to update charts (might work)
    loadHistoricalData();          // Async - fetches from server
    fetchData();                   // Async - fetches live data
    // ... event listeners
    setInterval(fetchData, 30000);
});
```

**Problem**: `loadHistoricalData()` is async but not awaited, so the charts might not exist when data arrives.

**Changes**:

1. **Make initialization properly async** (lines 717-739):
   ```javascript
   document.addEventListener('DOMContentLoaded', async function() {
       console.log('[Init] Starting initialization...');

       // Step 1: Initialize charts FIRST
       initCharts();
       console.log('[Init] ✓ Charts created');

       // Step 2: Load cached data (synchronous)
       loadFromLocalStorage();
       console.log('[Init] ✓ localStorage loaded');

       // Step 3: Load historical data from server (async - WAIT for it)
       try {
           await loadHistoricalData();
           console.log('[Init] ✓ Historical data loaded and charts updated');
       } catch (error) {
           console.error('[Init] Failed to load historical data:', error);
       }

       // Step 4: Fetch live data
       fetchData();
       console.log('[Init] ✓ Live data fetch initiated');

       // Step 5: Setup event listeners
       document.getElementById('timeRange').addEventListener('change', function() {
           currentTimeRange = parseInt(this.value);
           updateChartsDisplay();
       });

       // Step 6: Start polling for live data
       setInterval(fetchData, 30000);
       console.log('[Init] ✓ Initialization complete');
   });
   ```

2. **Fix loadHistoricalData() to return a Promise** (lines 630-691):
   ```javascript
   async function loadHistoricalData() {
       // Load house/weather historical data from server
       try {
           console.log('[Historical] Loading house/weather data from server...');
           const response = await fetch('/api/house_historical');
           if (!response.ok) {
               throw new Error(`HTTP ${response.status}: ${response.statusText}`);
           }

           const data = await response.json();
           console.log('[Historical] Server data loaded:', Object.keys(data));

           // Convert server data format to our chart format
           if (data.house_temperature && data.house_temperature.length > 0) {
               indoorTempHistory = data.house_temperature.map(p => ({
                   x: new Date(p.timestamp),
                   y: p.value
               }));
               console.log('[Historical] Loaded', indoorTempHistory.length, 'indoor temp points');
           }

           if (data.weather_temperature && data.weather_temperature.length > 0) {
               outdoorTempHistory = data.weather_temperature.map(p => ({
                   x: new Date(p.timestamp),
                   y: p.value
               }));
               console.log('[Historical] Loaded', outdoorTempHistory.length, 'outdoor temp points');
           }

           if (data.house_humidity && data.house_humidity.length > 0) {
               indoorHumHistory = data.house_humidity.map(p => ({
                   x: new Date(p.timestamp),
                   y: p.value
               }));
               console.log('[Historical] Loaded', indoorHumHistory.length, 'indoor humidity points');
           }

           if (data.weather_humidity && data.weather_humidity.length > 0) {
               outdoorHumHistory = data.weather_humidity.map(p => ({
                   x: new Date(p.timestamp),
                   y: p.value
               }));
               console.log('[Historical] Loaded', outdoorHumHistory.length, 'outdoor humidity points');
           }

           // CRITICAL: Update charts ONLY if they exist
           if (temperatureChart && humidityChart) {
               updateChartsDisplay();
               console.log('[Historical] ✓ Charts updated with server data');
           } else {
               console.error('[Historical] ERROR: Charts not initialized!');
               throw new Error('Charts not initialized before data load');
           }

           // Also save to localStorage for backup
           saveToLocalStorage();

       } catch (error) {
           console.error('[Historical] Error loading data:', error);
           // Fall back to localStorage if server fails
           console.log('[Historical] Falling back to localStorage');
           loadFromLocalStorage();
           throw error; // Re-throw so caller knows it failed
       }
   }
   ```

3. **Add better error handling in updateChartsDisplay()** (lines 383-424):
   ```javascript
   function updateChartsDisplay() {
       if (!temperatureChart || !humidityChart) {
           console.error('[updateChartsDisplay] ERROR: Charts not initialized!');
           console.log('[updateChartsDisplay] temperatureChart:', temperatureChart);
           console.log('[updateChartsDisplay] humidityChart:', humidityChart);
           return;
       }

       const now = new Date();
       const cutoffTime = new Date(now.getTime() - (currentTimeRange * 60 * 60 * 1000));

       console.log('[updateChartsDisplay] Filtering data for', currentTimeRange, 'hour range');
       console.log('[updateChartsDisplay] History arrays:', {
           indoorTemp: indoorTempHistory.length,
           outdoorTemp: outdoorTempHistory.length,
           indoorHum: indoorHumHistory.length,
           outdoorHum: outdoorHumHistory.length
       });

       // Filter based on selected time range
       const filteredIndoorTemp = indoorTempHistory.filter(point => new Date(point.x) >= cutoffTime);
       const filteredOutdoorTemp = outdoorTempHistory.filter(point => new Date(point.x) >= cutoffTime);
       const filteredIndoorHum = indoorHumHistory.filter(point => new Date(point.x) >= cutoffTime);
       const filteredOutdoorHum = outdoorHumHistory.filter(point => new Date(point.x) >= cutoffTime);

       console.log('[updateChartsDisplay] Filtered to:', {
           indoorTemp: filteredIndoorTemp.length,
           outdoorTemp: filteredOutdoorTemp.length,
           indoorHum: filteredIndoorHum.length,
           outdoorHum: filteredOutdoorHum.length
       });

       // Update chart datasets
       try {
           temperatureChart.data.datasets[0].data = filteredIndoorTemp;
           temperatureChart.data.datasets[1].data = filteredOutdoorTemp;
           humidityChart.data.datasets[0].data = filteredIndoorHum;
           humidityChart.data.datasets[1].data = filteredOutdoorHum;

           // Update charts
           temperatureChart.update('none');
           humidityChart.update('none');

           console.log('[updateChartsDisplay] ✓ Charts updated successfully');
       } catch (error) {
           console.error('[updateChartsDisplay] ERROR updating charts:', error);
       }
   }
   ```

**Testing Plan**:
1. Fresh page load → charts should populate with historical data
2. Check console for proper initialization sequence
3. Change time range → charts should re-filter
4. Wait for live data → charts should update with new points
5. Refresh page → should work consistently

### Fix #3: Client-Side Caching (Issue #1)

**Files to Modify**:
- `templates/charts.html`

**Implementation**:

1. **Add cache management object** (before `updateChartData()` function):
   ```javascript
   // Chart data cache
   const chartCache = {
       data: null,
       timestamp: null,
       timeRange: null,
       maxAge: 5 * 60 * 1000, // 5 minutes

       set(data, timeRange) {
           try {
               this.data = data;
               this.timestamp = Date.now();
               this.timeRange = timeRange;

               // Save to sessionStorage (survives page reload, not tab close)
               sessionStorage.setItem('chartCache', JSON.stringify({
                   data: data,
                   timestamp: this.timestamp,
                   timeRange: timeRange
               }));

               console.log('[Cache] Saved', Object.keys(data).length, 'metrics to cache');
           } catch (error) {
               console.error('[Cache] Error saving:', error);
           }
       },

       get(timeRange) {
           // Check memory cache first
           if (this.isValid(timeRange)) {
               console.log('[Cache] Using memory cache');
               return this.data;
           }

           // Try sessionStorage
           try {
               const cached = sessionStorage.getItem('chartCache');
               if (!cached) {
                   console.log('[Cache] No sessionStorage cache found');
                   return null;
               }

               const parsed = JSON.parse(cached);
               this.data = parsed.data;
               this.timestamp = parsed.timestamp;
               this.timeRange = parsed.timeRange;

               if (this.isValid(timeRange)) {
                   console.log('[Cache] Using sessionStorage cache');
                   return this.data;
               }

               console.log('[Cache] sessionStorage cache expired or wrong range');
               return null;
           } catch (error) {
               console.error('[Cache] Error reading:', error);
               return null;
           }
       },

       isValid(timeRange) {
           if (!this.data || !this.timestamp) return false;

           const age = Date.now() - this.timestamp;
           const isExpired = age > this.maxAge;
           const wrongRange = this.timeRange !== timeRange;

           return !isExpired && !wrongRange;
       },

       clear() {
           this.data = null;
           this.timestamp = null;
           this.timeRange = null;
           sessionStorage.removeItem('chartCache');
           console.log('[Cache] Cleared');
       }
   };
   ```

2. **Modify updateChartData() to use cache** (lines 579-653):
   ```javascript
   function updateChartData(forceRefresh = false) {
       const hours = parseInt(document.getElementById('timeRange').value);

       // Check cache unless forced refresh
       if (!forceRefresh) {
           const cachedData = chartCache.get(hours);
           if (cachedData) {
               console.log('[Cache] Using cached data');
               historicalData = cachedData;
               updateCharts();
               updateDataSummary();
               document.getElementById('lastUpdate').textContent =
                   `Last update: ${new Date(chartCache.timestamp).toLocaleTimeString()} (cached)`;
               return;
           }
       }

       // Show loading state
       const dataSummaryDiv = document.getElementById('dataSummary');
       dataSummaryDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading data...</div>';

       // Fetch from server
       const endpoint = `/api/historical?hours=${hours}`;
       console.log(`[API] Fetching ${hours}h data from server...`);

       fetch(endpoint)
           .then(response => {
               if (!response.ok) {
                   throw new Error(`HTTP ${response.status}: ${response.statusText}`);
               }
               return response.json();
           })
           .then(data => {
               // Validate data structure
               if (!data || typeof data !== 'object') {
                   throw new Error('Invalid data format received from server');
               }

               // Check if we got data
               const hasData = Object.keys(data).length > 0;
               const dataPoints = hasData ? Object.values(data)[0]?.length || 0 : 0;

               if (dataPoints === 0) {
                   // NO FALLBACK - show empty state instead
                   console.log(`[API] No data available for ${hours}h time range`);
                   dataSummaryDiv.innerHTML = `
                       <div class="alert alert-info d-flex align-items-center justify-content-between">
                           <div>
                               <i class="fas fa-info-circle me-2"></i>
                               <strong>No data available for selected time range.</strong>
                               <br>
                               <small>Try selecting a longer time range or wait for data to be collected.</small>
                           </div>
                           <button class="btn btn-sm btn-primary" id="loadAllDataBtn">
                               <i class="fas fa-database"></i> Load All Available Data
                           </button>
                       </div>
                   `;

                   // Add event listener for manual "load all" button
                   document.getElementById('loadAllDataBtn')?.addEventListener('click', () => {
                       fetch('/api/historical/all')
                           .then(response => response.json())
                           .then(allData => {
                               historicalData = allData;
                               chartCache.set(allData, 8760); // Cache as "all data" (1 year worth)
                               updateCharts();
                               updateDataSummary();
                               document.getElementById('lastUpdate').textContent =
                                   `Last update: ${new Date().toLocaleTimeString()} (all data)`;
                           })
                           .catch(error => {
                               console.error('[API] Error loading all data:', error);
                           });
                   });
                   return;
               }

               // Save to cache
               chartCache.set(data, hours);

               historicalData = data;
               updateCharts();
               updateDataSummary();
               document.getElementById('lastUpdate').textContent =
                   `Last update: ${new Date().toLocaleTimeString()}`;
           })
           .catch(error => {
               console.error('[API] Error fetching historical data:', error);

               // Show user-friendly error message with retry button
               dataSummaryDiv.innerHTML = `
                   <div class="alert alert-danger d-flex align-items-center justify-content-between">
                       <div>
                           <i class="fas fa-exclamation-triangle me-2"></i>
                           <strong>Error loading data:</strong> ${error.message}
                       </div>
                       <button class="btn btn-sm btn-danger" onclick="updateChartData(true)">
                           <i class="fas fa-redo"></i> Retry
                       </button>
                   </div>
               `;
           });
   }
   ```

3. **Update refresh button to bypass cache** (line 812):
   ```javascript
   // Set up refresh button
   document.getElementById('refreshCharts').addEventListener('click', () => {
       console.log('[User] Manual refresh - bypassing cache');
       chartCache.clear();
       updateChartData(true); // Force refresh
   });
   ```

4. **Update time range selector to clear cache** (line 815):
   ```javascript
   // Set up time range selector
   document.getElementById('timeRange').addEventListener('change', () => {
       console.log('[User] Time range changed');
       updateChartData(); // Will use cache if valid for new range
   });
   ```

**Testing Plan**:
1. Fresh page load → should fetch from server and cache
2. Page reload → should use cache (< 5 min old)
3. Click refresh button → should bypass cache and fetch fresh
4. Change time range → should use cache if valid, else fetch
5. Wait 6 minutes, reload page → should invalidate cache and fetch fresh
6. Open DevTools → verify sessionStorage has data
7. Test with slow network → should show cached data immediately

## Development Cycles

### CYCLE 1: Fix Time Range Filtering (Issue #2)
**Branch**: `fix/charts-time-range-filtering`
**Duration**: 30-45 minutes
**Dependencies**: None

**Tasks**:
1. Create feature branch from current branch
2. Remove fallback mechanism (lines 607-616)
3. Add empty state with "Load All Data" button
4. Test all time ranges
5. Commit and push

**Deliverables**:
- Modified `templates/charts.html`
- Testing log showing all ranges work correctly
- Screenshot of empty state message

**Exit Criteria**:
- Time range filtering respects user selection
- No automatic fallback to all data
- Clear UI feedback when no data available
- Manual option to load all data works

### CYCLE 2: Fix House Page Charts (Issue #3)
**Branch**: `fix/house-chart-rendering`
**Duration**: 45-60 minutes
**Dependencies**: None

**Tasks**:
1. Create feature branch from master/main
2. Make DOMContentLoaded handler async
3. Convert loadHistoricalData() to proper async/await
4. Add chart initialization checks
5. Add comprehensive console logging
6. Test page load, refresh, and time range changes
7. Commit and push

**Deliverables**:
- Modified `templates/house.html`
- Console logs showing proper initialization sequence
- Screenshots of working charts

**Exit Criteria**:
- Charts populate on page load
- No race conditions
- Time range selector works
- Live data updates work
- Console shows clear initialization flow

### CYCLE 3: Add Client-Side Caching (Issue #1)
**Branch**: `feature/charts-client-caching`
**Duration**: 60-90 minutes
**Dependencies**: CYCLE 1 (builds on time range fix)

**Tasks**:
1. Create feature branch from `fix/charts-time-range-filtering` (after merge)
2. Implement cache management object
3. Modify updateChartData() to use cache
4. Add cache invalidation logic
5. Update UI to show cached vs fresh data
6. Test cache behavior across page reloads
7. Test cache expiration
8. Commit and push

**Deliverables**:
- Modified `templates/charts.html` with caching
- Testing log showing cache behavior
- Performance comparison (with/without cache)

**Exit Criteria**:
- Page reload uses cache when valid
- Manual refresh bypasses cache
- Cache expires after 5 minutes
- Cache invalidates on time range change
- sessionStorage used (survives page reload)
- No errors if storage full or disabled

## Testing Strategy

### Manual Testing Checklist

**For /charts (Issues #1 and #2)**:
- [ ] Fresh page load with no cache
- [ ] Page reload within 5 minutes (should use cache)
- [ ] Page reload after 6 minutes (should fetch fresh)
- [ ] Select 1 hour range with no data → shows empty state
- [ ] Click "Load All Data" button → loads all data
- [ ] Change time range from 24h to 12h → filters correctly
- [ ] Manual refresh button → bypasses cache
- [ ] Auto-refresh after 5 minutes → updates data
- [ ] Network failure → shows error with retry button
- [ ] Slow network → shows loading state

**For /house (Issue #3)**:
- [ ] Fresh page load → charts populate with historical data
- [ ] Page reload → charts still work
- [ ] Time range change → charts re-filter
- [ ] Wait for live data (30 sec) → charts update
- [ ] Check console → shows proper init sequence
- [ ] Network failure → shows error, charts still show cached data
- [ ] Multiple rapid time range changes → no errors

### Automated Testing (Future Enhancement)
- Add Playwright/Cypress tests for chart rendering
- Add API endpoint tests for historical data
- Add localStorage/sessionStorage mock tests

## Rollback Plan

If any fix causes issues:

1. **Immediate**: Revert the specific branch
2. **Branch naming** allows easy identification of which fix failed
3. **Separate branches** mean fixes are independent - one failing doesn't block others
4. **Test locally first** before deploying to batterypi

## Deployment Strategy

1. **Test locally** on development machine
2. **Deploy to batterypi** (10.241.119.52:5000)
3. **Monitor for 24 hours**
4. **Merge to master** if stable

Each cycle can be deployed independently.

## Progress Tracking

Progress will be tracked in `CHART_FIXES_PROGRESS.md` after each cycle completion.

## Success Criteria Summary

### Issue #2 (Time Range Filtering)
- [x] Investigation complete
- [ ] Code changes implemented
- [ ] Manual testing passed
- [ ] Deployed to batterypi
- [ ] Verified in production for 24h
- [ ] Merged to master

### Issue #3 (House Charts)
- [x] Investigation complete
- [ ] Code changes implemented
- [ ] Manual testing passed
- [ ] Deployed to batterypi
- [ ] Verified in production for 24h
- [ ] Merged to master

### Issue #1 (Client Caching)
- [x] Investigation complete
- [ ] Code changes implemented
- [ ] Manual testing passed
- [ ] Deployed to batterypi
- [ ] Verified in production for 24h
- [ ] Merged to master

---

**Document Version**: 1.0
**Created**: 2025-11-07
**Last Updated**: 2025-11-07
**Status**: Ready for execution
