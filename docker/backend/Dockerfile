FROM python:3.13.0a5-alpine

RUN apk update && \
    apk add --update --virtual build-deps gcc libc-dev linux-headers && \
    apk add jpeg-dev zlib-dev libpq=16.2-r1 python3-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

RUN apk upgrade

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN adduser -D django 

COPY --chown=django:django . . 

RUN chmod -R 755 /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt 
RUN pip install gunicorn

USER django

CMD [ "gunicorn", "web.wsgi", "-b 0.0.0.0:8000" ]