import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Получить список таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Таблицы в базе данных:")
for table in tables:
    print(table[0])

conn.close()