import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontMetrics, QFont

class Calculator(QWidget):
    """
    iPhone 계산기와 유사한 디자인과 기능을 가진 PyQt5 계산기 애플리케이션.
    고정된 UI 크기를 갖습니다.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Calculator")
        self.setStyleSheet("background-color: #2e2e2e; color: white;")
        
        # 창 크기를 고정하여 UI가 변하지 않도록 설정
        self.setFixedSize(QSize(360, 600))
        
        self.initUI()

    def initUI(self):
        """
        UI를 초기화하고 레이아웃을 설정합니다.
        """
        # 결과 표시 라벨
        self.display = QLabel("0")
        self.display.setStyleSheet("""
            font-size: 80px;
            padding: 20px;
            qproperty-alignment: 'AlignRight | AlignVCenter';
        """)
        
        # 라벨의 크기를 고정하여 텍스트 길이에 따라 라벨이 늘어나지 않도록 합니다.
        self.display.setFixedHeight(120)
        
        # 전체 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.addWidget(self.display)
        
        # 버튼 레이아웃
        button_grid = QGridLayout()
        button_grid.setSpacing(10)

        # 버튼 데이터: (버튼 텍스트, 행, 열, 가로 병합, 배경색)
        buttons = [
            ('AC', 0, 0, 1, '#a6a6a6'), ('+/-', 0, 1, 1, '#a6a6a6'), ('%', 0, 2, 1, '#a6a6a6'), ('/', 0, 3, 1, '#ff9500'),
            ('7', 1, 0, 1, '#505050'), ('8', 1, 1, 1, '#505050'), ('9', 1, 2, 1, '#505050'), ('*', 1, 3, 1, '#ff9500'),
            ('4', 2, 0, 1, '#505050'), ('5', 2, 1, 1, '#505050'), ('6', 2, 2, 1, '#505050'), ('-', 2, 3, 1, '#ff9500'),
            ('1', 3, 0, 1, '#505050'), ('2', 3, 1, 1, '#505050'), ('3', 3, 2, 1, '#505050'), ('+', 3, 3, 1, '#ff9500'),
            ('0', 4, 0, 2, '#505050'), ('.', 4, 2, 1, '#505050'), ('=', 4, 3, 1, '#ff9500'),
        ]

        # 버튼 생성 및 이벤트 연결
        for text, row, col, colspan, color in buttons:
            btn = QPushButton(text)
            
            # 버튼 텍스트 색상을 결정합니다. 'AC', '+/-', '%' 버튼은 검은색 글자를 사용합니다.
            text_color = "black" if text in ['AC', '+/-', '%'] else "white"

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
            btn.clicked.connect(self.on_button_click)
            button_grid.addWidget(btn, row, col, 1, colspan)

        main_layout.addLayout(button_grid)
        self.setLayout(main_layout)

    def adjust_font_size(self):
        """
        입력된 텍스트 길이에 따라 글꼴 크기를 동적으로 조절합니다.
        """
        text = self.display.text()
        font = self.display.font()
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.width(text)
        
        # 디스플레이 너비의 90%를 텍스트가 차지할 수 있는 최대 너비로 설정
        max_width = self.display.width() * 0.9
        
        if text_width > max_width:
            new_font_size = font.pointSize() * max_width / text_width
            new_font = QFont(font.family(), int(new_font_size))
            self.display.setFont(new_font)
        else:
            # 텍스트가 줄어들면 원래 크기로 되돌립니다.
            original_font = QFont(font.family(), 80)
            self.display.setFont(original_font)
            
    def on_button_click(self):
        """
        버튼 클릭 시 호출되는 슬롯 메서드입니다.
        """
        btn_text = self.sender().text()
        current_text = self.display.text()

        if btn_text == 'AC':
            self.display.setText("0")
        elif btn_text == '+/-':
            if current_text != "0" and not current_text.startswith('Error'):
                if current_text.startswith('-'):
                    self.display.setText(current_text[1:])
                else:
                    self.display.setText('-' + current_text)
        elif btn_text == '%':
            try:
                result = str(float(eval(current_text)) / 100)
                self.display.setText(result)
            except Exception:
                self.display.setText("Error")
        elif btn_text == '=':
            try:
                result = str(eval(current_text))
                self.display.setText(result)
            except Exception:
                self.display.setText("Error")
        else:
            if current_text == "0" or current_text.startswith('Error'):
                self.display.setText(btn_text)
            else:
                self.display.setText(current_text + btn_text)
        
        self.adjust_font_size()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())