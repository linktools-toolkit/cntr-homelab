FROM nextcloud:{{ NEXTCLOUD_TAG }}

# RUN apt-get update && \
#     apt-get install -y ffmpeg python3 curl aria2 youtube-dl && \
#     ln -sf /usr/bin/aria2c /usr/local/bin/aria2c && \
#     ln -sf /usr/bin/youtube-dl /usr/local/bin/youtube-dl \
#     rm -rf /var/lib/apt/lists/*

RUN cat <<EOF > /docker-entrypoint-hooks.d/before-starting/900-custom-cron.sh
#!/bin/sh
/custom-cron.sh &
EOF

RUN cat <<EOF > /custom-cron.sh
#!/bin/sh
while true; do
    php -f /var/www/html/cron.php &
    sleep 5m
done
EOF

RUN mkdir -p /usr/local/etc/php/conf.d/ && \
    chmod 777 /usr/local/etc/php/conf.d/ && \
    chmod +x /docker-entrypoint-hooks.d/before-starting/900-custom-cron.sh && \
    chmod +x /custom-cron.sh

# {% if DOCKER_UID != 0 %}

RUN (groupadd -g {{ DOCKER_GID }} {{ DOCKER_USER }} || true) && \
    useradd -m -u {{ DOCKER_UID }} -g {{ DOCKER_GID }} {{ DOCKER_USER }}

# {% endif %}
