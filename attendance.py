# attendance.py

import sqlite3
from datetime import date

DATABASE = "attendance.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# ---------------- MARK ATTENDANCE ----------------
def mark_attendance():
    conn = get_connection()
    cursor = conn.cursor()

    attendance_date = input(f"Enter Date (YYYY-MM-DD) [Default: {date.today()}]: ")

    if attendance_date == "":
        attendance_date = str(date.today())

    cursor.execute("SELECT student_id, roll_no, name FROM students")
    students = cursor.fetchall()

    if len(students) == 0:
        print("\nNo Students Found.")
        conn.close()
        return

    print("\n===== MARK ATTENDANCE =====")

    for student in students:

        print(f"\nRoll No : {student[1]}")
        print(f"Name    : {student[2]}")

        status = input("Present (P) / Absent (A): ").upper()

        if status == "P":
            status = "Present"
        else:
            status = "Absent"

        cursor.execute("""
        INSERT INTO attendance(student_id, date, status)
        VALUES(?,?,?)
        """, (student[0], attendance_date, status))

    conn.commit()
    conn.close()

    print("\nAttendance Saved Successfully.")


# ---------------- VIEW ATTENDANCE ----------------
def view_attendance():

    conn = get_connection()
    cursor = conn.cursor()

    attendance_date = input("Enter Date (YYYY-MM-DD): ")

    cursor.execute("""
    SELECT students.roll_no,
           students.name,
           attendance.date,
           attendance.status
    FROM attendance
    JOIN students
    ON attendance.student_id = students.student_id
    WHERE attendance.date = ?
    """, (attendance_date,))

    records = cursor.fetchall()

    if len(records) == 0:
        print("\nNo Attendance Found.")
    else:

        print("\n========== ATTENDANCE ==========")

        for row in records:
            print("----------------------------------")
            print("Roll No :", row[0])
            print("Name    :", row[1])
            print("Date    :", row[2])
            print("Status  :", row[3])

    conn.close()


# ---------------- ATTENDANCE PERCENTAGE ----------------
def attendance_percentage():

    conn = get_connection()
    cursor = conn.cursor()

    roll = input("Enter Roll Number: ")

    cursor.execute("""
    SELECT student_id,name
    FROM students
    WHERE roll_no=?
    """, (roll,))

    student = cursor.fetchone()

    if student is None:
        print("Student Not Found.")
        conn.close()
        return

    student_id = student[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM attendance
    WHERE student_id=?
    """, (student_id,))

    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM attendance
    WHERE student_id=?
    AND status='Present'
    """, (student_id,))

    present = cursor.fetchone()[0]

    if total == 0:
        percentage = 0
    else:
        percentage = (present / total) * 100

    print("\n========== REPORT ==========")
    print("Student :", student[1])
    print("Total Classes :", total)
    print("Present :", present)
    print("Attendance Percentage : {:.2f}%".format(percentage))

    conn.close()


# ---------------- MENU ----------------
def attendance_menu():

    while True:

        print("\n========== ATTENDANCE MENU ==========")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Attendance Percentage")
        print("4. Back")

        choice = input("Enter Choice : ")

        if choice == "1":
            mark_attendance()

        elif choice == "2":
            view_attendance()

        elif choice == "3":
            attendance_percentage()

        elif choice == "4":
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    attendance_menu()