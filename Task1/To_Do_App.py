import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import uic

class TodoListApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('todo.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)


        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        
        self.addButton.clicked.connect(self.add_task)
        self.deleteButton.clicked.connect(self.delete_task)
        self.completeButton.clicked.connect(self.complete_task)
        self.close_btn.clicked.connect(self.close_event)

        
        self.show()

    def close_event(self):
        self.close()

    def add_task(self):
        task = self.taskLineEdit.text()
        date_time = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        if task:
            self.taskListWidget.addItem(f"{task} (Due: {date_time})")
            self.taskLineEdit.clear()

    def delete_task(self):
        selected_items = self.taskListWidget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.taskListWidget.takeItem(self.taskListWidget.row(item))

    def complete_task(self):
        selected_items = self.taskListWidget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            item.setCheckState(QtCore.Qt.Checked)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_list_app = TodoListApp()
    sys.exit(app.exec_())
