def account_menu():
    while True:
        print("\n=== QUAN LY TAI KHOAN ===")
        print("1. Tao tai khoan")
        print("2. Doi mat khau")
        print("3. Khoa/Mo khoa tai khoan")
        print("0. Quay lai")

        choice = input("Chon: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            change_password()
        elif choice == "3":
            lock_unlock_account()
        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le!")

def create_account():
    print("==[ Tao tai khoan ]==")
    # để phần dữ liệu cho người khác

def change_password():
    print("==[ Doi mat khau ]==")

def lock_unlock_account():
    print("==[ Khoa / Mo khoa ]==")
