import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from . import register
from .  import user_screen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.abspath(os.path.join(BASE_DIR, "../../Database/users.db"))

# ---------- DATABASE ----------
def init_db():
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            locked INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# ---------- LOGIN ----------
def login():
    user = entry_user.get()
    pw = entry_pass.get()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT locked FROM users WHERE username=? AND password=?",
        (user, pw)
    )
    result = cursor.fetchone()
    conn.close()

    if not result:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")
        return

    if result[0] == 1:
        messagebox.showerror("Bị khóa", "Tài khoản đã bị khóa")
        return

    login_success(user)

def login_success(username):
    root.withdraw()
    user_screen.open_user_screen(username, root, DB_NAME)

def open_register():
    root.withdraw()
    register.open_register(root, DB_NAME, login_success)

# ---------- UI ----------
init_db()

root = tk.Tk()
root.title("Login")
root.geometry("850x600")

frame = tk.Frame(root)
frame.pack(expand=True)

tk.Label(frame, text="USER LOGIN", font=("Arial", 26, "bold")).pack(pady=30)

tk.Label(frame, text="Username", font=("Arial", 14)).pack()
entry_user = tk.Entry(frame, font=("Arial", 14), width=30)
entry_user.pack(ipady=8, pady=10)

tk.Label(frame, text="Password", font=("Arial", 14)).pack()
entry_pass = tk.Entry(frame, show="*", font=("Arial", 14), width=30)
entry_pass.pack(ipady=8, pady=10)

tk.Button(frame, text="Login", font=("Arial", 14, "bold"),
          width=20, height=2, command=login).pack(pady=20)

tk.Button(frame, text="Register", font=("Arial", 12),
          width=15, command=open_register).pack()

root.mainloop()
def main():
    root.mainloop()

if __name__ == "__main__":
    main()
