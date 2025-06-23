import requests
from .models import Mydogs, Category
import time
import random
from decimal import Decimal
import logging
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

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
        self.DOG_API_URL = "https://dog.ceo/api/breeds/image/random"

    def _get_random_dog_image_url(self):
        try:
            response = requests.get(self.DOG_API_URL, timeout=5)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            return data.get('message')
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении изображения собаки: {e}")
            return None

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

                # Получаем URL изображения
                image_url = self._get_random_dog_image_url()
                image_file = None
                if image_url:
                    try:
                        response = requests.get(image_url, stream=True, timeout=10)
                        response.raise_for_status()
                        file_name = image_url.split('/')[-1]  # Get filename from URL
                        image_content = ContentFile(response.content)
                        # Save the file using Django's default storage
                        image_path = default_storage.save(f'dogs_images/{file_name}', image_content)
                        image_file = image_path
                        logger.info(f"Изображение {file_name} сохранено.")
                    except requests.exceptions.RequestException as e:
                        logger.error(f"Ошибка при скачивании изображения {image_url}: {e}")
                    except Exception as e:
                        logger.error(f"Ошибка при сохранении файла изображения: {e}")

                # Создаем запись о собаке
                Mydogs.objects.create(
                    name=dog_data['name'],
                    breed=dog_data['breed'],
                    age=dog_data['age'],
                    price=dog_data['price'],
                    category=category,
                    image=image_file  # Assign the saved image path
                )
                saved_count += 1
                logger.info(f"Сохранена собака: {dog_data['name']}")

            except Exception as e:
                logger.error(f"Ошибка при сохранении собаки: {str(e)}")
                continue

        logger.info(f"Всего сохранено собак: {saved_count}")

if __name__ == "__main__":
    import django
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.djangoProject8.settings")
    django.setup()

    parser = DogParser()
    dogs_data = parser.parse_dogs()
    parser.save_dogs(dogs_data)
    print("Парсинг завершён!")