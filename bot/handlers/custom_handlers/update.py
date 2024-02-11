from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["update"])
def bot_start(message: Message):
    bot.reply_to(message, f"Команда update, {message.from_user.full_name}!")
