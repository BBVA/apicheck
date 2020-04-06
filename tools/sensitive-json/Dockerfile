FROM cr0hn/docker-python-async-deps

RUN apk update \
    && apk add --no-cache build-base

COPY ./requirements.txt /app/sensitive_json/requirements.txt
RUN pip install -U -r /app/sensitive_json/requirements.txt \
    && rm -rf /var/cache/apk/* /var/tmp/* /tmp/* /root/.cache/*

COPY ./sensitive_json /app/sensitive_json

EXPOSE 8080
ENTRYPOINT ["python", "/app/sensitive_json/__main__.py"]