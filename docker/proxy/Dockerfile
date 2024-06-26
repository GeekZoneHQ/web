FROM python:3.12.0rc2-alpine

RUN apk update && \
    apk add --update --virtual build-deps gcc libc-dev linux-headers && \
    apk add jpeg-dev zlib-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

RUN apk upgrade

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN ["python", "manage.py", "collectstatic"]

CMD [ "gunicorn", "web.wsgi", "-b 0.0.0.0:8000" ]

FROM nginx:alpine

RUN apk update && apk upgrade

# Install the fixed versions of libwebp and curl
RUN apk add --no-cache libwebp=1.3.2-r0 curl=8.5.0-r0

COPY docker/proxy/default.conf /etc/nginx/conf.d/
COPY docker/proxy/nginx.conf /etc/nginx/
COPY --from=0 /usr/src/app/static /var/www/static 

USER nginx