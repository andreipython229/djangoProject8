from django.test import TestCase
from mydogs.models import Mydogs, Category
from mydogs.serializers import MydogsSerializer

class MydogsSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='TestCategory')

    def test_dog_serialization(self):
        dog = Mydogs.objects.create(name='Doggy', breed='Beagle', age=3, price=500, gender='male', category=self.category)
        serializer = MydogsSerializer(dog)
        data = serializer.data
        self.assertEqual(data['name'], 'Doggy')
        self.assertEqual(data['breed'], 'Beagle')
        self.assertEqual(data['age'], 3)
        self.assertTrue(data['price'] == '500.00 ₽' or data['price'].startswith('500'))

    def test_negative_age(self):
        data = {'name': 'Doggy', 'breed': 'Beagle', 'age': -1, 'price': 500, 'gender': 'male', 'category': self.category.id}
        serializer = MydogsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('age', serializer.errors)

    def test_negative_price(self):
        data = {'name': 'Doggy', 'breed': 'Beagle', 'age': 3, 'price': -100, 'gender': 'male', 'category': self.category.id}
        serializer = MydogsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors) 