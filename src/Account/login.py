import tkinter as tk
from tkinter import messagebox
from src.Account.Register import open_register
from src.database import get_conn, init_database, DB_NAME

# ---------- CALLBACKS ----------
def on_login_success(username):
    root.withdraw()
    from src.Account.dashboard import open_dashboard
    open_dashboard(username, on_logout)

def on_logout():
    root.deiconify()

# ---------- LOGIN ----------
def login():
    username = entry_user.get()
    password = entry_pass.get()

    if not username or not password:
        messagebox.showwarning("Thiếu", "Vui lòng nhập đầy đủ thông tin")
        return

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT locked, role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()

    if not result:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")
        return

    if result[0] == 1:
        messagebox.showerror("Bị khóa", "Tài khoản đã bị khóa")
        return

    messagebox.showinfo("OK", "Đăng nhập thành công")
    on_login_success(username)

# ---------- UI ----------
def main():
    init_database()
    
    global root, entry_user, entry_pass
    
    root = tk.Tk()
    root.title("Hệ thống Quản lý Trường học")
    root.geometry("850x600")
    root.configure(bg="#ecf0f1")

    frame = tk.Frame(root, bg="#ecf0f1")
    frame.pack(expand=True)

    tk.Label(frame, text="ĐĂNG NHẬP", font=("Arial", 28, "bold"), 
             bg="#ecf0f1", fg="#2c3e50").pack(pady=40)

    tk.Label(frame, text="Username", font=("Arial", 14), 
             bg="#ecf0f1", fg="#34495e").pack()
    entry_user = tk.Entry(frame, font=("Arial", 14), width=30)
    entry_user.pack(ipady=8, pady=10)

    tk.Label(frame, text="Password", font=("Arial", 14), 
             bg="#ecf0f1", fg="#34495e").pack()
    entry_pass = tk.Entry(frame, show="*", font=("Arial", 14), width=30)
    entry_pass.pack(ipady=8, pady=10)

    tk.Button(frame, text="Đăng nhập", font=("Arial", 14, "bold"),
              width=20, height=2, command=login,
              bg="#3498db", fg="white", activebackground="#2980b9").pack(pady=20)

    tk.Button(
        frame,
        text="Đăng ký",
        font=("Arial", 12),
        width=15,
        command=lambda: (
            root.withdraw(),
            open_register(root, DB_NAME, on_login_success)
        ),
        bg="#95a5a6", fg="white", activebackground="#7f8c8d"
    ).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
