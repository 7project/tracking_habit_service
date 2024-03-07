from loader import bot
from telebot.types import Message
from states.perform import PerformHabit
from sqlalchemy.orm import Session
from utils.req.crud import get_local_token_to_api, perform_habit, get_habit


@bot.message_handler(commands=["tracking"])
def bot_start(message: Message):
    bot.reply_to(message, f"Команда tracking - выполнить привычку {message.from_user.full_name}!")
    bot.set_state(message.from_user.id, PerformHabit.habit_id, message.chat.id)
    bot.send_message(message.chat.id, 'Введите id вашей привычки для ее трекинга, для пропуска ввода из команды нажмите'
                                      ' /cancel >>>')


@bot.message_handler(state=PerformHabit.habit_id)
def tracking_id_habit_get(message: Message, data: dict[str, Session]):
    """
    State 1.
    """
    if message.text == '0':
        bot.send_message(message.chat.id, f"Счетчик не увеличен!")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_:
            data_['habit_id'] = message.text

        token = get_local_token_to_api(session=data['session'], telegram_id=message.from_user.id)
        if token is None:
            bot.send_message(message.chat.id, f"Токен не получен")

        habit_response = get_habit(habit_id=data_['habit_id'], token=token)

        # TODO заменить 401 на статус кода из библиотеке status HTTP
        if habit_response.status_code == 401:
            bot.send_message(message.chat.id, f"Ошибка авторизации на сервере."
                                              f"Нажмите /token для повторной авторизации.")
            bot.delete_state(message.from_user.id, message.chat.id)

        # TODO заменить 404 на статус кода из библиотеке status HTTP
        if habit_response.status_code == 404:
            bot.send_message(message.chat.id, f"Не могу обновить счетчик данной привычки!\n"
                                              f"Проверьте есть ли id #{data_['habit_id']} данной привычки в вашем "
                                              f"списке /habits.")
            bot.delete_state(message.from_user.id, message.chat.id)

        habit_count = habit_response.json()['tracking']['count']
        out_habit_count = str(int(habit_count) + 1)
        json_data = {
            "habit": {
                "habit_id": data_["habit_id"],
            },
            "habit_update": {
                "tracking": {
                    "count": out_habit_count
                }
            }
        }

        perform_response = perform_habit(json_data=json_data, token=token)

        # TODO заменить 401 на статус кода из библиотеке status HTTP
        if perform_response.status_code == 401:
            bot.send_message(message.chat.id, f"Ошибка авторизации на сервере."
                                              f"Нажмите /token для повторной авторизации.")
            bot.delete_state(message.from_user.id, message.chat.id)

        # TODO заменить 409 на статус кода из библиотеке status HTTP
        if perform_response.status_code == 409:
            bot.send_message(message.chat.id, f"Invalid request get_user_to_telegram_id. "
                                              f"Нажмите /start для повторной авторизации.")

        # TODO заменить 422 на статус кода из библиотеке status HTTP
        if perform_response.status_code == 422:
            bot.send_message(message.chat.id, "422 Validation Error")

        if perform_response.status_code == 200:
            bot.send_message(message.chat.id, f"Счетчик привычки #{perform_response.json()['tracking']['habit_id']}: "
                                              f"{perform_response.json()['name_habit']}. - Увеличен.\n"
                                              f"Количество выполнений: {perform_response.json()['tracking']['count']}.\n"
                                              f"Просмотреть список всех привычек /habits.")
        else:
            bot.send_message(message.chat.id, f"Счетчик не увеличен! Ответ сервера: {perform_response.json()}")

    bot.delete_state(message.from_user.id, message.chat.id)
