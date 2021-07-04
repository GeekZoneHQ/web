FROM python:3.8-alpine

RUN apk update && \
    apk add --update --virtual build-deps gcc libc-dev linux-headers && \
    apk add jpeg-dev zlib-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN adduser -D django
RUN chown -R django:django /usr/src/app && chmod -R 755 /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

USER django
 
CMD [ "gunicorn", "web.wsgi", "-b 0.0.0.0:8000" ]