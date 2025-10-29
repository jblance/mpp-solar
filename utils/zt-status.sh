#!/bin/bash

# Quick ZeroTier Status Check
echo "=== ZeroTier Quick Status ==="
echo "Service: $(systemctl is-active zerotier-one)"

# Get ZeroTier status
ZT_STATUS=$(sudo zerotier-cli status 2>/dev/null)
if echo "$ZT_STATUS" | grep -q "ONLINE"; then
    echo "Status:  ONLINE"
elif echo "$ZT_STATUS" | grep -q "OFFLINE"; then
    echo "Status:  OFFLINE"
else
    echo "Status:  ERROR"
fi

echo "Networks:"
sudo zerotier-cli listnetworks 2>/dev/null | grep -v "<nwid>" | while read -r line; do
    if [[ -n "$line" ]]; then
        NAME=$(echo "$line" | awk '{print $4}')
        STATUS=$(echo "$line" | awk '{print $6}')
        DEV=$(echo "$line" | awk '{print $7}')
        IP=$(echo "$line" | awk '{print $8}')
        echo "  - $NAME: $STATUS (dev: $DEV, IP: $IP)"
    fi
done

PEER_COUNT=$(sudo zerotier-cli peers 2>/dev/null | grep -c 'DIRECT\|RELAY' || echo '0')
echo "Peers: $PEER_COUNT"
