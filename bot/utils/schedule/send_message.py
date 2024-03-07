import time
import pytz
import schedule
import telebot
from config_data.config import BLOCKED_ID_TELEGRAM_USER1, BLOCKED_ID_TELEGRAM_USER2, BLOCKED_ID_TELEGRAM_USER3
from database.schedule.get_data_schedule import get_all_number_chat_id_and_time_traking_habit
from loader import bot
from .create_message import get_message

BLOCKED_ID_TELEGRAM = [BLOCKED_ID_TELEGRAM_USER1,
                       BLOCKED_ID_TELEGRAM_USER2,
                       BLOCKED_ID_TELEGRAM_USER3]

BLOCKED_MIN_LEN_ID_TELEGRAM = 7


def morning_send_message():
    print('<<<<<< START morning_send_message >>>>')
    print(BLOCKED_ID_TELEGRAM)
    response = get_all_number_chat_id_and_time_traking_habit()
    if len(response) != 0:
        # TODO Получить сообщение из get_message и сформировать его
        message_text = (f'Время выполнить вашу привычку.\n'
                        f'Обновите свой токен /token\n'
                        f'Нажмите /habits для получения списка привычек,\n'
                        f'далее /tracking что бы ее выполнить, введите id привычки >>>')
        for telegram_id, data_time in response:

            if len(str(telegram_id)) < BLOCKED_MIN_LEN_ID_TELEGRAM:
                print(f'<<<<< SKIP #{telegram_id} schedule >>>>>')
                continue
            if str(telegram_id) in BLOCKED_ID_TELEGRAM:
                print(f'<<<<< SKIP #{telegram_id} schedule >>>>>')
                continue

            print(f'<<<<< START send_message #{telegram_id} schedule >>>>>')
            try:
                bot.send_message(telegram_id, message_text)
                time.sleep(3)
            except telebot.apihelper.ApiTelegramException as exp:
                print('morning_send_message >>>>> ', exp, exp.result, exp.result_json)


schedule.every().days.at("11:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().days.at("15:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().days.at("20:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
