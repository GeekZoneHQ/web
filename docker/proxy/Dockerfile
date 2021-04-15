FROM python:3.8-alpine

RUN apk update && \
    apk add --update --virtual build-deps gcc libc-dev linux-headers && \
    apk add jpeg-dev zlib-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN ["python", "manage.py", "collectstatic"]

CMD [ "gunicorn", "web.wsgi", "-b 0.0.0.0:8000" ]

FROM nginx:alpine

# note - should setup nginx user for security.

COPY docker/proxy/nginx.conf /etc/nginx/templates/nginx.conf.template
COPY --from=0 /usr/src/app/theme/static/css/styles.css /var/www/static
RUN rm /etc/nginx/conf.d/default.conf
