import requests
from dotenv import load_dotenv
from os import getenv
from json import dumps

load_dotenv()

def register():
    site = getenv('FACE_CLOUD_SITE')
    login = getenv('FACE_CLOUD_LOGIN')
    password = getenv('FACE_CLOUD_PASSWORD')

    # Формируем данные в формате JSON
    data = {
        "billing_type": "demo",
        "email": login,
        "password": password
    }

    try:
        # Отправляем POST-запрос с заголовком, указывающим, что данные в формате JSON
        response = requests.post(
            f'{site}api/v1/users',
            headers={'Content-Type': 'application/json'},
            data=dumps(data)  # Преобразуем словарь в строку JSON
        )

        response.raise_for_status()  # Проверка на наличие ошибок HTTP

        # Парсим JSON-ответ
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
       
def get_new_token():
    site = getenv('FACE_CLOUD_SITE')
    login = getenv('FACE_CLOUD_LOGIN')
    password = getenv('FACE_CLOUD_PASSWORD')

    # Формируем данные в формате JSON
    data = {
        "email": login,
        "password": password
    }

    try:
        # Отправляем POST-запрос с заголовком, указывающим, что данные в формате JSON
        response = requests.post(
            f'{site}api/v1/login',
            headers={'Content-Type': 'application/json'},
            data=dumps(data)  # Преобразуем словарь в строку JSON
        )

        response.raise_for_status()  # Проверка на наличие ошибок HTTP

        # Парсим JSON-ответ
        return response.json().get('data', {}).get('access_token')
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

