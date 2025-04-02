# mydogs/management/commands/run_myscript.py
from django.core.management.base import BaseCommand
from mydogs.models import Mydogs

class Command(BaseCommand):
    help = 'Запуск скрипта, который выводит информацию о всех собаках из модели Mydogs'

    def handle(self, *args, **kwargs):
        self.stdout.write("Выполнение команды run_myscript")
        dogs = Mydogs.objects.all()
        for dog in dogs:
            self.stdout.write(f"{dog.name} - {dog.age}")