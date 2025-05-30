import logging
import requests
from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Mydogs, Client, Category, Place
from .serializers import (
    MydogsSerializer,
    ClientSerializer,
    CategorySerializer,
    PlaceSerializer,
)

logger = logging.getLogger(__name__)

# -------------------------------
# CSP middleware helpers
# -------------------------------
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
        return add_csp_header(response, nonce)
    return _wrapped_view

# -------------------------------
# CSP report endpoint
# -------------------------------
def csp_report_view(request):
    if request.method == 'POST':
        logger.info(f"CSP Report: {request.body}")
        return JsonResponse({'status': 'CSP report received'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=405)

# -------------------------------
# Main pages
# -------------------------------
@with_nonce
def index_view(request):
    return render(request, 'mydogs/index.html', {
        'exception_notes': 'Нет ошибок',
        'nonce': request.csp_nonce
    })

@csrf_protect
@with_nonce
def register(request):
    if request.method == "GET":
        return render(request, 'mydogs/register.html', {
            'exception_notes': 'Нет ошибок',
            'nonce': request.nonce
        })
    elif request.method == "POST":
        return JsonResponse({'message': 'User registered successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

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

@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Вы вышли из системы'}, status=200)

# -------------------------------
# DRF: Open API
# -------------------------------
class MydogsAPIList(generics.ListCreateAPIView):
    queryset = Mydogs.objects.all()
    serializer_class = MydogsSerializer

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

# -------------------------------
# 🔒 Защищённый API для текущего пользователя
# -------------------------------
class MydogsProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dogs = Mydogs.objects.filter(owner=request.user)
        serializer = MydogsSerializer(dogs, many=True)
        return Response(serializer.data)

# -------------------------------
# ViewSets (для router)
# -------------------------------
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MydogsViewSet(viewsets.ModelViewSet):
    queryset = Mydogs.objects.all()
    serializer_class = MydogsSerializer

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

# -------------------------------
# Страница с собаками
# -------------------------------
@with_nonce
def fetch_dogs(request):
    try:
        api_url = f"{settings.API_BASE_URL}/api/v1/mydogslist/"
        api_response = requests.get(api_url, timeout=5)
        data = api_response.json() if api_response.status_code == 200 else []
        exception_notes = 'OK' if api_response.status_code == 200 else f"Ошибка: {api_response.status_code}"
        return render(request, 'public/places.html', {
            'dogs': data,
            'exception_notes': exception_notes,
            'nonce': request.nonce
        })
    except Exception as e:
        logger.error(f"Exception in fetch_dogs: {str(e)}")
        return JsonResponse({'error': 'Ошибка при получении данных'}, status=500)
