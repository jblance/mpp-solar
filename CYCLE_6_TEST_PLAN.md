# CYCLE 6: Test Plan and Validation

**Created:** 2025-11-03
**Purpose:** Systematic testing of chart error handling implementation
**Related:** CYCLE_6.md Phase 6 (Days 8-9)

---

## Test Environment Setup

### Prerequisites
```bash
# 1. Ensure web server is running
python web_interface.py

# 2. Access URLs:
# Standard Charts: http://localhost:5000/charts
# LCARS Charts:    http://localhost:5000/charts/lcars

# 3. Open browser developer console (F12) to monitor:
# - Console logs
# - Network requests
# - JavaScript errors
```

### Test Data States

**State A: Normal Operation**
- Daemon running with `prom_file` output
- Historical data available
- All metrics being collected

**State B: No Data**
- Daemon stopped or no historical files
- Empty/missing Prometheus files

**State C: Partial Data**
- Some metrics available, others missing
- Simulated by temporarily removing some prom files

**State D: Server Error**
- Web server stopped or API endpoints failing
- Simulated network errors

---

## Test Scenarios

### 1. Happy Path Testing ✅

#### 1.1 Standard Charts Page (`/charts`)

**Test ID:** HP-STD-001
**Objective:** Verify all charts load successfully with data

**Steps:**
1. Navigate to http://localhost:5000/charts
2. Wait for page to fully load
3. Check all 6 charts render:
   - [ ] Battery Voltage Chart
   - [ ] AC Input Voltage Chart
   - [ ] Power Chart (3 lines)
   - [ ] Temperature Chart
   - [ ] Current Chart (2 lines)
   - [ ] Status Chart (3 lines)
4. Verify console shows 6 success messages:
   ```
   Battery Voltage Chart initialized successfully
   AC Input Voltage Chart initialized successfully
   Power Chart initialized successfully
   Temperature Chart initialized successfully
   Current Chart initialized successfully
   Status Chart initialized successfully
   ```
5. Verify data summary cards show metrics

**Expected Result:**
- All charts display with data
- No errors in console
- Data summary populated
- "Last update" shows timestamp

**Pass Criteria:**
- [ ] All 6 charts visible
- [ ] Data rendered on all charts
- [ ] No console errors
- [ ] Summary cards show current/avg/min/max values

---

#### 1.2 LCARS Charts Page (`/charts/lcars`)

**Test ID:** HP-LCARS-001
**Objective:** Verify all LCARS charts load successfully with data

**Steps:**
1. Navigate to http://localhost:5000/charts/lcars
2. Wait for page to fully load
3. Check all 5 charts render:
   - [ ] Voltage Chart (3 lines: Battery, AC Output, AC Input)
   - [ ] Power Chart (3 lines)
   - [ ] Temperature Chart
   - [ ] Current Chart (2 lines)
   - [ ] Status Chart (3 lines)
4. Verify console shows 5 success messages:
   ```
   LCARS Voltage Chart initialized successfully
   LCARS Power Chart initialized successfully
   LCARS Temperature Chart initialized successfully
   LCARS Current Chart initialized successfully
   LCARS Status Chart initialized successfully
   ```
5. Verify LCARS styling applied (orange/purple theme)

**Expected Result:**
- All charts display with LCARS theme
- No errors in console
- Data summary shows metrics with LCARS styling

**Pass Criteria:**
- [ ] All 5 charts visible with LCARS theme
- [ ] Data rendered on all charts
- [ ] No console errors
- [ ] Summary cards show current/avg/min/max values
- [ ] Orange/purple color scheme applied

---

#### 1.3 Time Range Selector

**Test ID:** HP-TIME-001
**Objective:** Verify time range selector filters data correctly

**Steps:**
1. On standard charts page, select different time ranges:
   - [ ] Last Hour
   - [ ] Last 6 Hours
   - [ ] Last 12 Hours
   - [ ] Last 24 Hours
   - [ ] Last 48 Hours
   - [ ] Last Week (All Data)
2. Verify charts update after each selection
3. Check console for "Loading data..." message
4. Verify "Last update" timestamp changes

**Expected Result:**
- Charts update with filtered data
- X-axis adjusts to show selected time range
- No errors during updates

**Pass Criteria:**
- [ ] All time ranges work
- [ ] Data filters correctly
- [ ] Charts re-render smoothly
- [ ] No console errors

---

#### 1.4 Manual Refresh

**Test ID:** HP-REFRESH-001
**Objective:** Verify refresh button updates charts

**Steps:**
1. Click "Refresh Charts" button
2. Observe loading state
3. Verify charts update
4. Check "Last update" timestamp

**Expected Result:**
- Loading spinner appears briefly
- Charts reload with current data
- Timestamp updates

**Pass Criteria:**
- [ ] Refresh button works
- [ ] Loading state displays
- [ ] Charts update successfully
- [ ] Timestamp reflects new load time

---

#### 1.5 Auto-Refresh

**Test ID:** HP-AUTO-001
**Objective:** Verify auto-refresh works (5 minute interval)

**Steps:**
1. Load chart page
2. Note initial "Last update" timestamp
3. Wait 5 minutes
4. Verify auto-refresh occurs

**Expected Result:**
- Charts automatically update after 5 minutes
- "Last update" timestamp changes
- No user interaction required

**Pass Criteria:**
- [ ] Auto-refresh triggers at 5 minutes
- [ ] Charts update automatically
- [ ] No console errors during auto-refresh

---

### 2. Error Scenario Testing ⚠️

#### 2.1 API Endpoint Down

**Test ID:** ERR-API-001
**Objective:** Verify graceful handling when API is unavailable

**Steps:**
1. Load chart page successfully
2. Stop web server: `Ctrl+C` in terminal running web_interface.py
3. Click "Refresh Charts" button
4. Observe error handling

**Expected Result:**
- Error message displays in data summary area:
  ```
  Error loading data: HTTP 0: Failed to fetch
  ```
  (or similar network error)
- Retry button appears
- Existing chart data remains visible
- Console shows error log

**Pass Criteria:**
- [ ] Error message displays
- [ ] Retry button visible and clickable
- [ ] Charts don't crash/disappear
- [ ] Previous data still visible
- [ ] Console logs error clearly

**Cleanup:**
```bash
# Restart web server
python web_interface.py
```

---

#### 2.2 Malformed JSON Response

**Test ID:** ERR-JSON-001
**Objective:** Verify handling of invalid JSON data

**Steps:**
1. Temporarily modify `web_interface.py` to return invalid JSON
2. Reload chart page
3. Observe error handling

**Alternative (Browser DevTools):**
1. Open DevTools → Network tab
2. Right-click `/api/historical` request → Block request URL
3. Refresh page
4. Observe error handling

**Expected Result:**
- Error message: "Invalid data format received from server"
- Retry button appears
- No chart crash
- Console error logged

**Pass Criteria:**
- [ ] Error detected and handled
- [ ] User-friendly message shown
- [ ] Retry button functional
- [ ] No JavaScript exceptions

---

#### 2.3 Empty Data Arrays

**Test ID:** ERR-EMPTY-001
**Objective:** Verify handling when no historical data exists

**Steps:**
1. Backup Prometheus files: `mv output/*.prom /tmp/`
2. Stop daemon (if running)
3. Reload chart page
4. Observe handling of empty data

**Expected Result:**
- Info message displays:
  ```
  No historical data available yet. Data will appear as the daemon collects metrics.
  ```
- Charts initialize but show empty
- Console warns: "No data available for [chart name]"
- No errors/crashes

**Pass Criteria:**
- [ ] Informative message shown (not error)
- [ ] Charts render empty (no crash)
- [ ] Console warnings (not errors)
- [ ] Page remains functional

**Cleanup:**
```bash
# Restore Prometheus files
mv /tmp/*.prom output/
```

---

#### 2.4 Network Timeout

**Test ID:** ERR-TIMEOUT-001
**Objective:** Verify handling of slow/timeout responses

**Steps:**
1. Use browser DevTools → Network tab
2. Throttle to "Slow 3G"
3. Reload chart page
4. Observe loading behavior

**Expected Result:**
- Loading spinner displays during fetch
- If timeout occurs, error message appears
- Retry button available
- Charts don't break

**Pass Criteria:**
- [ ] Loading state visible during slow load
- [ ] Timeout handled gracefully
- [ ] Error message if timeout
- [ ] Retry works

---

#### 2.5 Mixed Data (Partial Metrics)

**Test ID:** ERR-PARTIAL-001
**Objective:** Verify graceful degradation with partial data

**Steps:**
1. Temporarily rename some Prometheus metric files
2. Reload chart page
3. Observe chart behavior

**Expected Result:**
- Charts with data display normally
- Charts without data show empty but don't crash
- Console warns: "No data available for [metric]"
- Page remains functional

**Pass Criteria:**
- [ ] Charts with data work
- [ ] Charts without data show empty
- [ ] No JavaScript errors
- [ ] Partial summary data shown

---

#### 2.6 Chart Canvas Not Found

**Test ID:** ERR-CANVAS-001
**Objective:** Verify handling when canvas element missing

**Steps:**
1. Edit `templates/charts.html`
2. Temporarily change a canvas ID: `batteryVoltageChart` → `batteryVoltageChart_TEST`
3. Reload page
4. Observe error handling

**Expected Result:**
- Console warning: "Battery Voltage Chart canvas not found"
- Error message displays in chart area (if showChartError works)
- Other charts still load
- Page doesn't crash

**Pass Criteria:**
- [ ] Missing canvas detected
- [ ] Console warning logged
- [ ] Other charts unaffected
- [ ] No uncaught exceptions

**Cleanup:**
```bash
# Revert canvas ID change
git checkout templates/charts.html
```

---

#### 2.7 Chart.js Initialization Failure

**Test ID:** ERR-INIT-001
**Objective:** Verify try-catch blocks around Chart.js

**Steps:**
1. Open browser DevTools → Console
2. Before page loads, run:
   ```javascript
   window.Chart = undefined;
   ```
3. Reload page
4. Observe error handling

**Expected Result:**
- Console error: "Failed to initialize [chart name]"
- Error messages display in chart containers
- Retry buttons appear
- Page doesn't crash

**Pass Criteria:**
- [ ] Initialization errors caught
- [ ] Error messages displayed
- [ ] Retry buttons functional
- [ ] No uncaught exceptions

---

### 3. Cross-Browser Testing 🌐

#### 3.1 Chrome (Desktop)

**Test ID:** XB-CHROME-001
**Browser:** Chrome/Chromium (latest)

**Steps:**
1. Open http://localhost:5000/charts in Chrome
2. Run all Happy Path tests (1.1-1.5)
3. Run all Error Scenario tests (2.1-2.7)
4. Note any issues

**Pass Criteria:**
- [ ] All happy path tests pass
- [ ] Error handling works correctly
- [ ] No browser-specific issues

---

#### 3.2 Firefox (Desktop)

**Test ID:** XB-FIREFOX-001
**Browser:** Firefox (latest)

**Steps:**
1. Open http://localhost:5000/charts in Firefox
2. Run all Happy Path tests (1.1-1.5)
3. Test error scenarios (at least 2.1, 2.3, 2.5)
4. Note any rendering differences

**Pass Criteria:**
- [ ] Charts render correctly
- [ ] Error handling works
- [ ] No Firefox-specific issues

---

#### 3.3 Safari (Desktop - if available)

**Test ID:** XB-SAFARI-001
**Browser:** Safari (latest)

**Steps:**
1. Open http://localhost:5000/charts in Safari
2. Run Happy Path tests (1.1, 1.2)
3. Test basic error handling (2.1, 2.3)
4. Note any Safari-specific issues

**Pass Criteria:**
- [ ] Charts render correctly
- [ ] Basic functionality works
- [ ] No Safari-specific issues

---

#### 3.4 Mobile Safari (iOS - if available)

**Test ID:** XB-MOBILE-SAFARI-001
**Device:** iPhone/iPad

**Steps:**
1. Access http://[your-ip]:5000/charts from iOS device
2. Test touch interactions
3. Verify responsive design
4. Test tab switching

**Pass Criteria:**
- [ ] Charts visible on mobile
- [ ] Touch scrolling works
- [ ] Tabs switchable
- [ ] Readable on small screen

---

#### 3.5 Chrome Mobile (Android - if available)

**Test ID:** XB-MOBILE-CHROME-001
**Device:** Android phone/tablet

**Steps:**
1. Access http://[your-ip]:5000/charts from Android
2. Test touch interactions
3. Verify responsive design
4. Test landscape/portrait orientation

**Pass Criteria:**
- [ ] Charts visible on mobile
- [ ] Touch interactions work
- [ ] Responsive layout adapts
- [ ] Works in both orientations

---

### 4. Responsive Design Testing 📱

#### 4.1 Desktop (1920x1080)

**Test ID:** RESP-DESKTOP-001
**Resolution:** 1920x1080 (Full HD)

**Steps:**
1. Set browser window to full screen
2. Load both chart pages
3. Verify layout uses available space
4. Check chart sizing

**Pass Criteria:**
- [ ] Charts use available width
- [ ] 400px height maintained
- [ ] No horizontal scroll
- [ ] Tabs/controls visible

---

#### 4.2 Laptop (1366x768)

**Test ID:** RESP-LAPTOP-001
**Resolution:** 1366x768 (Common laptop)

**Steps:**
1. Resize browser to 1366x768
2. Load both chart pages
3. Verify layout adapts
4. Check readability

**Pass Criteria:**
- [ ] No horizontal scroll
- [ ] Charts readable
- [ ] All controls accessible
- [ ] Text not cut off

---

#### 4.3 Tablet (768x1024)

**Test ID:** RESP-TABLET-001
**Resolution:** 768x1024 (iPad portrait)

**Steps:**
1. Resize browser to 768px width
2. Or test on actual tablet
3. Verify mobile/responsive layout triggers
4. Test tab navigation

**Pass Criteria:**
- [ ] Responsive layout activates
- [ ] Charts stack vertically
- [ ] Tabs/controls usable
- [ ] No overflow issues

---

#### 4.4 Mobile (375x667)

**Test ID:** RESP-MOBILE-001
**Resolution:** 375x667 (iPhone 8)

**Steps:**
1. Resize browser to 375px width
2. Or use DevTools device emulation
3. Verify mobile layout
4. Test all interactions

**Pass Criteria:**
- [ ] Charts fit screen width
- [ ] Vertical scrolling works
- [ ] Tabs stack if needed
- [ ] Readable and usable

---

### 5. Performance Testing ⚡

#### 5.1 Page Load Time

**Test ID:** PERF-LOAD-001
**Objective:** Verify charts load within 2 seconds

**Steps:**
1. Open DevTools → Network tab
2. Hard reload page (Ctrl+Shift+R)
3. Check "Load" time at bottom
4. Verify DOM content loaded quickly

**Expected Result:**
- Page loads in < 2 seconds
- Charts initialize quickly
- Data fetches efficiently

**Pass Criteria:**
- [ ] Load time < 2s
- [ ] Chart initialization < 500ms
- [ ] Data fetch < 1s

---

#### 5.2 Memory Usage

**Test ID:** PERF-MEM-001
**Objective:** Verify no memory leaks

**Steps:**
1. Open DevTools → Performance Monitor
2. Load chart page
3. Let auto-refresh run 3-4 times (15-20 min)
4. Monitor memory usage

**Expected Result:**
- Memory stays stable
- No continuous growth
- Charts update without accumulating

**Pass Criteria:**
- [ ] Memory usage stable
- [ ] No leaks detected
- [ ] Auto-refresh doesn't accumulate

---

### 6. Code Review Checklist ✓

**Test ID:** CODE-REVIEW-001

**Items to verify in code:**

**Error Handling:**
- [ ] All chart initializations wrapped in try-catch
- [ ] All fetch calls have .catch() handlers
- [ ] All error messages are user-friendly
- [ ] Console.log/warn/error used appropriately

**Code Quality:**
- [ ] No debug/console.log statements left in production (or intentional)
- [ ] Comments explain complex logic
- [ ] Function names are descriptive
- [ ] No duplicate code

**Accessibility:**
- [ ] ARIA labels present on interactive elements
- [ ] Keyboard navigation works
- [ ] Color contrast sufficient (WCAG AA)
- [ ] Screen reader compatible

**Best Practices:**
- [ ] Event listeners properly attached
- [ ] No global variable pollution
- [ ] Error messages localized/consistent
- [ ] Retry mechanisms work

---

## Test Results Template

```markdown
## Test Execution Log

**Date:** YYYY-MM-DD
**Tester:** [Name]
**Environment:** [OS, Browser versions]

### Test Results Summary

| Test ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| HP-STD-001 | Standard charts happy path | ✅ PASS | All charts loaded |
| HP-LCARS-001 | LCARS charts happy path | ✅ PASS | |
| ERR-API-001 | API endpoint down | ⚠️ FAIL | [details] |
| ... | ... | ... | ... |

### Issues Found

**Issue #1:**
- **Severity:** High/Medium/Low
- **Test ID:** ERR-API-001
- **Description:** Error message not displaying in Safari
- **Steps to Reproduce:** [steps]
- **Expected:** [expected]
- **Actual:** [actual]
- **Screenshot:** [if applicable]

### Overall Assessment

- **Total Tests:** 25
- **Passed:** 23
- **Failed:** 2
- **Skipped:** 0

**Recommendation:** [Ready for production / Needs fixes / etc]
```

---

## Quick Test Commands

```bash
# Start web server
python web_interface.py

# Stop daemon (for no-data testing)
sudo systemctl stop mpp-solar-daemon

# Start daemon
sudo systemctl start mpp-solar-daemon

# Check daemon status
sudo systemctl status mpp-solar-daemon

# View daemon logs
sudo journalctl -u mpp-solar-daemon -f

# Backup Prometheus files
mkdir -p /tmp/prom-backup
cp output/*.prom /tmp/prom-backup/

# Restore Prometheus files
cp /tmp/prom-backup/*.prom output/

# View web server logs
tail -f web_interface.log
```

---

## Browser DevTools Tips

### Console Commands

```javascript
// Manually trigger chart update
updateChartData()

// Check charts object
console.log(charts)

// Check historical data
console.log(historicalData)

// Manually trigger error
throw new Error('Test error')

// Clear all charts
Object.values(charts).forEach(chart => chart.destroy())
```

### Network Throttling

1. DevTools → Network tab
2. Throttling dropdown (Online → Slow 3G)
3. Reload page to test slow loading

### Device Emulation

1. DevTools → Toggle device toolbar (Ctrl+Shift+M)
2. Select device (iPhone, iPad, etc)
3. Test responsive layout

---

## Exit Criteria

Phase 6 is complete when:

- [ ] All Happy Path tests pass (1.1-1.5)
- [ ] All Error Scenario tests documented (2.1-2.7)
- [ ] Tested on at least 2 browsers (Chrome + Firefox minimum)
- [ ] Responsive design verified on at least 2 screen sizes
- [ ] Performance acceptable (< 2s load time)
- [ ] Code review checklist complete
- [ ] All critical issues fixed
- [ ] Test results documented

---

## Known Limitations

- Auto-refresh testing requires 5-minute wait
- Mobile device testing requires physical devices or emulator
- Safari testing requires macOS/iOS
- Network timeout testing depends on browser behavior

---

**Next Phase:** Phase 7 - Documentation and Cleanup
