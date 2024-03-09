from telebot.types import Message
from states.create import CreateHabit
from loader import bot
from utils.req.crud import create_habit, get_local_token_to_api
from sqlalchemy.orm import Session


@bot.message_handler(commands=["create"])
def bot_create(message: Message):
    bot.reply_to(message, f"Команда /create, {message.from_user.full_name}!")
    bot.set_state(message.from_user.id, CreateHabit.name_habit, message.chat.id)
    bot.send_message(message.chat.id, 'Введите имя вашей привычки, для выхода из команды нажмите /cancel >>>')


@bot.message_handler(state=CreateHabit.name_habit)
def name_habit_handler(message: Message):
    """
    State 1.
    """
    bot.send_message(message.chat.id, 'Введите описание вашей привычки >>>')
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

    token = get_local_token_to_api(session=data['session'], telegram_id=message.from_user.id)
    if token is None:
        bot.send_message(message.chat.id, f"Токен не получен")
    response = create_habit(name_habit=data_["name_habit"], description=data_["description"], token=token)
    print('response.json() >>> ', response.json())
    print('response.status_code >>> ', response.status_code)

    # TODO заменить 401 на статус кода из библиотеке status HTTP
    if response.status_code == 401:
        bot.send_message(message.chat.id, f"Ошибка авторизации на сервере. "
                                          f"Нажмите /token для повторной авторизации.")
    # TODO заменить 409 на статус кода из библиотеке status HTTP
    if response.status_code == 409:
        bot.send_message(message.chat.id, f"Invalid request get_user_to_telegram_id. "
                                          f"Нажмите /start для повторной авторизации.")

    if response.status_code == 200:
        bot.send_message(message.chat.id, f"Привычка #{response.json()['tracking']['habit_id']}: "
                                          f"{response.json()['name_habit']}. - Добавлена.")
        bot.send_message(message.chat.id, f"Выведите весь список ваших привычек /habits.")
    else:
        bot.send_message(message.chat.id, f"Привычка не добавлена! Ответ сервера: {response.json()}")

    bot.delete_state(message.from_user.id, message.chat.id)
