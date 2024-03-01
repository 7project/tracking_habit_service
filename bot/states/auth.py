from telebot.handler_backends import State, StatesGroup


class AuthUser(StatesGroup):
    name = State()
    password = State()


class UpdateToken(StatesGroup):
    password = State()
