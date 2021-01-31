FROM alpine:3.10

# use local versions of BFR and PHP ox
COPY ./BFR /opt/BFR
COPY ./ox /opt/phpox

#
# Install packages
RUN sed -i 's/dl-cdn/dl-2/g' /etc/apk/repositories && \
    apk -U --no-cache add \
               build-base \
               file \
               git \
               make \
               php7 \
               php7-dev \
               php7-tokenizer \
               python3 \
               python3-dev \
               re2c && \
# BFR copied above
    cd /opt/BFR && \
    phpize7 && \
    ./configure \
      --with-php-config=/usr/bin/php-config7 \
      --enable-bfr && \
    make && \
    make install && \
    cd / && \
    rm -rf /opt/BFR /tmp/* /var/tmp/* && \
    echo "zend_extension = "$(find /usr -name bfr.so) >> /etc/php7/php.ini && \
# PHP ox copied above
    cd /opt/phpox && \
    pip3 install -r requirements.txt && \
    make && \
# Clean up
    apk del --purge build-base \
                    git \
                    php7-dev \
                    python3-dev && \
    rm -rf /root/* && \
    rm -rf /var/cache/apk/*
    
# Set workdir and start phpsandbox
USER nobody:nobody
WORKDIR /opt/phpox
CMD ["python3", "sandbox.py"]
