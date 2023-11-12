import numpy as np
import tkinter as tk
from fractions import Fraction

RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}


# 定义一个打印函数
def dayin(data):
    A = np.array(data)

    a_sum0 = A.sum(axis=0)
    B = A / a_sum0
    b_sum = B.sum(axis=1)

    W = b_sum.sum()
    w_arr = []
    for w in b_sum:
        w = float(w)
        w_arr.append(w / W)

    AW = []
    for a in A:
        aa = a * w_arr
        AW.append(aa.sum())

    result = np.array(AW) / np.array(w_arr)
    row = result.shape[0]
    Max = result.sum() / row
    CI = (Max - row) / (row - 1)
    CR = CI / RI_dict[row]

    if CR < 0.1:
        output_label.config(text="W:" + str(w_arr) + "\n入max:" + str(Max) +"\nCR:" + str(CR)+ "<0.1\n通过了一致性检验")
    else:
        output_label.config(text="W:" + str(w_arr) + "\n入max:" + str(Max) +"\nCR:" + str(CR)+">=0.1\n没有通过一致性检验")
def create_text_boxes():
    num_spaces = int(entry.get()) ** 2
    if num_spaces < 4 or num_spaces > 81:
        label.config(text="变量个数")
        return
    label.config(text="计算页面")

    for widget in frame.winfo_children():
        widget.destroy()

    rows = int(num_spaces ** 0.5)
    cols = num_spaces // rows
    if num_spaces % rows != 0:
        cols += 1

    text_boxes = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if i * cols + j < num_spaces:
                text_box = tk.Entry(frame)
                text_box.grid(row=i, column=j, padx=5, pady=5)
                row.append(text_box)
        text_boxes.append(row)

    export_button.config(state="normal")
    global text_boxes_list
    text_boxes_list = text_boxes


def export_data():
    data = []
    for row in text_boxes_list:
        row_data = []
        for text_box in row:
            content = text_box.get()
            try:
                fraction = Fraction(content)  # 尝试将内容转换为分数类型
                row_data.append(fraction)
            except ValueError:
                row_data.append(0)  # 如果无法转换为分数，可以进行其他处理，比如设置为默认值
        data.append(row_data)
    dayin(data)


root = tk.Tk()
root.title("层次分析法")

label = tk.Label(root, text="变量数量：")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="创建矩阵", command=create_text_boxes)
button.pack()

frame = tk.Frame(root)
frame.pack()

export_button = tk.Button(root, text="计算", command=export_data, state="disabled")
export_button.pack()

output_label = tk.Label(root, text="")
output_label.pack()
root.mainloop()
