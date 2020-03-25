FROM python:3.8-alpine

RUN apk update && apk upgrade --no-cache && apk add bash jq

COPY ./kapow-linux /usr/local/bin/kapow
RUN chmod +x /usr/local/bin/kapow

COPY ./ac_sensitive_data/requirements.txt /requirements.txt
RUN pip install -U -r /requirements.txt

COPY ./ac_sensitive_data /tmp/ac-sensitive-data
RUN cd /tmp/ac-sensitive-data && pip install .

COPY ./ac_sensitive.pow /ac_sensitive.pow

ENTRYPOINT ["/usr/local/bin/kapow", "server", "/ac_sensitive.pow"]