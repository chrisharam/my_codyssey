# calculator.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Calculator Clone")
        self.setFixedSize(300, 400)
        self.initUI()

    def initUI(self):
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 30px; padding: 10px; background: white; border: 1px solid #ccc;")

        vbox = QVBoxLayout()
        vbox.addWidget(self.display)

        grid = QGridLayout()

        # 아이폰 계산기 버튼 배치
        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        # 버튼 추가
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                if btn_text == "0":
                    btn = QPushButton(btn_text)
                    btn.setFixedHeight(60)
                    btn.setStyleSheet("font-size: 18px;")
                    btn.clicked.connect(lambda _, b=btn_text: self.on_button_click(b))
                    grid.addWidget(btn, row_idx + 1, 0, 1, 2)  # 0은 가로로 2칸 차지
                elif btn_text == "." and len(row) == 3:
                    btn = QPushButton(btn_text)
                    btn.setFixedHeight(60)
                    btn.setStyleSheet("font-size: 18px;")
                    btn.clicked.connect(lambda _, b=btn_text: self.on_button_click(b))
                    grid.addWidget(btn, row_idx + 1, 2)
                elif btn_text == "=" and len(row) == 3:
                    btn = QPushButton(btn_text)
                    btn.setFixedHeight(60)
                    btn.setStyleSheet("font-size: 18px;")
                    btn.clicked.connect(lambda _, b=btn_text: self.on_button_click(b))
                    grid.addWidget(btn, row_idx + 1, 3)
                else:
                    btn = QPushButton(btn_text)
                    btn.setFixedSize(60, 60)
                    btn.setStyleSheet("font-size: 18px;")
                    btn.clicked.connect(lambda _, b=btn_text: self.on_button_click(b))
                    grid.addWidget(btn, row_idx + 1, col_idx)

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def on_button_click(self, value):
        if self.display.text() == "0" and value not in ["+", "-", "×", "÷", "%", "."]:
            self.display.setText(value)
        else:
            self.display.setText(self.display.text() + value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
