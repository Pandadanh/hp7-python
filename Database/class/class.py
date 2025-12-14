import tkinter as tk
from tkinter import messagebox


class ClassUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nhập thông tin lớp")
        self.root.geometry("300x220")

        tk.Label(self.root, text="Mã lớp").pack()
        self.e_id = tk.Entry(self.root)
        self.e_id.pack()

        tk.Label(self.root, text="Tên lớp").pack()
        self.e_name = tk.Entry(self.root)
        self.e_name.pack()

        tk.Label(self.root, text="Mã GVCN").pack()
        self.e_gvcn = tk.Entry(self.root)
        self.e_gvcn.pack()

        tk.Button(self.root, text="OK", command=self.submit).pack(pady=10)

        self.root.mainloop()

    def submit(self):
        print("LỚP:",
              self.e_id.get(),
              self.e_name.get(),
              self.e_gvcn.get())

        messagebox.showinfo("OK", "Đã nhập thông tin lớp")


if __name__ == "__main__":
    ClassUI()
