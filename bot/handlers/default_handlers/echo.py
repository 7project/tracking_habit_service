from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(
        message, "Это сообщение Эхо без состояния или фильтра. Нажмите /help\n" f"Дублирую ваше сообщение: {message.text}"
    )
