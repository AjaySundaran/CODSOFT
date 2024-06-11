import sys
import random
import string
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import uic
from PyQt5.QtGui import QMovie,QIcon,QImage,QPixmap

class Password(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Src/Password_Generator.ui', self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=50)
        self.bg_blue.setGraphicsEffect(self.effect)

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=80)
        self.ft_blue.setGraphicsEffect(self.effect)

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=80)
        self.bg_blue_big.setGraphicsEffect(self.effect)

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=200)
        self.bg_blue_big_2.setGraphicsEffect(self.effect)

        


        self.image1.setScaledContents(True)
        self.image1.setPixmap(QPixmap("./Src/image1.png"))

        self.generateButton.clicked.connect(self.generate_password)
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

    def generate_password(self):
        # Get the desired length from the input field
        length = self.lineEdit.text()
        
        if length.isdigit():
            length = int(length)
            # Define the characters to use in the password
            characters = string.ascii_letters + string.digits + string.punctuation
            # Generate the password
            password = ''.join(random.choice(characters) for _ in range(length))
            # Display the password in the text edit field
            self.textEdit.setText(password)
        else:
            self.textEdit.setText("Please enter a valid number for the length.")
        
        
   

app = QtWidgets.QApplication(sys.argv)
password = Password()
password.show()
sys.exit(app.exec_())
