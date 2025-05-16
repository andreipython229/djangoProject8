import logging
import requests
from django.conf import settings
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
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
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
        f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; img-src 'self' data:;"
    )
    return response


# CSP отчёт
def csp_report_view(request):
    if request.method == 'POST':
        logger.info(f"CSP Report: {request.body}")
        return JsonResponse({'status': 'CSP report received'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=405)


# Главная страница
def index_view(request):
    try:
        nonce = get_random_string(16)
        response = render(request, 'mydogs/index.html', {
            'exception_notes': 'Нет ошибок',
            'nonce': nonce
        })
        return add_csp_header(response, nonce)
    except Exception as e:
        logger.error(f"Exception in index_view: {str(e)}")
        return JsonResponse({'error': 'Ошибка на главной странице'}, status=500)


# Регистрация
@csrf_protect
def register(request):
    try:
        nonce = get_random_string(16)
        if request.method == "GET":
            response = render(request, 'mydogs/register.html', {
                'exception_notes': 'Нет ошибок',
                'nonce': nonce
            })
            return add_csp_header(response, nonce)
        elif request.method == "POST":
            # Простейшая заглушка: можно доработать под создание пользователя
            return JsonResponse({'message': 'User registered successfully'})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
    except Exception as e:
        logger.error(f"Exception in register: {str(e)}")
        return JsonResponse({'error': 'Ошибка во время регистрации'}, status=500)


# Логин
@csrf_protect
def login_view(request):
    nonce = get_random_string(16)
    if request.method == "GET":
        response = render(request, 'mydogs/login.html', {
            'exception_notes': '',
            'nonce': nonce
        })
        return add_csp_header(response, nonce)

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Успешный вход'}, status=200)
        else:
            response = render(request, 'mydogs/login.html', {
                'exception_notes': 'Неверное имя пользователя или пароль',
                'nonce': nonce
            })
            return add_csp_header(response, nonce)
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
    def get_instance(self, pk):
        try:
            return Mydogs.objects.get(pk=pk)
        except Mydogs.DoesNotExist:
            logger.error(f"Mydogs object with id {pk} does not exist")
            return None

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
            logger.error("PUT request without pk")
            return Response({'error': 'ID is required'}, status=400)

        instance = self.get_instance(pk)
        if not instance:
            return Response({'error': 'Object not found'}, status=404)

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

        instance = self.get_instance(pk)
        if not instance:
            return Response({'error': 'Object not found'}, status=404)

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
def fetch_dogs(request):
    try:
        nonce = get_random_string(16)
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

        response = render(request, 'public/places.html', {
            'dogs': data,
            'exception_notes': exception_notes,
            'nonce': nonce
        })
        return add_csp_header(response, nonce)
    except Exception as e:
        logger.error(f"Exception in fetch_dogs: {str(e)}")
        return JsonResponse({'error': 'Ошибка при получении данных'}, status=500)
