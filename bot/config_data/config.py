import os
from dotenv import load_dotenv, find_dotenv
from envparse import Env


env = Env()
env.read_envfile()


BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    BOT_TOKEN = env("BOT_TOKEN")

DATABASE_URL_NOT_ASYNC = os.getenv("DATABASE_URL_NOT_ASYNC")
if DATABASE_URL_NOT_ASYNC is None:
    DATABASE_URL_NOT_ASYNC = env("DATABASE_URL_NOT_ASYNC")

BLOCKED_ID_TELEGRAM_USER1 = os.getenv("BLOCKED_ID_TELEGRAM_USER1")
if BLOCKED_ID_TELEGRAM_USER1 is None:
    BLOCKED_ID_TELEGRAM_USER1 = env("BLOCKED_ID_TELEGRAM_USER1")

BLOCKED_ID_TELEGRAM_USER2 = os.getenv("BLOCKED_ID_TELEGRAM_USER2")
if BLOCKED_ID_TELEGRAM_USER2 is None:
    BLOCKED_ID_TELEGRAM_USER2 = env("BLOCKED_ID_TELEGRAM_USER2")

BLOCKED_ID_TELEGRAM_USER3 = os.getenv("BLOCKED_ID_TELEGRAM_USER3")
if BLOCKED_ID_TELEGRAM_USER3 is None:
    BLOCKED_ID_TELEGRAM_USER3 = env("BLOCKED_ID_TELEGRAM_USER3")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота, аутентификация."),
    ("create", "Создание привычки"),
    ("delete", "Удаление привычки"),
    ("tracking", "Выполнить привычку"),
    ("habits", "Список всех отслеживаемых привычек"),
    ("update", "Обновить информацию привычки"),
    ("token", "Обновить токен доступа к API"),
    ("help", "Вывести справку"),
    ("cancel", "Выйти из состояния")
)
