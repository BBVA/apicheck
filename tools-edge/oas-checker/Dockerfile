FROM node:14.11.0-alpine3.12

RUN apk update && \
    apk upgrade && \
    npm install -g @stoplight/spectral

# Load default ruleset from a suitable source
COPY spectral.yml .spectral.yml

COPY linter.sh /bin

ENTRYPOINT ["linter.sh"]
