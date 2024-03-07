import datetime
import json
from pprint import pprint

from telebot.types import Message
from sqlalchemy.orm import Session
from loader import bot
from utils.req.crud import get_local_token_to_api, get_habits


@bot.message_handler(commands=["habits"])
def bot_start(message: Message, data: dict[str, Session]):
    bot.reply_to(message, f"Команда /habits, выводит все ваши привычки, {message.from_user.full_name}!")

    token = get_local_token_to_api(session=data['session'], telegram_id=message.from_user.id)
    if token is None:
        bot.send_message(message.chat.id, f"Токен не получен")
    response = get_habits(token)

    # TODO заменить 405 на статус кода из библиотеке status HTTP
    if response.status_code == 405:
        bot.send_message(message.chat.id, "405 Method Not Allowed")
    # TODO заменить 401 на статус кода из библиотеке status HTTP
    if response.status_code == 401:
        bot.send_message(message.chat.id, f"Ошибка авторизации на сервере. "
                                          f"Нажмите /token для повторной авторизации.")
    # TODO заменить 200 на статус кода из библиотеке status HTTP
    if response.status_code == 200:
        data_response = json.loads(response.text)
        if data_response is not None:
            for items in data_response:
                try:
                    output_string_datatime = datetime.datetime.strptime(items['tracking']['alert_time'],
                                                                        '%Y-%m-%dT%H:%M:%S.%fZ')
                    correct_format_datetime = output_string_datatime.strftime('%d %A %Y, %H:%M')
                    bot.send_message(message.chat.id,
                                     f"Привычка #{items['tracking']['habit_id']} - {items['name_habit']}.\n"
                                     f"Описание: {items['description']}.\n"
                                     f"Время создания\\выполнения: {correct_format_datetime}\n"
                                     f"Количество выполнения привычки: {items['tracking']['count']}.")
                except ValueError:
                    bot.send_message(message.chat.id, f"Не правильный формат времени привычки "
                                                      f"#{items['tracking']['habit_id']} \n ожидается такой "
                                                      f"{datetime.datetime.now()}\n"
                                                      f"Введите новый формат времени изменив ее /update.")
            bot.send_message(message.chat.id, f"Используйте команду /tracking для выполнении привычки указав ее #id")
        else:
            bot.send_message(message.chat.id, f"Список привычек пуст.")
