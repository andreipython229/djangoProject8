import os
from django.test import TestCase
from mydogs.models import Mydogs, Category
from django.contrib.auth.models import User
from mydogs.models import Order

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject8.settings")
# Тест модели Mydogs
class MydogsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Friendly')

    def test_create_dog(self):
        """
        Проверяет, что объект собаки создаётся с нужными полями.
        """
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

# Тест модели Order
class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Friendly')
        self.dog = Mydogs.objects.create(
            name='Rex', breed='Labrador', age=3, price=5000, category=self.category
        )

    def test_create_order(self):
        """
        Проверяет, что можно создать заказ и добавить в него собаку.
        """
        order = Order.objects.create(user=self.user)
        order.dogs.add(self.dog)
        self.assertEqual(order.user.username, 'testuser')
        self.assertIn(self.dog, order.dogs.all())