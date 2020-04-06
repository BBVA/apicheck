FROM python:3.8-alpine

RUN apk update \
    && apk add --no-cache build-base

COPY ./requirements.txt /app/requirements.txt
RUN pip install -U -r /app/requirements.txt \
    && rm -rf /var/cache/apk/* /var/tmp/* /tmp/* /root/.cache/*

COPY ./sendtoproxy /app/sendtoproxy

ENTRYPOINT ["python", "/app/sendtoproxy/__main__.py"]