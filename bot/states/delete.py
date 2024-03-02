from telebot.handler_backends import State, StatesGroup


class DeletedHabit(StatesGroup):
    habit_id = State()
