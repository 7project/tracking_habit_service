FROM debian:buster

RUN apt-get update && apt-get install -y init && apt install -y python3-dev python3-pip systemd

WORKDIR /code
ADD . /code

RUN chmod +x main_send_message_bot.py
RUN cp main_send_message_bot.service /etc/systemd/system/
RUN service main_send_message_bot.service on
RUN service main_send_message_bot.service start
