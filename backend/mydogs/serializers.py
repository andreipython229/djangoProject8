from rest_framework import serializers
from .models import Mydogs, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class MydogsSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        help_text="ID категории"
    )
    category_data = CategorySerializer(source='category', read_only=True)

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
        ]
        read_only_fields = ['id', 'category_data']

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
