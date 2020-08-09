FROM python:3.8-alpine

COPY . /app

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps --update gcc build-base \
    && pip install pip==20.2.1 && pip install -r requirements/deploy.txt \
    && apk del .build-deps

CMD gunicorn -b 0.0.0.0:$PORT -w 4 -t 300 src.wsgi:app