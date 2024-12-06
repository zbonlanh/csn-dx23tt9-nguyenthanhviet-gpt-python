import tkinter as tk
from tkinter import messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk  # Thư viện xử lý hình ảnh

current_canvas = None  # Biến lưu trạng thái đồ thị

def clear_canvas():
    global current_canvas
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()
        current_canvas = None

def ve_do_thi_bac_nhat(a, b):
    fig, ax = plt.subplots(figsize=(5, 4))
    x = np.linspace(-10, 10, 400)
    y = a * x + b
    ax.plot(x, y, label=f"{a}x + {b} = 0")
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid()
    ax.legend()
    ax.set_title("Đồ thị phương trình bậc nhất")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return fig

def ve_do_thi_bac_hai(a, b, c):
    fig, ax = plt.subplots(figsize=(5, 4))
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c
    ax.plot(x, y, label=f"{a}x² + {b}x + {c} = 0")
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid()
    ax.legend()
    ax.set_title("Đồ thị phương trình bậc hai")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return fig

def show_solution(solution):
    """Hiển thị lời giải chi tiết trong khung văn bản"""
    text_output.delete('1.0', tk.END)  # Xóa nội dung cũ
    text_output.insert(tk.END, solution)  # Thêm lời giải mới

def giai_bac_nhat():
    global current_canvas
    clear_canvas()  # Xóa đồ thị cũ trước khi vẽ mới
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        if a == 0:
            if b == 0:
                solution = "Phương trình vô số nghiệm vì 0x + 0 = 0."
                show_solution(solution)
            else:
                solution = "Phương trình vô nghiệm vì 0x + b = 0 với b ≠ 0."
                show_solution(solution)
        else:
            x = -b / a
            solution = (
                f"Phương trình: {a}x + {b} = 0\n"
                f"Giải:\n"
                f"  Chuyển b về vế phải: {a}x = {-b}\n"
                f"  Chia cả hai vế cho {a}: x = {-b} / {a}\n"
                f"  Kết quả: x = {x:.2f}"
            )
            show_solution(solution)
            fig = ve_do_thi_bac_nhat(a, b)
            current_canvas = FigureCanvasTkAgg(fig, master=root)
            current_canvas.draw()
            current_canvas.get_tk_widget().pack()
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

def giai_bac_hai():
    global current_canvas
    clear_canvas()  # Xóa đồ thị cũ trước khi vẽ mới
    try:
        a = float(entry_a2.get())
        b = float(entry_b2.get())
        c = float(entry_c2.get())
        if a == 0:
            giai_bac_nhat()
        else:
            delta = b**2 - 4*a*c
            solution = (
                f"Phương trình: {a}x² + {b}x + {c} = 0\n"
                f"Tính delta:\n"
                f"  Δ = b² - 4ac = {b}² - 4*{a}*{c} = {delta}\n"
            )
            if delta < 0:
                solution += "Kết luận: Phương trình vô nghiệm vì Δ < 0."
                show_solution(solution)
            elif delta == 0:
                x = -b / (2 * a)
                solution += (
                    f"Δ = 0 => Phương trình có nghiệm kép:\n"
                    f"  x = -b / (2a) = {-b} / (2*{a}) = {x:.2f}"
                )
                show_solution(solution)
            else:
                x1 = (-b + delta**0.5) / (2 * a)
                x2 = (-b - delta**0.5) / (2 * a)
                solution += (
                    f"Δ > 0 => Phương trình có hai nghiệm phân biệt:\n"
                    f"  x1 = (-b + √Δ) / (2a) = ({-b} + √{delta}) / (2*{a}) = {x1:.2f}\n"
                    f"  x2 = (-b - √Δ) / (2a) = ({-b} - √{delta}) / (2*{a}) = {x2:.2f}"
                )
                show_solution(solution)
            fig = ve_do_thi_bac_hai(a, b, c)
            current_canvas = FigureCanvasTkAgg(fig, master=root)
            current_canvas.draw()
            current_canvas.get_tk_widget().pack()
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giải phương trình và vẽ đồ thị")

# Đặt icon
try:
    root.iconbitmap("icon.ico")  # Thay "icon.ico" bằng đường dẫn icon của bạn
except Exception as e:
    print(f"Không thể mở icon: {e}")

# Đặt hình nền
try:
    bg_image = Image.open("background.jpg")  # Thay "background.jpg" bằng ảnh nền của bạn
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print(f"Không thể mở hình nền: {e}")

# Khung và widget cho giao diện
frame_bac_nhat = tk.Frame(root, bg="#ffffff")
frame_bac_nhat.pack(pady=10)

tk.Label(frame_bac_nhat, text="Giải phương trình bậc nhất: ax + b = 0", bg="#ffffff").pack()
tk.Label(frame_bac_nhat, text="Nhập a:", bg="#ffffff").pack(side=tk.LEFT)
entry_a = tk.Entry(frame_bac_nhat)
entry_a.pack(side=tk.LEFT)

tk.Label(frame_bac_nhat, text="Nhập b:", bg="#ffffff").pack(side=tk.LEFT)
entry_b = tk.Entry(frame_bac_nhat)
entry_b.pack(side=tk.LEFT)

btn_bac_nhat = tk.Button(frame_bac_nhat, text="Giải", command=giai_bac_nhat)
btn_bac_nhat.pack(side=tk.LEFT, padx=10)

# Khung và widget cho giao diện phương trình bậc 2
frame_bac_hai = tk.Frame(root, bg="#ffffff")
frame_bac_hai.pack(pady=10)

tk.Label(frame_bac_hai, text="Giải phương trình bậc hai: ax² + bx + c = 0", bg="#ffffff").pack()
tk.Label(frame_bac_hai, text="Nhập a:").pack(side=tk.LEFT)
entry_a2 = tk.Entry(frame_bac_hai)
entry_a2.pack(side=tk.LEFT)

tk.Label(frame_bac_hai, text="Nhập b:").pack(side=tk.LEFT)
entry_b2 = tk.Entry(frame_bac_hai)
entry_b2.pack(side=tk.LEFT)

tk.Label(frame_bac_hai, text="Nhập c:").pack(side=tk.LEFT)
entry_c2 = tk.Entry(frame_bac_hai)
entry_c2.pack(side=tk.LEFT)

btn_bac_hai = tk.Button(frame_bac_hai, text="Giải", command=giai_bac_hai)
btn_bac_hai.pack(side=tk.LEFT, padx=10)

frame_solution = tk.Frame(root, bg="#ffffff")
frame_solution.pack(pady=10)

tk.Label(frame_solution, text="Lời giải chi tiết:", bg="#ffffff").pack()
text_output = scrolledtext.ScrolledText(frame_solution, width=60, height=10, wrap=tk.WORD)
text_output.pack()

root.mainloop()
