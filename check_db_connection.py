import sys
import os

os.system("chcp 1251")
sys.stdout.reconfigure(encoding='UTF-8')

import django
import psycopg
from psycopg import OperationalError
from django.db import connections
from django.db.utils import OperationalError

# Установите переменную окружения для модуля настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject8.settings')

# Инициализируйте настройки Django
django.setup()

db_conn = connections['default']
try:
    c = db_conn.cursor()
    print("Connection successful!")
except OperationalError:
    print("Connection failed!")