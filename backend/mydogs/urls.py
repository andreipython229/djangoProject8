from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Mydog
from .serializers import MydogSerializer
from rest_framework.generics import RetrieveAPIView

# Главная страница — отдаёт React приложение или что-то простое
def index_view(request):
    return render(request, 'index.html')


# Регистрация — если у тебя кастомная регистрация через DRF, можно тут сделать
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    # пример простой заглушки — сделай свою логику создания пользователя
    return JsonResponse({"detail": "Регистрация не реализована"}, status=501)


# Пример для выдачи списка собак
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def fetch_dogs(request):
    dogs = Mydog.objects.all()
    serializer = MydogSerializer(dogs, many=True)
    return Response(serializer.data)


# CSP отчет (оставлю как есть)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def csp_report_view(request):
    print('CSP violation report:', request.data)
    return Response(status=204)


# Вью для конкретной собаки, используя APIView
class MydogsAPIView(RetrieveAPIView):
    queryset = Mydog.objects.all()
    serializer_class = MydogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ViewSet для CRUD Mydog
class MydogsViewSet(viewsets.ModelViewSet):
    queryset = Mydog.objects.all()
    serializer_class = MydogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Вход (логин) — если нужен, можно реализовать или использовать SimpleJWT views


# Logout с blacklist токенов
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
