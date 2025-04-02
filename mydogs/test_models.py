import os
from django.test import TestCase
from mydogs.models import Mydogs, Category

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject8.settings")


class MydogsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Friendly')

    def test_create_dog(self):
        dog = Mydogs.objects.create(
            name='Motlik',
            breed='Korgi',
            age=2,
            price=3000,
            category=self.category
        )
        self.assertEqual(dog.name, 'Motlik')
        self.assertEqual(dog.breed, 'Korgi')
        self.assertEqual(dog.age, 2)
        self.assertEqual(dog.price, 3000)
        self.assertEqual(dog.category.name, 'Friendly')