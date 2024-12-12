from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
    bot.send_message(message.chat.id, f"Сервис по трекингу\выполнения полезных привычек.\n"
                                      f"Время оповещения о ваших привычках /habits.\n"
                                      f"Фиксировано: 08:15 10:15 12:15 15:15 18:15 20:15 МСК.\n"
                                      f"Текущая версия: 1.0.0")
