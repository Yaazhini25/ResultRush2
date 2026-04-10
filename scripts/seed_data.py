import sqlite3
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "results.db")

names = [
    "Arjun Kumar", "Priya Sharma", "Rahul Verma",
    "Sneha Patel", "Vikram Singh"
]

subjects = [
    "Mathematics", "Data Structures", "Operating Systems",
    "Database Management", "Computer Networks"
]

grades = ["O", "A+", "A", "B+", "B"]


def seed_data():
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Ensure tables exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            reg_no TEXT PRIMARY KEY,
            dob TEXT,
            name TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            reg_no TEXT,
            semester INTEGER,
            subject TEXT,
            grade TEXT,
            marks INTEGER,
            PRIMARY KEY (reg_no, semester, subject)
        )
    """)

    c.execute("DELETE FROM students")
    c.execute("DELETE FROM results")

    for i in range(5000):
        reg_no = str(20211000 + i)
        dob = "2003-05-15"
        name = random.choice(names)

        c.execute(
            "INSERT INTO students (reg_no, dob, name) VALUES (?, ?, ?)",
            (reg_no, dob, name)
        )

        for subject in subjects:
            grade = random.choice(grades)
            marks = random.randint(70, 99)

            c.execute("""
                INSERT INTO results
                (reg_no, semester, subject, grade, marks)
                VALUES (?, 4, ?, ?, ?)
            """, (reg_no, subject, grade, marks))

    conn.commit()
    conn.close()
    print("✅ Seeded 5000 students successfully")


if __name__ == "__main__":
    seed_data()