FROM python:3.8-alpine

RUN apk update \
    && apk add --no-cache build-base

COPY ./requirements.txt /app/sensitive_json/requirements.txt
RUN pip install -U -r /app/sensitive_json/requirements.txt \
    && rm -rf /var/cache/apk/* /var/tmp/* /tmp/* /root/.cache/*

COPY ./sensitive_json /app/sensitive_json

EXPOSE 8080
ENTRYPOINT ["/app/sensitive_json/__main__", "--server", "0.0.0.0:8080"]