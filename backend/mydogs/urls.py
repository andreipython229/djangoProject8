from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    register,
    login_view,
    ClientViewSet,
    CategoryViewSet,
    MydogsViewSet,
    PlaceViewSet,
    MydogsAPIList,
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'mydogs', MydogsViewSet)
router.register(r'places', PlaceViewSet)

urlpatterns = [
    # ViewSets
    path('', include(router.urls)),

    # Auth
    path('register/', register, name='api-register'),
    path('login/', login_view, name='api-login'),

    # Другие API-эндпоинты
    path('mydogslist/', MydogsAPIList.as_view(), name='mydogs_list'),
]