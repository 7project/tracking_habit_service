import requests


def backend_authentication_to_service(user_id: int, name: str, password: str):
    response = get_token(user_id, password)
    if response is None:
        print('Ошибка получения токена')
        return None
    else:
        print(response.status_code)
        return response
    # TODO дописать логику аутентификации нового пользователя
    # TODO дописать логику обновления токена


def get_token(telegram_id, password):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'telegram_id': telegram_id,
        'password': password,
    }
    try:
        response = requests.post('http://fastapi:8000/api/v1/jwt/token', headers=headers, data=data)
        return response
    except Exception as exp:
        print(f"get_token 401 Unauthorized >>> {exp}")
    return None


def update_local_token(token: str):
    ...
