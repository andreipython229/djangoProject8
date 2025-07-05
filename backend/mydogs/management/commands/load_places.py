from django.core.management.base import BaseCommand
from mydogs.models import Place
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Загружает тестовые места с картинками для пользователей andrei2 и Linas.'

    def handle(self, *args, **kwargs):
        # Пути к картинкам (относительно static/images/)
        image_paths = [
            'static/images/a629a148751349305bee9c1864120902_cropped_510x340.webp',
            'static/images/cbbe299229e7d5c49d378287632d4deb_cropped_666x444.webp',
            'static/images/d5a2bde913a14c179a94c172e5afbbb5.jpg',
            'static/images/istockphoto-1482199015-1024x1024.jpg',
            'static/images/pexels-charlesdeluvio-1851164.jpg',
            'static/images/photo_2024-10-28_23-03-43.jpg',
        ]
        names = [
            'Парк Дружбы',
            'Кафе "Лапка"',
            'Площадка для выгула',
            'Зоомагазин',
            'Ветклиника',
            'Озеро Счастья',
        ]
        addresses = [
            'ул. Парковая, 1',
            'ул. Кафейная, 5',
            'ул. Спортивная, 10',
            'ул. Зоологическая, 3',
            'ул. Ветеринарная, 7',
            'ул. Озёрная, 12',
        ]
        descriptions = [
            'Большой парк для прогулок с собаками.',
            'Дружелюбное кафе, куда можно с питомцем.',
            'Огороженная площадка для активных игр.',
            'Магазин товаров для животных.',
            'Современная ветеринарная клиника.',
            'Живописное озеро для прогулок.',
        ]
        # Получаем пользователей
        try:
            admin = User.objects.get(username='andrei2')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователь andrei2 не найден!'))
            return
        try:
            user = User.objects.get(username='Linas')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователь Linas не найден!'))
            return
        # Добавляем по 3 места для каждого
        for i in range(3):
            Place.objects.create(
                user=admin,
                name=names[i],
                address=addresses[i],
                description=descriptions[i],
                image=image_paths[i]
            )
        for i in range(3, 6):
            Place.objects.create(
                user=user,
                name=names[i],
                address=addresses[i],
                description=descriptions[i],
                image=image_paths[i]
            )
        self.stdout.write(self.style.SUCCESS('Места успешно добавлены для andrei2 и Linas!')) 