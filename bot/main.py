from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from telebot.handler_backends import BaseMiddleware
from database.db_main import create_db, session
from sqlalchemy.orm import Session


class Middleware(BaseMiddleware):
    def __init__(self, session_pool):
        super().__init__()
        self.update_types = ['message']
        self.session_pool = session_pool

    def pre_process(self, message, data):
        with self.session_pool() as session_:
            data['session']: Session = session_

    def post_process(self, message, data, exception=None):
        print(data['session'])
        if exception:
            print(exception)


if __name__ == "__main__":
    set_default_commands(bot)
    create_db()
    bot.setup_middleware(Middleware(session))
    bot.infinity_polling(timeout=25, long_polling_timeout=10)
