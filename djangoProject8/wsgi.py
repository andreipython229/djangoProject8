"""
WSGI config for djangoProject8 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Получение базового пути директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Загрузка переменных окружения из файла .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Установка переменной DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject8.settings')

try:
    import djangoProject8.settings
    print("Setting module imported successfully.")
except ImportError as e:
    print(f"Error: importing settings module: {e}")

# Получение WSGI-приложения
try:
    application = get_wsgi_application()
except Exception as e:
    sys.stderr.write(f"WSGI Error: {e}\n")
    raise
