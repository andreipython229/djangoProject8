import requests
from bs4 import BeautifulSoup

url = 'http://example.com'  # Замените на URL, который вы хотите парсить
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print(soup.title.text)