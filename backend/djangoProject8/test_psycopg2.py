import psycopg

try:
    conn = psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="andrzej10071994",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except Exception as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")