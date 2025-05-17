from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    index_view,
    register,
    fetch_dogs,
    csp_report_view,
    login_view,
    MydogsAPIView,
    MydogsViewSet,
)
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Роутер без префикса (чтобы было /api/mydogs/)
router = DefaultRouter()
router.register(r'', MydogsViewSet, basename='mydogs')

urlpatterns = [
    # API endpoints
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('mydogs/', include(router.urls)),  # ← даст /api/mydogs/ и /api/mydogs/<pk>/
    path('mydogs/<int:pk>/', MydogsAPIView.as_view(), name='mydogs-detail'),  # ← опционально, если ты используешь кастомный APIView

    # Статические страницы
    path('', index_view, name='home'),
    path('places/', fetch_dogs, name='places'),
    path('test/', TemplateView.as_view(template_name="test.html"), name='test'),

    # CSP отчёт
    path('csp-violation-report/', csp_report_view, name='csp-violation-report'),
]

# Раздача статики в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
