# ZeroTier Auto-Recovery System

## Overview
This system automatically monitors ZeroTier connectivity and restarts the service when issues are detected, eliminating the need for daily system reboots.

## Key Components

### 1. Health Check Script (`zerotier-health-check.sh`)
- **Auto-restart**: Automatically restarts ZeroTier when OFFLINE
- **Comprehensive checks**: Service status, connectivity, networks, peers
- **Smart logging**: Color-coded output with persistent logs
- **Flexibility**: Can disable auto-restart with `--no-restart` flag

**Usage:**
```bash
# Normal operation (with auto-restart)
sudo ./zerotier-health-check.sh

# Quiet mode (for cron)
sudo ./zerotier-health-check.sh --quiet

# Check only (no auto-restart)
sudo ./zerotier-health-check.sh --no-restart

# Custom log file
sudo ./zerotier-health-check.sh --log-file /path/to/logfile
```

### 2. Quick Status Script (`zt-status.sh`)
Quick overview of ZeroTier status without full health check.

**Usage:**
```bash
sudo ./zt-status.sh
```

### 3. Automated Monitoring Schedule
- **Health Check**: Every 5 minutes (auto-restart enabled)
- **Boot Logging**: Tracks successful system boots
- **Daily Reboot**: DISABLED (replaced with targeted auto-restart)

## Current Cron Schedule
```
*/5 * * * * /home/constantine/zerotier-health-check.sh --quiet
@reboot sleep 120 && /home/constantine/log-boot.sh
# DISABLED - Daily reboot replaced with ZeroTier auto-restart
# 5 0 * * * /home/constantine/reboot.sh
```

## Log Files
- **Main Health Log**: `/var/log/zerotier-health.log`
- **Boot Tracking**: `/var/log/scheduled_reboots.log`
- **Reboot Debugging**: `/var/log/reboot_attempts.log`

## Auto-Restart Behavior
When ZeroTier issues are detected:
1. **Detection**: Service down OR status OFFLINE
2. **Restart**: `systemctl restart zerotier-one`
3. **Verification**: Wait 15 seconds, verify ONLINE status
4. **Logging**: Full restart sequence logged with timestamps
5. **Recovery**: Continue with full health check if successful

## Benefits
- **Fast Recovery**: Issues resolved within 5 minutes maximum
- **Targeted Solution**: Only restarts ZeroTier, not entire system
- **Reduced Downtime**: No more daily reboot interruptions
- **Better Monitoring**: Detailed logs of all restart events
- **Flexible Control**: Can disable auto-restart when needed

## Manual Operations
```bash
# Check current ZeroTier status
sudo zerotier-cli status

# Quick status overview
sudo ./zt-status.sh

# Full health check with restart
sudo ./zerotier-health-check.sh

# Health check without restart
sudo ./zerotier-health-check.sh --no-restart

# View recent health logs
sudo tail -f /var/log/zerotier-health.log

# View auto-restart events
sudo grep "RESTART" /var/log/zerotier-health.log
```

## Troubleshooting
If auto-restart fails repeatedly:
1. Check logs: `sudo tail -20 /var/log/zerotier-health.log`
2. Manual restart: `sudo systemctl restart zerotier-one`
3. Check network connectivity: `ping 103.195.103.66`
4. Verify ZeroTier configuration: `sudo zerotier-cli listnetworks`

