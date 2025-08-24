import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QFontMetrics

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
        return self.current

    def input_dot(self):
        """소수점을 입력합니다. 이미 소수점이 있으면 입력되지 않습니다."""
        if "." not in self.current:
            self.current += "."
        return self.current

    def negative_positive(self):
        """현재 숫자의 부호를 변경합니다."""
        if self.current.startswith("-"):
            self.current = self.current[1:]
        elif self.current != "0":
            self.current = "-" + self.current
        return self.current

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
        return self.current

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
            return self.current
        self.operator = op
        self.current = "0"
        return str(self.operand)

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
        return self.current

class CalculatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.setWindowTitle("iPhone Calculator Clone")
        self.setFixedSize(QSize(360, 600))
        self.setStyleSheet("background-color: black;")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 결과 표시 라벨
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet("""
            font-size: 80px;
            padding: 20px;
            color: white;
        """)
        self.display.setFixedHeight(120)
        
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addStretch()
        main_layout.addWidget(self.display)
        
        button_grid = QGridLayout()
        button_grid.setSpacing(10)
        main_layout.addLayout(button_grid)

        # 버튼 데이터: (버튼 텍스트, 행, 열, 가로 병합, 배경색)
        # 새로운 로직의 연산자 기호에 맞게 변경
        buttons = [
            ('AC', 0, 0, 1, '#a6a6a6'), ('+/-', 0, 1, 1, '#a6a6a6'), ('%', 0, 2, 1, '#a6a6a6'), ('÷', 0, 3, 1, '#ff9500'),
            ('7', 1, 0, 1, '#333333'), ('8', 1, 1, 1, '#333333'), ('9', 1, 2, 1, '#333333'), ('×', 1, 3, 1, '#ff9500'),
            ('4', 2, 0, 1, '#333333'), ('5', 2, 1, 1, '#333333'), ('6', 2, 2, 1, '#333333'), ('-', 2, 3, 1, '#ff9500'),
            ('1', 3, 0, 1, '#333333'), ('2', 3, 1, 1, '#333333'), ('3', 3, 2, 1, '#333333'), ('+', 3, 3, 1, '#ff9500'),
            ('0', 4, 0, 2, '#333333'), ('.', 4, 2, 1, '#333333'), ('=', 4, 3, 1, '#ff9500'),
        ]
        
        # 버튼 크기 설정
        button_size = QSize(80, 80)
        zero_button_size = QSize(170, 80)

        # 버튼 생성 및 이벤트 연결
        for text, row, col, colspan, color in buttons:
            btn = QPushButton(text)
            
            # 버튼 텍스트 색상을 결정합니다. 'AC', '+/-', '%' 버튼은 검은색 글자를 사용합니다.
            text_color = "black" if text in ['AC', '+/-', '%'] else "white"

            style_sheet = f"""
                QPushButton {{
                    font-size: 30px;
                    background-color: {color};
                    border-radius: 40px;
                    color: {text_color};
                }}
                QPushButton:pressed {{
                    background-color: #d1d1d1;
                }}
            """
            
            # '0' 버튼은 너비를 더 넓게 설정합니다.
            if text == '0':
                btn.setFixedSize(zero_button_size)
            else:
                btn.setFixedSize(button_size)
            
            # 버튼 크기 정책을 무시하도록 설정
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setStyleSheet(style_sheet)
            
            # 버튼 폰트를 'Inter'로 설정
            btn_font = QFont("Inter", 30)
            btn.setFont(btn_font)
            
            btn.clicked.connect(partial(self.handle_button, text))
            button_grid.addWidget(btn, row, col, 1, colspan)

    def handle_button(self, value):
        """
        버튼 클릭 이벤트를 처리하고 계산기 로직과 연결합니다.
        """
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
        self.adjust_font_size()

    def adjust_font_size(self):
        """
        입력된 텍스트 길이에 따라 글꼴 크기를 동적으로 조절합니다.
        """
        text = self.display.text()
        font = self.display.font()
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.width(text)
        
        max_width = self.display.width() * 0.9
        
        if text_width > max_width:
            new_font_size = font.pointSize() * max_width / text_width
            new_font = QFont("Inter", int(new_font_size))
            self.display.setFont(new_font)
        else:
            original_font = QFont("Inter", 80)
            self.display.setFont(original_font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec_())