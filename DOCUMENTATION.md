# Tài liệu Source Code - Hệ thống Quản lý Học sinh

## Tổng quan
Hệ thống quản lý học sinh được xây dựng bằng Python với giao diện Tkinter và SQLite database. Hệ thống hỗ trợ đăng nhập, quản lý tài khoản, quản lý học sinh, lớp học, điểm số, môn học và học phí.

## Cấu trúc thư mục

```
hp7-python/
├── main.py                    # File chính, entry point của ứng dụng
├── UI.py                      # Giao diện Tkinter (demo/alternative)
├── Common/                    # Thư mục chứa code dùng chung
│   └── a.py
├── Config/                    # Cấu hình
│   └── test.py
├── Database/                  # Database SQLite
│   └── users.db
└── src/                       # Source code chính
    ├── Account/               # Module quản lý tài khoản
    ├── Student/               # Module học sinh
    ├── student-management/    # Quản lý học sinh
    ├── classroom-management/  # Quản lý lớp học
    ├── score/                 # Quản lý điểm số
    ├── subject/               # Quản lý môn học
    └── tuition/               # Quản lý học phí
```

---

## 1. Module Account (Quản lý Tài khoản)

### 1.1. `login.py`
**Chức năng:** Xử lý đăng nhập người dùng

**Các hàm chính:**
- `init_db()`: Khởi tạo database, tạo bảng `users` nếu chưa tồn tại
- `login()`: Xác thực username/password, kiểm tra trạng thái khóa tài khoản
- `on_login_success(username)`: Callback khi đăng nhập thành công, mở user screen
- `on_logout()`: Callback khi đăng xuất, quay lại màn hình login

**Database Schema:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    locked INTEGER DEFAULT 0
)
```

**UI Components:**
- Form đăng nhập với username và password
- Nút "Login" để đăng nhập
- Nút "Register" để chuyển sang màn hình đăng ký

**Lưu ý:**
- File có một số hàm bị trùng lặp (`on_login_success`, `on_logout` được định nghĩa 2 lần)
- Import có vấn đề: `from . import register` nhưng file là `Register.py` (chữ R hoa)

---

### 1.2. `Register.py`
**Chức năng:** Xử lý đăng ký tài khoản mới

**Các hàm chính:**
- `is_valid_gmail(email)`: Kiểm tra định dạng email Gmail hợp lệ
- `open_register(parent, db_path, on_success_login)`: Mở cửa sổ đăng ký

**Validation:**
- Username phải là email Gmail (format: `xxx@gmail.com`)
- Password tối thiểu 6 ký tự
- Password và Confirm Password phải khớp
- Không được để trống các trường

**Database:**
- Lưu user mới vào bảng `users` với `locked=0` (tài khoản mở)

**UI:**
- Form đăng ký với Username, Password, Confirm Password
- Nút "Create Account" để tạo tài khoản
- Nút "Back" để quay lại màn hình login

---

### 1.3. `mainAccount.py`
**Chức năng:** Menu quản lý tài khoản (CLI)

**Các hàm:**
- `account_menu()`: Menu chính với các tùy chọn:
  - Tạo tài khoản
  - Đổi mật khẩu
  - Khóa/Mở khóa tài khoản
- `create_account()`: Placeholder (chưa implement)
- `change_password()`: Placeholder (chưa implement)
- `lock_unlock_account()`: Placeholder (chưa implement)

**Lưu ý:** Module này chỉ có menu structure, các chức năng chưa được implement đầy đủ.

---

### 1.4. `user_screen.py`
**Chức năng:** Màn hình dashboard sau khi đăng nhập thành công

**Các hàm:**
- `get_conn()`: Kết nối database
- `open_user_screen(username, on_logout)`: Mở màn hình user với sidebar và content area

**Tính năng:**
- **Sidebar:** Menu bên trái với các nút:
  - 👤 Thông tin: Hiển thị thông tin tài khoản (username, trạng thái)
  - 🔒 Tự khóa: Khóa tài khoản của chính mình
  - 🚪 Đăng xuất: Đăng xuất và quay lại login

- **Content Area:** Hiển thị thông tin động dựa trên lựa chọn

**UI Design:**
- Sidebar màu xám đậm (#2c3e50)
- Content area màu trắng
- Buttons có hover effect (#1abc9c)

---

## 2. Module Student (Học sinh)

### 2.1. `mainStudent.py`
**Chức năng:** Menu quản lý học sinh (CLI)

**Các hàm:**
- `student_menu()`: Menu chính với các tùy chọn:
  - Thêm học sinh
  - Sửa thông tin học sinh
  - Xóa học sinh
  - Tìm kiếm học sinh
- `add_student()`: Placeholder
- `edit_student()`: Placeholder
- `delete_student()`: Placeholder
- `search_student()`: Placeholder

**Lưu ý:** Module này chỉ có menu structure, các chức năng chưa được implement.

---

## 3. Module Student Management (Quản lý Học sinh)

### 3.1. `add-edit-delete.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Xử lý thêm, sửa, xóa học sinh

---

### 3.2. `see-list.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Hiển thị danh sách học sinh

---

## 4. Module Classroom Management (Quản lý Lớp học)

### 4.1. `add-class.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Thêm lớp học mới

---

### 4.2. `add-students-to-class.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Thêm học sinh vào lớp

---

## 5. Module Score (Quản lý Điểm số)

### 5.1. `enter-score.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Nhập điểm cho học sinh

---

### 5.2. `see-score.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Xem điểm số của học sinh

---

## 6. Module Subject (Quản lý Môn học)

### 6.1. `daily-subjects-of-each-class.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Quản lý môn học hàng ngày của từng lớp

---

### 6.2. `lesson-list.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Danh sách bài học

---

## 7. Module Tuition (Quản lý Học phí)

### 7.1. `entertuition.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Nhập học phí

---

### 7.2. `paid-underpaid.py`
**Trạng thái:** File trống, chưa có code

**Dự kiến:** Quản lý học phí đã đóng/chưa đóng

---

## 8. File chính

### 8.1. `main.py`
**Chức năng:** Entry point của ứng dụng

**Flow:**
1. Gọi `login()` để đăng nhập
2. Hiển thị menu chính:
   - Quản lý tài khoản (chỉ admin)
   - Quản lý học sinh
   - Thoát

**Lưu ý:** File có code trùng lặp ở cuối (import và main block bị lặp)

---

### 8.2. `UI.py`
**Chức năng:** Giao diện Tkinter demo/alternative

**Các class:**
- `StudentUI`: Giao diện cho học sinh
- `TeacherUI`: Giao diện cho giáo viên
- `LoginUI`: Giao diện đăng nhập

**Lưu ý:** 
- File này có vẻ là demo/alternative implementation
- Sử dụng dữ liệu hardcode (không dùng database)
- Có thể không được sử dụng trong phiên bản chính

---

## Database

### Cấu trúc hiện tại:
- **users.db**: Database SQLite chứa thông tin người dùng
- **Bảng users:**
  - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
  - `username`: TEXT UNIQUE (email Gmail)
  - `password`: TEXT (lưu plain text - cần cải thiện bảo mật)
  - `locked`: INTEGER DEFAULT 0 (0 = mở, 1 = khóa)

---

## Vấn đề cần khắc phục

1. **Bảo mật:**
   - Password đang lưu plain text, nên hash bằng bcrypt hoặc hashlib
   - Thiếu validation input để tránh SQL injection

2. **Code quality:**
   - Nhiều file trống, chưa implement
   - Code trùng lặp trong `login.py` và `main.py`
   - Import path không nhất quán (Register vs register)

3. **Database:**
   - Chưa có schema cho học sinh, lớp học, điểm số, môn học, học phí
   - Cần thiết kế database schema đầy đủ

4. **UI/UX:**
   - Có 2 implementation UI khác nhau (`login.py` và `UI.py`)
   - Cần thống nhất một giao diện

5. **Error handling:**
   - Thiếu xử lý lỗi đầy đủ
   - Cần thêm try-catch cho database operations

---

## Hướng phát triển

1. **Hoàn thiện các module:**
   - Implement các chức năng trong student-management
   - Implement classroom-management
   - Implement score management
   - Implement subject management
   - Implement tuition management

2. **Database schema:**
   - Tạo bảng students, classes, scores, subjects, tuition
   - Thiết lập relationships giữa các bảng

3. **Bảo mật:**
   - Hash passwords
   - Input validation
   - SQL injection prevention

4. **Testing:**
   - Unit tests cho các module
   - Integration tests

5. **Documentation:**
   - API documentation
   - User manual

---

## Cách sử dụng

1. **Chạy ứng dụng:**
```bash
python main.py
```

2. **Đăng ký tài khoản mới:**
   - Click "Register" trên màn hình login
   - Nhập email Gmail và password (tối thiểu 6 ký tự)
   - Click "Create Account"

3. **Đăng nhập:**
   - Nhập username (email) và password
   - Click "Login"

4. **Sử dụng dashboard:**
   - Xem thông tin tài khoản
   - Tự khóa tài khoản nếu cần
   - Đăng xuất

---

## Dependencies

- Python 3.x
- tkinter (thường đi kèm Python)
- sqlite3 (thường đi kèm Python)

---

*Tài liệu được tạo tự động - Cập nhật: 2024*

