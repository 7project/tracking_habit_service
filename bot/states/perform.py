from telebot.handler_backends import State, StatesGroup


class PerformHabit(StatesGroup):
    habit_id = State()
