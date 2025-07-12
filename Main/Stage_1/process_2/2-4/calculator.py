import sys
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt

# 계산 로직 클래스
class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = "0"
        self.operator = None
        self.operand = None
        self.result_shown = False

    def input_digit(self, digit):
        if self.result_shown:
            self.current = digit
            self.result_shown = False
        elif self.current == "0":
            self.current = digit
        else:
            self.current += digit

    def input_dot(self):
        if "." not in self.current:
            self.current += "."

    def negative_positive(self):
        if self.current.startswith("-"):
            self.current = self.current[1:]
        elif self.current != "0":
            self.current = "-" + self.current

    def percent(self):
        try:
            val = float(self.current) / 100
            self.current = str(val)
            if self.current.endswith(".0"):
                self.current = self.current[:-2]
        except:
            self.current = "Error"

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0: raise ZeroDivisionError
        return a / b

    def prepare_operation(self, op):
        if self.operator and not self.result_shown:
            self.equal()
        try:
            self.operand = float(self.current)
        except:
            self.current = "Error"
            return
        self.operator = op
        self.current = "0"

    def equal(self):
        if not self.operator or self.operand is None:
            return
        try:
            right = float(self.current)
            if self.operator == "+": result = self.add(self.operand, right)
            elif self.operator == "-": result = self.subtract(self.operand, right)
            elif self.operator == "×": result = self.multiply(self.operand, right)
            elif self.operator == "÷": result = self.divide(self.operand, right)
            self.current = str(result)
            if self.current.endswith(".0"):
                self.current = self.current[:-2]
            self.operator = None
            self.operand = None
            self.result_shown = True
        except ZeroDivisionError:
            self.current = "Error: Div by 0"
        except:
            self.current = "Error"

# UI 클래스
class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("iPhone Calculator Clone")
        self.setFixedSize(300, 400)

        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet(
            "font-size: 30px; padding: 10px; background: white; color: black; border: 1px solid #ccc;"
        )
        self.display.setFixedHeight(60)  # ✅ 텍스트가 잘 보이도록 높이 지정

        vbox = QVBoxLayout()
        vbox.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for row_idx, row in enumerate(buttons):
            col_idx = 0
            for btn_text in row:
                btn = QPushButton(btn_text)
                btn.setFixedHeight(60)
                btn.setStyleSheet("font-size: 18px;")
                if btn_text == "0":
                    grid.addWidget(btn, row_idx + 1, col_idx, 1, 2)
                    col_idx += 2
                else:
                    grid.addWidget(btn, row_idx + 1, col_idx)
                    col_idx += 1
                # 핵심: 버튼 텍스트를 partial로 전달
                btn.clicked.connect(partial(self.handle_button, btn_text))

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def handle_button(self, value):
        if value == "AC":
            self.calc.reset()
        elif value == "+/-":
            self.calc.negative_positive()
        elif value == "%":
            self.calc.percent()
        elif value in ["+", "-", "×", "÷"]:
            self.calc.prepare_operation(value)
        elif value == "=":
            self.calc.equal()
        elif value == ".":
            self.calc.input_dot()
        else:
            self.calc.input_digit(value)

        self.display.setText(self.calc.current)

# 실행부
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())
