FROM alpine:3.10

COPY ./requirements.txt /opt/tanner/

# Setup apt
RUN sed -i 's/dl-cdn/dl-2/g' /etc/apk/repositories && \
    apk -U --no-cache add \
               build-base \
               git \
               libcap \
               libffi-dev \
               libressl-dev \
               linux-headers \
               py3-yarl \
               python3 \
               python3-dev && \
# Setup Tanner begin
    cd /opt/tanner/ && \
    pip3 install --no-cache-dir setuptools && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . /opt/tanner/

RUN cd /opt/tanner/ && \
    python3 setup.py install && \
    cd / && \
# Setup configs, user, groups
    chown -R nobody:nobody /opt/tanner && \
# Clean up
    apk del --purge \
            build-base \
            linux-headers \
            python3-dev && \
    rm -rf /root/* && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /var/cache/apk/*

# Start tanner
USER nobody:nobody
WORKDIR /opt/tanner
CMD tanner --config /opt/tanner/tanner/data/config.yaml
