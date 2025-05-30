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
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'mydogs', MydogsViewSet)
router.register(r'places', PlaceViewSet)

urlpatterns = [
    path('mydogs-protected/', MydogsProtectedView.as_view(), name='mydogs-protected'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('fetch-dogs/', fetch_dogs, name='fetch_dogs'),
    path('csp-report/', csp_report_view, name='csp_report'),

    # API на основе generics
    path('mydogslist/', MydogsAPIList.as_view(), name='mydogs_list'),
    path('mydogs/<int:pk>/', MydogsAPIView.as_view(), name='mydogs_detail'),

    # Автоматически подключаем viewsets
    path('', include(router.urls)),

    # favicon перенаправление
    path('favicon.ico', RedirectView.as_view(url=static('img/icons8-favicon-50.png'), permanent=True)),
]
