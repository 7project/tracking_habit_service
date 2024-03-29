from loader import bot
from telebot.types import Message
from states.delete import DeletedHabit
from sqlalchemy.orm import Session

from utils.req.crud import get_local_token_to_api, deleted_habit


@bot.message_handler(commands=["delete"])
def bot_delete_habit(message: Message):
    bot.reply_to(message, f"Команда /delete удаляет вашу привычку по ее id, {message.from_user.full_name}!")
    bot.set_state(message.from_user.id, DeletedHabit.habit_id, message.chat.id)
    bot.send_message(message.chat.id, 'Введите id привычки для удаления, для выхода из команды нажмите /cancel  >>>')


@bot.message_handler(state=DeletedHabit.habit_id)
def habit_id_get(message: Message, data: dict[str, Session]):
    """
    State 1.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_:
        data_['habit_id'] = message.text

    token = get_local_token_to_api(session=data['session'], telegram_id=message.from_user.id)
    if token is None:
        bot.send_message(message.chat.id, f"Токен не получен")

    response = deleted_habit(habit_id=data_['habit_id'], token=token)
    # TODO заменить 401 на статус кода из библиотеке status HTTP
    if response.status_code == 401:
        bot.send_message(message.chat.id, f"Ошибка авторизации на сервере. "
                                          f"Нажмите /token для повторной авторизации.")

    # TODO заменить 409 на статус кода из библиотеке status HTTP
    if response.status_code == 409:
        bot.send_message(message.chat.id, f"Invalid request get_user_to_telegram_id. "
                                          f"Нажмите /start для повторной авторизации.")

    # TODO заменить 422 на статус кода из библиотеке status HTTP
    if response.status_code == 422:
        print('habit_id_get delete - 422 Validation Error')
        # bot.send_message(message.chat.id, "422 Validation Error")

    # TODO заменить 405 на статус кода из библиотеке status HTTP
    if response.status_code == 405:
        print('habit_id_get delete - 405 Method Not Allowed')
        # bot.send_message(message.chat.id, "405 Method Not Allowed")
    # TODO заменить 204 на статус кода из библиотеке status HTTP
    if response.status_code == 204:
        bot.send_message(message.chat.id, f"Habit #{data_['habit_id']} - удалена!")
    # TODO заменить 404 на статус кода из библиотеке status HTTP
    elif response.status_code == 404:
        bot.send_message(message.chat.id, f"Habit #{data_['habit_id']} - не удалена!")
    else:
        bot.send_message(message.chat.id, f"Привычка #{data_['habit_id']} - не удалена! ")

    bot.delete_state(message.from_user.id, message.chat.id)
