from mydogs.models import Mydogs
# scripts/myscript.py
#from mydogs.models import Mydogs

def run():
    print("Выполнение скрипта myscript")
    dogs = Mydogs.objects.all()
    for dog in dogs:
        print(f"{dog.name} - {dog.age}")

# Вызов функции run
run()
