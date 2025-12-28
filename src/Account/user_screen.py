import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# ===== DB CONFIG =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.abspath(os.path.join(BASE_DIR, "../../Database/users.db"))

def get_conn():
    return sqlite3.connect(DB_NAME)

# ===== USER SCREEN =====
def open_user_screen(username, on_logout):
    win = tk.Toplevel()
    win.title("User Dashboard")
    win.geometry("850x600")

    container = tk.Frame(win)
    container.pack(fill="both", expand=True)

    # ----- SIDEBAR -----
    sidebar = tk.Frame(container, width=220, bg="#2c3e50")
    sidebar.pack(side="left", fill="y")

    # ----- CONTENT -----
    content = tk.Frame(container, bg="white")
    content.pack(side="right", fill="both", expand=True)

    header = tk.Label(
        content,
        text=f"Xin chào {username}",
        font=("Arial", 20, "bold"),
        bg="white"
    )
    header.pack(pady=30)

    def clear_content():
        for w in content.winfo_children()[1:]:
            w.destroy()

    # ===== ACTIONS =====
    def show_info():
        clear_content()

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT username, locked FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        conn.close()

        status = "LOCKED" if user[1] else "ACTIVE"

        tk.Label(content, text="Thông tin tài khoản", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        tk.Label(content, text=f"Username: {user[0]}", bg="white", font=("Arial", 14)).pack(pady=5)
        tk.Label(content, text=f"Trạng thái: {status}", bg="white", font=("Arial", 14)).pack(pady=5)

    def lock_account():
        if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn khóa tài khoản?"):
            return

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE users SET locked=1 WHERE username=?", (username,))
        conn.commit()
        conn.close()

        messagebox.showinfo("OK", "Tài khoản đã bị khóa")
        win.destroy()
        on_logout()

    # ===== SIDEBAR BUTTONS =====
    btn = dict(
        font=("Arial", 12),
        fg="white",
        bg="#34495e",
        activebackground="#1abc9c",
        width=20,
        bd=0,
        pady=10
    )

    tk.Button(sidebar, text="👤 Thông tin", command=show_info, **btn).pack(pady=10)
    tk.Button(sidebar, text="🔒 Tự khóa", command=lock_account, **btn).pack(pady=10)
    tk.Button(
        sidebar,
        text="🚪 Đăng xuất",
        command=lambda: (win.destroy(), on_logout()),
        **btn
    ).pack(side="bottom", pady=20)

    show_info()
