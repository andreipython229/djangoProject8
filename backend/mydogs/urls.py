from django.urls import path, include
from rest_framework import routers
from .views import MydogsProtectedView
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

router = routers.DefaultRouter()
router.register(r'mydogs', MydogsViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('api/mydogs/', MydogsProtectedView.as_view(), name='mydogs-protected'),
    path('', index_view, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('fetch-dogs/', fetch_dogs, name='fetch_dogs'),
    path('csp-report/', csp_report_view, name='csp_report'),

    # API на основе generics
    path('mydogslist/', MydogsAPIList.as_view(), name='mydogs_list'),
    path('mydogs/<int:pk>/', MydogsAPIView.as_view(), name='mydogs_detail'),

    # Подключаем router
    path('', include(router.urls)),  # 👈 теперь /api/clients/ и /api/mydogs/ работают
]
