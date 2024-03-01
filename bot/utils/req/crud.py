import requests
from sqlalchemy import select
from database.models import UserTelegram
from sqlalchemy.orm import Session


def get_local_token_to_api(session: Session):
    qwerty = select(UserTelegram).order_by(UserTelegram.id.desc())
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
        'Authorization': 'Bearer {token}'.format(token=token),  # TODO как динамически вставлять токен в словарь
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