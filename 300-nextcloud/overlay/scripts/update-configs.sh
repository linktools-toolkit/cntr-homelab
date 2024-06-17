#!/bin/sh

if [ -n "$MAINTENANCE_WINDOW_START" ]; then
    php /var/www/html/occ config:system:set maintenance_window_start --type=integer --value="$MAINTENANCE_WINDOW_START"
fi

# OnlyOffice
if [ "$ONLYOFFICE_ENABLED" = 'yes' ]; then
#    while ! nc -z "$ONLYOFFICE_HOST" 80; do
#        echo "waiting for OnlyOffice to become available..."
#        sleep 5
#    done
    if ! [ -d "/var/www/html/custom_apps/onlyoffice" ]; then
        php /var/www/html/occ app:install onlyoffice
    elif [ "$(php /var/www/html/occ config:app:get onlyoffice enabled)" != "yes" ]; then
        php /var/www/html/occ app:enable onlyoffice
    elif [ "$SKIP_UPDATE" != 1 ]; then
        php /var/www/html/occ app:update onlyoffice
    fi
    php /var/www/html/occ config:system:set onlyoffice jwt_secret --value="$ONLYOFFICE_SECRET"
    php /var/www/html/occ config:app:set onlyoffice jwt_secret --value="$ONLYOFFICE_SECRET"
    php /var/www/html/occ config:system:set onlyoffice jwt_header --value="AuthorizationJwt"
    php /var/www/html/occ config:app:set onlyoffice DocumentServerUrl --value="$OVERWRITECLIURL/onlyoffice"
fi
