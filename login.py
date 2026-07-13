# login.py

def admin_login():
    print("\n========== ADMIN LOGIN ==========")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if username == "admin" and password == "admin123":
        print("\n✅ Login Successful!\n")
        return True
    else:
        print("\n❌ Invalid Username or Password!\n")
        return False
        