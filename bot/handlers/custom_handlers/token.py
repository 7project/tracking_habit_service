from database.models import UserTelegram
from loader import bot

from utils.auth.authentication import get_token
from telebot.types import Message
from states.auth import UpdateToken
from sqlalchemy.orm import Session


@bot.message_handler(commands=["token"])
def bot_token(message: Message):
    bot.reply_to(message, f"Команда token, {message.from_user.full_name}!")
    bot.set_state(message.from_user.id, UpdateToken.password, message.chat.id)
    bot.send_message(message.chat.id, 'Enter your password >>>')


@bot.message_handler(state=UpdateToken.password)
def password_get(message: Message, data: dict[str, Session]):
    """
    State 1.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_:
        data_['password'] = message.text
    # TODO удаляем сообщение с введенным именем пользователя
    bot.delete_message(message.chat.id, message.message_id)

    response = get_token(telegram_id=message.from_user.id, password=data_['password'])

    # TODO заменить 401 на статус кода из библиотеке status HTTP
    if response.status_code == 401:
        bot.send_message(message.chat.id, f"Ошибка авторизации на сервере. "
                                          f"Нажмите /start для повторной авторизации.")
    # TODO заменить 409 на статус кода из библиотеке status HTTP
    if response.status_code == 409:
        bot.send_message(message.chat.id, f"Invalid request get_user_to_telegram_id. "
                                          f"Нажмите /start для повторной авторизации.")

    if response.status_code == 200:
        # TODO Start
        result = response.json()
        session: Session = data['session']
        first_user = UserTelegram(telegram_id=message.from_user.id,
                                  token=result['access_token'], )
        session.add(first_user)
        session.commit()
        # TODO End
        bot.send_message(message.chat.id, f"Токен обновлен! Ответ сервера: {response.json()}")
    else:
        bot.send_message(message.chat.id, f"Токен не обновлен! Ответ сервера: {response.json()}")

    bot.delete_state(message.from_user.id, message.chat.id)
