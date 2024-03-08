import time
import pytz
import schedule
import telebot
from config_data.config import BLOCKED_ID_TELEGRAM_USER1, BLOCKED_ID_TELEGRAM_USER2, BLOCKED_ID_TELEGRAM_USER3
from database.schedule.get_data_schedule import get_all_number_chat_id_and_time_traking_habit
from loader import bot
from .create_message import get_message

BLOCKED_ID_TELEGRAM = [
                       # BLOCKED_ID_TELEGRAM_USER1,
                       # BLOCKED_ID_TELEGRAM_USER2,
                       # BLOCKED_ID_TELEGRAM_USER3
                       ]

BLOCKED_MIN_LEN_ID_TELEGRAM = 7


def morning_send_message():
    print('<<<<<< START morning_send_message >>>>')
    print(BLOCKED_ID_TELEGRAM)
    response = get_all_number_chat_id_and_time_traking_habit()
    print('<<<<<< LEN  response get_all_number_chat_id_and_time_traking_habit>>>>', len(response))
    if len(response) != 0:
        # TODO Получить сообщение из get_message и сформировать его

        for habit_id, telegram_id, name_habits, count_tracking, data_time in response:

            if len(str(telegram_id)) < BLOCKED_MIN_LEN_ID_TELEGRAM:
                print(f'<<<<< SKIP #{telegram_id} {name_habits} {count_tracking} {data_time} schedule >>>>>')
                continue
            if str(telegram_id) in BLOCKED_ID_TELEGRAM:
                print(f'<<<<< SKIP #{telegram_id} {name_habits} {count_tracking} {data_time} schedule >>>>>')
                continue

            print(f'<<<<< START send_message #{telegram_id} schedule >>>>>')
            try:
                # if len(str(data_time.minute)) == 1:
                #     data_time.minute = f'0{data_time.minute}'
                message_text = (f'Время выполнить вашу привычку:\n'
                                f'#{habit_id} - {name_habits}.\n'
                                f'Текущий счетчик выполнений равен = {count_tracking}\n'
                                f'Время создания {data_time.hour}:{data_time.minute}\n'
                                f'Нажмите /tracking для фиксации выполнения. Указав id - {habit_id}\n'
                                f'Нажмите /habits для получения списка привычек,\n'
                                f'далее /tracking что бы ее выполнить, введите id - {habit_id} привычки.')
                bot.send_message(telegram_id, message_text)
                time.sleep(3)
            except telebot.apihelper.ApiTelegramException as exp:
                print('morning_send_message >>>>> ', exp, exp.result, exp.result_json)


# TODO Исправлено - уходит в бесконечный цикл
# TODO правки:
# TODO поменял days() -> day() как в documentation
schedule.every().day.at("09:55", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().day.at("11:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().day.at("15:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().day.at("20:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
