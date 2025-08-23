import sys
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QFontMetrics

# logic of calculation
class Calculator:
    """
    사칙 연산 및 특수 기능을 담당하는 계산기 로직 클래스입니다.
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
            # 소수점 아래가 .0이면 제거
            if self.current.endswith(".0"):
                self.current = self.current[:-2]
        except:
            self.current = "Error"

    def add(self, a, b):
        return a + b
        
    def subtract(self, a, b):
        return a - b
        
    def multiply(self, a, b):
        return a * b
        
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b

    def prepare_operation(self, op):
        """
        새로운 연산자를 준비하거나 이전 연산을 수행합니다.
        """
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
        """
        현재 수식의 결과를 계산하여 표시합니다.
        """
        if not self.operator or self.operand is None:
            return
        
        try:
            right = float(self.current)
            if self.operator == "+":
                result = self.add(self.operand, right)
            elif self.operator == "-":
                result = self.subtract(self.operand, right)
            elif self.operator == "×":
                result = self.multiply(self.operand, right)
            elif self.operator == "÷":
                result = self.divide(self.operand, right)
            
            self.current = str(result)
            # 소수점 아래가 .0이면 제거
            if self.current.endswith(".0"):
                self.current = self.current[:-2]
            
            self.operator = None
            self.operand = None
            self.result_shown = True
        except ZeroDivisionError:
            self.current = "Error"
        except:
            self.current = "Error"

# UI
class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.initUI()

    def initUI(self):
        """
        UI를 초기화하고 레이아웃을 설정합니다.
        """
        self.setWindowTitle("iPhone Calculator Clone")
        self.setFixedSize(360, 600)
        self.setStyleSheet("background-color: #2e2e2e; color: white;")

        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet("""
            font-size: 80px;
            padding: 20px;
        """)
        self.display.setFixedHeight(120)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.addWidget(self.display)
        
        button_grid = QGridLayout()
        button_grid.setSpacing(10)

        # 버튼 데이터를 행, 열, 텍스트로 구성
        buttons = [
            ("AC", 0, 0), ("+/-", 0, 1), ("%", 0, 2), ("÷", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0), (".", 4, 2), ("=", 4, 3)
        ]
        
        # 버튼 스타일 및 레이아웃 설정
        for btn_text, row, col in buttons:
            btn = QPushButton(btn_text)
            
            # 버튼 스타일 설정
            if btn_text in ["+", "-", "×", "÷", "="]:
                color = "#ff9500"
                text_color = "white"
            elif btn_text in ["AC", "+/-", "%"]:
                color = "#a6a6a6"
                text_color = "black"
            else:
                color = "#505050"
                text_color = "white"
            
            # '0' 버튼은 가로로 두 칸 차지
            colspan = 2 if btn_text == "0" else 1

            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 30px;
                    background-color: {color};
                    border-radius: 40px;
                    height: 80px;
                    color: {text_color};
                }}
                QPushButton:pressed {{
                    background-color: #d1d1d1;
                }}
            """)
            
            button_grid.addWidget(btn, row, col, 1, colspan)

            btn.clicked.connect(partial(self.handle_button, btn_text))

        main_layout.addLayout(button_grid)
        self.setLayout(main_layout)

    def handle_button(self, value):
        """버튼 클릭 이벤트를 처리하고 계산기 로직과 연결합니다."""
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())