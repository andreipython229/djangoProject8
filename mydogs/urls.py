from django.contrib import admin
from django.urls import path, include
from mydogs.views import (
    csp_report_view,
    register,
    MydogsAPIList,
    MydogsAPIView,
    fetch_dogs,
    MydogsViewSet,
    index_view  # Добавляем index_view
)
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Настраиваем DefaultRouter
router = DefaultRouter()
router.register(r'mydogs', MydogsViewSet, basename='mydogs')

# Основные маршруты
urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # API
    path('api/register/', register, name='register'),
    path('api/v1/mydogslist/', include(router.urls)),
    path('api/v1/mydogslist/<int:pk>/', MydogsAPIView.as_view(), name='mydogs-detail'),

    # Страницы
    path('', index_view, name='home'),  # Используем index_view вместо MydogsAPIView
    path('dogs/', fetch_dogs, name='fetch-dogs'),
    path('test/', TemplateView.as_view(template_name="test.html")),

    # CSP
    path('csp-violation-report-endpoint/', csp_report_view, name='csp-violation-report-endpoint'),
]

# Подключение статических файлов
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)