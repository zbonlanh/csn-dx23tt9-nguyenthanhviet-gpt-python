import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox
from sympy import symbols, Eq, solve
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io
import numpy as np

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giải Phương Trình và Vẽ Đồ Thị")
root.geometry("1000x600")

# Biến toàn cục lưu trạng thái
current_mode = tk.StringVar(value="Phương trình bậc nhất")

# Tạo khung giao diện
input_frame = ttk.Frame(root, padding=10)
input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

solution_frame = ttk.Frame(root, padding=10)
solution_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Khung hiển thị kết quả
solution_text = scrolledtext.ScrolledText(solution_frame, wrap=tk.WORD, height=20, width=80)
solution_text.pack(expand=True, fill=tk.BOTH)

# Nhãn và ô nhập liệu
a_label = ttk.Label(input_frame, text="Hệ số a:")
a_label.grid(row=0, column=0, padx=5, pady=5)
a_entry = ttk.Entry(input_frame, width=10)
a_entry.grid(row=0, column=1, padx=5, pady=5)

b_label = ttk.Label(input_frame, text="Hệ số b:")
b_label.grid(row=0, column=2, padx=5, pady=5)
b_entry = ttk.Entry(input_frame, width=10)
b_entry.grid(row=0, column=3, padx=5, pady=5)

c_label = ttk.Label(input_frame, text="Hệ số c:")
c_label.grid(row=0, column=4, padx=5, pady=5)
c_entry = ttk.Entry(input_frame, width=10)
c_entry.grid(row=0, column=5, padx=5, pady=5)

# Hàm vẽ đồ thị và hiển thị trong solution_text
def plot_graph_to_text(a, b, c=None):
    # Xây dựng giá trị x và y
    x_vals = np.linspace(-10, 10, 400)
    if c is None:
        y_vals = a * x_vals + b
    else:
        y_vals = a * x_vals**2 + b * x_vals + c

    # Vẽ đồ thị
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x_vals, y_vals, label="Đồ thị", color="blue")
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_title("Đồ thị phương trình")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)

    # Lưu đồ thị vào bộ nhớ
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    # Nhúng đồ thị vào solution_text
    image = Image.open(buf)
    photo = ImageTk.PhotoImage(image)
    solution_text.image_create(tk.END, image=photo)
    solution_text.insert(tk.END, "\n")
    solution_text.image = photo  # Lưu tham chiếu để không bị xóa bộ nhớ

# Hàm giải phương trình
def solve_equation():
    try:
        a = float(a_entry.get())
        b = float(b_entry.get())
        c = float(c_entry.get()) if current_mode.get() == "Phương trình bậc hai" else None

        x = symbols('x')
        if current_mode.get() == "Phương trình bậc nhất":
            eq = Eq(a * x + b, 0)
            solution = solve(eq, x)
            solution_text.delete('1.0', tk.END)
            solution_text.insert(tk.END, f"Phương trình: {eq}\n")
            solution_text.insert(tk.END, f"Nghiệm: x = {solution[0]}\n")
            plot_graph_to_text(a, b)
        else:
            eq = Eq(a * x**2 + b * x + c, 0)
            delta = b**2 - 4*a*c
            solution_text.delete('1.0', tk.END)
            solution_text.insert(tk.END, f"Phương trình: {eq}\n")
            solution_text.insert(tk.END, f"Tính Δ = b² - 4ac = {delta:.2f}\n")

            if delta > 0:
                solution = solve(eq, x)
                solution_text.insert(tk.END, f"Δ > 0: Phương trình có 2 nghiệm phân biệt.\n")
                solution_text.insert(tk.END, f"Nghiệm x₁ = {solution[0]:.2f}, x₂ = {solution[1]:.2f}\n")
            elif delta == 0:
                solution = solve(eq, x)
                solution_text.insert(tk.END, f"Δ = 0: Phương trình có nghiệm kép.\n")
                solution_text.insert(tk.END, f"Nghiệm x₁ = x₂ = {solution[0]:.2f}\n")
            else:
                solution_text.insert(tk.END, "Δ < 0: Phương trình vô nghiệm.\n")

            plot_graph_to_text(a, b, c)

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ cho hệ số a, b, c!")

# Chọn loại phương trình
type_label = ttk.Label(input_frame, text="Loại phương trình:")
type_label.grid(row=0, column=6, padx=5, pady=5)
type_combobox = ttk.Combobox(input_frame, textvariable=current_mode, state="readonly", 
                             values=["Phương trình bậc nhất", "Phương trình bậc hai"])
type_combobox.grid(row=0, column=7, padx=5, pady=5)

# Nút giải
solve_button = ttk.Button(input_frame, text="Giải", command=solve_equation)
solve_button.grid(row=0, column=8, padx=5, pady=5)

# Hiển thị giao diện ban đầu
def toggle_c_entry(event=None):
    if current_mode.get() == "Phương trình bậc nhất":
        c_label.grid_remove()
        c_entry.grid_remove()
    else:
        c_label.grid(row=0, column=4, padx=5, pady=5)
        c_entry.grid(row=0, column=5, padx=5, pady=5)

type_combobox.bind("<<ComboboxSelected>>", toggle_c_entry)
toggle_c_entry()

root.mainloop()
