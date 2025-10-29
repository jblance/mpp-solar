#!/bin/bash

# Log successful boot
echo "$(date): System boot completed successfully" >> /var/log/scheduled_reboots.log
echo "Uptime at boot completion: $(uptime)" >> /var/log/scheduled_reboots.log
echo "---" >> /var/log/scheduled_reboots.log
