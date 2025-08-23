import sys
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class EngineeringCalculator(QWidget):
    """
    아이폰 가로모드 공학용 계산기와 유사한 UI를 구현하는 클래스입니다.
    """
    def __init__(self):
        super().__init__()
        self.input_expression = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("iPhone Engineering Calculator UI")
        self.setFixedSize(700, 400)  # 창 크기를 이미지에 맞게 조정
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

        # 상단 라벨과 디스플레이를 위한 가로 레이아웃
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
            btn.clicked.connect(partial(self.button_clicked, btn_text))

        main_layout.addLayout(button_grid)
        self.setLayout(main_layout)

    def button_clicked(self, value):
        """
        버튼 클릭 시 호출되는 메서드로, 화면에 텍스트를 추가합니다.
        """
        if value == "AC":
            self.input_expression = ""
            self.display.setText("0")
        else:
            self.input_expression += value
            self.display.setText(self.input_expression)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec_())