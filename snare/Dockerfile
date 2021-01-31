FROM python:3.6-alpine3.8

RUN apk -U --no-cache add git build-base && \
    rm -rf /root/* && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /var/cache/apk/*
RUN pip3 install --no-cache-dir -U pip setuptools
ADD requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ADD . .
RUN python3 setup.py install
ENV PORT 80

CMD snare --no-dorks true --auto-update false --host-ip 0.0.0.0 --port $PORT --page-location "$PAGE_LOCATION" --tanner $TANNER
