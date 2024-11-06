Добро пожаловать!
Это демонстрационный проект сервиса с REST API на основе HTTP с передачей данных в формате
JSON. Он позволяет вести каталог bounding-box'ов лиц.

##Получение токена##
Убедитесь, что у вас есть рабочий токен для работы с API Facecloud (если он есть, переходите к следующему шагу).
1. В файле .env настройте переменные в строках 13-15. Это актуальный сервер API Facecloud, а также логин и пароль для аккаунта. Если у вас нет аккаунта, то для создания демо-аккаунта укажите любую пару email-пароль.
2. Откройте файл gen_token.py. Если у вас уже есть аккаунт, закомментируйте функцию для регистрации.
3. Запустите файл. В консоли должен появиться токен.
4. Если возникли какие-то проблемы с предудущим шагом, возможно вы пытаетесь войти в существующий аккаунт или несуществующий сайт. Внесите необходимые изменения или же добудьте токен другим путем.
5. Обновите полученным токеном переменную TOKEN в файле .env в строке 20.

##Локальный первый запуск##
Выполните следующие действия, если вы собираетесь запускать проект локально.
1. Убедитесь, что у вас установлена версия Python 3.10.
2. Перейдите в консоли в нужную директорию и установите требуемые библиотеки командой: ```pip install -r requirements.txt```
3. Перейдите в файл .env и сконфигурируйте Postgres в строчках 3-6.
4. Для надлежащей защиты поменяйте переменные в строках 23-24 .env.
5. При необходимости выпустите сертификат ssl. Положите файлы cert.pem и key.pem в папку sertificates.
6. Запустить проект можно с помощью следующей команды в консоли:
```uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile=sertificates/key.pem --ssl-certfile=sertificates/cert.pem```

##Первый запуск с помощью Docker##
1. При необходимости сконфигурируйте Postgres, изменяя строки с 3 по 9 файла .env. Обратите внимание, строку 10 трогать не нужно, она влияет только на локальный запуск.
2. При необходимости выпустите сертификат ssl. Положите файлы cert.pem и key.pem в папку sertificates.
3. При необходимости поменяйте переменные в строках 23-24 .env.
4. Если вы хотите протестировать сервис на своих фотографиях, положите их в папку pics или в любое другое место в корневой папке.
5. Смонтируйте и запустите образ: `docker-compose up --build`.

При повторном запуске можно не менять никакие переменные или файлы, только выполнять нужную консольную команду.  
Если все сделано правильно, то вы имеете возможность выполнять четыре требуемых команды:

##API Команды##

1. PUT /task/{{task_id}}/add_task/  
Добавляет в базу данных новое задание и возвращает его статистику  
Запрос:  
Нет тела запроса  
Авторизация:  
Basic  
Ответ:  
Json соответствующей схемы
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

2. GET /task/{{task_id2}}/get  
Получает информацию о задании, включая названия, рамки лиц и статистику.  
Запрос:  
Нет тела запроса  
Авторизация:  
Basic  
Ответ:  
Json соответствующей схемы  

```
{
    "task_id": 7,
    "images": [
        {
            "image_id": 8,
            "name": "me",
            "faces": [
                {
                    "face_id": 10,
                    "bounding_box": {
                        "x": 245,
                        "y": 107,
                        "w": 213,
                        "h": 301
                    },
                    "gender": "male",
                    "age": 30
                },
                {
                    "face_id": 11,
                    "bounding_box": {
                        "x": 418,
                        "y": 243,
                        "w": 188,
                        "h": 294
                    },
                    "gender": "female",
                    "age": 29
                }
            ]
        }
    ],
    "stat": {
        "faces_count": 2,
        "male_count": 1,
        "female_count": 1,
        "male_ages": 30.0,
        "female_ages": 29.0
    }
}
```


3. DELETE /tasks/{task_id}/delete_task  
Удаляет задание с указанным task_id. Все связанные данные также удаляются.  
Авторизация:  
Basic  
Ответ:  
Json соответствующей схемы
```
{
"message": "Task 7 deleted successfully"
}
```

4. PUT /task/{{task_id}}/add_image  
Добавляет изображение в задание с указанным task_id и обновляет статистику.  
Параметры запроса:  
file_location: Путь к изображению относительно папки faces.  
name: Название нового изображения в каталоге  
Авторизация:  
Basic  
Ответ:  
Json соответствующей схемы
```
{
    "message": "Image and faces added successfully"
}
```
