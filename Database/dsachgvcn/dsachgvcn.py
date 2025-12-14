import tkinter as tk
from tkinter import messagebox


class GVCN_UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nhập giáo viên chủ nhiệm")
        self.root.geometry("300x220")

        tk.Label(self.root, text="Mã GVCN").pack()
        self.e_id = tk.Entry(self.root)
        self.e_id.pack()

        tk.Label(self.root, text="Tên giáo viên").pack()
        self.e_name = tk.Entry(self.root)
        self.e_name.pack()

        tk.Label(self.root, text="Môn dạy").pack()
        self.e_subject = tk.Entry(self.root)
        self.e_subject.pack()

        tk.Button(self.root, text="OK", command=self.submit).pack(pady=10)

        self.root.mainloop()

    def submit(self):
        print("GVCN:",
              self.e_id.get(),
              self.e_name.get(),
              self.e_subject.get())

        messagebox.showinfo("OK", "Đã nhập GVCN")


if __name__ == "__main__":
    GVCN_UI()
