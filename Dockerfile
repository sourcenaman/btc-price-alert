FROM alpine:3.18

ENV DockerHOME /home/app/price_alert

RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME

ENV PYTHONUNBUFFERED 1

COPY . $DockerHOME

RUN apk update \
    && apk upgrade \
    && apk add --no-cache python3 py3-pip \
    && pip install virtualenv \
    && virtualenv venv \
    && source venv/bin/activate \
    && pip install -r requirements.txt \
    && deactivate

EXPOSE 8000



