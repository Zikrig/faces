# Укажите базовый образ с Python 3.10
FROM python:3.10

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы проекта в контейнер
COPY . /app

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запустите приложение с использованием SSL
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "sertificates/key.pem", "--ssl-certfile", "sertificates/cert.pem"]
