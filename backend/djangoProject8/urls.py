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
from mydogs.views import (
    register, 
    login_view, 
    logout_view,
    dog_list,
    dog_detail,
    dogs_by_category,
    places_view
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from mydogs.views import index_view

# Заглушка для DevTools
def devtools_json(request):
    return HttpResponse("{}", content_type="application/json")

# Редирект /api/places/ → /api/v1/places/
def redirect_places(request):
    return redirect('/api/v1/places/')

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # JWT аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Редирект со старого пути
    path('api/places/', redirect_places),

    # API v1
    path('api/v1/', include('mydogs.urls')),

    # Страницы с собаками
    path('dogs/', dog_list, name='dog_list'),
    path('dogs/<int:dog_id>/', dog_detail, name='dog_detail'),
    path('dogs/category/<str:category>/', dogs_by_category, name='dogs_by_category'),

    # Страница Places
    path('places/', places_view, name='places'),

    # React-страницы
    path('contacts/', index_view, name='contacts'),
    path('about/', index_view, name='about'),
    path('favorite-places/', index_view, name='favorite_places'),

    # Главная страница
    path('', index_view, name='home'),

    # DevTools путь
    path('.well-known/appspecific/com.chrome.devtools.json', devtools_json),

    # Аутентификация
    path('register/', register, name='register_page'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('places/index.html', lambda request: redirect('/places/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)