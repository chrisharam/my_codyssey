import sys
import math
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

# 기본 계산기 로직
class Calculator:
    """
    사칙 연산 및 기본 기능을 담당하는 계산기 로직 클래스입니다.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        """계산기 상태를 초기화합니다."""
        self.current = "0"
        self.operator = None
        self.operand = None
        self.result_shown = False

    def input_digit(self, digit):
        """숫자를 입력받아 현재 숫자에 추가합니다."""
        if self.result_shown:
            self.current = digit
            self.result_shown = False
        elif self.current == "0":
            self.current = digit
        else:
            self.current += digit

    def input_dot(self):
        """소수점을 입력합니다. 이미 소수점이 있으면 입력되지 않습니다."""
        if "." not in self.current:
            self.current += "."

    def negative_positive(self):
        """현재 숫자의 부호를 변경합니다."""
        if self.current.startswith("-"):
            self.current = self.current[1:]
        elif self.current != "0":
            self.current = "-" + self.current

    def percent(self):
        """현재 숫자를 백분율로 변환합니다."""
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
        """새로운 연산자를 준비하거나 이전 연산을 수행합니다."""
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
        """현재 수식의 결과를 계산하여 표시합니다."""
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
    """
    공학용 계산 기능을 추가한 클래스입니다.
    """
    def calc_sin(self): self._apply_func(lambda x: math.sin(math.radians(x)))
    def calc_cos(self): self._apply_func(lambda x: math.cos(math.radians(x)))
    def calc_tan(self): self._apply_func(lambda x: math.tan(math.radians(x)))
    def calc_sinh(self): self._apply_func(math.sinh)
    def calc_cosh(self): self._apply_func(math.cosh)
    def calc_tanh(self): self._apply_func(math.tanh)
    def square(self): self._apply_func(lambda x: x ** 2)
    def cube(self): self._apply_func(lambda x: x ** 3)
    def inverse(self): self._apply_func(lambda x: 1 / x)
    def square_root(self): self._apply_func(math.sqrt)
    def cube_root(self): self._apply_func(lambda x: x**(1/3))
    def factorial(self): self._apply_func(math.factorial)
    def power(self): self.prepare_operation("**")
    def ten_to_power(self): self._apply_func(lambda x: 10 ** x)
    def e_to_power(self): self._apply_func(lambda x: math.e ** x)
    def log(self): self._apply_func(math.log10)
    def natural_log(self): self._apply_func(math.log)

    def insert_pi(self):
        self.current = str(math.pi)
        self.result_shown = True

    def _apply_func(self, func):
        """단일 피연산자 함수를 적용하고 결과를 업데이트합니다."""
        try:
            self.current = str(func(float(self.current)))
            if self.current.endswith(".0"):
                self.current = self.current[:-2]
            self.result_shown = True
        except:
            self.current = "Error"

# UI
class EngineeringCalculatorApp(QWidget):
    """
    아이폰 공학용 계산기 UI와 기능을 통합한 클래스입니다.
    """
    def __init__(self):
        super().__init__()
        self.calc = EngineeringCalculator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("iPhone Engineering Calculator UI")
        self.setFixedSize(700, 400)
        self.setStyleSheet("background-color: #1c1c1c; color: white;")

        # 결과 표시 라벨
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet(
            "font-size: 50px; padding: 10px; border: none;"
        )
        self.display.setFixedHeight(80)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        
        # 'Rad' 라벨 추가
        rad_label = QLabel("Rad")
        rad_label.setStyleSheet("font-size: 15px; color: #a6a6a6; margin-left: 20px;")
        rad_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        top_layout = QVBoxLayout()
        top_layout.addWidget(rad_label)
        top_layout.addWidget(self.display)
        top_layout.setSpacing(0)
        
        main_layout.addLayout(top_layout)
        
        button_grid = QGridLayout()
        button_grid.setSpacing(5)

        # 이미지에 정확히 맞춰서 버튼 위치를 정의
        # (버튼 텍스트, 행, 열, 가로 병합)
        buttons = [
            # 0행
            ("(", 0, 0), (")", 0, 1), ("mc", 0, 2), ("m+", 0, 3), 
            ("m-", 0, 4), ("mr", 0, 5), ("AC", 0, 6), ("+/-", 0, 7), 
            ("%", 0, 8), ("÷", 0, 9),
            # 1행
            ("2nd", 1, 0), ("x²", 1, 1), ("x³", 1, 2), ("xʸ", 1, 3), 
            ("eˣ", 1, 4), ("10ˣ", 1, 5), ("7", 1, 6), ("8", 1, 7), 
            ("9", 1, 8), ("×", 1, 9),
            # 2행
            ("¹/x", 2, 0), ("√x", 2, 1), ("∛x", 2, 2), ("sin", 2, 3), 
            ("cos", 2, 4), ("tan", 2, 5), ("4", 2, 6), ("5", 2, 7), 
            ("6", 2, 8), ("-", 2, 9),
            # 3행
            ("ln", 3, 0), ("log₁₀", 3, 1), ("e", 3, 2), ("EE", 3, 3), 
            ("1", 3, 6), ("2", 3, 7), ("3", 3, 8), ("+", 3, 9),
            # 4행
            ("Deg", 4, 0), ("sinh", 4, 1), ("cosh", 4, 2), ("tanh", 4, 3), 
            ("π", 4, 4), ("Rand", 4, 5), ("0", 4, 6, 2), (".", 4, 8), 
            ("=", 4, 9)
        ]

        # 버튼 생성 및 레이아웃에 추가
        for item in buttons:
            btn_text = item[0]
            row = item[1]
            col = item[2]
            colspan = item[3] if len(item) > 3 else 1

            btn = QPushButton(btn_text)
            
            # 버튼 스타일
            if btn_text in ["÷", "×", "-", "+", "="]:
                color = "#ff9500"
                text_color = "white"
            elif btn_text in ["AC", "+/-", "%"]:
                color = "#a6a6a6"
                text_color = "black"
            else:
                color = "#505050"
                text_color = "white"
            
            # '0' 버튼은 가로로 두 칸 차지
            if btn_text == "0":
                grid_width = 2
            else:
                grid_width = 1

            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 20px;
                    background-color: {color};
                    border-radius: 20px;
                    height: 50px;
                    color: {text_color};
                }}
            """)
            
            button_grid.addWidget(btn, row, col, 1, grid_width)
            
            # 이벤트 핸들러 연결
            if btn_text in ["sin", "cos", "tan", "sinh", "cosh", "tanh", "x²", "x³", "π", "¹/x", "√x", "∛x", "x!"]:
                # 공학용 버튼
                btn.clicked.connect(partial(self.handle_engineering_button, btn_text))
            else:
                # 일반 버튼
                btn.clicked.connect(partial(self.handle_basic_button, btn_text))


        main_layout.addLayout(button_grid)
        self.setLayout(main_layout)

    def handle_basic_button(self, value):
        """일반 계산기 버튼 이벤트를 처리합니다."""
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
        """공학용 계산기 버튼 이벤트를 처리합니다."""
        if value == "sin": self.calc.calc_sin()
        elif value == "cos": self.calc.calc_cos()
        elif value == "tan": self.calc.calc_tan()
        elif value == "sinh": self.calc.calc_sinh()
        elif value == "cosh": self.calc.calc_cosh()
        elif value == "tanh": self.calc.calc_tanh()
        elif value == "x²": self.calc.square()
        elif value == "x³": self.calc.cube()
        elif value == "¹/x": self.calc.inverse()
        elif value == "√x": self.calc.square_root()
        elif value == "∛x": self.calc.cube_root()
        elif value == "x!": self.calc.factorial()
        elif value == "π": self.calc.insert_pi()
        self.display.setText(self.calc.current)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculatorApp()
    window.show()
    sys.exit(app.exec_())