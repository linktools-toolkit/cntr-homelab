#!/bin/sh

if [ -n "$MAINTENANCE_WINDOW_START" ]; then
    php /var/www/html/occ config:system:set maintenance_window_start --type=integer --value="$MAINTENANCE_WINDOW_START"
fi
