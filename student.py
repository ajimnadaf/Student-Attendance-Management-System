# student.py

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "attendance.db")

def get_connection():
    return sqlite3.connect(DATABASE)


# ---------------- ADD STUDENT ----------------
def add_student():
    conn = get_connection()
    cursor = conn.cursor()

    roll_no = input("Enter Roll No: ")
    name = input("Enter Name: ")
    class_name = input("Enter Class: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")

    try:
        cursor.execute("""
        INSERT INTO students(roll_no, name, class_name, email, phone)
        VALUES (?, ?, ?, ?, ?)
        """, (roll_no, name, class_name, email, phone))

        conn.commit()
        print("\n✅ Student Added Successfully.")

    except sqlite3.IntegrityError:
        print("\n❌ Roll Number already exists.")

    conn.close()


# ---------------- VIEW STUDENTS ----------------
def view_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    print("\n========== STUDENT LIST ==========")

    if len(students) == 0:
        print("No Students Found.")
    else:
        for student in students:
            print("---------------------------------------")
            print(f"ID      : {student[0]}")
            print(f"Roll No : {student[1]}")
            print(f"Name    : {student[2]}")
            print(f"Class   : {student[3]}")
            print(f"Email   : {student[4]}")
            print(f"Phone   : {student[5]}")

    conn.close()


# ---------------- UPDATE STUDENT ----------------
def update_student():
    conn = get_connection()
    cursor = conn.cursor()

    student_id = input("Enter Student ID to Update: ")

    cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    student = cursor.fetchone()

    if student is None:
        print("\n❌ Student Not Found.")
        conn.close()
        return

    name = input("Enter New Name: ")
    class_name = input("Enter New Class: ")
    email = input("Enter New Email: ")
    phone = input("Enter New Phone: ")

    cursor.execute("""
    UPDATE students
    SET name=?, class_name=?, email=?, phone=?
    WHERE student_id=?
    """, (name, class_name, email, phone, student_id))

    conn.commit()
    conn.close()

    print("\n✅ Student Updated Successfully.")


# ---------------- DELETE STUDENT ----------------
def delete_student():
    conn = get_connection()
    cursor = conn.cursor()

    student_id = input("Enter Student ID to Delete: ")

    cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    student = cursor.fetchone()

    if student is None:
        print("\n❌ Student Not Found.")
        conn.close()
        return

    cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))

    conn.commit()
    conn.close()

    print("\n✅ Student Deleted Successfully.")


# ---------------- MENU ----------------
def student_menu():

    while True:

        print("\n========== STUDENT MENU ==========")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Back")

        choice = input("Enter Choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            update_student()

        elif choice == "4":
            delete_student()

        elif choice == "5":
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    student_menu()