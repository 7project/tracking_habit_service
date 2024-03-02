import datetime
from telebot.types import Message

from loader import bot
from states.update import UpdateHabit
from utils.req.crud import get_local_token_to_api, update_habit
from sqlalchemy.orm import Session


@bot.message_handler(commands=["update"])
def bot_update_habit(message: Message):
    bot.reply_to(message, f"Команда update, {message.from_user.full_name}!")
    bot.set_state(message.from_user.id, UpdateHabit.habit_id, message.chat.id)
    bot.send_message(message.chat.id, 'Enter your id habit to corrected >>>')


@bot.message_handler(state=UpdateHabit.habit_id)
def habit_id_update_habit(message: Message):
    """
    State 1.
    """
    bot.send_message(message.chat.id, 'Enter your name habit, enter number 0 (ZERO) to skip  >>>')
    bot.set_state(message.from_user.id, UpdateHabit.name_habit, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['habit_id'] = message.text


@bot.message_handler(state=UpdateHabit.name_habit)
def name_habit_update_habit(message: Message):
    """
    State 2.
    """
    bot.send_message(message.chat.id, 'Enter your description habit, enter number 0 (ZERO) to skip  >>>')
    bot.set_state(message.from_user.id, UpdateHabit.description, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == '0':
            data['name_habit'] = None
        else:
            data['name_habit'] = message.text


@bot.message_handler(state=UpdateHabit.description)
def description_update_habit(message: Message):
    """
    State 3.
    """
    time_now = datetime.datetime.now()
    bot.send_message(message.chat.id, f'Enter your alert time habit, exemple -> {time_now} '
                                      f'enter number 0 (ZERO) to skip >>>')
    bot.set_state(message.from_user.id, UpdateHabit.alert_time, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == '0':
            data['description'] = None
        else:
            data['description'] = message.text


@bot.message_handler(state=UpdateHabit.alert_time)
def alert_time_update_habit(message: Message):
    """
    State 4.
    """

    bot.send_message(message.chat.id, f'Enter your count completed habit, enter number 0 (ZERO) to skip >>>')
    bot.set_state(message.from_user.id, UpdateHabit.count, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == '0':
            data['alert_time'] = None
        else:
            data['alert_time'] = message.text


@bot.message_handler(state=UpdateHabit.count)
def count_update_habit(message: Message, data: dict[str, Session]):
    """
    State 5.
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_:
        if message.text == '0':
            data_['count'] = None
        else:
            data_['count'] = message.text

    # TODO сформировать json_data и вызвать
    # {
    #   "habit": {
    #     "habit_id": 0
    #   },
    #   "habit_update": {
    #     "name_habit": "string",
    #     "description": "string",
    #     "tracking": {
    #       "alert_time": "2024-03-02T19:29:35.433Z",
    #       "count": 0
    #     }
    #   }
    # }

    out_json_data = {
        "tracking": {

        }
    }

    json_data = {
        "habit": {
            "habit_id": data_["habit_id"],
        },
        "habit_update": {

        }
    }

    if data_['name_habit'] is not None and data_['name_habit'] != '':
        json_data['habit_update']['name_habit'] = data_['name_habit']
    if data_['description'] is not None and data_['description'] != '':
        json_data['habit_update']['description'] = data_['description']
    if data_['alert_time'] is not None and data_['alert_time'] != '':
        out_json_data['tracking']['alert_time'] = data_['alert_time']
    if data_['count'] is not None and data_['count'] != '':
        out_json_data['tracking']['count'] = data_['count']
    if ((data_['alert_time'] is not None and data_['alert_time'] != '')
            or (data_['count'] is not None and data_['count'] != '')):
        json_data['habit_update'].update(out_json_data)

    token = get_local_token_to_api(session=data['session'], telegram_id=message.from_user.id)
    if token is None:
        bot.send_message(message.chat.id, f"Токен не получен")

    response = update_habit(json_data=json_data, token=token)

    # TODO заменить 401 на статус кода из библиотеке status HTTP
    if response.status_code == 401:
        bot.send_message(message.chat.id, f"Ошибка авторизации на сервере."
                                          f"Нажмите /token для повторной авторизации.")

    # TODO заменить 409 на статус кода из библиотеке status HTTP
    if response.status_code == 409:
        bot.send_message(message.chat.id, f"Invalid request get_user_to_telegram_id. "
                                          f"Нажмите /start для повторной авторизации.")

    # TODO заменить 422 на статус кода из библиотеке status HTTP
    if response.status_code == 422:
        bot.send_message(message.chat.id, "422 Validation Error")

    if response.status_code == 200:
        bot.send_message(message.chat.id, f"Привычка #{response.json()['tracking']['habit_id']}: "
                                          f"{response.json()['name_habit']}. - Изменена.")
    else:
        bot.send_message(message.chat.id, f"Привычка не изменена! Ответ сервера: {response.json()}")

    bot.delete_state(message.from_user.id, message.chat.id)
