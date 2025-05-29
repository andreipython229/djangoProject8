from django.conf import settings
import random
import string
from django.utils.crypto import get_random_string

class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Инициализация middleware

    def __call__(self, request):
        # Генерация nonce
        nonce = get_random_string(16)
        request.csp_nonce = nonce  # Сохраняем nonce в объект запроса

        # Обработка ответа
        response = self.get_response(request)

        # Добавляем заголовок CSP только для HTML-ответов
        if 'text/html' in response.get('Content-Type', ''):
            if settings.DEBUG:
                # В режиме разработки упрощенный CSP — чтобы не мешал inline-стилям и скриптам
                response['Content-Security-Policy'] = (
                    "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data:;"
                )
            else:
                # В продакшене — строгий CSP с nonce
                response['Content-Security-Policy'] = (
                    f"default-src 'self'; script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
                    f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; img-src 'self' data:;"
            )
        return response