FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

CMD [ "gunicorn", "web.wsgi", "-b 0.0.0.0:8000" ]
