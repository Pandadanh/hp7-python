import tkinter as tk
from . import register

def open_user_screen(username, parent, db_path):
    win = tk.Toplevel(parent)
    win.title("User Screen")
    win.geometry("850x600")

    frame = tk.Frame(win)
    frame.pack(expand=True)

    tk.Label(frame,
             text=f"Xin chào {username}",
             font=("Arial", 22, "bold")).pack(pady=40)

    def open_register_again():
        register.open_register(
            win,
            db_path,
            lambda u: None
        )

    def logout():
        win.destroy()
        parent.deiconify()

    tk.Button(frame, text="➕ Đăng ký tài khoản mới",
              font=("Arial", 14),
              width=30, height=2,
              command=open_register_again).pack(pady=15)

    tk.Button(frame, text="🚪 Đăng xuất",
              font=("Arial", 14),
              width=30, height=2,
              command=logout).pack(pady=15)
