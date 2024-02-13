from telebot.types import Message
from sqlalchemy.orm import Session
from loader import bot
from sqlalchemy import select
from database.models import UserTelegram


@bot.message_handler(commands=["start"])
def bot_start(message: Message, data):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\n"
                          f"message_id -> {message.message_id}\n"
                          f"user_id -> {message.from_user.id}\n")
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
    # TODO создать слой отвечающий за эти запросы services или utils

    # TODO Передать на вход функции user_id для запроса авторизованного пользователя
    # TODO если текущий пользователь есть -> обновить токен
    # TODO записать токен в таблицу telegram_id token

    # TODO если текущего пользователя нет -> запросить пароль, создать пользователя
    # TODO обновить токен
    # TODO записать токен в таблицу telegram_id token

    # TODO удалить сообщение о вводе пароля
    # TODO написать сообщение что пользователь авторизован\аутентифицирован
