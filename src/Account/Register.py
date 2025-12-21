import tkinter as tk
from tkinter import messagebox
import sqlite3

def open_register(parent, db_path, on_success_login):
    reg = tk.Toplevel(parent)
    reg.title("Register")
    reg.geometry("850x600")

    frame = tk.Frame(reg)
    frame.pack(expand=True)

    tk.Label(frame, text="REGISTER", font=("Arial", 26, "bold")).pack(pady=30)

    tk.Label(frame, text="Username", font=("Arial", 14)).pack()
    entry_user = tk.Entry(frame, font=("Arial", 14), width=30)
    entry_user.pack(ipady=8, pady=10)

    tk.Label(frame, text="Password", font=("Arial", 14)).pack()
    entry_pass = tk.Entry(frame, show="*", font=("Arial", 14), width=30)
    entry_pass.pack(ipady=8, pady=10)

    tk.Label(frame, text="Confirm Password", font=("Arial", 14)).pack()
    entry_confirm = tk.Entry(frame, show="*", font=("Arial", 14), width=30)
    entry_confirm.pack(ipady=8, pady=10)

    def back():
        reg.destroy()
        parent.deiconify()

    def register():
        user = entry_user.get()
        pw = entry_pass.get()
        cf = entry_confirm.get()

        if not user or not pw:
            messagebox.showwarning("Thiếu", "Không được để trống")
            return

        if pw != cf:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp")
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users(username,password,locked) VALUES (?,?,0)",
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

    tk.Button(frame, text="Create Account",
              font=("Arial", 14, "bold"),
              width=20, height=2,
              command=register).pack(pady=25)

    tk.Button(frame, text="Back",
              font=("Arial", 12),
              width=15,
              command=back).pack()
