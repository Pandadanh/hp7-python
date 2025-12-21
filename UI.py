import tkinter as tk
from tkinter import messagebox

# ==========================
# UI HỌC SINH
# ==========================
class StudentUI:
    def __init__(self, master, logout_callback):
        self.window = tk.Toplevel(master)
        self.window.title("Giao diện Học sinh")
        self.window.geometry("300x200")

        tk.Label(self.window, text="Chào mừng Học sinh!",
                 font=("Arial", 16)).pack(pady=20)

        tk.Button(self.window, text="Đăng xuất",
                  bg="red", fg="white",
                  command=self.logout).pack(pady=20)

        self.logout_callback = logout_callback
        master.withdraw()

    def logout(self):
        self.window.destroy()
        self.logout_callback()

# ==========================
# UI GIÁO VIÊN
# ==========================
class TeacherUI:
    def __init__(self, master, logout_callback):
        self.window = tk.Toplevel(master)
        self.window.title("Giao diện Giáo viên")
        self.window.geometry("300x200")

        tk.Label(self.window, text="Chào mừng Giáo viên!",
                 font=("Arial", 16)).pack(pady=20)

        tk.Button(self.window, text="Đăng xuất",
                  bg="red", fg="white",
                  command=self.logout).pack(pady=20)

        self.logout_callback = logout_callback
        master.withdraw()

    def logout(self):
        self.window.destroy()
        self.logout_callback()

# ==========================
# UI ĐĂNG NHẬP
# ==========================
class LoginUI:
    def __init__(self, master):
        self.master = master
        master.title("Đăng nhập")
        master.geometry("300x250")

        tk.Label(master, text="ĐĂNG NHẬP", font=("Arial", 16)).pack(pady=10)

        tk.Label(master, text="Tài khoản:").pack()
        self.entry_user = tk.Entry(master)
        self.entry_user.pack(pady=5)

        tk.Label(master, text="Mật khẩu:").pack()
        self.entry_pass = tk.Entry(master, show="*")
        self.entry_pass.pack(pady=5)

        tk.Button(master, text="Đăng nhập", bg="blue", fg="white",
                  command=self.login).pack(pady=15)

        # Dữ liệu demo
        self.accounts = {
            "hocsinh": {"password": "123", "role": "student"},
            "giaovien": {"password": "456", "role": "teacher"}
        }

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        if username in self.accounts and self.accounts[username]["password"] == password:
            role = self.accounts[username]["role"]

            if role == "student":
                StudentUI(self.master, self.show_login)

            elif role == "teacher":
                TeacherUI(self.master, self.show_login)

        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

    def show_login(self):
        self.master.deiconify()

# ==========================
# CHẠY CHƯƠNG TRÌNH
# ==========================
root = tk.Tk()
app = LoginUI(root)
root.mainloop()
