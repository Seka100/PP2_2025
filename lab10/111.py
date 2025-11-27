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
            name = input("Username: ")
            print(find_by_username(name))
        elif choice == "6":
            phone = input("Phone: ")
            print(find_by_phone(phone))
        elif choice == "7":
            pattern = input("Pattern: ")
            print(search_like(pattern))
        elif choice == "8":
            name = input("Username: ")
            delete_by_username(name)
        elif choice == "9":
            phone = input("Phone: ")
            delete_by_phone(phone)
        elif choice == "0":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    menu()
