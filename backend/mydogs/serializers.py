from rest_framework import serializers
from .models import Mydogs, Category, Client, Place
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone']


class MydogsSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        help_text="ID категории"
    )
    category_data = CategorySerializer(source='category', read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Mydogs
        fields = [
            'id',
            'name',
            'breed',
            'age',
            'price',
            'category',
            'category_data',
            'owner',
            'image',
        ]
        read_only_fields = ['id', 'category_data', 'owner', 'image']

    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError("Возраст не может быть отрицательным.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['price'] = f"{rep['price']} ₽"
        return rep


class PlaceSerializer(serializers.ModelSerializer):
    mydog_name = serializers.CharField(source='mydog.name', read_only=True)
    mydog_age = serializers.IntegerField(source='mydog.age', read_only=True)
    mydog_image = serializers.ImageField(source='mydog.image', read_only=True)

    class Meta:
        model = Place
        fields = '__all__'
