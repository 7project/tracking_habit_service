from telebot.types import Message
from states.create import CreateHabit
from loader import bot
from utils.req.crud import create_habit, get_local_token_to_api
from sqlalchemy.orm import Session


@bot.message_handler(commands=["create"])
def bot_start(message: Message):
    bot.reply_to(message, f"Команда create, {message.from_user.full_name}!")
    bot.set_state(message.from_user.id, CreateHabit.name_habit, message.chat.id)
    bot.send_message(message.chat.id, 'Enter your name habit >>>')


@bot.message_handler(state=CreateHabit.name_habit)
def name_habit_handler(message: Message):
    """
    State 1.
    """
    bot.send_message(message.chat.id, 'Enter your description habit >>>')
    bot.set_state(message.from_user.id, CreateHabit.description, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_habit'] = message.text
    # TODO удаляем сообщение с введенным description habit
    # bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(state=CreateHabit.description)
def description_handler(message: Message, data: dict[str, Session]):
    """
    State 2.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_:
        data_['description'] = message.text
    # TODO удаляем сообщение с введенным description
    # bot.delete_message(message.chat.id, message.message_id)

    # TODO написать функцию вызова запроса к API
    # TODO на создание http://fastapi:8000/api/v1/jwt/habit/create
    # TODO name_habit=data_["name_habit"] description=data_["description"]
    token = get_local_token_to_api(session=data['session'])
    if token is None:
        bot.send_message(message.chat.id, f"Токен не получен")
    response = create_habit(name_habit=data_["name_habit"], description=data_["description"], token=token)
    print('response.json() >>> ', response.json())
    print('response.status_code >>> ', response.status_code)
    # TODO заменить 401 на статус кода из библиотеке status HTTP
    if response.status_code == 401:
        bot.send_message(message.chat.id, f"Ошибка авторизации на сервере. "
                                          f"Нажмите /start для повторной авторизации.")
    # TODO заменить 409 на статус кода из библиотеке status HTTP
    if response.status_code == 409:
        bot.send_message(message.chat.id, f"Invalid request get_user_to_telegram_id. "
                                          f"Нажмите /start для повторной авторизации.")

    # bot.send_message(message.chat.id, f"{response.json()}")
    if response.status_code == 200:
        bot.send_message(message.chat.id, f"Привычка #{response.json()['tracking']['habit_id']}: "
                                          f"{response.json()['name_habit']}. - Добавлена.")
    else:
        bot.send_message(message.chat.id, f"Привычка не добавлена! Ответ сервера: {response.json()}")