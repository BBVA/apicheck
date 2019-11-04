FROM python:3.7-slim as BASE

RUN apt-get update \
    && pip install -U pip \
    && apt-get install --no-install-recommends -y gosu curl

FROM BASE as COMPILER
RUN apt-get install --no-install-recommends -y build-essential gcc python3-dev libffi-dev libyaml-0-2

COPY ./ /tmp

RUN cd /tmp && python setup.py install \
    && rm -rf /var/cache/apt \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache

ENTRYPOINT ["/bin/bash"]