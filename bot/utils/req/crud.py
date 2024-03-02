import requests
from sqlalchemy import select
from database.models import UserTelegram
from sqlalchemy.orm import Session


def get_local_token_to_api(session: Session, telegram_id: int):
    qwerty = select(UserTelegram).where(UserTelegram.telegram_id == telegram_id).order_by(UserTelegram.id.desc())
    result_sql = session.execute(qwerty)
    first_row = result_sql.first()

    if first_row:
        telegram_token = first_row[0].token
        return telegram_token
    else:
        print("Создайте токен. Нажмите /start для повторной авторизации.")
        return None


def create_habit(name_habit: str, description: str, token: str):

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer {token}'.format(token=token),
        'Content-Type': 'application/json',
        }

    json_data = {
        # TODO user_id подумать как убрать не нужна
        'user_id': 0,
        'name_habit': name_habit,
        'description': description,
    }

    response = requests.post('http://fastapi:8000/api/v1/jwt/habit/create', headers=headers, json=json_data)
    print('create_habit status code >>>> ', response.status_code)
    return response


def deleted_habit(habit_id: int, token: str):

    headers_deleted = {
        'accept': '*/*',
        'Authorization': 'Bearer {token}'.format(token=token),
        'Content-Type': 'application/json',
        }

    json_data = {
        'habit_id': habit_id,
    }

    response = requests.delete('http://fastapi:8000/api/v1/jwt/habit/delete', headers=headers_deleted, json=json_data)
    print('deleted_habit status code >>>> ', response.status_code)
    return response


def get_habits(token: str):

    headers_habits = {
        'accept': 'application/json',
        'Authorization': 'Bearer {token}'.format(token=token),
        }

    response = requests.get('http://fastapi:8000/api/v1/jwt/user/me/habits', headers=headers_habits)
    print('get_habits status code >>>> ', response.status_code)
    return response
