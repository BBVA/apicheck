#!/usr/bin/env bash

docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD

for tool_dir in $(ls tools); do

  # Add plugin title to documentation file
  DOCKERFILE="tools/${tool_dir}/Dockerfile"
  DOCKER_IMAGE_NAME=$(cat tools/${tool_dir}/META | jq -r ".name")
  DOCKER_IMAGE_VERSION=$(cat tools/${tool_dir}/META | jq -r ".version")

  docker build -T ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION} -t ${DOCKER_IMAGE_NAME}:latest ${DOCKERFILE}
  docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION}
  docker push ${DOCKER_IMAGE_NAME}:latest
done