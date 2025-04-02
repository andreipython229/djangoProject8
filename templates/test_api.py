
import requests

url =path('api/v1/mydogslist/', MydogsAPIView.as_view(), name='mydogs-list')  # Замени на реальный URL твоего API

response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # Обработка JSON-ответа
    for dog in data:
        print(f"Name: {dog['name']}, Breed: {dog['breed']}, Age: {dog['age']}, Price: {dog['price']}")
else:
    print(f"Ошибка: {response.status_code}")



