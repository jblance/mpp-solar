# Quick Start: House Historical Data

## TL;DR
Your house/weather data is now stored historically and displayed like the inverter charts!

## Activate in 3 Steps

### 1. Restart Web Server
```bash
sudo systemctl restart mpp-solar-web
```

### 2. Verify It's Working
```bash
# Check logs (Ctrl+C to exit)
sudo journalctl -u mpp-solar-web -n 50 | grep -i historical

# Should see:
# "Loading historical house and weather data from Prometheus files..."
# "Loaded XXXX house data points and XXXX weather data points"
```

### 3. Test in Browser
1. Open http://your-server:5000/house
2. Press F12 (open console)
3. Reload page
4. Look for: `[Historical] Loaded XXX indoor temp points`
5. **Charts should show hours of data immediately!**

## Quick Test Commands

```bash
# Count available data files
ls /home/constantine/mpp-solar/prometheus/house-*.prom | wc -l
ls /home/constantine/mpp-solar/prometheus/weather-*.prom | wc -l

# Test API endpoint
curl -s http://localhost:5000/api/house_historical | jq keys

# Expected output:
# [
#   "house_temperature",
#   "house_humidity",
#   "house_pressure",
#   "weather_temperature",
#   "weather_humidity",
#   "weather_pressure",
#   "weather_wind_speed",
#   "weather_wind_direction",
#   "weather_rain"
# ]

# Check data point count
curl -s http://localhost:5000/api/house_historical | \
  jq '{house_temp: .house_temperature | length, weather_temp: .weather_temperature | length}'

# Expected output (numbers vary):
# {
#   "house_temp": 487,
#   "weather_temp": 489
# }
```

## What Changed

### Before
- Charts started empty
- Only showed last ~50 minutes (100 points from localStorage)
- Data lost on browser clear

### After
- Charts show data immediately on page load
- Up to 41 hours of history per sensor (500 points)
- Data persists across all browsers/devices
- Works exactly like /charts page for inverter

## Troubleshooting

### Charts Still Empty?

1. **Check if data exists:**
   ```bash
   ls -lh /home/constantine/mpp-solar/prometheus/house-temperature-*.prom | head -5
   ```
   
   Should see files like: `house-temperature-20251029_144910.prom`

2. **Check if server loaded data:**
   ```bash
   sudo journalctl -u mpp-solar-web -n 100 | grep "Loaded.*data points"
   ```

3. **Check browser console:**
   - Open /house page
   - Press F12
   - Look for `[Historical]` messages
   - Should see "Loaded XXX indoor temp points"

4. **Test API directly:**
   ```bash
   curl http://localhost:5000/api/house_historical | jq '.house_temperature[0]'
   ```
   
   Should return something like:
   ```json
   {
     "timestamp": "2025-10-29T14:49:10",
     "value": 17.61
   }
   ```

### Server Won't Start?

```bash
# Check for syntax errors
python3 -m py_compile /home/constantine/mpp-solar/web_interface.py

# Check service status
sudo systemctl status mpp-solar-web

# View errors
sudo journalctl -u mpp-solar-web -n 50
```

## Files Modified

- `web_interface.py` - Backend server
- `templates/house.html` - Frontend charts

## Rollback If Needed

```bash
# Restore from git (if tracked)
cd /home/constantine/mpp-solar
git checkout HEAD~1 web_interface.py templates/house.html
sudo systemctl restart mpp-solar-web

# Or use backup files if they exist
cp web_interface.py.backup web_interface.py
cp templates/house.html.backup templates/house.html
sudo systemctl restart mpp-solar-web
```

## More Info

See `HOUSE_HISTORICAL_IMPLEMENTATION.md` for full technical details.

## Success Indicators

✅ Server logs show "Loaded XXXX house data points"
✅ API endpoint returns data: `/api/house_historical`
✅ Browser console shows "[Historical] Loaded XXX points"
✅ Charts display immediately on page load
✅ Charts show hours of historical data

**Enjoy your persistent house/weather charts! 🎉**
