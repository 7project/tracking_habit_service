from telebot.types import Message
from sqlalchemy.orm import Session
from loader import bot
from sqlalchemy import select
from database.models import UserTelegram
from states.auth import AuthUser


@bot.message_handler(commands=["start"])
def bot_start(message: Message, data):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\n"
                          f"message_id -> {message.message_id}\n"
                          f"user_id -> {message.from_user.id}\n")

    bot.set_state(message.from_user.id, AuthUser.name, message.chat.id)
    bot.send_message(message.chat.id, 'Введите имя')

    # TODO пример записи в таблицу sqlite

    session: Session = data['session']
    first_user = UserTelegram(telegram_id=message.from_user.id,
                              token="asdasdasdfasdfasdfasdf", )
    session.add(first_user)
    session.commit()

    qwerty = select(UserTelegram)
    result = session.execute(qwerty)
    bot.reply_to(message, f"user -> , {result.scalars().all()}")

    # TODO написать логику запросов через requests to endpoint API

    # TODO Передать на вход функции user_id для запроса авторизованного пользователя
    # TODO если текущий пользователь есть -> обновить токен
    # TODO записать токен в таблицу telegram_id token

    # TODO если текущего пользователя нет -> запросить пароль, создать пользователя
    # TODO обновить токен
    # TODO записать токен в таблицу telegram_id token

    # TODO удалить сообщение о вводе пароля
    # TODO написать сообщение что пользователь авторизован\аутентифицирован


@bot.message_handler(state=AuthUser.name)
def name_get(message):
    """
    State 1.
    """
    bot.send_message(message.chat.id, 'Enter your password >>>')
    bot.set_state(message.from_user.id, AuthUser.password, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text


@bot.message_handler(state=AuthUser.password)
def password_get(message):
    """
    State 2.
    """
    # TODO нужно сформировать данные для запроса к API
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['password'] = message.text
    # TODO вызвать backend_authentication_to_service(user_id: int, password: str)
    bot.delete_state(message.from_user.id, message.chat.id)
