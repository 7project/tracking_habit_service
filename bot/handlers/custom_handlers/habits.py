import datetime
import json
import re
from pprint import pprint

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session

from database.schedule.get_data_schedule import update_tracking_habit_count_add_one
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
                    markup_inline = InlineKeyboardMarkup()
                    tracking = InlineKeyboardButton(text="Выполнить",
                                                    callback_data=f"tracking_habit_now_id{items['tracking']['habit_id']}")
                    skip = InlineKeyboardButton(text="Пропустить", callback_data="tracking_habit_skip")
                    markup_inline.add(tracking, skip)

                    bot.send_message(message.chat.id,
                                     f"Привычка #{items['tracking']['habit_id']} - {items['name_habit']}.\n"
                                     f"Описание: {items['description']}.\n"
                                     f"Время создания\\выполнения: {correct_format_datetime}\n"
                                     f"Количество выполнения привычки: {items['tracking']['count']}.",
                                     reply_markup=markup_inline)
                except ValueError:
                    bot.send_message(message.chat.id, f"Не правильный формат времени привычки "
                                                      f"#{items['tracking']['habit_id']} \n ожидается такой "
                                                      f"{datetime.datetime.now()}\n"
                                                      f"Введите новый формат времени изменив ее /update.")
            # bot.send_message(message.chat.id, f"Используйте команду /tracking для выполнении привычки указав ее #id")
        else:
            bot.send_message(message.chat.id, f"Список привычек пуст.")


@bot.callback_query_handler(state="*", func=lambda call: str(call.data).startswith("tracking_"))
def tracking_habit_now_skip(call):
    if str(call.data).startswith("tracking_habit_now_id"):
        habit_id = re.search("tracking_habit_now_id*?(\d+)", call.data).group(1)
        print("re.search  habit_id >>>>", habit_id)
        print("tracking_habit_now_id  call.data >>>>", call.data)
        # TODO Написать логику выполнения привычки запрос к базе на +1
        update_tracking_habit_count_add_one(habit_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "tracking_habit_skip":
        bot.delete_message(call.message.chat.id, call.message.message_id)

