from django.views.generic import RedirectView
from django.templatetags.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    index_view,
    register,
    login_view,
    logout_view,
    fetch_dogs,
    csp_report_view,
    MydogsAPIList,
    MydogsAPIView,
    MydogsProtectedView,
    ClientViewSet,
    CategoryViewSet,
    MydogsViewSet,
    PlaceViewSet,
    places_view,
    dog_list,
    dog_detail,
    dogs_by_category,
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'mydogs', MydogsViewSet)
router.register(r'places', PlaceViewSet)

urlpatterns = [
    # HTML-страницы для просмотра собак
    path('dogs/', dog_list, name='dog_list'),
    path('dogs/<int:dog_id>/', dog_detail, name='dog_detail'),
    path('dogs/category/<str:category>/', dogs_by_category, name='dogs_by_category'),

    # HTML-страница с любимыми местами (собаки)
    path('places/', places_view, name='places_page'),

    # Защищённый API текущего пользователя
    path('mydogs-protected/', MydogsProtectedView.as_view(), name='mydogs-protected'),

    # Регистрация, вход и выход
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Получение данных для страницы с собаками
    path('fetch-dogs/', fetch_dogs, name='fetch_dogs'),

    # CSP report endpoint
    path('csp-report/', csp_report_view, name='csp_report'),

    # API с generics
    path('mydogslist/', MydogsAPIList.as_view(), name='mydogs_list'),
    path('mydogs/<int:pk>/', MydogsAPIView.as_view(), name='mydogs_detail'),

    # ViewSet router
    path('api/', include(router.urls)),

    # favicon перенаправление
    path('favicon.ico', RedirectView.as_view(url=static('img/icons8-favicon-50.png'), permanent=True)),
]