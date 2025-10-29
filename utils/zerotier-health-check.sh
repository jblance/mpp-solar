#!/bin/bash

# ZeroTier Health Check Script with Auto-Restart
# Usage: ./zerotier-health-check.sh [--quiet] [--log-file <path>] [--no-restart]

QUIET=0
LOG_FILE="/var/log/zerotier-health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
EXIT_CODE=0
AUTO_RESTART=1

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --quiet)
            QUIET=1
            shift
            ;;
        --log-file)
            LOG_FILE="$2"
            shift 2
            ;;
        --no-restart)
            AUTO_RESTART=0
            shift
            ;;
        *)
            echo "Usage: $0 [--quiet] [--log-file <path>] [--no-restart]"
            exit 1
            ;;
    esac
done

log() {
    local level=$1
    local message=$2
    local log_entry="[$TIMESTAMP] [$level] $message"
    
    echo "$log_entry" >> "$LOG_FILE"
    
    if [[ $QUIET -eq 0 ]]; then
        case $level in
            "ERROR")
                echo -e "\033[31m$log_entry\033[0m" >&2
                ;;
            "WARN")
                echo -e "\033[33m$log_entry\033[0m"
                ;;
            "INFO")
                echo -e "\033[32m$log_entry\033[0m"
                ;;
            "RESTART")
                echo -e "\033[36m$log_entry\033[0m"
                ;;
            *)
                echo "$log_entry"
                ;;
        esac
    fi
}

restart_zerotier() {
    log "RESTART" "Attempting to restart ZeroTier service..."
    
    if systemctl restart zerotier-one; then
        log "RESTART" "ZeroTier service restart initiated"
        
        # Wait a moment for service to start
        sleep 5
        
        # Check if restart was successful
        if systemctl is-active --quiet zerotier-one; then
            log "RESTART" "ZeroTier service restart successful"
            
            # Wait a bit more for ZeroTier to establish connectivity
            sleep 10
            
            # Check connectivity again
            ZT_STATUS_AFTER=$(sudo zerotier-cli status 2>/dev/null)
            if echo "$ZT_STATUS_AFTER" | grep -q "ONLINE"; then
                log "RESTART" "ZeroTier connectivity restored - now ONLINE"
                return 0
            else
                log "ERROR" "ZeroTier service restarted but still showing: $(echo $ZT_STATUS_AFTER | awk '{print $4}')"
                return 1
            fi
        else
            log "ERROR" "ZeroTier service restart failed - service not active"
            return 1
        fi
    else
        log "ERROR" "Failed to restart ZeroTier service"
        return 1
    fi
}

# Check 1: Service Status
log "INFO" "Starting ZeroTier health check..."

SERVICE_FAILED=0
if ! systemctl is-active --quiet zerotier-one; then
    log "ERROR" "ZeroTier service is not running"
    SERVICE_FAILED=1
    EXIT_CODE=1
else
    log "INFO" "ZeroTier service is running"
fi

# Check 2: ZeroTier Status
ZT_STATUS_FAILED=0
ZT_STATUS=$(sudo zerotier-cli status 2>/dev/null)
if [[ $? -ne 0 ]]; then
    log "ERROR" "Cannot communicate with ZeroTier daemon"
    ZT_STATUS_FAILED=1
    EXIT_CODE=1
else
    if echo "$ZT_STATUS" | grep -q "ONLINE"; then
        log "INFO" "ZeroTier status: ONLINE"
    else
        ZT_CURRENT_STATUS=$(echo $ZT_STATUS | awk '{print $4}')
        log "ERROR" "ZeroTier status: $ZT_CURRENT_STATUS"
        ZT_STATUS_FAILED=1
        EXIT_CODE=1
    fi
fi

# Auto-restart logic
if [[ $AUTO_RESTART -eq 1 ]] && [[ $EXIT_CODE -ne 0 ]] && ([[ $SERVICE_FAILED -eq 1 ]] || [[ $ZT_STATUS_FAILED -eq 1 ]]); then
    log "RESTART" "ZeroTier issues detected - initiating auto-restart"
    
    if restart_zerotier; then
        log "RESTART" "Auto-restart successful - continuing health check"
        # Reset exit code since we recovered
        EXIT_CODE=0
        SERVICE_FAILED=0
        ZT_STATUS_FAILED=0
    else
        log "ERROR" "Auto-restart failed - manual intervention may be required"
        EXIT_CODE=1
    fi
fi

# Continue with remaining checks only if service is working
if [[ $SERVICE_FAILED -eq 0 ]] && [[ $ZT_STATUS_FAILED -eq 0 ]]; then
    # Check 3: Network Status
    NETWORKS=$(sudo zerotier-cli listnetworks 2>/dev/null | grep -v "<nwid>")
    if [[ -z "$NETWORKS" ]]; then
        log "WARN" "No ZeroTier networks configured"
    else
        while read -r network; do
            if [[ -n "$network" ]]; then
                NETWORK_ID=$(echo "$network" | awk '{print $3}')
                NETWORK_NAME=$(echo "$network" | awk '{print $4}')
                NETWORK_STATUS=$(echo "$network" | awk '{print $6}')
                
                if [[ "$NETWORK_STATUS" == "OK" ]]; then
                    log "INFO" "Network $NETWORK_NAME ($NETWORK_ID): $NETWORK_STATUS"
                else
                    log "ERROR" "Network $NETWORK_NAME ($NETWORK_ID): $NETWORK_STATUS"
                    EXIT_CODE=1
                fi
            fi
        done <<< "$NETWORKS"
    fi

    # Check 4: Interface Status
    ZT_INTERFACES=$(ip link show | grep zt | wc -l)
    if [[ $ZT_INTERFACES -eq 0 ]]; then
        log "WARN" "No ZeroTier interfaces found"
    else
        log "INFO" "Found $ZT_INTERFACES ZeroTier interface(s)"
        
        # Check specific interface from our network
        if ip link show ztly5x5dt4 >/dev/null 2>&1; then
            if ip link show ztly5x5dt4 | grep -q "UP"; then
                log "INFO" "Interface ztly5x5dt4 is UP"
                
                # Check IP assignment
                ZT_IP=$(ip addr show ztly5x5dt4 | grep "inet " | awk '{print $2}')
                if [[ -n "$ZT_IP" ]]; then
                    log "INFO" "Interface ztly5x5dt4 has IP: $ZT_IP"
                else
                    log "WARN" "Interface ztly5x5dt4 has no IP assigned"
                fi
            else
                log "ERROR" "Interface ztly5x5dt4 is DOWN"
                EXIT_CODE=1
            fi
        fi
    fi

    # Check 5: Peer Connectivity
    PEER_COUNT=$(sudo zerotier-cli peers 2>/dev/null | grep -c "DIRECT\|RELAY")
    if [[ $PEER_COUNT -eq 0 ]]; then
        log "ERROR" "No active peers found"
        EXIT_CODE=1
    else
        log "INFO" "Active peers: $PEER_COUNT"
        
        # Check planet connectivity
        PLANET_COUNT=$(sudo zerotier-cli peers 2>/dev/null | grep -c "PLANET.*DIRECT")
        if [[ $PLANET_COUNT -eq 0 ]]; then
            log "WARN" "No direct planet connections"
        else
            log "INFO" "Direct planet connections: $PLANET_COUNT"
        fi
    fi

    # Check 6: Connectivity Test
    log "INFO" "Testing connectivity to ZeroTier root server..."
    if ping -c 2 -W 3 103.195.103.66 >/dev/null 2>&1; then
        log "INFO" "ZeroTier root server ping: SUCCESS"
    else
        log "ERROR" "ZeroTier root server ping: FAILED"
        EXIT_CODE=1
    fi

    # Check 7: Test peer connectivity (if available)
    if ping -c 1 -W 2 10.42.1.51 >/dev/null 2>&1; then
        log "INFO" "Peer connectivity test (10.42.1.51): SUCCESS"
    else
        log "WARN" "Peer connectivity test (10.42.1.51): FAILED"
    fi
fi

# Summary
if [[ $EXIT_CODE -eq 0 ]]; then
    log "INFO" "ZeroTier health check: PASSED"
else
    log "ERROR" "ZeroTier health check: FAILED"
fi

log "INFO" "Health check completed"

exit $EXIT_CODE
