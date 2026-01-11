import tkinter as tk
from tkinter import messagebox, ttk
from src.database import get_conn

def open_classroom_management(parent):
    # Header
    header = tk.Frame(parent, bg="#3498db", height=60)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="QUẢN LÝ LỚP HỌC", font=("Arial", 18, "bold"), 
             bg="#3498db", fg="white").pack(pady=15)

    # Main frame
    main_frame = tk.Frame(parent, bg="white")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Buttons frame
    btn_frame = tk.Frame(main_frame, bg="white")
    btn_frame.pack(fill="x", pady=10)

    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)
        
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.class_code, c.class_name, c.grade, c.room, c.school_year,
                   t.full_name
            FROM classes c
            LEFT JOIN teachers t ON c.teacher_id = t.id
            ORDER BY c.class_code
        """)
        
        for row in cursor.fetchall():
            teacher_name = row[6] if row[6] else "Chưa phân công"
            tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], teacher_name))
        conn.close()

    def add_class():
        dialog = tk.Toplevel(parent)
        dialog.title("Thêm lớp học")
        dialog.geometry("500x400")
        dialog.configure(bg="#ecf0f1")

        tk.Label(dialog, text="Mã lớp", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_code = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_code.pack(pady=5)

        tk.Label(dialog, text="Tên lớp", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_name = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_name.pack(pady=5)

        tk.Label(dialog, text="Khối", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_grade = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_grade.pack(pady=5)

        tk.Label(dialog, text="Phòng học", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_room = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_room.pack(pady=5)

        tk.Label(dialog, text="Năm học", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_year = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_year.pack(pady=5)

        tk.Label(dialog, text="Giáo viên chủ nhiệm", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name FROM teachers ORDER BY full_name")
        teachers = cursor.fetchall()
        conn.close()

        teacher_var = tk.StringVar()
        combo_teacher = ttk.Combobox(dialog, textvariable=teacher_var, width=27, state="readonly")
        combo_teacher['values'] = ["Không"] + [f"{t[0]}-{t[1]}" for t in teachers]
        combo_teacher.current(0)
        combo_teacher.pack(pady=5)

        def save():
            if not all([entry_code.get(), entry_name.get()]):
                messagebox.showwarning("Thiếu", "Vui lòng nhập đầy đủ thông tin")
                return

            conn = get_conn()
            cursor = conn.cursor()
            try:
                teacher_id = None
                if combo_teacher.get() != "Không":
                    teacher_id = int(combo_teacher.get().split("-")[0])
                
                cursor.execute("""
                    INSERT INTO classes (class_code, class_name, grade, room, school_year, teacher_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (entry_code.get(), entry_name.get(), entry_grade.get(), 
                      entry_room.get(), entry_year.get(), teacher_id))
                conn.commit()
                messagebox.showinfo("Thành công", "Thêm lớp học thành công")
                dialog.destroy()
                refresh_table()
            except sqlite3.IntegrityError:
                messagebox.showerror("Lỗi", "Mã lớp đã tồn tại")
            finally:
                conn.close()

        tk.Button(dialog, text="Lưu", command=save, bg="#27ae60", fg="white",
                 font=("Arial", 12), width=15).pack(pady=20)

    def edit_class():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn lớp học cần sửa")
            return

        item = tree.item(selected[0])
        class_id = item['values'][0]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
        cls = cursor.fetchone()
        conn.close()

        dialog = tk.Toplevel(parent)
        dialog.title("Sửa lớp học")
        dialog.geometry("500x400")
        dialog.configure(bg="#ecf0f1")

        tk.Label(dialog, text="Mã lớp", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_code = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_code.insert(0, cls[1])
        entry_code.pack(pady=5)

        tk.Label(dialog, text="Tên lớp", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_name = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_name.insert(0, cls[2])
        entry_name.pack(pady=5)

        tk.Label(dialog, text="Khối", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_grade = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_grade.insert(0, cls[3] or "")
        entry_grade.pack(pady=5)

        tk.Label(dialog, text="Phòng học", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_room = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_room.insert(0, cls[4] or "")
        entry_room.pack(pady=5)

        tk.Label(dialog, text="Năm học", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        entry_year = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry_year.insert(0, cls[5] or "")
        entry_year.pack(pady=5)

        tk.Label(dialog, text="Giáo viên chủ nhiệm", font=("Arial", 12), bg="#ecf0f1").pack(pady=5)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name FROM teachers ORDER BY full_name")
        teachers = cursor.fetchall()
        conn.close()

        teacher_var = tk.StringVar()
        combo_teacher = ttk.Combobox(dialog, textvariable=teacher_var, width=27, state="readonly")
        teacher_list = ["Không"] + [f"{t[0]}-{t[1]}" for t in teachers]
        combo_teacher['values'] = teacher_list
        if cls[6]:
            for i, val in enumerate(teacher_list):
                if val.startswith(f"{cls[6]}-"):
                    combo_teacher.current(i)
                    break
        else:
            combo_teacher.current(0)
        combo_teacher.pack(pady=5)

        def save():
            conn = get_conn()
            cursor = conn.cursor()
            teacher_id = None
            if combo_teacher.get() != "Không":
                teacher_id = int(combo_teacher.get().split("-")[0])
            
            cursor.execute("""
                UPDATE classes SET class_code=?, class_name=?, grade=?, room=?, school_year=?, teacher_id=?
                WHERE id=?
            """, (entry_code.get(), entry_name.get(), entry_grade.get(), 
                  entry_room.get(), entry_year.get(), teacher_id, class_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Sửa lớp học thành công")
            dialog.destroy()
            refresh_table()

        tk.Button(dialog, text="Lưu", command=save, bg="#3498db", fg="white",
                 font=("Arial", 12), width=15).pack(pady=20)

    def delete_class():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn lớp học cần xóa")
            return

        if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa lớp học này?"):
            return

        item = tree.item(selected[0])
        class_id = item['values'][0]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM classes WHERE id=?", (class_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thành công", "Xóa lớp học thành công")
        refresh_table()

    # Buttons
    def manage_students():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chọn", "Vui lòng chọn lớp học")
            return
        
        item = tree.item(selected[0])
        class_id = item['values'][0]
        from src.class_students import open_class_students
        open_class_students(parent, class_id)

    tk.Button(btn_frame, text="➕ Thêm", command=add_class, bg="#27ae60", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="✏️ Sửa", command=edit_class, bg="#3498db", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🗑️ Xóa", command=delete_class, bg="#e74c3c", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="👥 Học sinh", command=manage_students, bg="#f39c12", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🔄 Làm mới", command=refresh_table, bg="#95a5a6", fg="white",
             font=("Arial", 12), width=12).pack(side="left", padx=5)

    # Table
    tree_frame = tk.Frame(main_frame, bg="white")
    tree_frame.pack(fill="both", expand=True, pady=10)

    columns = ("ID", "Mã lớp", "Tên lớp", "Khối", "Phòng", "Năm học", "GVCN")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    refresh_table()

