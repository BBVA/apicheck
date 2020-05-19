#!/bin/sh

LISTEN_ADDR=${LISTEN_ADD:=0.0.0.0}
LISTEN_PORT=${LISTEN_PORT:=8080}

mitmdump -s /addons/apicheck_addon.py --flow-detail 0 --cert *=/data/certificates/apicheck.pem --listen-host ${LISTEN_ADDR} --listen-port ${LISTEN_PORT}

