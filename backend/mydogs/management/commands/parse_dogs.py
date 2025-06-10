from django.core.management.base import BaseCommand
from mydogs.parsers import DogParser
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Генерирует тестовые данные о собаках'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Начинаем генерацию тестовых данных...')

            parser = DogParser()
            dogs_data = parser.parse_dogs()

            if dogs_data:
                parser.save_dogs(dogs_data)
                self.stdout.write(self.style.SUCCESS('Данные успешно сгенерированы и сохранены'))
            else:
                self.stdout.write(self.style.ERROR('Не удалось сгенерировать данные'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {str(e)}'))

