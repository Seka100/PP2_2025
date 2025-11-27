import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="phonebook",
    user="postgres",
    password="Serik_100"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    phone VARCHAR(20) UNIQUE
)
""")
conn.commit()


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook(first_name, phone) VALUES(%s, %s)", (name, phone))
    conn.commit()


def insert_from_csv(file):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO phonebook(first_name, phone) VALUES(%s, %s)", (row[0], row[1]))
    conn.commit()


def update_name(phone, new_name):
    cur.execute("UPDATE phonebook SET first_name=%s WHERE phone=%s", (new_name, phone))
    conn.commit()


def update_phone(name, new_phone):
    cur.execute("UPDATE phonebook SET phone=%s WHERE first_name=%s", (new_phone, name))
    conn.commit()


def query_all():
    cur.execute("SELECT * FROM phonebook")
    return cur.fetchall()


def query_by_name(name):
    cur.execute("SELECT * FROM phonebook WHERE first_name=%s", (name,))
    return cur.fetchall()


def query_by_phone(phone):
    cur.execute("SELECT * FROM phonebook WHERE phone=%s", (phone,))
    return cur.fetchall()


def delete_by_name(name):
    cur.execute("DELETE FROM phonebook WHERE first_name=%s", (name,))
    conn.commit()


def delete_by_phone(phone):
    cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()


insert_from_console()
insert_from_csv("data.csv")
print(query_all())

update_name("123456", "Alex")
update_phone("Alex", "999999")

print(query_by_name("Alex"))
delete_by_phone("999999")

cur.close()
conn.close()
