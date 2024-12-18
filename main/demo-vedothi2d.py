import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import sympy as sp
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giải phương trình bậc một và bậc hai")
root.geometry("1000x600")  # Kích thước cửa sổ rộng hơn

# Biến toàn cục lưu trữ đối tượng đồ thị
current_canvas = None

# Hàm vẽ đồ thị
def plot_graph(a, b, c=None):
    global current_canvas

    # Xóa đồ thị cũ nếu có
    if current_canvas:
        current_canvas.get_tk_widget().destroy()  # Xóa widget đồ thị cũ

    # Xây dựng giá trị x từ -10 đến 10 cho đồ thị
    x_vals = np.linspace(-10, 10, 400)

    if c is None:
        # Phương trình bậc nhất: y = ax + b
        y_vals = a * x_vals + b
    else:
        # Phương trình bậc hai: y = ax² + bx + c
        y_vals = a * x_vals**2 + b * x_vals + c

    # Vẽ đồ thị
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(x_vals, y_vals, label="Đồ thị", color="blue")

    # Đánh dấu nghiệm của phương trình
    if c is None:
        x_root = -b / a  # Nghiệm phương trình bậc nhất
        ax.scatter(x_root, 0, color='red', zorder=5)
        ax.text(x_root, 0.5, f'x = {x_root:.2f}', color='red', ha='center', fontsize=10)  # Dịch nhãn lên trên một chút
    else:
        delta = b**2 - 4*a*c
        if delta >= 0:
            # Hai nghiệm phân biệt hoặc nghiệm kép
            x1 = (-b + math.sqrt(delta)) / (2 * a)
            x2 = (-b - math.sqrt(delta)) / (2 * a)

            ax.scatter(x1, 0, color='red', zorder=5)
            ax.scatter(x2, 0, color='red', zorder=5)

            # Điều chỉnh nhãn nghiệm
            ax.text(x1, -0.5, f'x₁ = {x1:.2f}', color='red', ha='center', fontsize=10, verticalalignment='top')
            ax.text(x2, 0.5, f'x₂ = {x2:.2f}', color='red', ha='center', fontsize=10, verticalalignment='bottom')
        else:
            # Vô nghiệm: không cần vẽ các điểm
            ax.text(0, 0, "Vô nghiệm", color='red', ha='center', fontsize=12)

    # Tinh chỉnh đồ thị
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_title("Đồ thị phương trình")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()

    # Hiển thị đồ thị trong Tkinter
    current_canvas = FigureCanvasTkAgg(fig, master=solution_frame)
    current_canvas.draw()
    current_canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Hàm giải phương trình bậc nhất
def solve_linear():
    try:
        # Lấy giá trị từ các ô nhập liệu
        a = float(entry_a.get())
        b = float(entry_b.get())
        
        # Kiểm tra trường hợp a = 0 (phương trình không phải bậc nhất)
        if a == 0:
            messagebox.showerror("Lỗi", "a không thể bằng 0 trong phương trình bậc nhất!")
            return
        
        # Tính nghiệm của phương trình ax + b = 0
        x = -b / a
        solution_text.delete(1.0, tk.END)  # Xóa các kết quả cũ
        solution_text.insert(tk.END, f"Phương trình: {a}x + {b} = 0\n\n")
        solution_text.insert(tk.END, "Giải:\n")
        solution_text.insert(tk.END, f"Bước 1: Chuyển vế đổi dấu {a}x = {-b}\n")
        solution_text.insert(tk.END, f"Bước 2: Tính x = {-b} / {a}\n")
        solution_text.insert(tk.END, f"Vậy: x = {x}\n")
    
        # Vẽ đồ thị
        plot_graph(a, b)
        
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ cho a và b!")

# Hàm giải phương trình bậc hai
def solve_quadratic():
    try:
        # Lấy giá trị từ các ô nhập liệu
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        
        # Kiểm tra trường hợp a = 0 (phương trình không phải bậc hai)
        if a == 0:
            messagebox.showerror("Lỗi", "a không thể bằng 0 trong phương trình bậc hai!")
            return
        
        # Tính delta
        delta = b**2 - 4*a*c
        
        solution_text.delete(1.0, tk.END)  # Xóa các kết quả cũ
        solution_text.insert(tk.END, f"Phương trình: {a}x² + {b}x + {c} = 0\n\n")
        solution_text.insert(tk.END, "Giải:\n")
        solution_text.insert(tk.END, f"Bước 1: Tính giá trị của Delta Δ = {b}² - 4×{a}×{c} = {b**2} - {4*a*c} = {delta}")
        
        if delta > 0:
            # Hai nghiệm phân biệt
            x1 = (-b + math.sqrt(delta)) / (2 * a)
            x2 = (-b - math.sqrt(delta)) / (2 * a)
            solution_text.insert(tk.END, " > 0\n")
            solution_text.insert(tk.END, "Bước 2: Do Δ > 0 nên phương trình có 2 nghiệm phân biệt.\n")
            solution_text.insert(tk.END, f"Nghiệm 1: x₁ = (-{b} + √{delta}) / (2×{a}) = {x1}\n")
            solution_text.insert(tk.END, f"Nghiệm 2: x₂ = (-{b} - √{delta}) / (2×{a}) = {x2}\n")
            solution_text.insert(tk.END, f"Giải: x₁ = {x1}, x₂ = {x2}\n")
        elif delta == 0:
            # Một nghiệm kép
            x = -b / (2 * a)
            solution_text.insert(tk.END, "Bước 2: Phương trình có 1 nghiệm kép.\n")
            solution_text.insert(tk.END, f"Nghiệm: x = {-b} / (2×{a}) = {x}\n")
            solution_text.insert(tk.END, f"Giải: x = {x}\n")
        else:
            # Vô nghiệm
            solution_text.insert(tk.END, "Bước 2: Phương trình vô nghiệm trong tập số thực.\n")
            solution_text.insert(tk.END, "Giải: Vô nghiệm\n")
    
        # Vẽ đồ thị
        plot_graph(a, b, c)
        
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ cho a, b và c!")

# Hàm thay đổi ô nhập liệu khi chọn phương trình
def change_equation(event=None):
    equation_type = equation_var.get()
    
    # Xóa dữ liệu đã nhập
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    entry_c.delete(0, tk.END)
    solution_text.delete(1.0, tk.END)  # Xóa lời giải chi tiết
    
    # Xóa đồ thị cũ khi thay đổi phương trình
    if current_canvas:
        current_canvas.get_tk_widget().destroy()
    
    if equation_type == "Bậc 1":
        label_c.grid_forget()  # Ẩn ô nhập liệu c
        entry_c.grid_forget()  # Ẩn ô nhập liệu c
    elif equation_type == "Bậc 2":
        label_c.grid(row=2, column=0, padx=10, pady=10)  # Hiển thị lại ô nhập liệu c
        entry_c.grid(row=2, column=1, padx=10, pady=10)

# Tạo các widget
equation_var = tk.StringVar(value="Bậc 1")
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_equation = tk.Label(frame, text="Chọn phương trình:")
label_equation.grid(row=0, column=0, padx=10, pady=10)
option_equation = ttk.Combobox(frame, textvariable=equation_var, values=["Bậc 1", "Bậc 2"], state="readonly", width=10)
option_equation.grid(row=0, column=1, padx=10, pady=10)
option_equation.bind("<<ComboboxSelected>>", change_equation)

label_a = tk.Label(frame, text="Nhập a:")
label_a.grid(row=1, column=0, padx=10, pady=10)
entry_a = tk.Entry(frame)
entry_a.grid(row=1, column=1, padx=10, pady=10)

label_b = tk.Label(frame, text="Nhập b:")
label_b.grid(row=1, column=2, padx=10, pady=10)
entry_b = tk.Entry(frame)
entry_b.grid(row=1, column=3, padx=10, pady=10)

label_c = tk.Label(frame, text="Nhập c:")
label_c.grid(row=2, column=0, padx=10, pady=10)
entry_c = tk.Entry(frame)
entry_c.grid(row=2, column=1, padx=10, pady=10)

# Nút giải phương trình
btn_solve = tk.Button(root, text="Giải", command=lambda: solve_linear() if equation_var.get() == "Bậc 1" else solve_quadratic(), width=20, height=2)
btn_solve.pack(pady=20)

# Ô hiển thị kết quả (lời giải chi tiết và đồ thị)
solution_frame = tk.Frame(root)
solution_frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)

# Chia solution_frame thành 2 cột cho đồ thị và lời giải chi tiết
solution_frame.grid_columnconfigure(0, weight=1, uniform="equal")  # Cột 1 cho đồ thị
solution_frame.grid_columnconfigure(1, weight=1, uniform="equal")  # Cột 2 cho lời giải chi tiết

# Widget lời giải chi tiết
solution_text = scrolledtext.ScrolledText(solution_frame, width=50, height=15, wrap=tk.WORD)
solution_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
solution_text2 = scrolledtext.ScrolledText(solution_frame, width=50, height=15, wrap=tk.WORD)
solution_text2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Khởi tạo giao diện ban đầu
change_equation()  # Đảm bảo giao diện ban đầu được điều chỉnh đúng

# Chạy ứng dụng
root.mainloop()