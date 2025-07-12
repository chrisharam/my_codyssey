import sys
import math
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt

# 기본 계산기 로직
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
        self.result_shown = False

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

# 공학용 계산기 로직
class EngineeringCalculator(Calculator):
    def calc_sin(self): self._apply_func(lambda x: math.sin(math.radians(x)))
    def calc_cos(self): self._apply_func(lambda x: math.cos(math.radians(x)))
    def calc_tan(self): self._apply_func(lambda x: math.tan(math.radians(x)))
    def calc_sinh(self): self._apply_func(math.sinh)
    def calc_cosh(self): self._apply_func(math.cosh)
    def calc_tanh(self): self._apply_func(math.tanh)
    def square(self): self._apply_func(lambda x: x ** 2)
    def cube(self): self._apply_func(lambda x: x ** 3)

    def insert_pi(self):
        self.current = str(math.pi)
        self.result_shown = True

    def _apply_func(self, func):
        try:
            self.current = str(func(float(self.current)))
            if self.current.endswith(".0"):
                self.current = self.current[:-2]
            self.result_shown = True
        except:
            self.current = "Error"

# UI
class EngineeringCalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = EngineeringCalculator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Engineering Calculator")
        self.setFixedSize(400, 550)

        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet(
            "font-size: 30px; padding: 10px; background: white; color: black; border: 1px solid #ccc;"
        )
        self.display.setFixedHeight(60)

        vbox = QVBoxLayout()
        vbox.addWidget(self.display)

        grid = QGridLayout()

        # 공학용 버튼
        eng_buttons = [
            ["sin", "cos", "tan", "π"],
            ["sinh", "cosh", "tanh", "x²"],
            ["x³"]
        ]

        for row_idx, row in enumerate(eng_buttons):
            for col_idx, btn_text in enumerate(row):
                btn = QPushButton(btn_text)
                btn.setFixedHeight(50)
                btn.setStyleSheet("font-size: 18px; background-color: black; color: white; border: 1px solid white;")
                btn.clicked.connect(partial(self.handle_engineering_button, btn_text))
                grid.addWidget(btn, row_idx, col_idx)

        # 일반 계산기 버튼
        basic_buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for row_idx, row in enumerate(basic_buttons):
            col_idx = 0
            for btn_text in row:
                btn = QPushButton(btn_text)
                btn.setFixedHeight(60)
                btn.setStyleSheet("font-size: 18px; background-color: black; color: white; border: 1px solid white;")
                if btn_text == "0":
                    grid.addWidget(btn, row_idx + 3, col_idx, 1, 2)
                    col_idx += 2
                else:
                    grid.addWidget(btn, row_idx + 3, col_idx)
                    col_idx += 1
                btn.clicked.connect(partial(self.handle_basic_button, btn_text))

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def handle_basic_button(self, value):
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

    def handle_engineering_button(self, value):
        if value == "sin": self.calc.calc_sin()
        elif value == "cos": self.calc.calc_cos()
        elif value == "tan": self.calc.calc_tan()
        elif value == "sinh": self.calc.calc_sinh()
        elif value == "cosh": self.calc.calc_cosh()
        elif value == "tanh": self.calc.calc_tanh()
        elif value == "π": self.calc.insert_pi()
        elif value == "x²": self.calc.square()
        elif value == "x³": self.calc.cube()
        self.display.setText(self.calc.current)

# 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculatorApp()
    window.show()
    sys.exit(app.exec_())
