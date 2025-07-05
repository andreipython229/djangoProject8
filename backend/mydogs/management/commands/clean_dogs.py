from django.core.management.base import BaseCommand
from mydogs.models import Mydogs

class Command(BaseCommand):
    help = 'Очищает базу данных от старых записей о собаках'

    def handle(self, *args, **options):
        try:
            # Удаляем записи с дефолтными значениями
            old_dogs = Mydogs.objects.filter(
                name='Unknown',
                breed='Unknown',
                age=0,
                price=0
            )
            count = old_dogs.count()
            old_dogs.delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Успешно удалено {count} старых записей')
            )
            
            # Показываем оставшиеся записи
            remaining = Mydogs.objects.count()
            self.stdout.write(
                self.style.SUCCESS(f'В базе осталось {remaining} записей')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Произошла ошибка: {str(e)}')
            ) 