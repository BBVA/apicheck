FROM python:3.8-alpine as base

RUN apk update && \
    apk upgrade && \
    apk --no-cache --update add openssl ca-certificates

FROM base as builder

RUN apk add --no-cache build-base gcc musl-dev python3-dev libffi-dev openssl-dev libcurl curl-dev
COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --no-cache-dir -U pip wheel && \
    python -m pip wheel --no-cache-dir --wheel-dir=/root/wheels -r /app/requirements.txt

FROM base
COPY --from=builder /root/wheels /root/wheels
COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --no-cache --no-index --find-links=/root/wheels -r /app/requirements.txt
RUN rm -rf /root/wheels

COPY ./sensitive_json /app/sensitive_json
EXPOSE 8080
ENTRYPOINT ["python", "/app/sensitive_json/__main__.py"]
