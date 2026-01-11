import sqlite3
import tkinter as tk
from tkinter import messagebox

# ===== DATABASE =====
conn = sqlite3.connect("lien_he_phu_huynh.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS lien_he (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten_ph TEXT,
    ten_hs TEXT,
    sdt TEXT,
    noi_dung TEXT
)
""")
conn.commit()

# ===== FUNCTIONS =====
def clear_entry():
    ten_ph.set("")
    ten_hs.set("")
    sdt.set("")
    noi_dung.set("")

def load_data():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM lien_he")
    for row in cursor.fetchall():
        listbox.insert(tk.END, row)

def them():
    if ten_ph.get() == "":
        messagebox.showwarning("Lỗi", "Chưa nhập tên phụ huynh")
        return
    cursor.execute(
        "INSERT INTO lien_he (ten_ph, ten_hs, sdt, noi_dung) VALUES (?, ?, ?, ?)",
        (ten_ph.get(), ten_hs.get(), sdt.get(), noi_dung.get())
    )
    conn.commit()
    load_data()
    clear_entry()

def chon(event):
    try:
        row = listbox.get(listbox.curselection())
        ten_ph.set(row[1])
        ten_hs.set(row[2])
        sdt.set(row[3])
        noi_dung.set(row[4])
    except:
        pass

def sua():
    try:
        row = listbox.get(listbox.curselection())
        cursor.execute("""
        UPDATE lien_he
        SET ten_ph=?, ten_hs=?, sdt=?, noi_dung=?
        WHERE id=?
        """, (ten_ph.get(), ten_hs.get(), sdt.get(), noi_dung.get(), row[0]))
        conn.commit()
        load_data()
        clear_entry()
    except:
        messagebox.showwarning("Lỗi", "Chọn dòng để sửa")

def xoa():
    try:
        row = listbox.get(listbox.curselection())
        cursor.execute("DELETE FROM lien_he WHERE id=?", (row[0],))
        conn.commit()
        load_data()
        clear_entry()
    except:
        messagebox.showwarning("Lỗi", "Chọn dòng để xóa")

# ===== UI =====
root = tk.Tk()
root.title("Liên hệ phụ huynh")

# KÍCH THƯỚC CỬA SỔ
WIDTH = 850
HEIGHT = 600

# SPAWN GIỮA MÀN HÌNH
root.update_idletasks()
x = (root.winfo_screenwidth() // 2) - (WIDTH // 2)
y = (root.winfo_screenheight() // 2) - (HEIGHT // 2)
root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

root.resizable(False, False)

# ===== FRAME =====
left_frame = tk.Frame(root, padx=20, pady=20)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(root, padx=20, pady=20)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

ten_ph = tk.StringVar()
ten_hs = tk.StringVar()
sdt = tk.StringVar()
noi_dung = tk.StringVar()

# ===== FORM (LEFT) =====
tk.Label(left_frame, text="Tên phụ huynh").pack(anchor="w")
tk.Entry(left_frame, textvariable=ten_ph, width=30).pack(pady=5)

tk.Label(left_frame, text="Tên học sinh").pack(anchor="w")
tk.Entry(left_frame, textvariable=ten_hs, width=30).pack(pady=5)

tk.Label(left_frame, text="SĐT").pack(anchor="w")
tk.Entry(left_frame, textvariable=sdt, width=30).pack(pady=5)

tk.Label(left_frame, text="Nội dung họp / góp ý").pack(anchor="w")
tk.Entry(left_frame, textvariable=noi_dung, width=30).pack(pady=5)

tk.Button(left_frame, text="Thêm", width=20, command=them).pack(pady=5)
tk.Button(left_frame, text="Sửa", width=20, command=sua).pack(pady=5)
tk.Button(left_frame, text="Xóa", width=20, command=xoa).pack(pady=5)

# ===== LIST (RIGHT) =====
listbox = tk.Listbox(right_frame, width=80, height=25)
listbox.pack(fill=tk.BOTH, expand=True)
listbox.bind("<<ListboxSelect>>", chon)

load_data()
root.mainloop()
