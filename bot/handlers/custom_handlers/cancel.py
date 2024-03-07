from telebot.types import Message

from loader import bot


# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message: Message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, f"Текущее состояние {bot.get_state(message.from_user.id, message.chat.id)} "
                                      f"было завершено.")
    bot.delete_state(message.from_user.id, message.chat.id)
