import logging
import requests
from functools import wraps

from django.conf import settings
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Mydogs
from .serializers import MydogsSerializer

logger = logging.getLogger(__name__)


# CSP-заголовок
def add_csp_header(response, nonce):
    response['Content-Security-Policy'] = (
        f"default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
        f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
        f"img-src 'self' data:;"
    )
    return response


# Декоратор для генерации nonce и добавления CSP
def with_nonce(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        nonce = get_random_string(16)
        request.nonce = nonce  # сохранить nonce в объект запроса
        response = view_func(request, *args, **kwargs)
        return add_csp_header(response, nonce)
    return _wrapped_view


# CSP отчёт
def csp_report_view(request):
    if request.method == 'POST':
        logger.info(f"CSP Report: {request.body}")
        return JsonResponse({'status': 'CSP report received'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=405)


# Главная страница
@with_nonce
def index_view(request):
    try:
        return render(request, 'mydogs/index.html', {
            'exception_notes': 'Нет ошибок',
            'nonce': request.nonce
        })
    except Exception as e:
        logger.error(f"Exception in index_view: {str(e)}")
        return JsonResponse({'error': 'Ошибка на главной странице'}, status=500)


# Регистрация
@csrf_protect
@with_nonce
def register(request):
    try:
        if request.method == "GET":
            return render(request, 'mydogs/register.html', {
                'exception_notes': 'Нет ошибок',
                'nonce': request.nonce
            })
        elif request.method == "POST":
            # TODO: Реализовать создание пользователя
            return JsonResponse({'message': 'User registered successfully'})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
    except Exception as e:
        logger.error(f"Exception in register: {str(e)}")
        return JsonResponse({'error': 'Ошибка во время регистрации'}, status=500)


# Логин
@csrf_protect
@with_nonce
def login_view(request):
    if request.method == "GET":
        return render(request, 'mydogs/login.html', {
            'exception_notes': '',
            'nonce': request.nonce
        })

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Успешный вход'}, status=200)
        else:
            return render(request, 'mydogs/login.html', {
                'exception_notes': 'Неверное имя пользователя или пароль',
                'nonce': request.nonce
            })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# Logout
@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Вы вышли из системы'}, status=200)


# API - Список / создание
class MydogsAPIList(generics.ListCreateAPIView):
    queryset = Mydogs.objects.all()
    serializer_class = MydogsSerializer


# API - GET/POST/PUT/DELETE по id
class MydogsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            dogs = Mydogs.objects.all()
            serializer = MydogsSerializer(dogs, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Exception in MydogsAPIView GET: {str(e)}")
            return Response({'error': 'Ошибка при получении данных'}, status=500)

    def post(self, request):
        try:
            serializer = MydogsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            post_new = serializer.save()
            return Response({'post': MydogsSerializer(post_new).data})
        except Exception as e:
            logger.error(f"Exception in MydogsAPIView POST: {str(e)}")
            return Response({'error': 'Ошибка при создании записи'}, status=500)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error': 'ID is required'}, status=400)

        instance = get_object_or_404(Mydogs, pk=pk)

        try:
            serializer = MydogsSerializer(instance=instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'post': serializer.data})
        except Exception as e:
            logger.error(f"Exception in MydogsAPIView PUT: {str(e)}")
            return Response({'error': 'Ошибка при обновлении записи'}, status=500)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error': 'ID is required'}, status=400)

        instance = get_object_or_404(Mydogs, pk=pk)

        try:
            instance.delete()
            return Response({'deleted': True})
        except Exception as e:
            logger.error(f"Exception in MydogsAPIView DELETE: {str(e)}")
            return Response({'error': 'Ошибка при удалении записи'}, status=500)


# ViewSet для DRF
class MydogsViewSet(viewsets.ModelViewSet):
    queryset = Mydogs.objects.all()
    serializer_class = MydogsSerializer


# Получение списка собак (с API)
@with_nonce
def fetch_dogs(request):
    try:
        api_url = f"{settings.API_BASE_URL}/api/v1/mydogslist/"
        try:
            api_response = requests.get(api_url, timeout=5)
            if api_response.status_code == 200:
                data = api_response.json()
                exception_notes = 'Данные успешно получены'
            else:
                data = []
                exception_notes = f"Ошибка при запросе к API: {api_response.status_code}"
        except requests.exceptions.RequestException as e:
            data = []
            exception_notes = f"Ошибка соединения: {str(e)}"

        return render(request, 'public/places.html', {
            'dogs': data,
            'exception_notes': exception_notes,
            'nonce': request.nonce
        })
    except Exception as e:
        logger.error(f"Exception in fetch_dogs: {str(e)}")
        return JsonResponse({'error': 'Ошибка при получении данных'}, status=500)
