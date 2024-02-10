FROM debian:unstable-slim

WORKDIR /code

RUN apt-get update && apt install -y python3-dev python3-pip systemd systemd-cron

ADD . /code

RUN chmod +x main_send_message_bot.py
RUN cp main_send_message_bot.service /etc/systemd/system/
