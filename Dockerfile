FROM python:slim

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements/deploy.txt

CMD gunicorn -b 0.0.0.0:${PORT:=8000} -w 4 -t 300 wsgi:app