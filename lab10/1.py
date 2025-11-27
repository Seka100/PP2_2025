import psycopg2
from database import get_connection
import csv


def create_phonebook_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)

    conn.commit()
    conn.close()



def insert_from_console():
    username = input("Введите имя: ").strip()
    phone = input("Введите телефон: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s);",
        (username, phone)
    )

    conn.commit()
    conn.close()
    print("Данные успешно добавлены.")


def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            username, phone = row
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s);",
                (username, phone)
            )

    conn.commit()
    conn.close()
    print("CSV данные загружены.")


def update_phone(username, new_phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s;",
                (new_phone, username))

    conn.commit()
    conn.close()


def update_username(phone, new_username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET username = %s WHERE phone = %s;",
                (new_username, phone))

    conn.commit()
    conn.close()


def search_by_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE username = %s;", (name,))
    rows = cur.fetchall()
    conn.close()
    return rows


def search_by_phone(phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE phone = %s;", (phone,))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_by_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE username = %s;", (name,))
    conn.commit()
    conn.close()


def delete_by_phone(phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE phone = %s;", (phone,))
    conn.commit()
    conn.close()
