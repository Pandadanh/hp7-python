import tkinter as tk
from tkinter import messagebox, ttk
from src.database import get_conn

def open_dashboard(username, on_logout):
    win = tk.Toplevel()
    win.title("Trang chủ - Hệ thống Quản lý Trường học")
    win.geometry("1200x700")
    win.configure(bg="#ecf0f1")

    # Sidebar
    sidebar = tk.Frame(win, width=250, bg="#2c3e50")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Header sidebar
    tk.Label(sidebar, text="MENU", font=("Arial", 18, "bold"), 
             bg="#2c3e50", fg="white").pack(pady=20)

    # Content area
    content = tk.Frame(win, bg="white")
    content.pack(side="right", fill="both", expand=True)

    # Header content
    header_frame = tk.Frame(content, bg="#3498db", height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text=f"Xin chào, {username}", 
             font=("Arial", 20, "bold"), bg="#3498db", fg="white").pack(pady=25)

    # Main content frame
    main_content = tk.Frame(content, bg="white")
    main_content.pack(fill="both", expand=True, padx=20, pady=20)

    def clear_content():
        for widget in main_content.winfo_children():
            widget.destroy()

    # Button style
    btn_style = {
        "font": ("Arial", 12),
        "fg": "white",
        "bg": "#34495e",
        "activebackground": "#1abc9c",
        "width": 25,
        "bd": 0,
        "pady": 12,
        "anchor": "w",
        "relief": "flat"
    }

    # Import các module
    from src.classroom_management import open_classroom_management
    from src.teacher_management import open_teacher_management
    from src.student_management import open_student_management
    from src.parent_contact import open_parent_contact

    # Menu buttons
    def show_home():
        clear_content()
        tk.Label(main_content, text="TRANG CHỦ", font=("Arial", 24, "bold"), 
                 bg="white", fg="#2c3e50").pack(pady=20)
        
        # Thống kê
        stats_frame = tk.Frame(main_content, bg="white")
        stats_frame.pack(pady=20)
        
        conn = get_conn()
        cursor = conn.cursor()
        
        # Đếm số lượng
        cursor.execute("SELECT COUNT(*) FROM teachers")
        teacher_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM classes")
        class_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM parent_contacts")
        contact_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Hiển thị thống kê
        stats = [
            ("Giáo viên", teacher_count, "#3498db"),
            ("Học sinh", student_count, "#2ecc71"),
            ("Lớp học", class_count, "#e74c3c"),
            ("Liên hệ", contact_count, "#f39c12")
        ]
        
        for i, (label, count, color) in enumerate(stats):
            frame = tk.Frame(stats_frame, bg=color, width=200, height=150)
            frame.grid(row=i//2, column=i%2, padx=15, pady=15)
            frame.pack_propagate(False)
            
            tk.Label(frame, text=str(count), font=("Arial", 36, "bold"), 
                    bg=color, fg="white").pack(pady=20)
            tk.Label(frame, text=label, font=("Arial", 16), 
                    bg=color, fg="white").pack()

    def open_classroom():
        clear_content()
        open_classroom_management(main_content)

    def open_teacher():
        clear_content()
        open_teacher_management(main_content)

    def open_student():
        clear_content()
        open_student_management(main_content)

    def open_contact():
        clear_content()
        open_parent_contact(main_content)

    # Sidebar buttons
    tk.Button(sidebar, text="🏠 Trang chủ", command=show_home, **btn_style).pack(pady=5, padx=10)
    tk.Button(sidebar, text="📚 Quản lý lớp học", command=open_classroom, **btn_style).pack(pady=5, padx=10)
    tk.Button(sidebar, text="👨‍🏫 Danh sách giáo viên", command=open_teacher, **btn_style).pack(pady=5, padx=10)
    tk.Button(sidebar, text="👨‍🎓 Quản lý học sinh", command=open_student, **btn_style).pack(pady=5, padx=10)
    tk.Button(sidebar, text="📞 Liên hệ phụ huynh", command=open_contact, **btn_style).pack(pady=5, padx=10)
    
    tk.Button(sidebar, text="🚪 Đăng xuất",
              command=lambda: (win.destroy(), on_logout()),
              font=("Arial", 12, "bold"),
              fg="white", bg="#e74c3c", activebackground="#c0392b",
              width=25, bd=0, pady=12).pack(side="bottom", pady=20, padx=10)

    show_home()

