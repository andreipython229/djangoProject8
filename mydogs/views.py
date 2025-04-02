from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import requests
from rest_framework import generics, viewsets
from .models import Mydogs
from .serializers import MydogsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
import logging
import os
from django.conf import settings

# Настройка логирования
logger = logging.getLogger(__name__)

# Функция для обработки CSP-отчётов
def csp_report_view(request):
    if request.method == 'POST':
        logger.info(f"CSP Report: {request.body}")
        return JsonResponse({'status': 'CSP report received'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=405)

# Главная страница
def index_view(request):
    try:
        # Генерация nonce
        nonce = get_random_string(16)
        response = render(request, 'index.html', {'exception_notes': 'Нет ошибок', 'nonce': nonce})
        response['Content-Security-Policy'] = (
            f"default-src 'self'; script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
            f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; img-src 'self' data:;"
        )
        return response
    except Exception as e:
        logger.error(f"Exception in index_view: {str(e)}")
        return JsonResponse({'error': 'Ошибка на главной странице'}, status=500)

# Регистрация пользователя
def register(request):
    try:
        # Генерация nonce
        nonce = get_random_string(16)
        if request.method == "GET":
            response = render(request, 'register.html', {'exception_notes': 'Нет ошибок', 'nonce': nonce})
            response['Content-Security-Policy'] = (
                f"default-src 'self'; script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
                f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; img-src 'self' data:;"
            )
            return response
        elif request.method == "POST":
            return JsonResponse({'message': 'User registered successfully'})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
    except Exception as e:
        logger.error(f"Exception in register: {str(e)}")
        return JsonResponse({'error': 'Ошибка во время регистрации'}, status=500)

# API для работы с Mydogs
class MydogsAPIList(generics.ListCreateAPIView):
    queryset = Mydogs.objects.all()
    serializer_class = MydogsSerializer

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
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'}, status=400)

        instance = self.get_instance(pk)
        if not instance:
            return Response({'error': 'Object does not exist'}, status=404)
        try:
            serializer = MydogsSerializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'post': serializer.data})
        except Exception as e:
            logger.error(f"Exception in MydogsAPIView PUT: {str(e)}")
            return Response({'error': 'Ошибка при обновлении записи'}, status=500)

        def delete(self, request, *args, **kwargs):
            pk = kwargs.get('pk', None)
            if not pk:
                return Response({'error': 'Method DELETE not allowed'}, status=400)

            instance = self.get_instance(pk)
            if not instance:
                return Response({'error': 'Object does not exist'}, status=404)

            try:
                instance.delete()
                return Response({'deleted': True})
            except Exception as e:
                logger.error(f"Exception in MydogsAPIView DELETE: {str(e)}")
                return Response({'error': 'Ошибка при удалении записи'}, status=500)

        # ViewSet для Mydogs
        class MydogsViewSet(viewsets.ModelViewSet):
            queryset = Mydogs.objects.all()
            serializer_class = MydogsSerializer

        # Получение списка собак
        def fetch_dogs(request):
            """
            Функция для получения данных из API и рендеринга шаблона places.html.
            """
            try:
                # Генерация nonce
                nonce = get_random_string(16)
                api_url = f"{settings.API_BASE_URL}/api/v1/mydogslist/"
                api_response = requests.get(api_url)
                if api_response.status_code == 200:
                    data = api_response.json()
                    exception_notes = 'Данные успешно получены'
                else:
                    data = []
                    exception_notes = f"Ошибка при запросе к API: {api_response.status_code}"

                # Рендер шаблона places.html
                response = render(request, 'places.html',
                                  {'dogs': data, 'exception_notes': exception_notes, 'nonce': nonce})
                response['Content-Security-Policy'] = (
                    f"default-src 'self'; script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
                    f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; img-src 'self' data:;"
                )
                return response
            except Exception as e:
                logger.error(f"Exception in fetch_dogs: {str(e)}")
                return JsonResponse({'error': 'Ошибка при получении данных'}, status=500)
        # Динамическая обработка файлов из папки public
        def serve_public_file_with_nonce(request, file_name):
            nonce = get_random_string(16)
            file_path = os.path.join('public', file_name)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                content = content.replace('{{ nonce }}', nonce)
                response = HttpResponse(content)
                response['Content-Security-Policy'] = (
                    f"default-src 'self'; script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
                    f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; img-src 'self' data:;"
                )
                return response
            except FileNotFoundError:
                return HttpResponse("Файл не найден", status=404)

        # Динамическая обработка файлов из папки build
        def serve_build_file_with_nonce(request, file_name):
            nonce = get_random_string(16)
            file_path = os.path.join('build', file_name)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                content = content.replace('{{ nonce }}', nonce)
                response = HttpResponse(content)
                response['Content-Security-Policy'] = (
                    f"default-src 'self'; script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
                    f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; img-src 'self' data:;"
                )
                return response
            except FileNotFoundError:
                return HttpResponse("Файл не найден", status=404)