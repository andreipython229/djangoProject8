import requests
from .models import Mydogs, Category
import time
import random
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class DogParser:
    def __init__(self):
        # Список пород собак
        self.breeds = [
            "немецкая овчарка",
            "лабрадор",
            "хаски",
            "йоркширский терьер",
            "чихуахуа",
            "шпиц",
            "такса",
            "мопс",
            "бигль",
            "доберман",
            "ротвейлер",
            "боксер"
        ]

    def parse_dogs(self):
        try:
            logger.info("Начинаем генерацию данных о собаках")

            dogs_data = []

            # Генерируем тестовые данные
            for breed in self.breeds:
                # Создаем несколько собак каждой породы
                for i in range(3):
                    dog_data = {
                        'name': f"{breed.capitalize()} {i + 1}",
                        'breed': breed,
                        'age': random.randint(1, 10),
                        'price': Decimal(str(random.randint(10000, 100000))),
                        'category': 'Щенки' if random.random() > 0.5 else 'Взрослые'
                    }
                    dogs_data.append(dog_data)
                    logger.info(f"Создана карточка: {dog_data['name']}")

            logger.info(f"Всего создано карточек: {len(dogs_data)}")
            return dogs_data

        except Exception as e:
            logger.error(f"Ошибка при генерации данных: {str(e)}")
            return []

    def save_dogs(self, dogs_data):
        saved_count = 0
        for dog_data in dogs_data:
            try:
                # Создаем или получаем категорию
                category, _ = Category.objects.get_or_create(
                    name=dog_data['category']
                )

                # Создаем запись о собаке
                Mydogs.objects.create(
                    name=dog_data['name'],
                    breed=dog_data['breed'],
                    age=dog_data['age'],
                    price=dog_data['price'],
                    category=category
                )
                saved_count += 1
                logger.info(f"Сохранена собака: {dog_data['name']}")

            except Exception as e:
                logger.error(f"Ошибка при сохранении собаки: {str(e)}")
                continue

        logger.info(f"Всего сохранено собак: {saved_count}")