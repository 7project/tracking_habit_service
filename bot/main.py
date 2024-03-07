import handlers  # noqa

from database.db_main import create_db, session
from telebot import custom_filters
from telebot.handler_backends import BaseMiddleware
from loader import bot
from sqlalchemy.orm import Session

from utils.schedule.background import run_continuously
from utils.set_bot_commands import set_default_commands


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
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    # start schedule
    run_continuously()
    bot.infinity_polling(timeout=25, long_polling_timeout=10)
