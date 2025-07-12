import sys
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt


class EngineeringCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_expression = ""

    def initUI(self):
        self.setWindowTitle("iPhone Engineering Calculator UI")
        self.setFixedSize(600, 400)

        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet(
            "font-size: 28px; background: white; color: black; padding: 10px; border: 1px solid gray;"
        )
        self.display.setFixedHeight(60)

        vbox = QVBoxLayout()
        vbox.addWidget(self.display)

        # iPhone 가로모드 공학용 계산기의 기본 버튼 구성 일부 (좌우 정렬을 고려해 6열 구성)
        buttons = [
            ["2nd", "(", ")", "mc", "m+", "m-"],
            ["AC", "+/-", "%", "÷", "sin", "cos"],
            ["7", "8", "9", "×", "tan", "log"],
            ["4", "5", "6", "-", "ln", "√"],
            ["1", "2", "3", "+", "x²", "xʸ"],
            ["0", ".", "=", "", "", ""]
        ]

        grid = QGridLayout()
        for row, row_values in enumerate(buttons):
            for col, btn_text in enumerate(row_values):
                if btn_text == "":
                    continue
                btn = QPushButton(btn_text)
                btn.setFixedSize(80, 50)
                btn.setStyleSheet("font-size: 18px;")
                btn.clicked.connect(partial(self.button_clicked, btn_text)) # return each number value per button.
                grid.addWidget(btn, row, col)

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def button_clicked(self, value):
        if value == "AC":
            self.input_expression = ""
            self.display.setText("0")
        elif value == "=":
            # 계산 기능은 구현하지 않음
            pass
        else:
            self.input_expression += value
            self.display.setText(self.input_expression)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec_())
