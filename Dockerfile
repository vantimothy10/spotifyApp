# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /SpotifyApp

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV LISTEN_PORT = 8080
EXPOSE 8080

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]