# Chart Fixes Development Cycles

## Overview

This document breaks down the chart fixes into three independent development cycles. Each cycle can be executed in parallel or sequentially depending on resource availability.

---

## CYCLE 1: Fix Time Range Filtering (Issue #2)

### Priority
**HIGH** - Breaks user expectations

### Branch
`fix/charts-time-range-filtering`

### Scope
Fix the `/charts` page time range filtering by removing the automatic fallback to "all data" and providing explicit user control.

### Estimated Duration
30-45 minutes

### Dependencies
None - can start immediately

### Technical Tasks

1. **Create feature branch**
   ```bash
   git checkout -b fix/charts-time-range-filtering
   ```

2. **Remove automatic fallback** (`templates/charts.html` lines 607-616)
   - Delete the `if (dataPoints === 0)` block that fetches all data
   - Replace with empty state message

3. **Add user-controlled "Load All Data" option**
   - Create button in empty state alert
   - Add event listener for manual all-data fetch
   - Update UI to show when all data is loaded

4. **Test all time ranges**
   - Test: 1h, 6h, 12h, 24h, 48h, 168h
   - Verify: Each shows only requested range
   - Verify: Empty state appears if no data for range
   - Verify: "Load All Data" button works

5. **Commit and document**
   ```bash
   git add templates/charts.html
   git commit -m "Fix time range filtering - remove automatic fallback to all data

   - Remove lines 607-616 that automatically fetch all data when filtered result is empty
   - Add explicit 'Load All Data' button for user control
   - Improve UX by showing clear message when no data available for selected range
   - Respect user's time range selection instead of silently changing it

   Fixes Issue #2"
   ```

### Testing Checklist
- [ ] Select 1 hour range with no recent data → shows "No data available" message
- [ ] Click "Load All Data" button → charts populate with all available data
- [ ] Change time range to 24h → filters to last 24 hours
- [ ] Select 6h range with available data → shows only 6 hours
- [ ] Manual refresh works correctly
- [ ] Console shows no errors

### Deliverables
- Modified `templates/charts.html`
- Git commit with clear message
- Testing log (checklist above)

### Exit Criteria
✅ All items in testing checklist pass
✅ No console errors
✅ Code committed to feature branch
✅ Ready for deployment to batterypi

---

## CYCLE 2: Fix House Page Charts (Issue #3)

### Priority
**HIGH** - Charts completely non-functional

### Branch
`fix/house-chart-rendering`

### Scope
Fix the `/house` page chart rendering by properly sequencing async initialization and ensuring charts exist before attempting to update them.

### Estimated Duration
45-60 minutes

### Dependencies
None - can start immediately (independent of CYCLE 1)

### Technical Tasks

1. **Create feature branch**
   ```bash
   git checkout master  # or main
   git checkout -b fix/house-chart-rendering
   ```

2. **Make DOMContentLoaded handler async** (`templates/house.html` lines 718-739)
   - Change to `async function()`
   - Add proper await calls
   - Add try/catch blocks
   - Add detailed console logging

3. **Convert loadHistoricalData() to proper async** (lines 630-691)
   - Make function `async`
   - Add await for fetch
   - Add error handling
   - Add chart existence checks before updating
   - Re-throw errors for caller to handle

4. **Enhance updateChartsDisplay() error handling** (lines 383-424)
   - Add null checks for chart objects
   - Add detailed console logging
   - Add try/catch for chart update operations

5. **Test initialization sequence**
   - Fresh page load
   - Page reload
   - Time range changes
   - Live data updates
   - Monitor console logs

6. **Commit and document**
   ```bash
   git add templates/house.html
   git commit -m "Fix house page chart rendering with proper async initialization

   - Make DOMContentLoaded handler properly async with await
   - Convert loadHistoricalData() to async/await pattern
   - Add chart existence checks before attempting updates
   - Add comprehensive error handling and logging
   - Ensure charts are initialized before data is loaded
   - Fix race condition between chart init and data fetch

   Fixes Issue #3"
   ```

### Testing Checklist
- [ ] Fresh page load → charts populate with historical data
- [ ] Console shows proper initialization sequence
- [ ] Page reload → charts still work correctly
- [ ] Time range selector → charts re-filter data
- [ ] Wait 30 seconds → live data updates charts
- [ ] Check console → no errors, clear logging
- [ ] Rapid time range changes → no errors
- [ ] Network failure → graceful fallback to localStorage

### Deliverables
- Modified `templates/house.html`
- Git commit with clear message
- Console log screenshots showing successful init sequence
- Screenshots of working charts

### Exit Criteria
✅ All items in testing checklist pass
✅ Console shows clear initialization flow with no errors
✅ Charts render historical data on page load
✅ Code committed to feature branch
✅ Ready for deployment to batterypi

---

## CYCLE 3: Add Client-Side Caching (Issue #1)

### Priority
**MEDIUM** - Performance optimization

### Branch
`feature/charts-client-caching`

### Scope
Add client-side caching to `/charts` page to reduce server load and improve page load performance.

### Estimated Duration
60-90 minutes

### Dependencies
**Requires**: CYCLE 1 to be merged first (builds on time range fix)

### Technical Tasks

1. **Create feature branch from updated master**
   ```bash
   git checkout master
   git pull origin master  # After CYCLE 1 is merged
   git checkout -b feature/charts-client-caching
   ```

2. **Implement cache management object** (`templates/charts.html`)
   - Create `chartCache` object
   - Implement `set()`, `get()`, `isValid()`, `clear()` methods
   - Use sessionStorage for persistence
   - Add 5-minute expiration
   - Add error handling

3. **Modify updateChartData() to use cache**
   - Check cache before fetching
   - Add `forceRefresh` parameter
   - Save fetched data to cache
   - Show cache status in UI

4. **Update event listeners**
   - Refresh button → bypass cache
   - Time range change → use cache if valid
   - Auto-refresh → use cache if valid

5. **Add cache status indicators**
   - Update "Last update" text to show if cached
   - Add cache age to UI
   - Add cache size info

6. **Test caching behavior**
   - Fresh load → fetches from server
   - Reload < 5 min → uses cache
   - Reload > 5 min → fetches fresh
   - Manual refresh → bypasses cache
   - Time range change → uses cache if same range
   - Storage disabled → graceful fallback

7. **Performance testing**
   - Measure page load time without cache
   - Measure page load time with cache
   - Document improvement

8. **Commit and document**
   ```bash
   git add templates/charts.html
   git commit -m "Add client-side caching for chart data

   - Implement chartCache object with sessionStorage persistence
   - Cache data for 5 minutes to reduce server load
   - Add forceRefresh parameter for manual refresh
   - Show cache status in UI (cached vs fresh data)
   - Graceful fallback if storage disabled or full
   - Improve page load performance significantly

   Fixes Issue #1"
   ```

### Testing Checklist
- [ ] Fresh page load → fetches from server, caches data
- [ ] Page reload within 5 min → uses cache (instant load)
- [ ] Page reload after 6 min → fetches fresh data
- [ ] Click refresh button → bypasses cache, fetches fresh
- [ ] Change time range → uses cache if valid for new range
- [ ] Open DevTools → verify sessionStorage has chartCache entry
- [ ] Disable storage in DevTools → graceful fallback
- [ ] Fill storage (5MB limit) → handles quota exceeded error
- [ ] Performance: cached load < 100ms, fresh load > 500ms
- [ ] UI shows "cached" vs "fresh" status

### Deliverables
- Modified `templates/charts.html` with caching
- Git commit with clear message
- Performance comparison data (before/after)
- Testing log (checklist above)

### Exit Criteria
✅ All items in testing checklist pass
✅ Page reload uses cache when valid (< 5 min old)
✅ Manual refresh bypasses cache
✅ Performance improvement documented
✅ No errors when storage disabled
✅ Code committed to feature branch
✅ Ready for deployment to batterypi

---

## Cycle Execution Order

### Option A: Sequential (Recommended for single developer)
1. CYCLE 1 (30-45 min)
2. Deploy and verify CYCLE 1
3. CYCLE 2 (45-60 min) - can run in parallel with CYCLE 1 if needed
4. Deploy and verify CYCLE 2
5. Merge CYCLE 1 to master
6. CYCLE 3 (60-90 min) - depends on CYCLE 1 merge
7. Deploy and verify CYCLE 3
8. Merge all to master

**Total time**: ~3-4 hours including testing

### Option B: Parallel (if multiple developers or AI instances)
1. Start CYCLE 1 and CYCLE 2 simultaneously (independent)
2. Deploy both after completion
3. Merge both after 24h verification
4. Start CYCLE 3 after CYCLE 1 merged
5. Deploy and verify CYCLE 3
6. Merge CYCLE 3 after 24h verification

**Total time**: ~2-3 hours with parallel execution

---

## Risk Mitigation

### CYCLE 1 Risks
- **Risk**: Removing fallback might frustrate users with sparse data
- **Mitigation**: Provide clear "Load All Data" button as alternative
- **Rollback**: Simple git revert if needed

### CYCLE 2 Risks
- **Risk**: Async changes might break live data updates
- **Mitigation**: Extensive testing of all data flows
- **Rollback**: Keep old version as backup, easy revert

### CYCLE 3 Risks
- **Risk**: Cache might show stale data
- **Mitigation**: 5-minute expiration, manual refresh option
- **Risk**: Storage quota exceeded
- **Mitigation**: Try/catch blocks, graceful fallback
- **Rollback**: Easy to disable caching, falls back to current behavior

---

## Post-Cycle Review

After each cycle completion, update `CHART_FIXES_PROGRESS.md` with:
- Actual time taken vs estimate
- Issues encountered and solutions
- Testing results
- Deployment status
- Any deviations from plan

---

**Document Version**: 1.0
**Created**: 2025-11-07
**Status**: Ready for execution
