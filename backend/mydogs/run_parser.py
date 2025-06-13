import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.djangoProject8.settings')
django.setup()

from mydogs.parsers import DogParser

def main():
    parser = DogParser()
    dogs_data = parser.parse_dogs()
    parser.save_dogs(dogs_data)

if __name__ == '__main__':
    main()