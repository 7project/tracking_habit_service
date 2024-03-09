from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
    bot.send_message(message.chat.id, f"Сервис по треку полезных привычек находится в стадии разработки.\n"
                                      f"Функционал и логика на текущий момент дорабатывается.\n"
                                      f"Время оповещения о ваших привычках /habits.\n"
                                      f"В среднем три раза в день: 11:15 15:15 20:15 МСК.\n"
                                      f"Примерное время запуска бота ~11:00-21:00. МСК.\n"
                                      f"На текущий момент запускается в ручную для теста.")

