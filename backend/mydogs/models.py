from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

class Mydogs(models.Model):
    name = models.CharField(max_length=100, default='Unknown')
    breed = models.CharField(max_length=100, default='Unknown')
    age = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mydogs', null=True, blank=True)
    image = models.ImageField(upload_to='dogs_images/', blank=True, null=True)
    GENDER_CHOICES = [
        ('male', 'Мальчик'),
        ('female', 'Девочка'),
    ]
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default='male',
        verbose_name='Пол'
    )

    def __str__(self):
        return self.name

class Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='places')
    mydog = models.ForeignKey('Mydogs', on_delete=models.CASCADE, related_name='favorite_places', null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='places_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    dogs = models.ManyToManyField(Mydogs, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, default='pending')  # pending, paid, cancelled и т.д.

    def __str__(self):
        return f'Order #{self.id} by {self.user.username}'
