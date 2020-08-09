FROM python:3.8-alpine

COPY . /app

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps --update gcc build-base \
    && pip install pip==20.2.1 && pip install -r requirements/base.txt \
    && apk del .build-deps

CMD python src/app.py