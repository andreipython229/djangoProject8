import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from mydogs.views import (
    csp_report_view,
    register,
    MydogsAPIList,
    MydogsAPIView,
    fetch_dogs,
    MydogsViewSet,
    mydogs_list_view,
    serve_public_file_with_nonce,
    serve_build_file_with_nonce
)
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from mydogs.test_static import serve_static

# Настраиваем DefaultRouter
router = DefaultRouter()
router.register(r'mydogs', MydogsViewSet, basename='mydogs')

# Основные маршруты
urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # API
    path('api/register/', register, name='register'),  # Регистрация через API
    path('api/v1/mydogslist/', include(router.urls)),  # Эндпоинты ViewSet
    path('api/v1/mydogslist/<int:pk>/', MydogsAPIList.as_view(), name='mydogs-list-detail'),  # Детали объекта Mydogs

    # Страницы
    path('', MydogsAPIView.as_view(), name='home'),  # Главная страница
    path('dogs/', fetch_dogs, name='fetch-dogs'),  # Обработка маршрута /dogs/
    path('test/', TemplateView.as_view(template_name="test.html")),  # Пример тестового шаблона

    # Для обработки статических файлов
    path('static_test/<path:path>/', serve_static, name='static_test'),  # Для проверки статики

    # Динамическая обработка файлов из public и build
    path('public/<str:file_name>/', serve_public_file_with_nonce, name='serve_public_file'),
    path('build/<str:file_name>/', serve_build_file_with_nonce, name='serve_build_file'),

    # Дополнительные маршруты
    path('v1/mydogslist/', mydogs_list_view, name='mydogslist'),  # Дополнительный список
    path('csp-violation-report-endpoint/', csp_report_view, name='csp-violation-report-endpoint'),  # Отчёты CSP
]

# Маршруты для отладки (Debug Toolbar)
if settings.DEBUG:
    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),  # Стандартный путь для отладочной панели
    ]

# Подключение статических файлов
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Вывод списка маршрутов для проверки
from pprint import pprint
pprint(urlpatterns)