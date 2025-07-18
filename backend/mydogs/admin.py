from django.contrib import admin
from .models import Client, Category, Mydogs, Place, Order, UserProfile

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status', 'user')
    search_fields = ('user__username',)

admin.site.register(Order, OrderAdmin)
admin.site.register(UserProfile)
admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Mydogs)
admin.site.register(Place)
