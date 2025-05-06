import sqlite3

# 7.6 Adding Entries with Foreign Keys
def add_student(cursor, name, age, major):
    try:
        cursor.execute("SELECT * FROM Students WHERE name = ?", (name,))

        if cursor.fetchone():
            print(f"{name} is already in the database.")
            return
        cursor.execute("INSERT INTO Students (name, age, major) VALUES (?,?,?)", (name, age, major))
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")

def add_course(cursor, name, instructor):
    try:
        cursor.execute("SELECT * FROM Courses WHERE course_name = ?", (name,))
        if cursor.fetchone():
            print(f"{name} is already in the database.")
            return
        cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES (?,?)", (name, instructor))
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")

def enroll_student(cursor, student, course):
    cursor.execute("SELECT * FROM Students WHERE name = ?", (student,))
    results = cursor.fetchall()
    if len(results) > 0:
        student_id = results[0][0]
    else:
        print(f"There was no student named {student}.")
        return
    cursor.execute("SELECT * FROM Courses WHERE course_name = ?", (course,))
    results = cursor.fetchall()
    if len(results) > 0:
        course_id = results[0][0]
    else:
        print(f"There was no course named {course}.")
        return

    cursor.execute("SELECT * FROM Enrollments WHERE student_id = ? AND course_id = ?", (student_id, course_id))
    results = cursor.fetchall()
    if len(results) > 0:
        print(f"Student {student} is already enrolled in course {course}.")
        return

    cursor.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))

def clean_database(cursor):
    """Deletes all records from tables."""
    cursor.execute("DELETE FROM Enrollments")
    cursor.execute("DELETE FROM Students")
    cursor.execute("DELETE FROM Courses")
    cursor.connection.commit()
    print("All records deleted successfully.")

def update_student(cursor, old_name, new_name, new_age):
    cursor.execute("""
        UPDATE Students
        SET name = ?, age = ?
        WHERE name = ?;
    """, (new_name, new_age, old_name))
    print(f"\nStudent {old_name} updated to {new_name}, age {new_age}.")


# Connect to the database
with sqlite3.connect("../db/school.db") as conn:
    # clean db when needed
    # conn.execute("PRAGMA foreign_keys = ON")
    # cursor = conn.cursor()
    # clean_database(cursor)
    # conn.commit()
    # print("All records deleted successfully.")

    # add student
    conn.execute("PRAGMA foreign_keys = 1") # foreign key constraint
    cursor = conn.cursor()

    # Insert sample data into tables
    # cursor.execute("INSERT INTO Students (name, age, major) VALUES ('Alice', 20, 'Computer Science')")
    # cursor.execute("INSERT INTO Students (name, age, major) VALUES ('Bob', 22, 'History')")
    # cursor.execute("INSERT INTO Students (name, age, major) VALUES ('Charlie', 19, 'Biology')")
    # cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES ('Math 101', 'Dr. Smith')")
    # cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES ('English 101', 'Ms. Jones')")
    # cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES ('Chemistry 101', 'Dr. Lee')")

    add_student(cursor, 'Alice', 20, 'Computer Science')
    add_student(cursor, 'Bob', 22, 'History')
    add_student(cursor, 'Charlie', 19, 'Biology')
    add_course(cursor, 'Math 101', 'Dr. Smith')
    add_course(cursor, 'English 101', 'Ms. Jones')
    add_course(cursor, 'Chemistry 101', 'Dr. Lee')

    conn.commit()
    print("\nSample data inserted successfully.")

    # 7.5 Writing SQL Queries
    cursor.execute("SELECT * FROM Students WHERE name = 'Alice'")
    result = cursor.fetchall()
    for row in result:
        print(row)

    enroll_student(cursor, "Alice", "Math 101")
    enroll_student(cursor, "Alice", "Chemistry 101")
    enroll_student(cursor, "Bob", "Math 101")
    enroll_student(cursor, "Bob", "English 101")
    enroll_student(cursor, "Charlie", "English 101")
    conn.commit()

    # 7.7 More Complicated Queries
    print("\nCourses that start with 'math':")
    cursor.execute("SELECT * FROM Courses WHERE course_name LIKE 'math%'")
    for row in cursor.fetchall():
        print(row)

    print("\nStudents older than 20:")
    cursor.execute("SELECT * FROM Students WHERE age > 20")
    for row in cursor.fetchall():
        print(row)

    print("\nStudents whose major is not 'History':")
    cursor.execute("SELECT * FROM Students WHERE major <> 'History'")
    for row in cursor.fetchall():
        print(row)

    # Joins
    print("\nAll students with their enrolled courses:")
    cursor.execute("""
            SELECT Students.name, Courses.course_name 
            FROM Enrollments
            JOIN Students ON Enrollments.student_id = Students.student_id
            JOIN Courses ON Enrollments.course_id = Courses.course_id
        """)
    for row in cursor.fetchall():
        print(f"{row[0]} is enrolled in {row[1]}")

    print("\nStudents and the courses they are enrolled in:")
    cursor.execute("""
            SELECT s.name, c.course_name
            FROM Students s
            JOIN Enrollments e ON s.student_id = e.student_id
            JOIN Courses c ON e.course_id = c.course_id;
        """)
    rows = cursor.fetchall()
    for name, course in rows:
        print(f"{name} is enrolled in {course}")

    print("\nStudents and their enrolled courses:")
    cursor.execute("""
            SELECT Students.name, Courses.course_name 
            FROM Enrollments
            JOIN Students ON Enrollments.student_id = Students.student_id
            JOIN Courses ON Enrollments.course_id = Courses.course_id;
        """)
    rows = cursor.fetchall()
    for student_name, course_name in rows:
        print(f"{student_name} is enrolled in {course_name}")

    # 7.8 The UPDATE Statement
    update_student(cursor, 'Charlie', 'Charles', 20)
    conn.commit()

    # 7.9 The DELETE Statement - remove duplicates
    # delete from enrollments
    cursor.execute("""
            DELETE FROM Enrollments
            WHERE student_id NOT IN (
                SELECT MIN(student_id)
                FROM Students
                GROUP BY name, age, major
            );
        """)
    # delete duplicates
    cursor.execute("""
            DELETE FROM Students
            WHERE student_id NOT IN (
                SELECT MIN(student_id)
                FROM Students
                GROUP BY name, age, major
            );
        """)
    print("Duplicates removed successfully.")
    conn.commit()

    print("\nStudents and their enrolled courses (duplicated removed):")
    cursor.execute("SELECT * FROM Students")
    results = cursor.fetchall()
    for row in results:
        print(row)