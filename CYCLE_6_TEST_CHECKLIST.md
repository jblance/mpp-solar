# CYCLE 6: Quick Test Checklist

**Use this for rapid testing. See CYCLE_6_TEST_PLAN.md for detailed procedures.**

---

## Pre-Flight Check

```bash
# 1. Web server running?
python web_interface.py

# 2. Daemon running?
sudo systemctl status mpp-solar-daemon

# 3. URLs accessible?
# http://localhost:5000/charts
# http://localhost:5000/charts/lcars
```

---

## ✅ Quick Happy Path (5 minutes)

### Standard Charts
- [ ] Go to http://localhost:5000/charts
- [ ] All 6 charts visible with data?
- [ ] Console shows 6 "initialized successfully" messages?
- [ ] No red errors in console?
- [ ] Data summary cards populated?
- [ ] Click "Refresh Charts" - works?
- [ ] Change time range - updates?

### LCARS Charts
- [ ] Go to http://localhost:5000/charts/lcars
- [ ] All 5 charts visible with LCARS theme?
- [ ] Console shows 5 "LCARS ... initialized successfully" messages?
- [ ] No red errors in console?
- [ ] Orange/purple colors applied?
- [ ] Data summary cards show metrics?

**If all ✅ above: Happy path PASSED**

---

## ⚠️ Quick Error Tests (10 minutes)

### Test 1: No Data
```bash
# Stop daemon
sudo systemctl stop mpp-solar-daemon

# Reload chart page
# Expected: Info message "No historical data available yet"
```
- [ ] Info message displays (not error)?
- [ ] Charts render empty (no crash)?
- [ ] Retry button NOT shown (this is info, not error)?

```bash
# Restart daemon
sudo systemctl start mpp-solar-daemon
```

---

### Test 2: API Down
```bash
# Stop web server (Ctrl+C)
```
- [ ] Browser: Click "Refresh Charts"
- [ ] Error message displays?
- [ ] "Error loading data: HTTP ..." shown?
- [ ] Retry button visible?
- [ ] Click retry - works when server restarted?

```bash
# Restart web server
python web_interface.py
```

---

### Test 3: Missing Canvas
Edit `templates/charts.html`:
```html
<!-- Change line ~144: -->
<canvas id="batteryVoltageChart"></canvas>
<!-- To: -->
<canvas id="batteryVoltageChart_BROKEN"></canvas>
```

Reload page:
- [ ] Console warning: "Battery Voltage Chart canvas not found"?
- [ ] Other 5 charts still load?
- [ ] Page doesn't crash?

Revert change:
```bash
git checkout templates/charts.html
```

---

### Test 4: Time Range Selector
- [ ] Select "Last Hour" - chart updates?
- [ ] Select "Last Week" - chart updates?
- [ ] Console shows "Loading data..." during update?
- [ ] No errors?

**If all ✅ above: Error handling PASSED**

---

## 🌐 Quick Browser Test (5 minutes)

- [ ] Test in Chrome - works?
- [ ] Test in Firefox - works?
- [ ] Test in another browser - works?

---

## 📱 Quick Responsive Test (3 minutes)

### Desktop
- [ ] Full screen browser - charts use full width?

### Mobile Emulation
```
DevTools → Toggle device toolbar (Ctrl+Shift+M)
Select: iPhone 12 Pro
```
- [ ] Charts visible on mobile viewport?
- [ ] Tabs work on mobile?
- [ ] Text readable?
- [ ] No horizontal scroll?

---

## ⚡ Quick Performance Check (2 minutes)

```
DevTools → Network tab → Hard reload (Ctrl+Shift+R)
```
- [ ] Page loads in < 2 seconds?
- [ ] Charts render quickly?
- [ ] No "hanging" on data fetch?

---

## 📊 Results

**Date:** _________
**Tester:** _________

### Summary
- Happy Path: ✅ / ❌
- Error Handling: ✅ / ❌
- Cross-Browser: ✅ / ❌
- Responsive: ✅ / ❌
- Performance: ✅ / ❌

### Issues Found
1. ___________________________________
2. ___________________________________
3. ___________________________________

### Overall Status
- [ ] **PASS** - Ready for Phase 7 (Documentation)
- [ ] **NEEDS WORK** - Issues must be fixed
- [ ] **BLOCKED** - Cannot proceed

---

## Quick Issue Template

**Issue:** [Short description]
**Severity:** High / Medium / Low
**Browser:** Chrome / Firefox / Safari / Other
**Steps:**
1. ...
2. ...

**Expected:** ...
**Actual:** ...

---

## Next Steps After Testing

### If all tests PASS:
1. Mark Phase 6 complete in CYCLE_6.md
2. Proceed to Phase 7: Documentation
3. Prepare for merge to main branch

### If issues found:
1. Document each issue above
2. Fix critical/high severity issues
3. Re-test failed scenarios
4. Update test checklist with results

---

**Time Estimate:** ~25 minutes for full quick test
**Recommended:** Run full CYCLE_6_TEST_PLAN.md for production release
