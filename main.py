from src.Account.login import login
from src.Account.mainAccount import account_menu
from src.Student.mainStudent import student_menu

def main():
    user = login()

    while True:
        print("\n===== MENU CHINH =====")
        print("1. Quan ly tai khoan")
        print("2. Quan ly hoc sinh")
        print("0. Thoat")

        chon = input("Chon: ")

        if chon == "1":
            if user["role"] == "admin":
                account_menu()
            else:
                print("Ban khong co quyen truy cap!")
        elif chon == "2":
            student_menu()
        elif chon == "0":
            print("Tam biet!")
            break
        else:
            print("Lua chon khong hop le!")

if __name__ == "__main__":
    main()
