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
import os
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from mydogs.views import index_view, register

# Заглушка для DevTools
def devtools_json(request):
    return HttpResponse("{}", content_type="application/json")

# Редирект /api/places/ → /api/v1/places/
def redirect_places(request):
    return redirect('/api/v1/places/')

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Регистрация
    path('api/register/', register, name='register'),

    # Редирект со старого пути
    path('api/places/', redirect_places),

    # Страницы React
    path('contacts', index_view),
    path('about', index_view),

    # Основной API
    path('api/v1/', include('mydogs.urls')),

    # Главная страница
    path('', index_view, name='home'),

    # DevTools путь
    path('.well-known/appspecific/com.chrome.devtools.json', devtools_json),
]

# В режиме разработки Django отдаёт статику из папки React build/static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'frontend', 'build', 'static'))
