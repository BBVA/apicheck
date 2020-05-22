FROM node:14-slim

WORKDIR /app
COPY . /app

RUN npm install && npm run build && npm install -g

ENTRYPOINT ac-replay
