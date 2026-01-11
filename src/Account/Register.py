import tkinter as tk
from tkinter import messagebox
import sqlite3
import re

def is_valid_gmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email)

def open_register(parent, db_path, on_success_login):
    reg = tk.Toplevel(parent)
    reg.title("Đăng ký")
    reg.geometry("850x600")
    reg.configure(bg="#ecf0f1")

    frame = tk.Frame(reg, bg="#ecf0f1")
    frame.pack(expand=True)

    tk.Label(frame, text="ĐĂNG KÝ", font=("Arial", 26, "bold"), 
             bg="#ecf0f1", fg="#2c3e50").pack(pady=30)

    tk.Label(frame, text="Username (Gmail)", font=("Arial", 14), 
             bg="#ecf0f1", fg="#34495e").pack()
    entry_user = tk.Entry(frame, font=("Arial", 14), width=30)
    entry_user.pack(ipady=8, pady=10)

    tk.Label(frame, text="Password", font=("Arial", 14), 
             bg="#ecf0f1", fg="#34495e").pack()
    entry_pass = tk.Entry(frame, show="*", font=("Arial", 14), width=30)
    entry_pass.pack(ipady=8, pady=10)

    tk.Label(frame, text="Confirm Password", font=("Arial", 14), 
             bg="#ecf0f1", fg="#34495e").pack()
    entry_confirm = tk.Entry(frame, show="*", font=("Arial", 14), width=30)
    entry_confirm.pack(ipady=8, pady=10)

    def back():
        reg.destroy()
        parent.deiconify()

    def register():
        user = entry_user.get().strip()
        pw = entry_pass.get()
        cf = entry_confirm.get()

        if not user or not pw or not cf:
            messagebox.showwarning("Thiếu", "Không được để trống")
            return

        if not is_valid_gmail(user):
            messagebox.showerror(
                "Sai định dạng",
                "Username phải là Gmail (ví dụ: abc@gmail.com)"
            )
            return

        if len(pw) < 6:
            messagebox.showerror(
                "Mật khẩu yếu",
                "Mật khẩu phải có ít nhất 6 ký tự"
            )
            return

        if pw != cf:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp")
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users(username, password, locked, role) VALUES (?,?,0,'user')",
                (user, pw)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Username đã tồn tại")
            conn.close()
            return
        conn.close()

        messagebox.showinfo("OK", "Đăng ký thành công")
        reg.destroy()
        parent.deiconify()
        on_success_login(user)

    tk.Button(frame, text="Tạo tài khoản",
              font=("Arial", 14, "bold"),
              width=20, height=2,
              command=register,
              bg="#27ae60", fg="white", activebackground="#229954").pack(pady=25)

    tk.Button(frame, text="Quay lại",
              font=("Arial", 12),
              width=15,
              command=back,
              bg="#95a5a6", fg="white", activebackground="#7f8c8d").pack()
