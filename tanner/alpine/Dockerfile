FROM alpine:latest

RUN apk add --update --no-cache busybox-extras 

RUN addgroup -S www-data && adduser -S www-data -G www-data --home /var/www \
    && addgroup admin && adduser admin -G admin --home /home/admin/ --disabled-password \
    && mkdir /home/admin/.ssh/ \
    && touch /home/admin/.ssh/is_rsa /home/admin/.ssh/is_rsa.pub \
    && echo "admin:password123" | chpasswd \
    && echo "" > /etc/motd \
    && chmod +r /etc/shadow

ENTRYPOINT [ "telnetd", "-F" ]