# Chart Fixes Project - Context Recovery File

## Purpose

This file enables quick context recovery for AI assistants working on the MPP-Solar web interface chart fixes. Read this file first when starting a new session or after context reset.

---

## Project Quick Summary

**Objective**: Fix three critical issues affecting chart functionality in the MPP-Solar web interface

**Issues**:
1. `/charts` page has no client-side caching (performance issue)
2. `/charts` time range filtering broken (UX issue)
3. `/house` page charts don't render properly (functionality issue)

**Status**: Investigation complete, ready for implementation

**Current Phase**: Planning complete, awaiting execution decision

---

## Files to Read (In Order)

### 1. Investigation and Planning (Read These First)
- `CHART_FIXES_IMPLEMENTATION_PLAN.md` - **Primary technical plan**
  - Problem analysis
  - Technical implementation details
  - Success criteria
  - ~350 lines of detailed planning

- `CHART_FIXES_CYCLES.md` - **Execution roadmap**
  - 3 development cycles
  - Task breakdowns
  - Testing checklists
  - Timeline estimates

- `CHART_FIXES_PROGRESS.md` - **Current status**
  - What's done
  - What's pending
  - Timeline tracking
  - Decisions log

### 2. Main Project Documentation (For Context)
- `CLAUDE.md` - Quick reference for development commands
- `CONTEXT.md` - Overall project context (if exists)
- `IMPLEMENTATION_PLAN.md` - Main project architecture
- `PROGRESS.md` - Overall project progress

### 3. Code Files (Reference as Needed)
- `web_interface.py` - Flask backend (~738 lines)
  - Lines 61-91: `load_historical_prometheus_data()`
  - Lines 108-199: `load_historical_house_weather_data()`
  - Lines 365-401: `get_historical_data()`
  - Lines 430-435: `/api/historical` endpoint
  - Lines 482-500: `/api/house_historical` endpoint

- `templates/charts.html` - Inverter charts page (~823 lines)
  - **PROBLEM AREA**: Lines 607-616 (automatic fallback)
  - Lines 740-755: `getChartData()` function
  - Lines 579-653: `updateChartData()` function

- `templates/house.html` - House/weather charts page (~743 lines)
  - **PROBLEM AREA**: Lines 718-739 (async initialization)
  - Lines 630-691: `loadHistoricalData()` function
  - Lines 383-424: `updateChartsDisplay()` function

---

## Key Investigation Findings

### Issue #2: Time Range Filtering
- **Root Cause**: Lines 607-616 in `charts.html` automatically fetch ALL data when filtered result is empty
- **Impact**: User selects "1 hour" but sees days of data
- **Fix**: Remove fallback, add explicit "Load All Data" button

### Issue #3: House Charts Not Rendering
- **Root Cause**: Race condition in async initialization
- **Impact**: Historical data loads but charts don't update
- **Fix**: Proper async/await sequencing, ensure charts exist before data load

### Issue #1: No Client-Side Caching
- **Root Cause**: No caching implemented
- **Impact**: Every page reload fetches from server (slow)
- **Fix**: Implement sessionStorage cache with 5-min expiration

### Environment Details
- **Server**: batterypi at 10.241.119.52:5000
- **SSH**: `ssh batterypi`
- **Prometheus files**: 16,963 files in `/home/constantine/mpp-solar/prometheus/`
- **Backend memory**: 1000 inverter entries, 2100 per sensor for house/weather
- **Current branch**: `feature/cycle-6-chart-error-handling`
- **Main branch**: `master`

---

## Development Approach (Per claude_rob.md)

This project follows the structured approach from `claude_rob.md`:

1. ✅ **Define and Plan** - Created `CHART_FIXES_IMPLEMENTATION_PLAN.md`
2. ✅ **Break into Cycles** - Created `CHART_FIXES_CYCLES.md` with 3 cycles
3. ✅ **Track Progress** - Created `CHART_FIXES_PROGRESS.md`
4. ✅ **Build Context Recovery** - This file
5. ⏳ **Execute** - Ready to start
6. ⏳ **Maintain State** - Update progress after each cycle

---

## Quick Start Guide

### If Starting Fresh Session:
1. Read this file (you are here)
2. Read `CHART_FIXES_IMPLEMENTATION_PLAN.md` for technical details
3. Read `CHART_FIXES_CYCLES.md` for execution plan
4. Check `CHART_FIXES_PROGRESS.md` for current status
5. Ask user which cycle to execute

### If Resuming Mid-Cycle:
1. Check `CHART_FIXES_PROGRESS.md` first
2. Look for "Status" of each cycle
3. Continue from last checkpoint

### If Verifying Deployment:
1. Check `CHART_FIXES_PROGRESS.md` deployment status
2. SSH to batterypi: `ssh batterypi`
3. Check service: `sudo systemctl status mpp-solar-web`
4. Test endpoints: `curl http://10.241.119.52:5000/charts`

---

## Execution Options

### Option A: Sequential Execution (Recommended)
```
CYCLE 1 (30-45 min) → Deploy → Verify 24h
  ↓
Merge to master
  ↓
CYCLE 2 (45-60 min) → Deploy → Verify 24h
  ↓
Merge to master
  ↓
CYCLE 3 (60-90 min) → Deploy → Verify 24h
  ↓
Merge to master
```
**Total time**: ~3-4 hours + verification periods

### Option B: Parallel Execution
```
CYCLE 1 (30-45 min) ─┐
                      ├→ Deploy both → Verify 24h → Merge both
CYCLE 2 (45-60 min) ─┘
         ↓
CYCLE 3 (60-90 min) → Deploy → Verify 24h → Merge
```
**Total time**: ~2-3 hours + verification periods

---

## Branch Strategy

Each cycle has its own branch:
- `fix/charts-time-range-filtering` (CYCLE 1)
- `fix/house-chart-rendering` (CYCLE 2)
- `feature/charts-client-caching` (CYCLE 3)

**Note**: CYCLE 3 depends on CYCLE 1 being merged first.

---

## Testing Commands

```bash
# Test API endpoints
curl -s http://10.241.119.52:5000/api/data | python3 -m json.tool
curl -s http://10.241.119.52:5000/api/historical?hours=1 | python3 -m json.tool | head -50
curl -s http://10.241.119.52:5000/api/house_historical | python3 -m json.tool | head -50

# Check Prometheus files
ssh batterypi "ls -lh /home/constantine/mpp-solar/prometheus/ | head -30"
ssh batterypi "ls -1 /home/constantine/mpp-solar/prometheus/*.prom | wc -l"

# Check web service
ssh batterypi "sudo systemctl status mpp-solar-web"
ssh batterypi "tail -50 /home/constantine/mpp-solar/web_interface.log"
```

---

## Success Criteria (High Level)

### CYCLE 1 Complete When:
- Time range selector respects user choice
- No automatic fallback to all data
- Clear UI feedback for empty states
- Manual "Load All Data" option works

### CYCLE 2 Complete When:
- House page charts render on load
- No race conditions
- Console shows proper init sequence
- Time range filtering works

### CYCLE 3 Complete When:
- Page reload uses cache (< 5 min old)
- Manual refresh bypasses cache
- Cache expires properly
- Performance measurably improved

---

## Common Commands

```bash
# Development
make test                  # Run all tests
make unit-tests           # Unit tests only
pytest tests/unit/        # Direct pytest

# Web interface
python web_interface.py   # Start locally
# On batterypi: managed by systemd

# Git workflow
git checkout -b fix/charts-time-range-filtering
git add templates/charts.html
git commit -m "Fix: description"
git push origin fix/charts-time-range-filtering

# Deployment (on batterypi)
sudo systemctl restart mpp-solar-web
sudo systemctl status mpp-solar-web
sudo journalctl -u mpp-solar-web -f
```

---

## Questions to Ask User

When starting a session, clarify:
1. Which execution strategy? (Sequential or Parallel)
2. Which cycle to start with? (1, 2, or 3)
3. Deploy to batterypi immediately or test locally first?
4. Any changes to the plan?

---

## Notes and Warnings

- **DO NOT** modify backend (`web_interface.py`) unless absolutely necessary
- All fixes are frontend-only (HTML/JavaScript)
- Test locally before deploying to batterypi
- Each cycle is independent except CYCLE 3 depends on CYCLE 1
- Keep commits atomic and well-documented
- Update `CHART_FIXES_PROGRESS.md` after each cycle

---

**Document Version**: 1.0
**Created**: 2025-11-07
**For**: MPP-Solar Chart Fixes Project
**Status**: Active
