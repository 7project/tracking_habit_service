FROM debian

WORKDIR /code

RUN apt-get update && apt install -y python3-dev curl cron
RUN pip install --upgrade pip

ADD . /code

RUN chmod +x main_send_message_bot.py
RUN cp main_send_message_bot.service /etc/systemd/system/
RUN systemctl enable main_send_message_bot.service
RUN systemctl start main_send_message_bot.service
