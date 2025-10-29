# Test Historical Data Loading

## Quick Test - Open Browser Console

1. Open /house page in browser
2. Press F12 to open console
3. Run this command to clear localStorage and force reload from server:

```javascript
localStorage.removeItem('houseChartData');
location.reload();
```

4. Watch console output - you should see:
```
[Historical] Loading house/weather data from server...
[Historical] Server data loaded: (9 keys)
[Historical] Loaded 266 indoor temp points
[Historical] Loaded 500 outdoor temp points
[Historical] Loaded 266 indoor humidity points
[Historical] Loaded 500 outdoor humidity points
[updateChartsDisplay] ✓ Charts updated successfully
[Historical] ✓ Charts updated with server data
```

## Verify API is Working

From terminal:
```bash
curl -s http://localhost:5000/api/house_historical | python3 -c "import sys, json; d=json.load(sys.stdin); print('Data counts:'); print('  house_temp:', len(d['house_temperature'])); print('  weather_temp:', len(d['weather_temperature'])); print('  house_hum:', len(d['house_humidity'])); print('  weather_hum:', len(d['weather_humidity']))"
```

Expected output:
```
Data counts:
  house_temp: 266
  weather_temp: 500
  house_hum: 266
  weather_hum: 500
```

## Check What's Actually Happening

In browser console after page load:
```javascript
// Check if data was loaded
console.log('Indoor temp points:', indoorTempHistory.length);
console.log('Outdoor temp points:', outdoorTempHistory.length);
console.log('Indoor humidity points:', indoorHumHistory.length);
console.log('Outdoor humidity points:', outdoorHumHistory.length);

// Check first data point timestamp
if (indoorTempHistory.length > 0) {
    console.log('First indoor temp point:', indoorTempHistory[0]);
    console.log('Last indoor temp point:', indoorTempHistory[indoorTempHistory.length - 1]);
}
```

## Force Manual Load

If automatic loading isn't working, try manual load in console:
```javascript
await loadHistoricalData();
```

## Check Network Tab

1. Open DevTools → Network tab
2. Reload page
3. Filter by "house_historical"
4. Check if request is made
5. Check response - should show JSON with data

## Troubleshooting

**If you see "Loaded 0 points":**
- Server might not have loaded data yet
- Check terminal: `./manage_web.sh status`
- Restart: `./manage_web.sh restart`

**If you see old localStorage data:**
- Clear it: `localStorage.removeItem('houseChartData')`
- Reload page

**If fetch fails:**
- Check network tab for errors
- Verify API works: `curl http://localhost:5000/api/house_historical`

**Charts still empty:**
- Check console for errors
- Verify temperatureChart and humidityChart exist
- Try: `temperatureChart.data.datasets[0].data.length`
