from telebot.handler_backends import State, StatesGroup


class CreateHabit(StatesGroup):
    name_habit = State()
    description = State()
