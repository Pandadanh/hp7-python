def login():
    print("===== DANG NHAP HE THONG =====")

    username = input("Nhap username: ")
    password = input("Nhap password: ")

    # Tạm thời trả về dữ liệu giả để test giao diện
    user = {
        "username": username,
        "role": "admin" if username == "admin" else "student"
    }

    return user
