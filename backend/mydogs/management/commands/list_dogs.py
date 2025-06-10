from django.core.management.base import BaseCommand
from mydogs.models import Mydogs
from django.db.models import Count

class Command(BaseCommand):
    help = 'Показывает список созданных записей о собаках'

    def handle(self, *args, **options):
        try:
            # Получаем общее количество записей
            total_dogs = Mydogs.objects.count()
            self.stdout.write(f'Всего записей в базе: {total_dogs}\n')

            # Группируем по категориям
            categories = Mydogs.objects.values('category__name').annotate(count=Count('id'))
            self.stdout.write('Распределение по категориям:')
            for cat in categories:
                self.stdout.write(f"- {cat['category__name']}: {cat['count']} собак")

            # Группируем по породам
            breeds = Mydogs.objects.values('breed').annotate(count=Count('id'))
            self.stdout.write('\nРаспределение по породам:')
            for breed in breeds:
                self.stdout.write(f"- {breed['breed']}: {breed['count']} собак")

            # Показываем несколько примеров
            self.stdout.write('\nПримеры записей:')
            for dog in Mydogs.objects.all()[:5]:
                self.stdout.write(
                    f"- {dog.name} ({dog.breed}), {dog.age} лет, "
                    f"цена: {dog.price}, категория: {dog.category.name}"
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {str(e)}'))