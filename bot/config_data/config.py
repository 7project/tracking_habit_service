import os
from dotenv import load_dotenv, find_dotenv
from envparse import Env

# TODO появился баг вылетает сообщение: Переменные окружения не загружены т.к отсутствует файл .env
# TODO в таком закомментированном виде работает
# if not find_dotenv():
#     exit("Переменные окружения не загружены т.к отсутствует файл .env")
# else:
#     load_dotenv()
#     BOT_TOKEN = os.getenv("BOT_TOKEN")

env = Env()
env.read_envfile()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if BOT_TOKEN is None:
    BOT_TOKEN = env("BOT_TOKEN")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота, аутентификация."),
    ("create", "Создание привычки"),
    ("delete", "Удаление привычки"),
    ("tracking", "Выполнить привычку"),
    ("habits", "Список всех отслеживаемых привычек"),
    ("update", "Обновить информацию привычки"),
    ("token", "Обновить токен доступа к API"),
    ("help", "Вывести справку"),
)
