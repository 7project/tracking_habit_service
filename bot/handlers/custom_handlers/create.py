from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["create"])
def bot_start(message: Message):
    bot.reply_to(message, f"Команда create, {message.from_user.full_name}!")
