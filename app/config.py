# /app/config.py
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'DEBUG'