# syntax=docker/dockerfile:1
FROM alpine:latest

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apk add --no-cache \
      python3-dev \
      py3-pip \
      libffi-dev \
      openssl-dev \
      gcc \
      libc-dev \
      make \
      && pip install --no-cache-dir -r requirements.txt


COPY app.py ./
COPY wsgi.py ./
COPY verwaltungonline verwaltungonline
EXPOSE 5000
#ENTRYPOINT [ "sh" ]
CMD ["gunicorn", "--access-logfile", "-", "--workers=2", "--threads=4", "--worker-class=gthread", "--worker-tmp-dir", "/dev/shm", "--bind", "0.0.0.0:5000", "wsgi:app"]
