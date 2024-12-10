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
    bot.reply_to(message, f"{message.from_user.full_name}!\n"
                          f"Сервис по трекингу полезных привычек приветствует тебя.\n"
                          f"Время оповещения в среднем три раза в день: 11:15 15:15 20:15 МСК\n"
                          f"В первый раз нужно авторизоваться, введи учетные данные ниже, придумай логин и пароль.\n"
                          f"Если аккаунт есть, нажми /cancel для выхода из состояния команды, и потом команду "
                          f"/token для обновления токена введя пароль от ранее созданного пользователя.")

    # bot.reply_to(message, f"{message.from_user.full_name}!\n"
    #                       f"Бот по трекингу полезных привычек приветствует.\n"
    #                       f"Для использования бота нужно авторизоваться, введи учетные данные.\n"
    #                       f"Придумать логин и пароль.\n"
    #                       f"Если есть ранее созданный аккаунт, нажми /cancel для выхода из состояния команды, "
    #                       f"и потом команду "
    #                       f"/token для обновления токена введя пароль от ранее созданного пользователя.\n"
    #                       f"Токен выдается на 15 минут.")


    bot.set_state(message.from_user.id, AuthUser.name, message.chat.id)
    bot.send_message(message.chat.id, 'Введите ваш логин(на Английском) >>>')


@bot.message_handler(state=AuthUser.name)
def name_get(message: Message):
    """
    State 1.
    """
    bot.send_message(message.chat.id, 'Введите ваш пароль >>>')
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
        bot.delete_state(message.from_user.id, message.chat.id)

    # TODO заменить 409 на статус кода из библиотеке status HTTP
    if response.status_code == 409:
        bot.send_message(message.chat.id, f"Invalid request get_user_to_telegram_id. "
                                          f"Нажмите /start для повторной авторизации.")
        bot.delete_state(message.from_user.id, message.chat.id)

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

        qwerty = (select(UserTelegram).where(UserTelegram.telegram_id == message.from_user.id)
                  .order_by(UserTelegram.id.desc()))
        result_sql = session.execute(qwerty)
        # TODO end
        # bot.send_message(message.chat.id, f"{result_sql.scalars().all()}")
        first_row = result_sql.first()
        if first_row:
            # bot.send_message(message.chat.id, f"{first_row}")
            print('>>>>>>', type(first_row))
            print('>>>>>>', dir(first_row))
        print('>>>>>>', first_row[0])
        telegram_token = first_row[0].token
        print('telegram_token >>>>>>', telegram_token)
        bot.send_message(message.chat.id, f"Ваш токен обновлен.\n"
                                          f"Создание привычки /create\n"
                                          f"Список привычек /habits\n"
                                          f"Список команд /help.")

    bot.delete_state(message.from_user.id, message.chat.id)


# TODO Написать логику на добавления пользователя, без дублирования
# TODO работает получение токена и запись в бд авторизованному и нового пользователя.
