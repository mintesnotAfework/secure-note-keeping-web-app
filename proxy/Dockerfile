FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params

USER root
RUN apk add --update --no-chahe --virtual .tmp openssl
RUN mkdir -p /vol/static
RUN chmod 755 /vol/static
RUN mkdir -p /etc/nginx/ssl
RUN chmod 700 /etc/nginx/ssl

RUN openssl req -x509 -newKey rsa:4096 -nodes -k

RUN apk del .tmp
USER nginx