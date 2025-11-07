# Chart Fixes Progress Tracker

## Project Status: 🟡 IN PLANNING

**Started**: 2025-11-07
**Current Phase**: Planning and Investigation Complete

---

## Summary

This tracker documents progress on fixing three critical chart-related issues in the MPP-Solar web interface:
- **Issue #1**: Client-side caching (performance)
- **Issue #2**: Time range filtering broken
- **Issue #3**: House page charts not rendering

---

## Investigation Phase ✅ COMPLETE

**Duration**: ~1 hour
**Status**: ✅ Complete

### Findings

1. **Issue #2 Root Cause Identified**:
   - Lines 607-616 in `templates/charts.html` automatically fetch ALL data when filtered result is empty
   - This defeats the purpose of time-range selection
   - User expectation: see selected range OR get clear feedback
   - Actual behavior: silently loads all data regardless of selection

2. **Issue #3 Root Cause Identified**:
   - Race condition between chart initialization and data loading
   - `loadHistoricalData()` is async but not properly awaited
   - Charts might not exist when data update is attempted
   - Lines 718-739 in `templates/house.html` need proper async/await sequencing

3. **Issue #1 Analysis**:
   - No client-side caching implemented
   - Every page reload fetches from server
   - 16,963 Prometheus files on server
   - Backend loads 1000 files on startup (~67MB directory)
   - Significant performance opportunity

### Data Analysis
- **Prometheus files**: 16,963 total
- **File types**: inverter (qpigs), house sensors, weather data
- **Backend memory store**: 1000 entries for inverter, 2100 per sensor for house/weather
- **API endpoints working**: `/api/historical`, `/api/house_historical` both functional

---

## CYCLE 1: Time Range Filtering Fix ⏳ PENDING

**Branch**: `fix/charts-time-range-filtering`
**Priority**: HIGH
**Status**: 🟡 Not Started

### Plan
- Remove automatic fallback to all data (lines 607-616)
- Add explicit "Load All Data" button for user control
- Show clear empty state message when no data for range

### Timeline
- **Estimated**: 30-45 minutes
- **Actual**: TBD
- **Started**: TBD
- **Completed**: TBD

### Testing Results
*To be filled after implementation*

### Issues Encountered
*To be filled during implementation*

### Deployment
- **Deployed to batterypi**: ❌ No
- **Deployment date**: TBD
- **Verification period**: 24 hours
- **Production status**: TBD

### Merge Status
- **PR created**: ❌
- **PR reviewed**: ❌
- **Merged to master**: ❌
- **Merge date**: TBD

---

## CYCLE 2: House Page Charts Fix ⏳ PENDING

**Branch**: `fix/house-chart-rendering`
**Priority**: HIGH
**Status**: 🟡 Not Started

### Plan
- Make DOMContentLoaded handler properly async
- Convert `loadHistoricalData()` to async/await
- Add chart existence checks before updates
- Add comprehensive error handling

### Timeline
- **Estimated**: 45-60 minutes
- **Actual**: TBD
- **Started**: TBD
- **Completed**: TBD

### Testing Results
*To be filled after implementation*

### Issues Encountered
*To be filled during implementation*

### Deployment
- **Deployed to batterypi**: ❌ No
- **Deployment date**: TBD
- **Verification period**: 24 hours
- **Production status**: TBD

### Merge Status
- **PR created**: ❌
- **PR reviewed**: ❌
- **Merged to master**: ❌
- **Merge date**: TBD

---

## CYCLE 3: Client-Side Caching ⏳ PENDING

**Branch**: `feature/charts-client-caching`
**Priority**: MEDIUM
**Status**: 🟡 Not Started
**Dependency**: Requires CYCLE 1 merged to master

### Plan
- Implement `chartCache` object with sessionStorage
- 5-minute cache expiration
- Add forceRefresh parameter for manual refresh
- Show cache status in UI

### Timeline
- **Estimated**: 60-90 minutes
- **Actual**: TBD
- **Started**: TBD
- **Completed**: TBD

### Testing Results
*To be filled after implementation*

### Performance Metrics
- **Before**: TBD ms (page load without cache)
- **After**: TBD ms (page load with cache)
- **Improvement**: TBD%

### Issues Encountered
*To be filled during implementation*

### Deployment
- **Deployed to batterypi**: ❌ No
- **Deployment date**: TBD
- **Verification period**: 24 hours
- **Production status**: TBD

### Merge Status
- **PR created**: ❌
- **PR reviewed**: ❌
- **Merged to master**: ❌
- **Merge date**: TBD

---

## Overall Timeline

```
Investigation:  ████████████████████ 100% ✅ (2025-11-07)
CYCLE 1:        ░░░░░░░░░░░░░░░░░░░░   0%
CYCLE 2:        ░░░░░░░░░░░░░░░░░░░░   0%
CYCLE 3:        ░░░░░░░░░░░░░░░░░░░░   0%
```

**Overall Project**: 25% complete (investigation done, 3 cycles pending)

---

## Decisions and Changes

### Decision Log

1. **2025-11-07**: Decided to use separate branches for each fix
   - **Rationale**: Issues are independent, allows parallel work and isolated testing
   - **Impact**: Can deploy fixes individually, easier rollback

2. **2025-11-07**: Decided to use sessionStorage for caching (not localStorage)
   - **Rationale**: sessionStorage clears on tab close, preventing stale data across sessions
   - **Impact**: Better for development/testing, users get fresh data on new session

3. **2025-11-07**: Set cache expiration to 5 minutes
   - **Rationale**: Balance between performance and data freshness
   - **Impact**: Data no more than 5 minutes old, reduces server load significantly

### Deviations from Original Plan
*None yet*

---

## Technical Debt Identified

1. **No automated tests for charts**
   - Should add Playwright/Cypress tests
   - Would catch regressions in future

2. **Historical data loading happens on every server restart**
   - Could cache parsed data in Redis or similar
   - 16,963 files is a lot to parse on startup

3. **No HTTP caching headers**
   - Could add Cache-Control headers on API endpoints
   - Would enable browser-level caching

4. **Error handling could be more robust**
   - Should add retry logic for failed fetches
   - Should add exponential backoff

*Note*: These items are out of scope for current cycles but documented for future work.

---

## Risks and Mitigations

| Risk | Severity | Mitigation | Status |
|------|----------|------------|--------|
| Removing fallback frustrates users | Medium | Add clear "Load All Data" button | Planned |
| Async changes break live updates | High | Extensive testing before deploy | Planned |
| Cache shows stale data | Low | 5-minute expiration + manual refresh | Planned |
| Storage quota exceeded | Low | Try/catch + graceful fallback | Planned |

---

## Next Steps

1. ✅ Complete investigation
2. ⏳ Choose execution strategy (sequential vs parallel)
3. ⏳ Execute CYCLE 1 (time range filtering)
4. ⏳ Execute CYCLE 2 (house charts) - can run parallel with CYCLE 1
5. ⏳ Deploy and verify both cycles
6. ⏳ Merge CYCLE 1 to master
7. ⏳ Execute CYCLE 3 (caching) after CYCLE 1 merge
8. ⏳ Final verification and documentation

---

## Notes

- Server details: batterypi at 10.241.119.52:5000
- SSH access: `ssh batterypi`
- Prometheus directory: `/home/constantine/mpp-solar/prometheus/`
- Current branch: `feature/cycle-6-chart-error-handling`
- Main branch: `master`

---

**Last Updated**: 2025-11-07
**Updated By**: Claude Code (Investigation Phase)
**Next Update**: After CYCLE 1 completion
