from loader import bot
from telebot.types import Message
from states.delete import DeletedHabit
from sqlalchemy.orm import Session

from utils.req.crud import get_local_token_to_api, deleted_habit


@bot.message_handler(commands=["delete"])
def bot_delete_habit(message: Message):
    bot.reply_to(message, f"Команда delete удаляет вашу привычку по id, {message.from_user.full_name}!")
    bot.set_state(message.from_user.id, DeletedHabit.habit_id, message.chat.id)
    bot.send_message(message.chat.id, 'Enter your number id habit to deleted >>>')


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
    if response.status_code == 401:
        bot.send_message(message.chat.id, f"Ошибка авторизации на сервере. "
                                          f"Нажмите /token для повторной авторизации.")
    # TODO заменить 409 на статус кода из библиотеке status HTTP
    if response.status_code == 409:
        bot.send_message(message.chat.id, f"Invalid request get_user_to_telegram_id. "
                                          f"Нажмите /start для повторной авторизации.")
    if response.status_code == 422:
        bot.send_message(message.chat.id, "422 Validation Error")

    if response.status_code == 405:
        bot.send_message(message.chat.id, "405 Method Not Allowed")

    if response.status_code == 204:
        bot.send_message(message.chat.id, f"Habit #{data_['habit_id']} - удалена!")
    elif response.status_code == 404:
        bot.send_message(message.chat.id, f"Habit #{data_['habit_id']} - не удалена!")
    else:
        bot.send_message(message.chat.id, f"Привычка #{data_['habit_id']} - не удалена! "
                                          f"Ответ сервера: {response.json()}")

    bot.delete_state(message.from_user.id, message.chat.id)
