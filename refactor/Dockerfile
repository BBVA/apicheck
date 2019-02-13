FROM python:3.5-slim
MAINTAINER daniel.garcia2@bbva.com

ENV PORT=8888 \
    PYTHONDONTWRITEBYTECODE=1

# Install python dependecies
COPY requirements-runtest.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Install API Test
COPY dist/apitest-1.0.0.tar.gz /tmp/
RUN pip install /tmp/apitest-1.0.0.tar.gz

# Add new user
RUN adduser --disabled-password --gecos "" pytest

# Add xdist server
COPY thirdparty/socketserver.py /usr/local/bin/socketserver
RUN chmod +x /usr/local/bin/socketserver && chown pytest:pytest /usr/local/bin/socketserver

EXPOSE $PORT
USER pytest

CMD /usr/local/bin/socketserver