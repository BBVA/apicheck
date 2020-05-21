FROM node:14.2

WORKDIR /app
COPY . /app

RUN npm install && npm run build && npm install -g

ENTRYPOINT ac-replay
