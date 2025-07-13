from django.test import TestCase
from django.contrib.auth import get_user_model
from mydogs.models import Mydogs, Category

class DogOwnerLogicTest(TestCase):
    def test_assign_owner(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpass')
        category = Category.objects.create(name='TestCategory')
        dog = Mydogs.objects.create(name='TestDog', breed='TestBreed', age=2, price=1000, gender='male', category=category)
        dog.owner = user
        dog.save()
        dog.refresh_from_db()
        self.assertEqual(dog.owner, user) 