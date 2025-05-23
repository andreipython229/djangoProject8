"""
URL configuration for djangoProject8 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from mydogs.views import index_view, register

def devtools_json(request):
    return HttpResponse('{}', content_type='application/json')

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Регистрация (можно заменить на include, если больше путей)
    path('api/register/', register, name='register'),

    # Вызовы API из приложения mydogs
    path("api/v1/", include("mydogs.urls")),  # для запросов /api/v1/...
    path("api/", include("mydogs.urls")),     # для запросов /api/...


    # Главная страница
    path('', index_view, name='home'),

    # Для DevTools (специфичный путь)
    path('.well-known/appspecific/com.chrome.devtools.json', devtools_json),
]

# Раздача статики в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
