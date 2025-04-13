from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)


    def __str__(self):
        return self.name

class Mydogs(models.Model):
    name = models.CharField(max_length=100, default='Unknown')
    breed = models.CharField(max_length=100, default='Unknown')
    age = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


