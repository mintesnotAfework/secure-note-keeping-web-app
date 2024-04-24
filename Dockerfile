FROM python:3-alpine

ENV PATH="/scripts:${PATH}"

WORKDIR /app
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers

COPY  requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .tmp

COPY ./secure_note/ /app/
WORKDIR /app/

COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/static/password_rsa
RUN mkdir -p /vol/web/media
COPY ./secure_note/media /vol/web/media

RUN adduser -D user 
RUN chown -R user:user /vol
RUN chown -R user:user /app

RUN chmod -R 755 /vol/web
RUN chmod -R 755 /app


USER user
CMD ["entrypoint.sh"]