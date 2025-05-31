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
                response['Content-Security-Policy'] = (
                    f"default-src 'self'; "
                    f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
                    f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
                    f"img-src 'self' data:;"
                )

        return response