from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_client = models.BooleanField(default=False)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return f"Профиль {self.user.username}"

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile', null=True, blank=True)
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
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('paid', 'Оплачен'),
        ('cancelled', 'Отменён'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    dogs = models.ManyToManyField(Mydogs, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order #{self.id} by {self.user.username}'

@receiver(post_save, sender=Order)
def make_user_client_on_paid(sender, instance, **kwargs):
    if instance.status == 'paid':
        profile, created = UserProfile.objects.get_or_create(user=instance.user)
        if not profile.is_client:
            profile.is_client = True
            profile.save()
