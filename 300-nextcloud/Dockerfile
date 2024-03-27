FROM nextcloud:latest

RUN apt-get update && \
    apt-get install -y ffmpeg python3 curl aria2 youtube-dl && \
    ln -sf /usr/bin/aria2c /usr/local/bin/aria2c && \
    ln -sf /usr/bin/youtube-dl /usr/local/bin/youtube-dl \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/local/etc/php/conf.d/ && \
    chmod 777 /usr/local/etc/php/conf.d/
