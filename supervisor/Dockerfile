FROM debian:latest

RUN apt-get update && apt-get install -y init && apt install -y python3-dev python3-pip supervisor

WORKDIR /code
ADD . /code

RUN chmod +x main_send_message_bot.sh
RUN cp main_send_message_bot.conf /etc/supervisor/conf.d/

