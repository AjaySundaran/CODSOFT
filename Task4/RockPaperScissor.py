import sys
import random
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QMovie,QIcon,QImage,QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QTimer
import time

class RockPaperScissors(QtWidgets.QMainWindow):
    def __init__(self):
        super(RockPaperScissors, self).__init__()
        uic.loadUi('./Src/Game.ui', self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.user_score = 0
        self.computer_score = 0
        
        self.btnRock_1.clicked.connect(lambda: self.play('rock'))
        self.btnPaper_1.clicked.connect(lambda: self.play('paper'))
        self.btnScissors_1.clicked.connect(lambda: self.play('scissors'))
        self.btnPlayAgain.clicked.connect(self.reset_game)

        self.close_btn.clicked.connect(self.close_event)
        
        self.show()
        
    def play(self, user_choice):
        choices = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(choices)

        if 'rock' in computer_choice:
            image_source = "./Src/stone.png"
        elif 'paper' in computer_choice:
            image_source = "./Src/paper.png"
        else:
            image_source = "./Src/scissor.png"


        self.image.setPixmap(QPixmap("./Src/blank.png"))
        
        self.image.setScaledContents(True)
        self.image.setPixmap(QPixmap(image_source))
        
        self.labelComputerChoice.setText(f"{computer_choice.capitalize()}")
        
        if user_choice == computer_choice:
            result = "It's a tie!"
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'scissors' and computer_choice == 'paper') or \
             (user_choice == 'paper' and computer_choice == 'rock'):
            result = "You win!"
            self.user_score += 1
        else:
            result = "You lose!"
            self.computer_score += 1
        
        self.labelResult.setText(f"Result: {result}")
        self.labelUserScore.setText(f"User Score: {self.user_score}")
        self.labelComputerScore.setText(f"Computer Score: {self.computer_score}")
        
    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.labelComputerChoice.setText("")
        self.labelResult.setText("Result: ")
        self.labelUserScore.setText("User Score: 0")
        self.labelComputerScore.setText("Computer Score: 0")
        self.image.setPixmap(QPixmap("./Src/blank.png"))

    def close_event(self):
        self.close()

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

app = QtWidgets.QApplication(sys.argv)
window = RockPaperScissors()
sys.exit(app.exec_())
