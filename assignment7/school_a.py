import sqlite3
import os

db_dir = "../db"
os.makedirs(db_dir, exist_ok=True)

# Connect to a new SQLite database
with  sqlite3.connect("../db/school.db") as conn:
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                major TEXT
            )
        """)

    # print("Database created and connected successfully.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Courses (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL UNIQUE,
            instructor_name TEXT
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Enrollments (
            enrollment_id INTEGER PRIMARY KEY,
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES Students (student_id),
            FOREIGN KEY (course_id) REFERENCES Courses (course_id)
        )
        """)

    print("Tables created successfully.")
