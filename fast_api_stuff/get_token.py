import requests
from dotenv import load_dotenv
from os import getenv
from json import dumps

load_dotenv()

# Регистрация демо-пользователя
def register():
    site = getenv('FACE_CLOUD_SITE')
    login = getenv('FACE_CLOUD_LOGIN')
    password = getenv('FACE_CLOUD_PASSWORD')

    data = {
        "billing_type": "demo",
        "email": login,
        "password": password
    }

    try:
        response = requests.post(
            f'{site}api/v1/users',
            headers={'Content-Type': 'application/json'},
            data=dumps(data)
        )

        response.raise_for_status()

        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
       
# Получение токена
def get_new_token():
    site = getenv('FACE_CLOUD_SITE')
    login = getenv('FACE_CLOUD_LOGIN')
    password = getenv('FACE_CLOUD_PASSWORD')

    data = {
        "email": login,
        "password": password
    }

    try:
        response = requests.post(
            f'{site}api/v1/login',
            headers={'Content-Type': 'application/json'},
            data=dumps(data)
        )

        response.raise_for_status()

        return response.json().get('data', {}).get('access_token')
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
