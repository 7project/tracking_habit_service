from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
    bot.send_message(message.chat.id, f"Бот находится на стадии разработки\доработки.\n"
                                      f"Функционал и логика на текущий момент дорабатывается.\n"
                                      f"Время оповещения о /tracking три раза в день: 11:15 15:15 20:15 МСК\n")

