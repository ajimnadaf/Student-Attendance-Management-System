# file_handler.py

import sqlite3
import csv

DATABASE = "attendance.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def export_attendance():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT students.roll_no,
           students.name,
           attendance.date,
           attendance.status
    FROM attendance
    JOIN students
    ON attendance.student_id = students.student_id
    ORDER BY attendance.date
    """)

    records = cursor.fetchall()

    if len(records) == 0:
        print("\nNo Attendance Data Found.")
        conn.close()
        return

    with open("attendance.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Roll No",
            "Name",
            "Date",
            "Status"
        ])

        writer.writerows(records)

    conn.close()

    print("\n✅ Attendance exported successfully.")
    print("File Name : attendance.csv")


def read_csv():

    try:

        with open("attendance.csv", "r") as file:

            reader = csv.reader(file)

            print("\n========== ATTENDANCE CSV ==========\n")

            for row in reader:
                print("\t".join(row))

    except FileNotFoundError:

        print("\nCSV file not found.")


def file_menu():

    while True:

        print("\n========== FILE MENU ==========")
        print("1. Export Attendance to CSV")
        print("2. View CSV File")
        print("3. Back")

        choice = input("Enter Choice : ")

        if choice == "1":
            export_attendance()

        elif choice == "2":
            read_csv()

        elif choice == "3":
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    file_menu()