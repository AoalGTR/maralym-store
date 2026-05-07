import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

# ---------------- MODEL ----------------
class Calculator:
    def __init__(self):
        self.expression = ""

    def add_to_expression(self, char):
        self.expression += char

    def remove_last_character(self):
        self.expression = self.expression[:-1]

    def clear_expression(self):
        self.expression = ""

    def calculate(self):
        try:
            result = eval(self.expression)
            return result
        except ZeroDivisionError:
            return "Error"
        except:
            return "Error"

    def get_expression(self):
        return self.expression


# ---------------- VIEW + CONTROLLER ----------------
class CalculatorWindow(QWidget):
    def __init__(self, calculator):
        super().__init__()

        self.calculator = calculator
        self.setWindowTitle("Calculator")
        self.setFixedSize(300, 380)

        # ---- MAIN STYLE ----
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
            }

            QLineEdit {
                background-color: #b6d1b0;
                border-radius: 12px;
                padding: 10px;
                font-size: 22px;
                color: black;
            }

            QPushButton {
                background-color: #e5e5e5;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                color: black;
            }

            QPushButton:hover {
                background-color: #d6d6d6;
            }

            QPushButton#equalBtn {
                background-color: orange;
                color: white;
                font-size: 20px;
            }

            QPushButton#equalBtn:hover {
                background-color: #ff9800;
            }
        """)

        # ---- DISPLAY ----
        self.input = QLineEdit()
        self.input.setAlignment(Qt.AlignRight)
        self.input.setReadOnly(True)
        self.input.setFixedHeight(60)

        # ---- LAYOUTS ----
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input)

        grid = QGridLayout()

        buttons = [
            ('7',0,0), ('8',0,1), ('9',0,2), ('/',0,3),
            ('4',1,0), ('5',1,1), ('6',1,2), ('*',1,3),
            ('1',2,0), ('2',2,1), ('3',2,2), ('-',2,3),
            ('0',3,0), ('C',3,1), ('=',3,2), ('+',3,3),
        ]

        self.buttons = {}

        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedSize(60,60)

            if text == "=":
                button.setObjectName("equalBtn")

            grid.addWidget(button, row, col)
            self.buttons[text] = button

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

        # ---- CONNECT ----
        for key, button in self.buttons.items():
            button.clicked.connect(lambda checked, k=key: self.on_button_click(k))

    def on_button_click(self, key):

        if key == "C":
            self.calculator.clear_expression()
            self.input.setText("")

        elif key == "=":
            result = self.calculator.calculate()
            self.input.setText(str(result))

            if isinstance(result, (int, float)):
                self.calculator.expression = str(result)
            else:
                self.calculator.clear_expression()

        else:
            self.calculator.add_to_expression(key)
            self.input.setText(self.calculator.get_expression())


# ---------------- MAIN ----------------
def main():
    app = QApplication(sys.argv)

    model = Calculator()
    window = CalculatorWindow(model)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()