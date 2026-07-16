# report.py

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "attendance.db")

def get_connection():
    return sqlite3.connect(DATABASE)

# ---------------- DAILY REPORT ----------------
def daily_report():

    conn = get_connection()
    cursor = conn.cursor()

    report_date = input("Enter Date (YYYY-MM-DD): ")

    cursor.execute("""
    SELECT students.roll_no,
           students.name,
           attendance.status
    FROM attendance
    JOIN students
    ON attendance.student_id = students.student_id
    WHERE attendance.date = ?
    ORDER BY students.roll_no
    """, (report_date,))

    records = cursor.fetchall()

    print("\n========== DAILY ATTENDANCE REPORT ==========")

    if not records:
        print("No Record Found.")
    else:
        for row in records:
            print("--------------------------------------")
            print("Roll No :", row[0])
            print("Name    :", row[1])
            print("Status  :", row[2])

    conn.close()


# ---------------- STUDENT REPORT ----------------
def student_report():

    conn = get_connection()
    cursor = conn.cursor()

    roll = input("Enter Roll Number : ")

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
    SELECT date,status
    FROM attendance
    WHERE student_id=?
    ORDER BY date
    """, (student_id,))

    records = cursor.fetchall()

    print("\n========== STUDENT REPORT ==========")
    print("Student :", student[1])

    if not records:
        print("No Attendance Found.")
    else:
        for row in records:
            print("--------------------------------")
            print("Date   :", row[0])
            print("Status :", row[1])

    conn.close()


# ---------------- OVERALL REPORT ----------------
def overall_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
    students.roll_no,
    students.name,
    COUNT(attendance.attendance_id),
    SUM(CASE WHEN attendance.status='Present' THEN 1 ELSE 0 END)
    FROM students
    LEFT JOIN attendance
    ON students.student_id = attendance.student_id
    GROUP BY students.student_id
    ORDER BY students.roll_no
    """)

    records = cursor.fetchall()

    print("\n========== OVERALL REPORT ==========")

    for row in records:

        total = row[2]
        present = row[3] if row[3] else 0

        if total == 0:
            percentage = 0
        else:
            percentage = (present / total) * 100

        print("-------------------------------------------")
        print("Roll No    :", row[0])
        print("Name       :", row[1])
        print("Total      :", total)
        print("Present    :", present)
        print("Percentage : {:.2f}%".format(percentage))

    conn.close()


# ---------------- MENU ----------------
def report_menu():

    while True:

        print("\n========== REPORT MENU ==========")
        print("1. Daily Report")
        print("2. Student Report")
        print("3. Overall Report")
        print("4. Back")

        choice = input("Enter Choice : ")

        if choice == "1":
            daily_report()

        elif choice == "2":
            student_report()

        elif choice == "3":
            overall_report()

        elif choice == "4":
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    report_menu()