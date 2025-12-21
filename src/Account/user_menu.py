import sqlite3
import os

# ---------- DATABASE ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.abspath(os.path.join(BASE_DIR, "../../Database/users.db"))

def get_conn():
    return sqlite3.connect(DB_NAME)

# ---------- USER MENU ----------
def open_user_menu(username):
    while True:
        print(f"\n=== USER MENU ({username}) ===")
        print("1. Xem thong tin")
        print("2. Doi mat khau")
        print("3. Tu khoa tai khoan")
        print("0. Dang xuat")

        choice = input("Chon: ")

        if choice == "1":
            view_info(username)
        elif choice == "2":
            change_password(username)
        elif choice == "3":
            lock_my_account(username)
            break
        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le")

# ---------- READ ----------
def view_info(username):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, locked FROM users
        WHERE username=?
    """, (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        print("Khong tim thay tai khoan")
        return

    status = "LOCKED" if user[1] == 1 else "ACTIVE"
    print("\n--- Thong tin tai khoan ---")
    print("Username:", user[0])
    print("Trang thai:", status)

# ---------- UPDATE PASSWORD ----------
def change_password(username):
    old_pw = input("Mat khau cu: ")
    new_pw = input("Mat khau moi: ")

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM users
        WHERE username=? AND password=?
    """, (username, old_pw))

    if cursor.fetchone() is None:
        print("❌ Mat khau cu sai")
        conn.close()
        return

    cursor.execute("""
        UPDATE users
        SET password=?
        WHERE username=?
    """, (new_pw, username))

    conn.commit()
    conn.close()
    print("✔ Doi mat khau thanh cong")

# ---------- LOCK SELF ----------
def lock_my_account(username):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET locked=1
        WHERE username=?
    """, (username,))
    conn.commit()
    conn.close()
    print("🔒 Tai khoan da bi khoa. Dang xuat...")
