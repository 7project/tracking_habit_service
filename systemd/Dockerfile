FROM debian:buster

RUN apt-get update && apt-get install -y init && apt install -y python3-dev python3-pip systemd

WORKDIR /code
ADD . /code

RUN chmod +x main_send_message_bot.py
RUN cp main_send_message_bot.service /etc/systemd/system/
CMD ["sh", "-c", "sudo systemctl enable main_send_message_bot.service"]
CMD ["sh", "-c", "sudo systemctl start main_send_message_bot.service"]

