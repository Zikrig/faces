from fast_api_stuff.get_token import *

# Перед запуском дайте нужные значения переменным в .env

# FACE_CLOUD_SITE=https://backend.facecloud.tevian.ru/s
# Должно содержать актуальный сервер API

# Для демо-аккаунта сгодятся любые значения для регистрации
# FACE_CLOUD_LOGIN=mamda@grate.ru
# FACE_CLOUD_PASSWORD=password

# Создание нового аккаунта
# Если у вас уже есть аккаунт - закомментировать
register()

# Получение токена
# Токен скопировать из командной строки и положить в .env в переменную TOKEN
get_new_token()