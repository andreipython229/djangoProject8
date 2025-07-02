from django.contrib import admin
from .models import Mydogs, Category


@admin.register(Mydogs)
class MydogsAdmin(admin.ModelAdmin):
    # Настройка отображения полей в списке объектов
    list_display = ('name', 'breed', 'age', 'price', 'category', 'get_owner')
    # Настройка полей для фильтрации
    list_filter = ('breed', 'category')
    # Поля для поиска
    search_fields = ('name', 'breed')

    def get_owner(self, obj):
        return obj.owner.username if obj.owner else None
    get_owner.short_description = 'Владелец'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Настройка отображения полей
    list_display = ('name',)
    # Поля для поиска
    search_fields = ('name',)
