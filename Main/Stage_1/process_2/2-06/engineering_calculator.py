import sys
import math
import random
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QFontMetrics

# Calculator 클래스는 기본적인 사칙연산 및 계산기 기능을 담당합니다.
class Calculator:
    """
    기본적인 사칙연산 및 계산기 로직을 담당하는 부모 클래스입니다.
    """
    def __init__(self):
        self.input_expression = ""
        self.display_text = "0"
        self.last_was_operator = False
        self.memory = 0.0

    def _handle_number_input(self, value):
        """숫자 및 소수점 입력을 처리합니다."""
        if self.display_text == "0" or self.last_was_operator:
            self.display_text = value
        else:
            self.display_text += value
        self.input_expression += value
        self.last_was_operator = False

    def _handle_operator_input(self, value):
        """기본 연산자 입력을 처리합니다."""
        if self.input_expression and self.input_expression[-1] in ["*", "/", "-", "+"]:
            self.input_expression = self.input_expression[:-1] + value.replace("×", "*").replace("÷", "/")
            self.display_text = self.display_text[:-1] + value
        else:
            self.input_expression += value.replace("×", "*").replace("÷", "/")
            self.display_text += value
        self.last_was_operator = True

    def _handle_equals(self):
        """결과를 계산합니다."""
        try:
            # y√x와 xʸ의 특수 문자열을 Python 연산자로 변환
            temp_expression = self.input_expression.replace("y**", "**(1/").replace(")**", ")*")
            result = eval(temp_expression)
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""
        self.last_was_operator = False

    def _handle_clear(self):
        """모든 값을 초기화합니다."""
        self.input_expression = ""
        self.display_text = "0"
        self.last_was_operator = False
        self.memory = 0.0

    def _handle_sign_change(self):
        """현재 값의 부호를 변경합니다."""
        try:
            current_value = eval(self.input_expression)
            result = -current_value
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _handle_percentage(self):
        """현재 값의 퍼센트를 계산합니다."""
        try:
            result = eval(self.input_expression) / 100
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

class EngineeringCalculator(QWidget, Calculator):
    """
    Calculator 클래스를 상속받아 공학용 계산기 UI 및 기능을 구현하는 클래스입니다.
    """
    def __init__(self):
        # 부모 클래스의 생성자를 호출하여 초기화합니다.
        QWidget.__init__(self)
        Calculator.__init__(self)
        
        self.is_deg = True  # True: Degree, False: Radian

        self.initUI()

    def initUI(self):
        """
        UI를 초기화하고 레이아웃을 설정합니다.
        """
        self.setWindowTitle("iPhone Engineering Calculator UI")
        self.setFixedSize(700, 400)
        self.setStyleSheet("background-color: #1c1c1c; color: white;")

        # 결과 표시 라벨
        self.display = QLabel(self.display_text)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet(
            "font-size: 50px; padding: 10px; border: none;"
        )
        self.display.setFixedHeight(80)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        
        # 'Rad'/'Deg' 라벨 추가
        self.rad_label = QLabel("Deg")
        self.rad_label.setStyleSheet("font-size: 15px; color: #a6a6a6; margin-left: 20px;")
        self.rad_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 상단 라벨과 디스플레이를 위한 가로 레이아웃
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.rad_label)
        top_layout.addWidget(self.display)
        top_layout.setSpacing(0)
        
        main_layout.addLayout(top_layout)
        
        button_grid = QGridLayout()
        button_grid.setSpacing(5)
        
        # 이미지에 정확히 맞춰서 버튼 위치를 정의
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
            ("¹/x", 2, 0), ("√x", 2, 1), ("∛x", 2, 2), ("y√x", 2, 3), 
            ("ln", 2, 4), ("log₁₀", 2, 5), ("4", 2, 6), ("5", 2, 7), 
            ("6", 2, 8), ("-", 2, 9),
            # 3행
            ("x!", 3, 0), ("sin", 3, 1), ("cos", 3, 2), ("tan", 3, 3), 
            ("e", 3, 4), ("EE", 3, 5), ("1", 3, 6), ("2", 3, 7),
            ("3", 3, 8), ("+", 3, 9),
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
            elif btn_text in ["AC", "+/-", "%", "2nd", "Deg"]:
                color = "#a6a6a6"
                text_color = "black"
            else:
                color = "#505050"
                text_color = "white"
            
            # '0' 버튼은 가로로 두 칸 차지
            if btn_text == "0":
                grid_width = 2
                btn.setFixedSize(QSize(115, 50))
            else:
                grid_width = 1
                btn.setFixedSize(QSize(50, 50))

            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 20px;
                    background-color: {color};
                    border-radius: 25px;
                    color: {text_color};
                }}
                QPushButton:pressed {{
                    background-color: #d1d1d1;
                }}
            """)
            
            button_grid.addWidget(btn, row, col, 1, grid_width)
            btn.clicked.connect(partial(self.button_clicked, btn_text))

        main_layout.addLayout(button_grid)
        self.setLayout(main_layout)

    def button_clicked(self, value):
        """
        버튼 클릭 시 호출되는 메서드로, 계산 로직을 처리하고 화면에 표시합니다.
        """
        operators = ["÷", "×", "-", "+"]

        if value.isdigit() or value == ".":
            self._handle_number_input(value)
        elif value in operators:
            self._handle_operator_input(value)
        elif value == "AC":
            self._handle_clear()
        elif value == "=":
            self._handle_equals()
        elif value == "+/-":
            self._handle_sign_change()
        elif value == "%":
            self._handle_percentage()
        elif value == "x²":
            self._calculate_square()
        elif value == "x³":
            self._calculate_cube()
        elif value in ["sin", "cos", "tan", "sinh", "cosh", "tanh"]:
            self._calculate_trigonometric(value)
        elif value == "π":
            self._insert_pi()
        elif value == "xʸ":
            self.input_expression += "**"
            self.display_text += "ʸ"
            self.last_was_operator = True
        elif value == "eˣ":
            self._calculate_exp()
        elif value == "10ˣ":
            self._calculate_10_exp()
        elif value == "¹/x":
            self._calculate_reciprocal()
        elif value == "√x":
            self._calculate_sqrt()
        elif value == "∛x":
            self._calculate_cbrt()
        elif value == "y√x":
            self.input_expression += "y**"  # y와 ** 사이에 구분자를 추가
            self.display_text += "ʸ√"
            self.last_was_operator = True
        elif value == "ln":
            self._calculate_ln()
        elif value == "log₁₀":
            self._calculate_log10()
        elif value == "x!":
            self._calculate_factorial()
        elif value == "e":
            self._insert_e()
        elif value == "EE":
            self.input_expression += "e"
            self.display_text += "e"
        elif value == "Rand":
            self._generate_random()
        elif value == "Deg":
            self._toggle_degree_radian()
        elif value == "m+":
            self._add_to_memory()
        elif value == "m-":
            self._subtract_from_memory()
        elif value == "mc":
            self._clear_memory()
        elif value == "mr":
            self._recall_memory()
        elif value in ["(", ")"]:
            self.input_expression += value
            self.display_text += value

        self.display.setText(self.display_text)
        self.adjust_font_size()

    # --- 요청된 기능 구현 메소드 ---
    def _calculate_square(self):
        """x의 제곱(x²)을 계산합니다."""
        try:
            result = eval(self.input_expression) ** 2
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _calculate_cube(self):
        """x의 세제곱(x³)을 계산합니다."""
        try:
            result = eval(self.input_expression) ** 3
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _calculate_trigonometric(self, value):
        """삼각함수(sin, cos, tan) 및 쌍곡선 삼각함수(sinh, cosh, tanh)를 계산합니다."""
        try:
            val = eval(self.input_expression)
            if self.is_deg and value in ["sin", "cos", "tan"]:
                val = math.radians(val)
            
            if value == "sin":
                result = math.sin(val)
            elif value == "cos":
                result = math.cos(val)
            elif value == "tan":
                result = math.tan(val)
            elif value == "sinh":
                result = math.sinh(val)
            elif value == "cosh":
                result = math.cosh(val)
            elif value == "tanh":
                result = math.tanh(val)

            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _insert_pi(self):
        """원주율(π)을 입력합니다."""
        self.input_expression = str(math.pi)
        self.display_text = "π"
        self.last_was_operator = False

    # --- 기타 공학용 기능 구현 메소드 ---
    def _calculate_exp(self):
        """eˣ를 계산합니다."""
        try:
            result = math.exp(eval(self.input_expression))
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _calculate_10_exp(self):
        """10ˣ를 계산합니다."""
        try:
            result = 10 ** eval(self.input_expression)
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _calculate_reciprocal(self):
        """역수(¹/x)를 계산합니다."""
        try:
            result = 1 / eval(self.input_expression)
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _calculate_sqrt(self):
        """제곱근(√x)을 계산합니다."""
        try:
            result = math.sqrt(eval(self.input_expression))
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _calculate_cbrt(self):
        """세제곱근(∛x)을 계산합니다."""
        try:
            result = eval(self.input_expression) ** (1/3)
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""
    
    def _calculate_ln(self):
        """자연로그(ln)를 계산합니다."""
        try:
            result = math.log(eval(self.input_expression))
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _calculate_log10(self):
        """상용로그(log₁₀)를 계산합니다."""
        try:
            result = math.log10(eval(self.input_expression))
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""

    def _calculate_factorial(self):
        """팩토리얼(x!)을 계산합니다."""
        try:
            result = math.factorial(int(eval(self.input_expression)))
            self.display_text = str(result)
            self.input_expression = str(result)
        except Exception as e:
            self.display_text = "Error"
            self.input_expression = ""
    
    def _insert_e(self):
        """자연 상수(e)를 입력합니다."""
        self.input_expression = str(math.e)
        self.display_text = "e"
        self.last_was_operator = False

    def _generate_random(self):
        """무작위 수를 생성합니다."""
        result = random.random()
        self.display_text = str(result)
        self.input_expression = str(result)
    
    def _toggle_degree_radian(self):
        """각도/라디안 모드를 전환합니다."""
        self.is_deg = not self.is_deg
        self.rad_label.setText("Deg" if self.is_deg else "Rad")

    def _add_to_memory(self):
        """메모리에 현재 값을 더합니다."""
        try:
            self.memory += eval(self.input_expression)
        except Exception as e:
            self.display_text = "Error"
    
    def _subtract_from_memory(self):
        """메모리에서 현재 값을 뺍니다."""
        try:
            self.memory -= eval(self.input_expression)
        except Exception as e:
            self.display_text = "Error"

    def _clear_memory(self):
        """메모리 값을 0으로 초기화합니다."""
        self.memory = 0.0

    def _recall_memory(self):
        """메모리에 저장된 값을 불러옵니다."""
        self.input_expression = str(self.memory)
        self.display_text = str(self.memory)
        self.last_was_operator = False

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
            original_font = QFont("Inter", 50)
            self.display.setFont(original_font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec_())