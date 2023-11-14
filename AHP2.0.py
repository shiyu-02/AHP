import sys
from fractions import Fraction
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout
RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}

class AHPApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.result_label_end = QLabel()
        self.solutions_box = None
        self.solutions_entry = None
        self.criteria_entry = None
        self.result_label = QLabel()
        self.setWindowTitle("AHP计算器")
        self.criteria_names = []
        self.solutions_names = []
        self.criteria_entries = []
        self.solutions_entries = []
        self.criteria_matrix = None
        self.solutions_matrix = None
        self.criteria = None
        self.solutions = None

        self.create_input_page()


    def create_input_page(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout()
        self.central_widget.setLayout(layout)

        criteria_label = QLabel("请输入准则层数:")
        layout.addWidget(criteria_label, 0, 0)
        self.criteria_entry = QLineEdit()
        layout.addWidget(self.criteria_entry, 0, 1)

        solutions_label = QLabel("请输入方案层数:")
        layout.addWidget(solutions_label, 1, 0)
        self.solutions_entry = QLineEdit()
        layout.addWidget(self.solutions_entry, 1, 1)

        next_btn = QPushButton("下一步")
        next_btn.clicked.connect(self.create_criteria_matrix)
        layout.addWidget(next_btn, 2, 0, 1, 2)

    def create_criteria_matrix(self):
        self.criteria = int(self.criteria_entry.text())
        self.solutions = int(self.solutions_entry.text())

        self.criteria_names = []
        self.criteria_entries = []

        self.criteria_matrix_widget = QWidget()
        self.setCentralWidget(self.criteria_matrix_widget)

        layout = QGridLayout()
        self.criteria_matrix_widget.setLayout(layout)

        for i in range(self.criteria):
            name_label = QLabel(f"请输入第{i + 1}个准则的名称:")
            layout.addWidget(name_label, i, 0)
            name_entry = QLineEdit()
            layout.addWidget(name_entry, i, 1)
            self.criteria_names.append(name_entry)


        next_btn = QPushButton("下一步")
        next_btn.clicked.connect(self.create_solutions_matrix)
        layout.addWidget(next_btn, self.criteria, 0, 1, 2)

    def create_solutions_matrix(self):
        self.solutions_names = []
        self.solutions_entries = []
        self.solutions_matrix_widget = QWidget()
        self.setCentralWidget(self.solutions_matrix_widget)

        layout = QGridLayout()
        self.solutions_matrix_widget.setLayout(layout)

        for i in range(self.solutions):
            name_label = QLabel(f"请输入方案{i + 1}的名称:")
            layout.addWidget(name_label, i + 1, 0)
            name_entry = QLineEdit()
            layout.addWidget(name_entry, i + 1, 1)
            self.solutions_names.append(name_entry)
            global solutions_names


        next_btn = QPushButton("下一步")
        next_btn.clicked.connect(self.create_solutions)
        layout.addWidget(next_btn, self.solutions + self.criteria + 2, 0, 1, self.criteria + 1)

    def create_solutions(self):
        self.solutions_matrix_widget = QWidget()
        self.setCentralWidget(self.solutions_matrix_widget)


        layout = QVBoxLayout()  # 使用垂直布局
        self.solutions_matrix_widget.setLayout(layout)

        input_layout = QHBoxLayout()  # 用于放置输入相关部件的水平布局
        layout.addLayout(input_layout)

        num_boxes_label = QLabel("请输入变量数量：")
        input_layout.addWidget(num_boxes_label)
        self.num_boxes_entry = QLineEdit()
        input_layout.addWidget(self.num_boxes_entry)

        next_btn_1 = QPushButton("确定")
        next_btn_1.clicked.connect(self.create_text_boxes)
        input_layout.addWidget(next_btn_1)
        self.calc_button_count = 0  # 添加计数器
        self.calc_button_result =[]

        next_btn = QPushButton("计算")
        next_btn.clicked.connect(self.calculate)
        layout.addWidget(next_btn)
        layout.addWidget(self.result_label)  # 将result_label添加到布局中

    def create_text_boxes(self):
        # 清除之前的数据框
        if hasattr(self, 'grid_layout'):
            for i in reversed(range(self.grid_layout.count())):
                widget = self.grid_layout.itemAt(i).widget()
                widget.deleteLater()

        num_rows = int(self.num_boxes_entry.text())
        num_cols = int(self.num_boxes_entry.text())
        self.text_boxes = []
        self.grid_layout = QGridLayout()  # 使用网格布局
        for i in range(num_rows):
            row = []
            for j in range(num_cols):
                text_box = QLineEdit()
                self.grid_layout.addWidget(text_box, i, j)
                row.append(text_box)
            self.text_boxes.append(row)

        layout = self.solutions_matrix_widget.layout()
        layout.addLayout(self.grid_layout)

    def calculate(self):
        data = []
        for i in range(int(self.num_boxes_entry.text())):
            row = []
            for j in range(int(self.num_boxes_entry.text())):
                content = self.text_boxes[i][j].text()
                try:
                    fraction = Fraction(content)
                    row.append(fraction)
                except ValueError:
                    row.append(0)
            data.append(row)
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
            result_text = "W:" + str(w_arr) + "\n入max:" + str(Max) + "\nCR:" + str(CR) + "<0.1\n通过了一致性检验"
            self.calc_button_result.append(w_arr)
            self.calc_button_count += 1  # 每次点击计算按钮增加计数器的值
            if self.calc_button_count >= self.criteria + 1:
                self.calc_button_result_criteria = self.calc_button_result[0]
                self.calc_button_result_solutions = self.calc_button_result[1:]
                sum = 0
                sum_list =[]
                for i in range(self.solutions):
                    for j in range(self.criteria):
                        sum += self.calc_button_result_criteria[j] * self.calc_button_result_solutions[j][i]
                    sum_list.append(sum)
                    sum = 0
                result_text_end = "最终比值为："+ str(sum_list)

                self.result_label_end.setText(result_text_end)  # Set the text of the result_label to display the results
                self.end()



        else:
            result_text = "W:" + str(w_arr) + "\n入max:" + str(Max) + "\nCR:" + str(CR) + ">=0.1\n没有通过一致性检验"

        self.result_label.setText(result_text)  # Set the text of the result_label to display the results

    def end(self):
        self.end_widget = QWidget()
        self.setCentralWidget(self.end_widget)

        layout = QVBoxLayout()
        self.end_widget.setLayout(layout)

        layout.addWidget(self.result_label_end)  # 将result_label添加到布局中
        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.closeApp)
        layout.addWidget(ok_button)

    def closeApp(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ahp = AHPApp()
    ahp.show()
    sys.exit(app.exec_())