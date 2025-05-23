from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    index_view,
    register,
    fetch_dogs,
    MydogsAPIView,
    MydogsViewSet,
    login_view,
    logout_view,
)

router = DefaultRouter()
router.register(r'mydogs', MydogsViewSet, basename='mydogs')

urlpatterns = [
    path('', index_view, name='index'),                   # /api/
    path('register/', register, name='register'),         # /api/register/
    path('login/', login_view, name='login'),             # /api/login/
    path('fetch-dogs/', fetch_dogs, name='fetch_dogs'),   # /api/fetch-dogs/
    path('mydogs/', MydogsAPIView.as_view(), name='mydogs_api'),  # /api/mydogs/
    path('logout/', logout_view, name='logout'),          # /api/logout/
    path('', include(router.urls)),                       # /api/mydogs/ (ViewSet)
]
