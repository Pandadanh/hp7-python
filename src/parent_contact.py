import tkinter as tk
from tkinter import messagebox, ttk
from src.database import get_conn
import sqlite3
from datetime import datetime

def open_parent_contact(parent):
    header = tk.Frame(parent, bg="#3498db", height=60)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="LIÊN HỆ PHỤ HUYNH", font=("Arial", 18, "bold"), 
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
        cursor.execute("""
            SELECT pc.id, s.full_name, pc.contact_date, pc.contact_type, 
                   pc.content, t.full_name, pc.notes
            FROM parent_contacts pc
            LEFT JOIN students s ON pc.student_id = s.id
            LEFT JOIN teachers t ON pc.teacher_id = t.id
            ORDER BY pc.contact_date DESC
        """)
        
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def add_contact():
        dialog = tk.Toplevel(parent)
        dialog.title("Thêm liên hệ phụ huynh")
        dialog.geometry("600x500")
        dialog.configure(bg="#ecf0f1")

        tk.Label(dialog, text="Học sinh", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name FROM students ORDER BY full_name")
        students = cursor.fetchall()
        conn.close()

        student_var = tk.StringVar()
        combo_student = ttk.Combobox(dialog, textvariable=student_var, width=40, state="readonly")
        combo_student['values'] = [f"{s[0]}-{s[1]}" for s in students]
        if students:
            combo_student.current(0)
        combo_student.pack(pady=5)

        tk.Label(dialog, text="Ngày liên hệ", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_date = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        entry_date.pack(pady=5)

        tk.Label(dialog, text="Loại liên hệ", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        contact_type_var = tk.StringVar()
        type_frame = tk.Frame(dialog, bg="#ecf0f1")
        type_frame.pack()
        types = ["Điện thoại", "Gặp trực tiếp", "Email", "Khác"]
        for t in types:
            tk.Radiobutton(type_frame, text=t, variable=contact_type_var, value=t, 
                          bg="#ecf0f1").pack(side="left", padx=10)
        contact_type_var.set("Điện thoại")

        tk.Label(dialog, text="Nội dung", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        text_content = tk.Text(dialog, font=("Arial", 12), width=50, height=8)
        text_content.pack(pady=5)

        tk.Label(dialog, text="Giáo viên liên hệ", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name FROM teachers ORDER BY full_name")
        teachers = cursor.fetchall()
        conn.close()

        teacher_var = tk.StringVar()
        combo_teacher = ttk.Combobox(dialog, textvariable=teacher_var, width=40, state="readonly")
        combo_teacher['values'] = ["Không"] + [f"{t[0]}-{t[1]}" for t in teachers]
        combo_teacher.current(0)
        combo_teacher.pack(pady=5)

        tk.Label(dialog, text="Ghi chú", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        text_notes = tk.Text(dialog, font=("Arial", 12), width=50, height=4)
        text_notes.pack(pady=5)

        def save():
            if not combo_student.get():
                messagebox.showwarning("Thiếu", "Vui lòng chọn học sinh")
                return

            student_id = int(combo_student.get().split("-")[0])
            teacher_id = None
            if combo_teacher.get() != "Không":
                teacher_id = int(combo_teacher.get().split("-")[0])

            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO parent_contacts (student_id, contact_date, contact_type, 
                                           content, teacher_id, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (student_id, entry_date.get(), contact_type_var.get(), 
                  text_content.get("1.0", "end-1c"), teacher_id, text_notes.get("1.0", "end-1c")))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Thêm liên hệ thành công")
            dialog.destroy()
            refresh_table()

        tk.Button(dialog, text="Lưu", command=save, bg="#27ae60", fg="white",
                 font=("Arial", 12), width=15).pack(pady=20)

    def edit_contact():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn liên hệ cần sửa")
            return

        item = tree.item(selected[0])
        contact_id = item['values'][0]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM parent_contacts WHERE id=?", (contact_id,))
        contact = cursor.fetchone()
        conn.close()

        dialog = tk.Toplevel(parent)
        dialog.title("Sửa liên hệ phụ huynh")
        dialog.geometry("600x500")
        dialog.configure(bg="#ecf0f1")

        tk.Label(dialog, text="Học sinh", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name FROM students ORDER BY full_name")
        students = cursor.fetchall()
        conn.close()

        student_var = tk.StringVar()
        combo_student = ttk.Combobox(dialog, textvariable=student_var, width=40, state="readonly")
        student_list = [f"{s[0]}-{s[1]}" for s in students]
        combo_student['values'] = student_list
        for i, val in enumerate(student_list):
            if val.startswith(f"{contact[1]}-"):
                combo_student.current(i)
                break

        combo_student.pack(pady=5)

        tk.Label(dialog, text="Ngày liên hệ", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_date = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_date.insert(0, contact[2] or "")
        entry_date.pack(pady=5)

        tk.Label(dialog, text="Loại liên hệ", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        contact_type_var = tk.StringVar(value=contact[3] or "Điện thoại")
        type_frame = tk.Frame(dialog, bg="#ecf0f1")
        type_frame.pack()
        types = ["Điện thoại", "Gặp trực tiếp", "Email", "Khác"]
        for t in types:
            tk.Radiobutton(type_frame, text=t, variable=contact_type_var, value=t, 
                          bg="#ecf0f1").pack(side="left", padx=10)

        tk.Label(dialog, text="Nội dung", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        text_content = tk.Text(dialog, font=("Arial", 12), width=50, height=8)
        text_content.insert("1.0", contact[4] or "")
        text_content.pack(pady=5)

        tk.Label(dialog, text="Giáo viên liên hệ", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name FROM teachers ORDER BY full_name")
        teachers = cursor.fetchall()
        conn.close()

        teacher_var = tk.StringVar()
        combo_teacher = ttk.Combobox(dialog, textvariable=teacher_var, width=40, state="readonly")
        teacher_list = ["Không"] + [f"{t[0]}-{t[1]}" for t in teachers]
        combo_teacher['values'] = teacher_list
        if contact[5]:
            for i, val in enumerate(teacher_list):
                if val.startswith(f"{contact[5]}-"):
                    combo_teacher.current(i)
                    break
        else:
            combo_teacher.current(0)
        combo_teacher.pack(pady=5)

        tk.Label(dialog, text="Ghi chú", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        text_notes = tk.Text(dialog, font=("Arial", 12), width=50, height=4)
        text_notes.insert("1.0", contact[6] or "")
        text_notes.pack(pady=5)

        def save():
            student_id = int(combo_student.get().split("-")[0])
            teacher_id = None
            if combo_teacher.get() != "Không":
                teacher_id = int(combo_teacher.get().split("-")[0])

            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE parent_contacts SET student_id=?, contact_date=?, contact_type=?, 
                                        content=?, teacher_id=?, notes=?
                WHERE id=?
            """, (student_id, entry_date.get(), contact_type_var.get(), 
                  text_content.get("1.0", "end-1c"), teacher_id, 
                  text_notes.get("1.0", "end-1c"), contact_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Sửa liên hệ thành công")
            dialog.destroy()
            refresh_table()

        tk.Button(dialog, text="Lưu", command=save, bg="#3498db", fg="white",
                 font=("Arial", 12), width=15).pack(pady=20)

    def delete_contact():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn liên hệ cần xóa")
            return

        if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa liên hệ này?"):
            return

        item = tree.item(selected[0])
        contact_id = item['values'][0]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM parent_contacts WHERE id=?", (contact_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thành công", "Xóa liên hệ thành công")
        refresh_table()

    tk.Button(btn_frame, text="➕ Thêm", command=add_contact, bg="#27ae60", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="✏️ Sửa", command=edit_contact, bg="#3498db", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🗑️ Xóa", command=delete_contact, bg="#e74c3c", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🔄 Làm mới", command=refresh_table, bg="#95a5a6", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)

    tree_frame = tk.Frame(main_frame, bg="white")
    tree_frame.pack(fill="both", expand=True, pady=10)

    columns = ("ID", "Học sinh", "Ngày", "Loại", "Nội dung", "Giáo viên", "Ghi chú")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    refresh_table()

