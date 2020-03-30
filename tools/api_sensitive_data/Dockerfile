FROM python:3.8-alpine

RUN apk update \
    && apk add --no-cache build-base

COPY ./ac_sensitive_data/requirements.txt /requirements.txt
RUN pip install -U -r /requirements.txt \
    && rm -rf /var/cache/apk/* /var/tmp/* /tmp/* /root/.cache/*

COPY ./ac_sensitive_data /tmp/ac-sensitive-data
RUN cd /tmp/ac-sensitive-data && pip install . && rm -rf /tmp

EXPOSE 8080
ENTRYPOINT ["ac-sensitive", "--server", "0.0.0.0:8080"]