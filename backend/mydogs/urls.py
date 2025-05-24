from django.urls import path, include
from rest_framework import routers

from .views import (
    index_view,
    register,
    login_view,
    logout_view,
    fetch_dogs,
    csp_report_view,
    MydogsAPIList,
    MydogsAPIView,
    MydogsViewSet,
    ClientViewSet,
)

# DRF router для ViewSet'ов
router = routers.DefaultRouter()
router.register(r'mydogs', MydogsViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('', index_view, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('fetch-dogs/', fetch_dogs, name='fetch_dogs'),

    path('csp-report/', csp_report_view, name='csp_report'),

    # API на основе generics ListCreateAPIView
    path('api/v1/mydogslist/', MydogsAPIList.as_view(), name='mydogs_list'),

    # API с CRUD по ID (GET, POST, PUT, DELETE)
    path('api/v1/mydogs/<int:pk>/', MydogsAPIView.as_view(), name='mydogs_detail'),

    # Подключаем router с ViewSet-ами
    path('api/v1/', include(router.urls)),
    path('api/', include(router.urls)),  # 👈 это добавит /api/clients/
]
