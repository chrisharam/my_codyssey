import sys
import math
import random
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QFontMetrics

class EngineeringCalculator(QWidget):
    """
    아이폰 가로모드 공학용 계산기와 유사한 UI를 구현하는 클래스입니다.
    """
    def __init__(self):
        super().__init__()
        self.input_expression = ""
        self.display_text = "0"
        self.last_was_operator = False
        self.is_deg = True  # True: Degree, False: Radian
        self.memory = 0.0

        self.initUI()

    def initUI(self):
        """
        UI를 초기화하고 레이아웃을 설정합니다.
        """
        self.setWindowTitle("iPhone Engineering Calculator UI")
        self.setFixedSize(700, 400)  # 창 크기를 이미지에 맞게 조정
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
        
        # 숫자 및 소수점 입력 처리
        if value.isdigit() or value == ".":
            if self.display_text == "0" or self.last_was_operator:
                self.display_text = value
            else:
                self.display_text += value
            self.input_expression += value
            self.last_was_operator = False
        
        # 'AC' (All Clear)
        elif value == "AC":
            self.input_expression = ""
            self.display_text = "0"
            self.last_was_operator = False
            self.memory = 0.0

        # 괄호 입력
        elif value in ["(", ")"]:
            self.input_expression += value
            self.display_text += value

        # 기본 연산자
        elif value in operators:
            if self.input_expression and self.input_expression[-1] in ["*", "/", "-", "+"]:
                self.input_expression = self.input_expression[:-1] + value.replace("×", "*").replace("÷", "/")
                self.display_text = self.display_text[:-1] + value
            else:
                self.input_expression += value.replace("×", "*").replace("÷", "/")
                self.display_text += value
            self.last_was_operator = True

        # '=' (결과 계산)
        elif value == "=":
            try:
                # 'y√x'와 'xʸ'의 특수 문자열을 Python 연산자로 변환
                temp_expression = self.input_expression.replace("y**", "**(1/").replace(")**", ")*")
                result = eval(temp_expression)
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""
            self.last_was_operator = False

        # '+/-' (부호 변경)
        elif value == "+/-":
            try:
                current_value = eval(self.input_expression)
                result = -current_value
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""
        
        # '%' (퍼센트)
        elif value == "%":
            try:
                result = eval(self.input_expression) / 100
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""

        # 제곱 (x²)
        elif value == "x²":
            try:
                result = eval(self.input_expression) ** 2
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""
        
        # 세제곱 (x³)
        elif value == "x³":
            try:
                result = eval(self.input_expression) ** 3
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""

        # 거듭제곱 (xʸ)
        elif value == "xʸ":
            self.input_expression += "**"
            self.display_text += "ʸ"
            self.last_was_operator = True

        # eˣ
        elif value == "eˣ":
            try:
                result = math.exp(eval(self.input_expression))
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""

        # 10ˣ
        elif value == "10ˣ":
            try:
                result = 10 ** eval(self.input_expression)
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""
        
        # 역수 (¹/x)
        elif value == "¹/x":
            try:
                result = 1 / eval(self.input_expression)
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""

        # 제곱근 (√x)
        elif value == "√x":
            try:
                result = math.sqrt(eval(self.input_expression))
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""

        # 세제곱근 (∛x)
        elif value == "∛x":
            try:
                result = eval(self.input_expression) ** (1/3)
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""
        
        # y제곱근 (y√x)
        elif value == "y√x":
            self.input_expression += "y**"  # y와 ** 사이에 구분자를 추가
            self.display_text += "ʸ√"
            self.last_was_operator = True

        # 삼각함수
        elif value in ["sin", "cos", "tan", "sinh", "cosh", "tanh"]:
            try:
                val = eval(self.input_expression)
                if self.is_deg:
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
        
        # 자연로그 (ln)
        elif value == "ln":
            try:
                result = math.log(eval(self.input_expression))
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""

        # 상용로그 (log₁₀)
        elif value == "log₁₀":
            try:
                result = math.log10(eval(self.input_expression))
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""
        
        # 자연 상수 (e)
        elif value == "e":
            self.input_expression += str(math.e)
            self.display_text += "e"
        
        # EE (지수)
        elif value == "EE":
            self.input_expression += "e"
            self.display_text += "e"

        # 파이 (π)
        elif value == "π":
            self.input_expression += str(math.pi)
            self.display_text += "π"

        # 팩토리얼 (x!)
        elif value == "x!":
            try:
                result = math.factorial(int(eval(self.input_expression)))
                self.display_text = str(result)
                self.input_expression = str(result)
            except Exception as e:
                self.display_text = "Error"
                self.input_expression = ""

        # 랜덤 (Rand)
        elif value == "Rand":
            result = random.random()
            self.display_text = str(result)
            self.input_expression = str(result)
        
        # 각도/라디안 전환 (Deg/Rad)
        elif value == "Deg":
            self.is_deg = not self.is_deg
            self.rad_label.setText("Deg" if self.is_deg else "Rad")

        # 메모리 기능
        elif value == "m+":
            try:
                self.memory += eval(self.input_expression)
            except Exception as e:
                self.display_text = "Error"
        elif value == "m-":
            try:
                self.memory -= eval(self.input_expression)
            except Exception as e:
                self.display_text = "Error"
        elif value == "mc":
            self.memory = 0.0
        elif value == "mr":
            self.input_expression = str(self.memory)
            self.display_text = str(self.memory)
            self.last_was_operator = False

        self.display.setText(self.display_text)
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
            original_font = QFont("Inter", 50)
            self.display.setFont(original_font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec_())