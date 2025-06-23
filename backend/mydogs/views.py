import logging
import json
import requests
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Mydogs, Client, Category, Place
from .serializers import (
    MydogsSerializer,
    ClientSerializer,
    CategorySerializer,
    PlaceSerializer,
)

logger = logging.getLogger(__name__)

# CSP middleware helpers
def add_csp_header(response, nonce):
    response['Content-Security-Policy'] = (
        f"default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
        f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
        f"img-src 'self' data:;"
    )
    return response

def with_nonce(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        nonce = get_random_string(16)
        request.nonce = nonce
        response = view_func(request, *args, **kwargs)
        if hasattr(response, 'context_data') and response.context_data is not None:
            response.context_data['nonce'] = nonce
        return add_csp_header(response, nonce)
    return _wrapped_view

# CSP report endpoint
@csrf_protect
def csp_report_view(request):
    if request.method == 'POST':
        logger.info(f"CSP Report: {request.body.decode('utf-8')}")
        return JsonResponse({'status': 'CSP report received'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=405)

import secrets

def generate_nonce():
    return secrets.token_hex(12)

def index_view(request):
    # Используем nonce из CSPMiddleware
    nonce = getattr(request, 'csp_nonce', '')
    
    if request.path == '/':
        template_name = 'index.html'
    else:
        template_name = 'base_react.html'
        
    return render(request, template_name, {'nonce': nonce})

# Регистрация пользователя
@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email', '')

            if not username or not password:
                return JsonResponse({'error': 'Имя пользователя и пароль обязательны'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Пользователь с таким именем уже существует'}, status=400)

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            return JsonResponse({'message': 'Пользователь успешно зарегистрирован'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный формат JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Ошибка: {str(e)}'}, status=500)

    # Для GET-запросов и всех остальных случаев
    nonce = getattr(request, 'csp_nonce', '')
    return render(request, 'mydogs/register.html', {'nonce': nonce})

# Вход пользователя — с поддержкой messages и nonce
@csrf_protect
@with_nonce
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('mydogs-protected')  # или другой нужный URL name
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль.')
            return redirect('mydogs-protected')
    messages.info(request, 'Тестовое сообщение: всё работает!')
    return render(request, 'mydogs/login.html', {
        'nonce': request.nonce
    })

# Выход
@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Вы вышли из системы'}, status=200)

# API для списка собак
class MydogsAPIList(generics.ListCreateAPIView):
    queryset = Mydogs.objects.all()
    serializer_class = MydogsSerializer

# Полноценный CRUD через APIView
class MydogsAPIView(APIView):
    def get(self, request):
        dogs = Mydogs.objects.all()
        serializer = MydogsSerializer(dogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MydogsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_new = serializer.save()
        return Response({'post': MydogsSerializer(post_new).data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error': 'ID is required'}, status=400)

        instance = get_object_or_404(Mydogs, pk=pk)
        serializer = MydogsSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error': 'ID is required'}, status=400)

        instance = get_object_or_404(Mydogs, pk=pk)
        instance.delete()
        return Response({'deleted': True})

# Только для авторизованных
class MydogsProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dogs = Mydogs.objects.filter(owner=request.user)
        serializer = MydogsSerializer(dogs, many=True)
        return Response(serializer.data)

# ViewSets
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MydogsViewSet(viewsets.ModelViewSet):
    queryset = Mydogs.objects.all()
    serializer_class = MydogsSerializer

class IsAdminOrReadOnly(BasePermission):
    """
    Разрешает чтение всем аутентифицированным пользователям,
    а изменение только админам.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

# Страница с собаками (через API-запрос)
@with_nonce
def fetch_dogs(request):
    try:
        api_url = f"{settings.API_BASE_URL}/api/v1/mydogslist/"
        api_response = requests.get(api_url, timeout=5)

        if api_response.status_code == 200:
            data = api_response.json()
            exception_notes = 'OK'
        else:
            data = []
            exception_notes = f"Ошибка: {api_response.status_code}"

        return render(request, 'mydogs/dogs.html', {
            'dogs': data,
            'exception_notes': exception_notes,
            'nonce': request.nonce
        })

    except Exception as e:
        logger.error(f"Exception in fetch_dogs: {str(e)}")
        return JsonResponse({'error': 'Ошибка при получении данных'}, status=500)

# --- ДОБАВЛЕНО: страница places ---
@with_nonce
def places_view(request):
    return render(request, 'mydogs/places.html', {
        'nonce': request.nonce
    })

# Функции для отображения списка собак
@with_nonce
def dog_list(request):
    print("--- Функция dog_list вызвана! ---")
    dogs = Mydogs.objects.all()
    return render(request, 'mydogs/dog_list.html', {
        'dogs': dogs,
        'nonce': request.nonce
    })

@with_nonce
def dog_detail(request, dog_id):
    dog = get_object_or_404(Mydogs, id=dog_id)
    return render(request, 'mydogs/dog_detail.html', {
        'dog': dog,
        'nonce': request.nonce
    })

@with_nonce
def dogs_by_category(request, category):
    dogs = Mydogs.objects.filter(category__name=category)
    return render(request, 'mydogs/dog_list.html', {
        'dogs': dogs,
        'category': category,
        'nonce': request.nonce
    })