import sys
import os
import csv
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog, QListWidgetItem
from PyQt5.QtGui import QMovie,QIcon,QImage,QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent

# Load UIs
MainWindowUI = './Src/main_window.ui'
AddContactUI = './Src/add_contact.ui'
UpdateContactUI = './Src/update_contact.ui'
CSV_FILE = './Src/contacts.csv'


class ContactManager(QtWidgets.QMainWindow):
    def __init__(self):
        super(ContactManager, self).__init__()
        uic.loadUi(MainWindowUI, self)
        self.check_and_create_csv()
        self.load_contacts()
        self.setup_connections()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)

        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=90)
        self.bg_2.setGraphicsEffect(self.effect)

        self.image.setScaledContents(True)
        self.image.setPixmap(QPixmap("./Src/Contact.png"))
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

    def check_and_create_csv(self):
        if not os.path.isfile(CSV_FILE):
            with open(CSV_FILE, 'w', newline='') as csvfile:
                fieldnames = ['Store Name', 'Phone Number', 'Email', 'Address']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def setup_connections(self):
        self.addButton.clicked.connect(self.add_contact)
        self.updateButton.clicked.connect(self.update_contact)
        self.deleteButton.clicked.connect(self.delete_contact)
        self.searchButton.clicked.connect(self.search_contact)
        self.contactListWidget.itemDoubleClicked.connect(self.view_contact_details)

    def load_contacts(self):
        self.contactListWidget.clear()
        with open(CSV_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item = QListWidgetItem(f"{row['Store Name']} - {row['Phone Number']}")
                item.setData(1, row)
                self.contactListWidget.addItem(item)

    def add_contact(self):
        dialog = AddContactDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_contacts()

    def update_contact(self):
        selected_item = self.contactListWidget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Warning", "No contact selected!")
            return
        dialog = UpdateContactDialog(self, selected_item.data(1))
        if dialog.exec_() == QDialog.Accepted:
            self.load_contacts()

    def delete_contact(self):
        selected_item = self.contactListWidget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Warning", "No contact selected!")
            return

        contacts = self.get_all_contacts()
        contacts = [c for c in contacts if c['Phone Number'] != selected_item.data(1)['Phone Number']]
        self.save_all_contacts(contacts)
        self.load_contacts()

    def search_contact(self):
        search_term = self.searchLineEdit.text().lower()
        self.contactListWidget.clear()
        with open(CSV_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if search_term in row['Store Name'].lower() or search_term in row['Phone Number']:
                    item = QListWidgetItem(f"{row['Store Name']} - {row['Phone Number']}")
                    item.setData(1, row)
                    self.contactListWidget.addItem(item)

    def view_contact_details(self, item):
        contact = item.data(1)
        QMessageBox.information(self, "Contact Details", f"Store Name: {contact['Store Name']}\n"
                                                         f"Phone Number: {contact['Phone Number']}\n"
                                                         f"Email: {contact['Email']}\n"
                                                         f"Address: {contact['Address']}")

    def get_all_contacts(self):
        contacts = []
        with open(CSV_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                contacts.append(row)
        return contacts

    def save_all_contacts(self, contacts):
        with open(CSV_FILE, 'w', newline='') as csvfile:
            fieldnames = ['Store Name', 'Phone Number', 'Email', 'Address']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact)


class AddContactDialog(QDialog):
    def __init__(self, parent=None):
        super(AddContactDialog, self).__init__(parent)
        uic.loadUi(AddContactUI, self)
        self.saveButton.clicked.connect(self.save_contact)


        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)
        
        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=50)
        self.bg2.setGraphicsEffect(self.effect)

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

    def save_contact(self):
        store_name = self.storeNameLineEdit.text()
        phone_number = self.phoneNumberLineEdit.text()
        email = self.emailLineEdit.text()
        address = self.addressLineEdit.text()
        if not store_name or not phone_number or not email or not address:
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        with open(CSV_FILE, 'a', newline='') as csvfile:
            fieldnames = ['Store Name', 'Phone Number', 'Email', 'Address']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'Store Name': store_name,
                'Phone Number': phone_number,
                'Email': email,
                'Address': address
            })
        self.accept()


class UpdateContactDialog(QDialog):
    def __init__(self, parent=None, contact=None):
        super(UpdateContactDialog, self).__init__(parent)
        uic.loadUi(UpdateContactUI, self)
        self.contact = contact
        self.load_contact_details()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)
        
        self.effect = QtWidgets.QGraphicsBlurEffect(blurRadius=50)
        self.bg2.setGraphicsEffect(self.effect)
        
        self.saveButton.clicked.connect(self.save_contact)
        self.close_btn.clicked.connect(self.close_event)

    def close_event(self):
        self.close()

    def load_contact_details(self):
        self.storeNameLineEdit.setText(self.contact['Store Name'])
        self.phoneNumberLineEdit.setText(self.contact['Phone Number'])
        self.emailLineEdit.setText(self.contact['Email'])
        self.addressLineEdit.setText(self.contact['Address'])

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

    def save_contact(self):
        store_name = self.storeNameLineEdit.text()
        phone_number = self.phoneNumberLineEdit.text()
        email = self.emailLineEdit.text()
        address = self.addressLineEdit.text()
        if not store_name or not phone_number or not email or not address:
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        contacts = self.parent().get_all_contacts()
        for contact in contacts:
            if contact['Phone Number'] == self.contact['Phone Number']:
                contact['Store Name'] = store_name
                contact['Phone Number'] = phone_number
                contact['Email'] = email
                contact['Address'] = address
                break
        self.parent().save_all_contacts(contacts)
        self.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ContactManager()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
