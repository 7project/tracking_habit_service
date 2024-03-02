from telebot.handler_backends import State, StatesGroup


class UpdateHabit(StatesGroup):
    habit_id = State()
    name_habit = State()
    description = State()
    alert_time = State()
    count = State()
