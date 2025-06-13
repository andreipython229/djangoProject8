import os
import django
from django.core.management import call_command

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.djangoProject8.settings')
django.setup()

if __name__ == '__main__':
    call_command('parse_dogs') 