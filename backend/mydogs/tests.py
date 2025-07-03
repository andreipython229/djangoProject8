from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from mydogs.models import Mydogs, Category, Order

# Create your tests here.

class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apitest', password='testpass')
        self.category = Category.objects.create(name='TestCat')
        self.dog = Mydogs.objects.create(
            name='API Dog', breed='TestBreed', age=1, price=100, category=self.category
        )
        self.client.login(username='apitest', password='testpass')

    def test_create_order_api(self):
        """
        Проверяет, что можно создать заказ через API и возвращается корректный ответ.
        """
        url = reverse('order-list')  # Использует basename='order' из urls.py
        data = {
            "dogs_ids": [self.dog.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(len(response.data['dogs']), 1)
        self.assertEqual(response.data['dogs'][0]['name'], 'API Dog')

class MydogsAPICRUDTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apitest3', password='testpass')
        self.category = Category.objects.create(name='CatCRUD')
        self.dog = Mydogs.objects.create(
            name='DogCRUD', breed='BreedCRUD', age=3, price=300, category=self.category
        )
        self.client.login(username='apitest3', password='testpass')

    def test_get_dogs(self):
        """
        Проверяет, что можно получить список собак через API.
        """
        response = self.client.get('/api/v1/mydogslist/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_dog(self):
        """
        Проверяет, что можно создать собаку через API.
        """
        data = {
            'name': 'DogNew',
            'breed': 'BreedNew',
            'age': 2,
            'price': 200,
            'category': self.category.id,
            'gender': 'male'
        }
        response = self.client.post('/api/v1/mydogslist/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'DogNew')

    def test_update_dog(self):
        """
        Проверяет, что можно обновить собаку через API (PUT).
        """
        data = {
            'name': 'DogUpdated',
            'breed': 'BreedCRUD',
            'age': 4,
            'price': 350,
            'category': self.category.id,
            'gender': 'male'
        }
        url = f'/api/v1/mydogs/{self.dog.id}/'
        response = self.client.put(url, data, format='json')
        print('Status code:', response.status_code)
        print('Content-Type:', response.get('Content-Type'))
        print('Content:', response.content)
        self.assertEqual(response.status_code, 200)
        if response.get('Content-Type') == 'application/json':
            data = response.json()
            self.assertEqual(data['name'], 'DogUpdated')
        else:
            self.fail(f'Expected JSON response, got {response.get("Content-Type")}: {response.content}')

    def test_delete_dog(self):
        """
        Проверяет, что можно удалить собаку через API.
        """
        url = f'/api/v1/mydogs/{self.dog.id}/'
        response = self.client.delete(url)
        self.assertIn(response.status_code, [200, 204])

class MydogsAuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='authuser', password='testpass')
        self.category = Category.objects.create(name='AuthCat')
        self.dog = Mydogs.objects.create(
            name='AuthDog', breed='AuthBreed', age=2, price=150, category=self.category
        )

    def test_protected_endpoint(self):
        """
        Проверяет, как работает доступ к API без авторизации (можно изменить на проверку 403, если потребуется).
        """
        response = self.client.get('/api/v1/mydogslist/')
        self.assertEqual(response.status_code, 200)  # Если нужен IsAuthenticated, поменяйте на 403

class OrderOwnerLogicTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='orderuser', password='testpass')
        self.category = Category.objects.create(name='OrderCat')
        self.dog = Mydogs.objects.create(
            name='OrderDog', breed='OrderBreed', age=1, price=100, category=self.category
        )
        self.client.login(username='orderuser', password='testpass')

    def test_owner_assigned_after_order(self):
        """
        Проверяет, что после оформления заказа через API у собаки появляется владелец (owner).
        """
        url = reverse('order-list')
        data = {"dogs_ids": [self.dog.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.dog.refresh_from_db()
        self.assertEqual(self.dog.owner, self.user)
