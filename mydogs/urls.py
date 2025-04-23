from django.urls import path, include
from .views import (
    csp_report_view,
    register,
    MydogsAPIView,
    fetch_dogs,
    MydogsViewSet,
    index_view
)
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

# Настраиваем DefaultRouter
router = DefaultRouter()
router.register(r'mydogs', MydogsViewSet, basename='mydogs')

urlpatterns = [
    # API endpoints
    path('api/register/', register, name='register'),
    path('mydogs/', include(router.urls)),
    path('api/mydogs/<int:pk>/', MydogsAPIView.as_view(), name='mydogs-detail'),

    # Страницы
    path('', index_view, name='home'),
    path('places/', fetch_dogs, name='places'),
    path('test/', TemplateView.as_view(template_name="test.html"), name='test'),

    # CSP endpoint
    path('api/csp-violation-report/', csp_report_view, name='csp-violation-report'),
]