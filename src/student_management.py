import tkinter as tk
from tkinter import messagebox, ttk
from src.database import get_conn
import sqlite3

def open_student_management(parent):
    header = tk.Frame(parent, bg="#3498db", height=60)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="QUẢN LÝ HỌC SINH", font=("Arial", 18, "bold"), 
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
        cursor.execute("SELECT * FROM students ORDER BY student_code")
        
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def add_student():
        dialog = tk.Toplevel(parent)
        dialog.title("Thêm học sinh")
        dialog.geometry("500x550")
        dialog.configure(bg="#ecf0f1")

        tk.Label(dialog, text="Mã học sinh", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_code = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_code.pack(pady=5)

        tk.Label(dialog, text="Họ và tên", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_name = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_name.pack(pady=5)

        tk.Label(dialog, text="Ngày sinh (YYYY-MM-DD)", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_dob = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_dob.pack(pady=5)

        tk.Label(dialog, text="Giới tính", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        gender_var = tk.StringVar(value="Nam")
        gender_frame = tk.Frame(dialog, bg="#ecf0f1")
        gender_frame.pack()
        tk.Radiobutton(gender_frame, text="Nam", variable=gender_var, value="Nam", 
                      bg="#ecf0f1").pack(side="left", padx=10)
        tk.Radiobutton(gender_frame, text="Nữ", variable=gender_var, value="Nữ", 
                      bg="#ecf0f1").pack(side="left", padx=10)

        tk.Label(dialog, text="Địa chỉ", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_address = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_address.pack(pady=5)

        tk.Label(dialog, text="Số điện thoại", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_phone = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_phone.pack(pady=5)

        tk.Label(dialog, text="Email", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_email = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_email.pack(pady=5)

        tk.Label(dialog, text="Tên phụ huynh", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_parent = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_parent.pack(pady=5)

        tk.Label(dialog, text="SĐT phụ huynh", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_parent_phone = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_parent_phone.pack(pady=5)

        def save():
            if not entry_code.get() or not entry_name.get():
                messagebox.showwarning("Thiếu", "Vui lòng nhập mã và tên học sinh")
                return

            conn = get_conn()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO students (student_code, full_name, date_of_birth, gender, 
                                        address, phone, email, parent_name, parent_phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (entry_code.get(), entry_name.get(), entry_dob.get() or None, 
                      gender_var.get(), entry_address.get(), entry_phone.get(), 
                      entry_email.get(), entry_parent.get(), entry_parent_phone.get()))
                conn.commit()
                messagebox.showinfo("Thành công", "Thêm học sinh thành công")
                dialog.destroy()
                refresh_table()
            except sqlite3.IntegrityError:
                messagebox.showerror("Lỗi", "Mã học sinh đã tồn tại")
            finally:
                conn.close()

        tk.Button(dialog, text="Lưu", command=save, bg="#27ae60", fg="white",
                 font=("Arial", 12), width=15).pack(pady=20)

    def edit_student():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn học sinh cần sửa")
            return

        item = tree.item(selected[0])
        student_id = item['values'][0]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
        student = cursor.fetchone()
        conn.close()

        dialog = tk.Toplevel(parent)
        dialog.title("Sửa học sinh")
        dialog.geometry("500x550")
        dialog.configure(bg="#ecf0f1")

        tk.Label(dialog, text="Mã học sinh", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_code = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_code.insert(0, student[1])
        entry_code.pack(pady=5)

        tk.Label(dialog, text="Họ và tên", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_name = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_name.insert(0, student[2])
        entry_name.pack(pady=5)

        tk.Label(dialog, text="Ngày sinh (YYYY-MM-DD)", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_dob = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_dob.insert(0, student[3] or "")
        entry_dob.pack(pady=5)

        tk.Label(dialog, text="Giới tính", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        gender_var = tk.StringVar(value=student[4] or "Nam")
        gender_frame = tk.Frame(dialog, bg="#ecf0f1")
        gender_frame.pack()
        tk.Radiobutton(gender_frame, text="Nam", variable=gender_var, value="Nam", 
                      bg="#ecf0f1").pack(side="left", padx=10)
        tk.Radiobutton(gender_frame, text="Nữ", variable=gender_var, value="Nữ", 
                      bg="#ecf0f1").pack(side="left", padx=10)

        tk.Label(dialog, text="Địa chỉ", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_address = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_address.insert(0, student[5] or "")
        entry_address.pack(pady=5)

        tk.Label(dialog, text="Số điện thoại", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_phone = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_phone.insert(0, student[6] or "")
        entry_phone.pack(pady=5)

        tk.Label(dialog, text="Email", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_email = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_email.insert(0, student[7] or "")
        entry_email.pack(pady=5)

        tk.Label(dialog, text="Tên phụ huynh", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_parent = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_parent.insert(0, student[8] or "")
        entry_parent.pack(pady=5)

        tk.Label(dialog, text="SĐT phụ huynh", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_parent_phone = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_parent_phone.insert(0, student[9] or "")
        entry_parent_phone.pack(pady=5)

        def save():
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students SET student_code=?, full_name=?, date_of_birth=?, gender=?, 
                                address=?, phone=?, email=?, parent_name=?, parent_phone=?
                WHERE id=?
            """, (entry_code.get(), entry_name.get(), entry_dob.get() or None, 
                  gender_var.get(), entry_address.get(), entry_phone.get(), 
                  entry_email.get(), entry_parent.get(), entry_parent_phone.get(), student_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Sửa học sinh thành công")
            dialog.destroy()
            refresh_table()

        tk.Button(dialog, text="Lưu", command=save, bg="#3498db", fg="white",
                 font=("Arial", 12), width=15).pack(pady=20)

    def delete_student():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn học sinh cần xóa")
            return

        if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa học sinh này?"):
            return

        item = tree.item(selected[0])
        student_id = item['values'][0]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thành công", "Xóa học sinh thành công")
        refresh_table()

    tk.Button(btn_frame, text="➕ Thêm", command=add_student, bg="#27ae60", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="✏️ Sửa", command=edit_student, bg="#3498db", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🗑️ Xóa", command=delete_student, bg="#e74c3c", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🔄 Làm mới", command=refresh_table, bg="#95a5a6", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)

    tree_frame = tk.Frame(main_frame, bg="white")
    tree_frame.pack(fill="both", expand=True, pady=10)

    columns = ("ID", "Mã HS", "Họ tên", "Ngày sinh", "Giới tính", "Địa chỉ", "SĐT", "Email", "PH", "SĐT PH")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    refresh_table()

