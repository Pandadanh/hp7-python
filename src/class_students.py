import tkinter as tk
from tkinter import messagebox, ttk
from src.database import get_conn
import sqlite3

def open_class_students(parent, class_id):
    """Quản lý học sinh trong một lớp cụ thể"""
    dialog = tk.Toplevel(parent)
    dialog.title("Quản lý học sinh trong lớp")
    dialog.geometry("900x600")
    dialog.configure(bg="white")

    # Lấy thông tin lớp
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT class_code, class_name FROM classes WHERE id=?", (class_id,))
    class_info = cursor.fetchone()
    conn.close()

    header = tk.Frame(dialog, bg="#3498db", height=60)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text=f"Lớp: {class_info[0]} - {class_info[1]}", 
             font=("Arial", 18, "bold"), bg="#3498db", fg="white").pack(pady=15)

    main_frame = tk.Frame(dialog, bg="white")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    btn_frame = tk.Frame(main_frame, bg="white")
    btn_frame.pack(fill="x", pady=10)

    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)
        
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cs.id, s.student_code, s.full_name, s.date_of_birth, 
                   cs.enrollment_date, cs.status
            FROM class_students cs
            JOIN students s ON cs.student_id = s.id
            WHERE cs.class_id = ?
            ORDER BY s.full_name
        """, (class_id,))
        
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def add_student_to_class():
        # Lấy danh sách học sinh chưa có trong lớp
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.student_code, s.full_name
            FROM students s
            WHERE s.id NOT IN (
                SELECT student_id FROM class_students WHERE class_id = ?
            )
            ORDER BY s.full_name
        """, (class_id,))
        available_students = cursor.fetchall()
        conn.close()

        if not available_students:
            messagebox.showinfo("Thông báo", "Tất cả học sinh đã được thêm vào lớp này")
            return

        select_dialog = tk.Toplevel(dialog)
        select_dialog.title("Thêm học sinh vào lớp")
        select_dialog.geometry("500x400")
        select_dialog.configure(bg="#ecf0f1")

        tk.Label(select_dialog, text="Chọn học sinh", font=("Arial", 14, "bold"), 
                bg="#ecf0f1").pack(pady=10)

        listbox = tk.Listbox(select_dialog, font=("Arial", 12), height=15)
        listbox.pack(fill="both", expand=True, padx=20, pady=10)

        for student in available_students:
            listbox.insert("end", f"{student[1]} - {student[2]}")

        def add_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("Chọn", "Vui lòng chọn học sinh")
                return

            student_id = available_students[selected[0]][0]
            
            conn = get_conn()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO class_students (class_id, student_id, status)
                    VALUES (?, ?, 'active')
                """, (class_id, student_id))
                conn.commit()
                messagebox.showinfo("Thành công", "Thêm học sinh vào lớp thành công")
                select_dialog.destroy()
                refresh_table()
            except sqlite3.IntegrityError:
                messagebox.showerror("Lỗi", "Học sinh đã có trong lớp")
            finally:
                conn.close()

        tk.Button(select_dialog, text="Thêm", command=add_selected,
                 bg="#27ae60", fg="white", font=("Arial", 12), width=15).pack(pady=10)

    def remove_student_from_class():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn học sinh cần xóa")
            return

        if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa học sinh khỏi lớp?"):
            return

        item = tree.item(selected[0])
        cs_id = item['values'][0]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM class_students WHERE id=?", (cs_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thành công", "Xóa học sinh khỏi lớp thành công")
        refresh_table()

    tk.Button(btn_frame, text="➕ Thêm học sinh", command=add_student_to_class, 
             bg="#27ae60", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🗑️ Xóa khỏi lớp", command=remove_student_from_class, 
             bg="#e74c3c", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🔄 Làm mới", command=refresh_table, 
             bg="#95a5a6", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=5)

    tree_frame = tk.Frame(main_frame, bg="white")
    tree_frame.pack(fill="both", expand=True, pady=10)

    columns = ("ID", "Mã HS", "Họ tên", "Ngày sinh", "Ngày nhập học", "Trạng thái")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    refresh_table()

