import json

from telebot.types import Message
from sqlalchemy.orm import Session
from loader import bot
from sqlalchemy import select
from database.models import UserTelegram
from states.auth import AuthUser
from utils.auth.authentication import backend_authentication_to_service


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\n"
                          f"message_id -> {message.message_id}\n"
                          f"user_id -> {message.from_user.id}\n")
    # TODO переписать логику аутентификации\авторизации ниже по другому

    # TODO Передать на вход функции user_id для запроса авторизованного пользователя
    # TODO если текущий пользователь есть -> обновить токен
    # TODO записать токен в таблицу telegram_id token

    # TODO если текущего пользователя нет -> запросить пароль, создать пользователя
    # TODO обновить токен
    # TODO записать токен в таблицу telegram_id token

    # TODO написать сообщение что пользователь авторизован\аутентифицирован

    bot.set_state(message.from_user.id, AuthUser.name, message.chat.id)
    bot.send_message(message.chat.id, 'Enter your name >>>')


@bot.message_handler(state=AuthUser.name)
def name_get(message: Message):
    """
    State 1.
    """
    bot.send_message(message.chat.id, 'Enter your password >>>')
    bot.set_state(message.from_user.id, AuthUser.password, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    # TODO удаляем сообщение с введенным именем пользователя
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(state=AuthUser.password)
def password_get(message: Message, data: dict[str, Session]):
    """
    State 2.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_:
        data_['password'] = message.text
    # TODO удаляем сообщение с введенным паролем
    bot.delete_message(message.chat.id, message.message_id)
    # TODO удалить после дебага
    # bot.send_message(message.chat.id, f'Имя {data_["name"]} пароль {data_["password"]}')

    response = backend_authentication_to_service(user_id=message.from_user.id, name=data_["name"],
                                                 password=data_["password"])
    # TODO заменить 401 на статус кода из библиотеке status HTTP
    if response.status_code == 401:
        bot.send_message(message.chat.id, f"Ошибка авторизации на сервере. "
                                          f"Нажмите /start для повторной авторизации.")
    # TODO заменить 409 на статус кода из библиотеке status HTTP
    if response.status_code == 409:
        bot.send_message(message.chat.id, f"Invalid request get_user_to_telegram_id. "
                                          f"Нажмите /start для повторной авторизации.")

    # TODO проработать этот блок
    print('response', response.json())
    if response is not None and response.status_code != 409:
        print('response true>>>>>', type(response))
        result = response.json()
        print('result json >>>>>', result)
        # TODO вынести этот блок в отдельный слой логики
        # TODO Написать логику проверки что пользователь уже есть в базе
        # TODO start
        session: Session = data['session']
        first_user = UserTelegram(telegram_id=message.from_user.id,
                                  token=result['access_token'], )
        session.add(first_user)
        session.commit()

        qwerty = select(UserTelegram).order_by(UserTelegram.id.desc())
        result_sql = session.execute(qwerty)
        # TODO end
        # bot.send_message(message.chat.id, f"{result_sql.scalars().all()}")
        bot.send_message(message.chat.id, f"{result_sql.first()}")

    bot.delete_state(message.from_user.id, message.chat.id)


# TODO Написать логику на добавления пользователя, без дублирования
# TODO работает получение токена и запись в бд авторизованному и нового пользователя.
