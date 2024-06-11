import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import uic

class Calculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Calculator.ui', self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=60)
        self.bg.setGraphicsEffect(self.effect)
        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=70)
        self.b2.setGraphicsEffect(self.effect)

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=20)
        self.number1.setGraphicsEffect(self.effect)

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=20)
        self.number2.setGraphicsEffect(self.effect)
        

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=1.5)
        self.pushButton_calculate.setGraphicsEffect(self.effect)

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=1.5)
        self.comboBox_operation.setGraphicsEffect(self.effect)


        self.pushButton_calculate.clicked.connect(self.calculate_result)
        self.close_btn.clicked.connect(self.close_event)

    def close_event(self):
        self.close()

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()
        
        
    def calculate_result(self):
        number1 = float(self.lineEdit_number1.text())
        number2 = float(self.lineEdit_number2.text())
        operation = self.comboBox_operation.currentText()
        
        if operation == '+':
            result = number1 + number2
        elif operation == '-':
            result = number1 - number2
        elif operation == '*':
            result = number1 * number2
        elif operation == '/':
            if number2 != 0:
                result = number1 / number2
            else:
                result = 'Error: Division by zero'
        else:
            result = 'Invalid Operation'
        
        self.label_result.setText(f'{result}')

app = QtWidgets.QApplication(sys.argv)
calculator = Calculator()
calculator.show()
sys.exit(app.exec_())
