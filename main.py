# main.py

from database import create_tables
from login import admin_login
from student import student_menu
from attendance import attendance_menu
from report import report_menu
from file_handler import file_menu


def main():

    # Database Create
    create_tables()

    print("=" * 50)
    print(" STUDENT ATTENDANCE MANAGEMENT SYSTEM ")
    print("=" * 50)

    # Login
    if not admin_login():
        return

    while True:

        print("\n========== MAIN MENU ==========")
        print("1. Student Management")
        print("2. Attendance Management")
        print("3. Reports")
        print("4. File Handling")
        print("5. Exit")

        choice = input("Enter Choice : ")

        if choice == "1":
            student_menu()

        elif choice == "2":
            attendance_menu()

        elif choice == "3":
            report_menu()

        elif choice == "4":
            file_menu()

        elif choice == "5":
            print("\nThank You...")
            break

        else:
            print("\nInvalid Choice.")


if __name__ == "__main__":
    main()