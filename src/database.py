import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.abspath(os.path.join(BASE_DIR, "Database", "school.db"))

# Export DB_NAME để các module khác có thể dùng
__all__ = ['get_conn', 'init_database', 'DB_NAME']

def get_conn():
    """Kết nối database"""
    return sqlite3.connect(DB_NAME)

def init_database():
    """Khởi tạo tất cả các bảng trong database"""
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    conn = get_conn()
    cursor = conn.cursor()
    
    # Bảng users (tài khoản) - migrate từ users.db nếu cần
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            locked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Migrate dữ liệu từ users.db nếu có
    old_db = os.path.abspath(os.path.join(BASE_DIR, "Database", "users.db"))
    if os.path.exists(old_db):
        try:
            old_conn = sqlite3.connect(old_db)
            old_cursor = old_conn.cursor()
            old_cursor.execute("SELECT username, password, locked FROM users")
            old_users = old_cursor.fetchall()
            old_conn.close()
            
            for user in old_users:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO users (username, password, locked, role)
                        VALUES (?, ?, ?, 'user')
                    """, (user[0], user[1], user[2]))
                except:
                    pass
        except:
            pass
    
    # Bảng teachers (giáo viên)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_code TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            subject TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Bảng students (học sinh)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_code TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            date_of_birth DATE,
            gender TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            parent_name TEXT,
            parent_phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Bảng classes (lớp học)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_code TEXT UNIQUE NOT NULL,
            class_name TEXT NOT NULL,
            grade TEXT,
            teacher_id INTEGER,
            room TEXT,
            school_year TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
    """)
    
    # Bảng class_students (học sinh trong lớp)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS class_students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            enrollment_date DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            UNIQUE(class_id, student_id)
        )
    """)
    
    # Bảng parent_contacts (liên hệ phụ huynh)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parent_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            contact_date DATE DEFAULT CURRENT_DATE,
            contact_type TEXT,
            content TEXT,
            teacher_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
    """)
    
    conn.commit()
    conn.close()

