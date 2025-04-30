import sqlite3
import traceback
import os

db_dir = "../db"
print(os.path.dirname(os.path.realpath(__file__)))
os.makedirs(db_dir, exist_ok=True)

db_path = os.path.join(db_dir, "magazines.db")
print(db_path)

def pause():
    input("\nPress Enter to continue\n")

def create_tables(cursor):
    """Creates the required tables in the database.
    tables: publishers, magazines, subscribers, subscriptions"""
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                publisher_id INTEGER PRIMARY KEY,
                publisher_name TEXT NOT NULL UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                magazine_id INTEGER PRIMARY KEY,
                magazine_name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                subscriber_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscription_id INTEGER PRIMARY KEY,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id) ON DELETE CASCADE,
                FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id) ON DELETE CASCADE,
                UNIQUE (subscriber_id, magazine_id)
            )
        """)

        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def drop_tables():
    """Drops all tables from the magazines.db database if they exist."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS subscriptions;")
            cursor.execute("DROP TABLE IF EXISTS magazines;")
            cursor.execute("DROP TABLE IF EXISTS subscribers;")
            cursor.execute("DROP TABLE IF EXISTS publishers;")
            print("All tables dropped successfully.")
    except sqlite3.Error as e:
        print(f"Error dropping tables: {e}")

def add_publisher(cursor, publisher_name):
    """Adds a publisher."""
    try:
        statement1 = "SELECT publisher_id FROM publishers WHERE publisher_name = ?"
        cursor.execute(statement1, (publisher_name,))
        publisher = cursor.fetchone()
        if publisher:
            print(f"Publisher '{publisher_name}' already exists.")
            return
        statement2 = "INSERT INTO publishers (publisher_name) VALUES (?)"
        cursor.execute(statement2, (publisher_name,))
        print(f"Publisher '{publisher_name}' added.")
    except sqlite3.Error as e:
        print(f"Error adding publisher: {e}")


def add_magazine(cursor, magazine_name, publisher_id):
    """Adds a magazine linked to a publisher."""
    try:
        statement1 = "SELECT 1 FROM magazines WHERE magazine_name = ?"
        cursor.execute(statement1, (magazine_name,))
        magazine = cursor.fetchone()
        if magazine:
            print(f"Magazine '{magazine_name}' already exists.")
            return
        statement2 = "SELECT 1 FROM publishers WHERE publisher_id = ?"
        cursor.execute(statement2, (publisher_id,))
        publisher = cursor.fetchone()
        if not publisher:
            print(f"Publisher with ID {publisher_id} does not exist.")
            return

        statement3 = "INSERT INTO magazines (magazine_name, publisher_id) VALUES (?, ?)"
        cursor.execute(statement3, (magazine_name, publisher_id))
        print(f"Magazine '{magazine_name}' added.")
    except sqlite3.Error as e:
        print(f"Error adding magazine: {e}")

def add_subscriber(cursor, name, address):
    """Adds a subscriber."""
    try:
        statement1 = "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?"
        cursor.execute(statement1, (name, address))
        if cursor.fetchone():
            print(f"Subscriber '{name}' at '{address}' already exists.")
            return
        statement2 = "INSERT INTO subscribers (name, address) VALUES (?, ?)"
        cursor.execute(statement2, (name, address))
        print(f"Subscriber '{name}' at '{address}' added.")
    except sqlite3.Error as e:
        print(f"Error adding subscriber: {e}")

def add_subscription(cursor, subscriber_id, magazine_id, expiration_date):
    """Adds a subscription if the subscriber and magazine exist."""
    try:
        statement1 = "SELECT 1 FROM subscribers WHERE subscriber_id = ?"
        cursor.execute(statement1, (subscriber_id,))
        subscriber = cursor.fetchone()
        if not subscriber:
            print(f"Subscriber ID {subscriber_id} not found.")
            return

        statement2 = "SELECT 1 FROM magazines WHERE magazine_id = ?"
        cursor.execute(statement2, (magazine_id,))
        magazine = cursor.fetchone()
        if not magazine:
            print(f"Magazine ID {magazine_id} not found.")
            return

        statement3 = """SELECT 1 FROM subscriptions WHERE subscriber_id = ? AND magazine_id = ?"""
        cursor.execute(statement3, (subscriber_id, magazine_id))
        subscription = cursor.fetchone()
        if subscription:
            print(f"Subscription already exists: subscriber {subscriber_id} for magazine {magazine_id}")
            return

        statement4 = """INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)"""
        cursor.execute(statement4, (subscriber_id, magazine_id, expiration_date))
        print(f"Subscription added: subscriber {subscriber_id} for magazine {magazine_id}")
    except sqlite3.Error as e:
        print(f"Error adding subscription: {e}")

try:
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        create_tables(cursor)
        # drop_tables()
        print("Database created and connected successfully.")

        # insert data
        add_publisher(cursor, "American Media") # 1
        add_publisher(cursor, "Business Insider") # 2
        add_publisher(cursor, "National Geographic Partners") # 3
        add_publisher(cursor, "Time USA") # 4

        add_magazine(cursor, "National Geographic", 3)
        add_magazine(cursor, "Time", 4)
        add_magazine(cursor, "Finance Insights", 2)
        add_magazine(cursor, "Us Weekly", 1)

        add_subscriber(cursor, "Alice Wilson", "123 Main St, NY")
        add_subscriber(cursor, "Alice Wilson", "1485 Long Dr, CA")
        add_subscriber(cursor, "Bob Johnson", "456 Oak St, SF")
        add_subscriber(cursor, "Charlie Lee", "789 Pine St, WA")

        add_subscription(cursor, 1, 1, '2025-12-31')
        add_subscription(cursor, 1, 2, '2025-11-30')
        add_subscription(cursor, 2, 3, '2026-01-15')
        add_subscription(cursor, 3, 3, '2025-10-10')
        add_subscription(cursor, 3, 4, '2027-09-20')
        add_subscription(cursor, 4, 4, '2025-11-15')

        conn.commit()
        print("Data inserted successfully.")

except Exception as e:
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(
            f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")
else:
        print("All SQL operations completed.")
