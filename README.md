*Добро пожаловать!*
*Это демонстрационный проект сервиса с REST API на основе HTTP с передачей данных в форматеJSON. Он позволяет вести каталог bounding-box'ов лиц.*

## Получение токена ##
Убедитесь, что у вас есть рабочий токен для работы с API Facecloud (если он есть, переходите к следующему шагу).
1. В файле .env настройте переменные в строках 13-15. Это актуальный сервер API Facecloud, а также логин и пароль для аккаунта. Если у вас нет аккаунта, то для создания демо-аккаунта укажите любую пару email-пароль.
2. Откройте файл gen_token.py. Если у вас уже есть аккаунт, закомментируйте функцию для регистрации.
3. Запустите файл. В консоли должен появиться токен.
4. Если возникли какие-то проблемы с предудущим шагом, возможно вы пытаетесь войти в существующий аккаунт или несуществующий сайт. Внесите необходимые изменения или же добудьте токен другим путем.
5. Обновите полученным токеном переменную TOKEN в файле .env в строке 20.

## Локальный первый запуск ##
Выполните следующие действия, если вы собираетесь запускать проект локально.
1. Убедитесь, что у вас установлена версия Python 3.10.
2. Перейдите в консоли в нужную директорию и установите требуемые библиотеки командой: ```pip install -r requirements.txt```
3. Перейдите в файл .env и сконфигурируйте Postgres в строчках 3-6.
4. Для надлежащей защиты поменяйте переменные в строках 23-24 .env.
5. При необходимости выпустите сертификат ssl. Положите файлы cert.pem и key.pem в папку sertificates.
6. Запустить проект можно с помощью следующей команды в консоли:
```uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile=sertificates/key.pem --ssl-certfile=sertificates/cert.pem```

## Первый запуск с помощью Docker ##
1. При необходимости сконфигурируйте Postgres, изменяя строки с 3 по 9 файла .env. Обратите внимание, строку 10 трогать не нужно, она влияет только на локальный запуск.
2. При необходимости выпустите сертификат ssl. Положите файлы cert.pem и key.pem в папку sertificates.
3. При необходимости поменяйте переменные в строках 23-24 .env.
4. Если вы хотите протестировать сервис на своих фотографиях, положите их в папку pics или в любое другое место в корневой папке.
5. Смонтируйте и запустите образ: `docker-compose up --build`.

При повторном запуске можно не менять никакие переменные или файлы, только выполнять нужную консольную команду.  
Если все сделано правильно, то вы имеете возможность выполнять четыре требуемых команды:

## API Команды ##

### PUT /task/{task_id}/add_task
*Добавляет в базу данных новое задание и возвращает его статистику*  
Запрос:  
- *Нет тела запроса*  
Авторизация:  
- *Basic*  
Ответ:  
- *Json соответствующей схемы*
```
{
    "id": 7,
    "faces_count": 0,
    "male_count": 0,
    "female_count": 0,
    "male_ages": 0.0,
    "female_ages": 0.0
}
```

### PUT /task/{task_id}/add_image
*Добавляет изображение в задание с указанным task_id и обновляет статистику.*  
Параметры запроса:  
- *file_location: Путь к изображению относительно папки faces.*  
- *name: Название нового изображения в каталоге*  
Авторизация:  
*Basic*  
Ответ:  
*Json соответствующей схемы*
```
{
    "message": "Image and faces added successfully"
}
```

### GET /task/{task_id2}/get
*Получает информацию о задании, включая названия, рамки лиц и статистику.*  
Запрос:  
- *Нет тела запроса*  
Авторизация:  
- *Basic*  
Ответ:  
- *Json соответствующей схемы*  
```
{
    "task_id": 8,
    "images": [
        {
            "image_id": 10,
            "name": "me",
            "faces": [
                {
                    "face_id": 14,
                    "bounding_box": {
                        "x": 303,
                        "y": 456,
                        "w": 264,
                        "h": 357
                    },
                    "gender": "male",
                    "age": 24
                }
            ]
        },
        {
            "image_id": 11,
            "name": "y",
            "faces": [
                {
                    "face_id": 15,
                    "bounding_box": {
                        "x": 106,
                        "y": 20,
                        "w": 125,
                        "h": 177
                    },
                    "gender": "female",
                    "age": 42
                }
            ]
        },
        {
            "image_id": 12,
            "name": "y",
            "faces": [
                {
                    "face_id": 16,
                    "bounding_box": {
                        "x": 1229,
                        "y": 158,
                        "w": 235,
                        "h": 291
                    },
                    "gender": "male",
                    "age": 23
                },
                {
                    "face_id": 17,
                    "bounding_box": {
                        "x": 437,
                        "y": 149,
                        "w": 217,
                        "h": 280
                    },
                    "gender": "female",
                    "age": 17
                },
                {
                    "face_id": 18,
                    "bounding_box": {
                        "x": 1611,
                        "y": 253,
                        "w": 184,
                        "h": 250
                    },
                    "gender": "male",
                    "age": 17
                },
                {
                    "face_id": 19,
                    "bounding_box": {
                        "x": 963,
                        "y": 237,
                        "w": 183,
                        "h": 241
                    },
                    "gender": "male",
                    "age": 21
                },
                {
                    "face_id": 20,
                    "bounding_box": {
                        "x": 217,
                        "y": 335,
                        "w": 115,
                        "h": 167
                    },
                    "gender": "female",
                    "age": 11
                },
                {
                    "face_id": 21,
                    "bounding_box": {
                        "x": 1455,
                        "y": 341,
                        "w": 121,
                        "h": 145
                    },
                    "gender": "male",
                    "age": 44
                },
                {
                    "face_id": 22,
                    "bounding_box": {
                        "x": 0,
                        "y": 320,
                        "w": 65,
                        "h": 146
                    },
                    "gender": "female",
                    "age": 12
                }
            ]
        }
    ],
    "stat": {
        "faces_count": 9,
        "male_count": 5,
        "female_count": 4,
        "male_ages": 25.8,
        "female_ages": 20.5
    }
}
```


### DELETE /tasks/{task_id}/delete_task
*Удаляет задание с указанным task_id. Все связанные данные также удаляются.*  
Авторизация:  
- *Basic*  
Ответ:  
- *Json соответствующей схемы*
```
{
"message": "Task 7 deleted successfully"
}
```

## Настройки ##
Все настройки расположены в файле .env и откомментированны дополнительно.

#### Данные для подключения к Postgres
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
POSTGRES_DB=postgres
POSTGRES_HOST=localhost
DATABASE_URL_DOCKER=postgresql://${POSTGRES_DB}:${POSTGRES_PASSWORD}@db/${POSTGRES_DB}
DATABASE_URL_LOCAL=postgresql://${POSTGRES_DB}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}/${POSTGRES_DB}
```
#### Логин-пароль для API Facecloud (тестовые)
```
# Нужна для обозначения API-сервера
FACE_CLOUD_SITE=https://backend.facecloud.tevian.ru/  

# Нужны только для выпуска нового токена (через файл gen_token.py)  
FACE_CLOUD_LOGIN=ma@grate.ru  
FACE_CLOUD_PASSWORD=password  
```

### Токен для Facecloud. 
```
# Перед началом работы выпустите свежий токен замените им старый в настройках
TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzA1Njk3MzYsIm5iZiI6MTczMDU2OTczNiwianRpIjoiYzUzZjlmOTgtYTI5Yy00ZmExLTliODgtMGQzYWY1ZDJkMzBjIiwic3ViIjo0OTQsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.U-W_Qr7FkTAWvUhdorFTb-xwF1Wl7GhXiV7YpHzKDh8
```

### HTTP Basic Auth. Используется для авторизации в нашем апи.
```
# Используется внутри этого проекта для basic аутентификации, может быть легко заменен.
BASIC_AUTH_USERNAME=faces
BASIC_AUTH_PASSWORD=faces_password
```
### Переменная, которую не нужно менять
Последняя строка `ENVIRONMENT=local` не должна быть изменена, чтобы программа смогла определить, запускают ее через докер или нет.

## В заключение ##
В проекте отражены все требования из ТЗ, включая:
*Использование всех необходимых технологий, в том числе FastApi, Facecloud, Postgresql и SqlAlchemy*
*Предоставлен Dockerfile, позволяющий собрать контейнер с сервисом.*
*Предоставлен docker-compose.yml, позволяющий запустить сервис и PostgreSQL.*
*Доступ к API защищен с помощью HTTP Basic Auth*