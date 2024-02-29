import requests

HEADERS_TOKEN = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

HEADERS_JSON = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    }


def backend_authentication_to_service(user_id: int, name: str, password: str):
    response = get_token(user_id, password)
    if response is None or response.status_code == 409:
        print('Ошибка получения токена')
        create_user_response = create_user(telegram_id=user_id, name=name, password=password)
        print('create_user_response status_code >>>>', create_user_response.status_code)
        if create_user_response is None:
            return None
        response = get_token(user_id, password)
        return response
    else:
        print('backend_authentication_to_service status_code >>>>>', response.status_code)
        return response


def get_token(telegram_id, password):

    data = {
        'telegram_id': telegram_id,
        'password': password,
    }

    response = requests.post('http://fastapi:8000/api/v1/jwt/token', headers=HEADERS_TOKEN, data=data)
    print('get_token status code >>>> ', response.status_code)
    return response


def create_user(telegram_id: int, name: str, password: str):
    data = {
        'telegram_id': telegram_id,
        'name': name,
        'password': password,
    }
    response = requests.post('http://fastapi:8000/api/v1/user/create', headers=HEADERS_JSON, json=data)
    print('create_user status code >>>> ', response.status_code)
    return response
