import tkinter as tk
from tkinter import messagebox, ttk
from src.database import get_conn
import sqlite3

def open_teacher_management(parent):
    header = tk.Frame(parent, bg="#3498db", height=60)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="DANH SÁCH GIÁO VIÊN", font=("Arial", 18, "bold"), 
             bg="#3498db", fg="white").pack(pady=15)

    main_frame = tk.Frame(parent, bg="white")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    btn_frame = tk.Frame(main_frame, bg="white")
    btn_frame.pack(fill="x", pady=10)

    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)
        
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers ORDER BY teacher_code")
        
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def add_teacher():
        dialog = tk.Toplevel(parent)
        dialog.title("Thêm giáo viên")
        dialog.geometry("500x450")
        dialog.configure(bg="#ecf0f1")

        tk.Label(dialog, text="Mã giáo viên", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_code = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_code.pack(pady=5)

        tk.Label(dialog, text="Họ và tên", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_name = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_name.pack(pady=5)

        tk.Label(dialog, text="Email", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_email = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_email.pack(pady=5)

        tk.Label(dialog, text="Số điện thoại", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_phone = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_phone.pack(pady=5)

        tk.Label(dialog, text="Môn học", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_subject = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_subject.pack(pady=5)

        def save():
            if not entry_code.get() or not entry_name.get():
                messagebox.showwarning("Thiếu", "Vui lòng nhập mã và tên giáo viên")
                return

            conn = get_conn()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO teachers (teacher_code, full_name, email, phone, subject)
                    VALUES (?, ?, ?, ?, ?)
                """, (entry_code.get(), entry_name.get(), entry_email.get(), 
                      entry_phone.get(), entry_subject.get()))
                conn.commit()
                messagebox.showinfo("Thành công", "Thêm giáo viên thành công")
                dialog.destroy()
                refresh_table()
            except sqlite3.IntegrityError:
                messagebox.showerror("Lỗi", "Mã giáo viên đã tồn tại")
            finally:
                conn.close()

        tk.Button(dialog, text="Lưu", command=save, bg="#27ae60", fg="white",
                 font=("Arial", 12), width=15).pack(pady=20)

    def edit_teacher():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn giáo viên cần sửa")
            return

        item = tree.item(selected[0])
        teacher_id = item['values'][0]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE id=?", (teacher_id,))
        teacher = cursor.fetchone()
        conn.close()

        dialog = tk.Toplevel(parent)
        dialog.title("Sửa giáo viên")
        dialog.geometry("500x450")
        dialog.configure(bg="#ecf0f1")

        tk.Label(dialog, text="Mã giáo viên", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_code = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_code.insert(0, teacher[1])
        entry_code.pack(pady=5)

        tk.Label(dialog, text="Họ và tên", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_name = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_name.insert(0, teacher[2])
        entry_name.pack(pady=5)

        tk.Label(dialog, text="Email", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_email = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_email.insert(0, teacher[3] or "")
        entry_email.pack(pady=5)

        tk.Label(dialog, text="Số điện thoại", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_phone = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_phone.insert(0, teacher[4] or "")
        entry_phone.pack(pady=5)

        tk.Label(dialog, text="Môn học", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_subject = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_subject.insert(0, teacher[5] or "")
        entry_subject.pack(pady=5)

        def save():
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teachers SET teacher_code=?, full_name=?, email=?, phone=?, subject=?
                WHERE id=?
            """, (entry_code.get(), entry_name.get(), entry_email.get(), 
                  entry_phone.get(), entry_subject.get(), teacher_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Sửa giáo viên thành công")
            dialog.destroy()
            refresh_table()

        tk.Button(dialog, text="Lưu", command=save, bg="#3498db", fg="white",
                 font=("Arial", 12), width=15).pack(pady=20)

    def delete_teacher():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn giáo viên cần xóa")
            return

        if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa giáo viên này?"):
            return

        item = tree.item(selected[0])
        teacher_id = item['values'][0]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers WHERE id=?", (teacher_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thành công", "Xóa giáo viên thành công")
        refresh_table()

    tk.Button(btn_frame, text="➕ Thêm", command=add_teacher, bg="#27ae60", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="✏️ Sửa", command=edit_teacher, bg="#3498db", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🗑️ Xóa", command=delete_teacher, bg="#e74c3c", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🔄 Làm mới", command=refresh_table, bg="#95a5a6", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)

    tree_frame = tk.Frame(main_frame, bg="white")
    tree_frame.pack(fill="both", expand=True, pady=10)

    columns = ("ID", "Mã GV", "Họ tên", "Email", "SĐT", "Môn học", "Ngày tạo")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    refresh_table()

