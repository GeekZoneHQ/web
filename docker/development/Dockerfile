FROM python:3.8-alpine

RUN apk update && \
    apk add --update --virtual build-deps gcc libc-dev linux-headers && \
    apk add jpeg-dev zlib-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

RUN apk add --update nodejs-current npm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .
 
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
 
CMD [ "gunicorn", "web.wsgi", "-b 0.0.0.0:8000" ]