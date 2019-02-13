#!/bin/bash

TESTS_PATH=$1
WORKER_ADDR=$2
WORKER_PORT=$3

py.test --tx socket=${WORKER_ADDR}:${WORKER_PORT} --rsyncdir ${TESTS_PATH} ${TESTS_PATH}