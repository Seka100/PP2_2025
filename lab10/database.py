import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "dbname": "testdb",       # <-- измени на свою БД
    "user": "postgres",       # <-- имя пользователя
    "password": "Serik_100",       # <-- пароль PostgreSQL
    "port": 5432,
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
