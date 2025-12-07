def student_menu():
    while True:
        print("\n=== QUAN LY HOC SINH ===")
        print("1. Them hoc sinh")
        print("2. Sua thong tin hoc sinh")
        print("3. Xoa hoc sinh")
        print("4. Tim kiem hoc sinh")
        print("0. Quay lai")

        choice = input("Chon: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            edit_student()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            search_student()
        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le!")

def add_student():
    print("==[ Them hoc sinh ]==")

def edit_student():
    print("==[ Sua hoc sinh ]==")

def delete_student():
    print("==[ Xoa hoc sinh ]==")

def search_student():
    print("==[ Tim kiem hoc sinh ]==")
