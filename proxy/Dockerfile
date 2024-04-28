FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params

USER root
RUN apk add --update --no-chahe --virtual .tmp openssl
RUN mkdir -p /vol/static
RUN chmod 755 /vol/static -R
RUN mkdir -p /etc/nginx/ssl
RUN chmod 755  /etc/nginx -R

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/secure_note.key -out /etc/nginx/ssl/secure_note.crt -subj "/C=ET/ST=Amhara/L=Bahir Dar/O=Bahir dar/CN=mintesnot.afework"

RUN apk del .tmp
# USER nginx