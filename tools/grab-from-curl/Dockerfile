FROM python:3.8.2

COPY . /app

WORKDIR /app
RUN pip install -r requirements.txt && pip install .
RUN chmod +x burl

ENTRYPOINT ["/app/burl"] 
