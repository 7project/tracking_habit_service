import os
from dotenv import load_dotenv, find_dotenv
from envparse import Env

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

env = Env()
env.read_envfile()

if BOT_TOKEN is None:
    BOT_TOKEN = env("BOT_TOKEN")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("create", "Создание привычки"),
    ("delete", "Удаление привычки"),
    ("tracking", "Выполнить привычку"),
    ("habits", "Список всех отслеживаемых привычек"),
    ("update", "Обновить информацию привычки"),
    ("help", "Вывести справку")
)
