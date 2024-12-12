import time
import pytz
import schedule
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config_data.config import BLOCKED_ID_TELEGRAM_USER1, BLOCKED_ID_TELEGRAM_USER2, BLOCKED_ID_TELEGRAM_USER3
from database.schedule.get_data_schedule import get_all_number_chat_id_and_time_tracking_habit
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
    response = get_all_number_chat_id_and_time_tracking_habit()
    print('<<<<<< LEN  response get_all_number_chat_id_and_time_traking_habit>>>>', len(response))
    if len(response) != 0:
        # TODO Получить сообщение из get_message и сформировать его

        for (habit_id, telegram_id, name_habits, count_tracking, total_count_view, total_count_skip,
             data_time, is_active) in response:
            if not is_active:
                print(f'<<<<< NOT ACTIVE SKIP #{telegram_id} {name_habits} {count_tracking} {data_time} schedule >>>>>')
                continue
            if len(str(telegram_id)) < BLOCKED_MIN_LEN_ID_TELEGRAM:
                print(f'<<<<< SKIP #{telegram_id} {name_habits} {count_tracking} {data_time} schedule >>>>>')
                continue
            if str(telegram_id) in BLOCKED_ID_TELEGRAM:
                print(f'<<<<< SKIP #{telegram_id} {name_habits} {count_tracking} {data_time} schedule >>>>>')
                continue

            print(f'<<<<< START send_message #{telegram_id} schedule >>>>>')
            try:
                markup_inline = InlineKeyboardMarkup()
                tracking = InlineKeyboardButton(text="Выполнить",
                                                callback_data=f"schedule_tracking_habit_now_id{habit_id}")
                # TODO отдавать schedule_tracking_habit_skip_id{habit_id}
                skip = InlineKeyboardButton(text="Пропустить", callback_data=f"schedule_tracking_habit_skip_id{habit_id}")
                markup_inline.add(tracking, skip)
                message_text = (f'#{habit_id} - {name_habits}.\n'
                                f'Время выполнить вашу привычку!\n'
                                f'Количество выполнения привычки: {count_tracking}\n'
                                f'Количество пропуска привычки: {total_count_view}\n'
                                f'Количество показов уведомления: {total_count_skip}\n'
                                # TODO Есть баг с отображением минут 11:5 -> 11:05
                                # f'Время создания {data_time.hour}:{data_time.minute}\n'
                                # f'Нажмите /tracking для фиксации выполнения. Указав id - {habit_id}\n'
                                # f'Нажмите /habits для получения списка привычек и их выполнения.\n'
                                # f'далее /tracking что бы ее выполнить, введите id - {habit_id} привычки.'
                                )
                bot.send_message(telegram_id, message_text, reply_markup=markup_inline)
                time.sleep(3)
            except telebot.apihelper.ApiTelegramException as exp:
                print('morning_send_message >>>>> ', exp, exp.result, exp.result_json)


schedule.every().day.at("08:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().day.at("10:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().day.at("12:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().day.at("15:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().day.at("18:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().day.at("20:15", pytz.timezone("Europe/Moscow")).do(morning_send_message)
schedule.every().day.at("21:45", pytz.timezone("Europe/Moscow")).do(morning_send_message)