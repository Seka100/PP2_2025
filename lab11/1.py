import psycopg2
import csv

db_config = {
    "host": "localhost",
    "dbname": "phonebook",
    "user": "postgres",
    "password": "Serik_100",
    "port": 5432
}

def connect():
    return psycopg2.connect(**db_config)


# === CREATE TABLE ===
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        phone VARCHAR(20) NOT NULL
    );
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully")


# === Old functions ===
def insert_from_console():
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()
    sql = "INSERT INTO phonebook(username, phone) VALUES (%s, %s);"
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, (username, phone))
        conn.commit()
        print("Inserted successfully")
    except psycopg2.errors.UniqueViolation:
        print("Error: username already exists")
    finally:
        cur.close()
        conn.close()


def insert_from_csv(csv_file):
    try:
        conn = connect()
        cur = conn.cursor()
        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 2:
                    continue
                username, phone = row
                try:
                    cur.execute("INSERT INTO phonebook(username, phone) VALUES (%s, %s)", (username, phone))
                except psycopg2.errors.UniqueViolation:
                    conn.rollback()
                    continue
        conn.commit()
        print("CSV imported successfully")
    finally:
        cur.close()
        conn.close()


def update_username(old_name, new_name):
    sql = "UPDATE phonebook SET username = %s WHERE username = %s;"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (new_name, old_name))
    conn.commit()
    cur.close()
    conn.close()
    print("Username updated")


def update_phone(username, new_phone):
    sql = "UPDATE phonebook SET phone = %s WHERE username = %s;"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (new_phone, username))
    conn.commit()
    cur.close()
    conn.close()
    print("Phone updated")


def find_by_username(name):
    sql = "SELECT * FROM phonebook WHERE username = %s;"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (name,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def find_by_phone(phone):
    sql = "SELECT * FROM phonebook WHERE phone = %s;"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (phone,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def search_like(pattern):
    sql = "SELECT * FROM phonebook WHERE username ILIKE %s;"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (f"%{pattern}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def delete_by_username(name):
    sql = "DELETE FROM phonebook WHERE username = %s;"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (name,))
    conn.commit()
    cur.close()
    conn.close()
    print("Deleted by username")


def delete_by_phone(phone):
    sql = "DELETE FROM phonebook WHERE phone = %s;"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (phone,))
    conn.commit()
    cur.close()
    conn.close()
    print("Deleted by phone")


# === NEW DB FUNCTION CALLS (LAB 11) ===

def call_search_pattern(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def call_insert_or_update():
    username = input("Username: ")
    phone = input("Phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL insert_or_update(%s, %s)", (username, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Done")


def call_insert_many():
    n = int(input("How many users? "))
    usernames = []
    phones = []

    for _ in range(n):
        usernames.append(input("Username: "))
        phones.append(input("Phone: "))

    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL insert_many(%s, %s)", (usernames, phones))
    conn.commit()
    cur.close()
    conn.close()
    print("Batch insert complete")


def call_pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM paginate(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def call_delete():
    name = input("Username (skip = Enter): ").strip()
    phone = input("Phone (skip = Enter): ").strip()

    if name == "":
        name = None
    if phone == "":
        phone = None

    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Deleted")


# === MENU ===
def menu():
    create_table()
    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1 - Insert from console")
        print("2 - Insert from CSV")
        print("3 - Update username")
        print("4 - Update phone")
        print("5 - Search by username")
        print("6 - Search by phone")
        print("7 - Search LIKE pattern")
        print("8 - Delete by username")
        print("9 - Delete by phone")
        print("10 - Insert or update user  (DB procedure)")
        print("11 - Insert many users     (DB procedure)")
        print("12 - Search pattern        (DB function)")
        print("13 - Pagination            (DB function)")
        print("14 - Delete using procedure")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == "3":
            old = input("Old username: ")
            new = input("New username: ")
            update_username(old, new)
        elif choice == "4":
            name = input("Username: ")
            new = input("New phone: ")
            update_phone(name, new)
        elif choice == "5":
            print(find_by_username(input("Username: ")))
        elif choice == "6":
            print(find_by_phone(input("Phone: ")))
        elif choice == "7":
            print(search_like(input("Pattern: ")))
        elif choice == "8":
            delete_by_username(input("Username: "))
        elif choice == "9":
            delete_by_phone(input("Phone: "))
        elif choice == "10":
            call_insert_or_update()
        elif choice == "11":
            call_insert_many()
        elif choice == "12":
            print(call_search_pattern(input("Pattern: ")))
        elif choice == "13":
            print(call_pagination())
        elif choice == "14":
            call_delete()
        elif choice == "0":
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    menu()
