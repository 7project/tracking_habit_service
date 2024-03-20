from telebot.types import Message
import re

from database.schedule.get_data_schedule import update_tracking_habit_count_add_one, update_tracking_habit_skip_add_one, \
    update_tracking_habit_view_add_one
from loader import bot
# from handlers.custom_callback_query.callback_handlers import tracking_habit_now_skip  # noqa


# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message: Message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, f"Текущее состояние {bot.get_state(message.from_user.id, message.chat.id)} "
                                      f"было завершено.")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: str(call.data).startswith("schedule_"))
def schedule_tracking_habit_now_skip(call):
    if str(call.data).startswith("schedule_tracking_habit_now_id"):
        habit_id = re.search("schedule_tracking_habit_now_id*?(\d+)", call.data).group(1)
        print("re.search  schedule_tracking_habit >>>>", habit_id)
        print("tracking_habit_now_id  call.data >>>>", call.data)
        # TODO Написать логику выполнения привычки запрос к базе на +1
        update_tracking_habit_count_add_one(habit_id)
        update_tracking_habit_view_add_one(habit_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif str(call.data).startswith("schedule_tracking_habit_skip_id"):
        habit_id = re.search("schedule_tracking_habit_skip_id*?(\d+)", call.data).group(1)
        update_tracking_habit_skip_add_one(habit_id)
        update_tracking_habit_view_add_one(habit_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
