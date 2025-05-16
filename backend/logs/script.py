with open("django.log", "r", encoding="ISO-8859-1") as file:
    content = file.read()
with open("django_utf8.log", "w", encoding="utf-8") as file:
    file.write(content)

print("Файл успешно перекодирован!")