#!/usr/bin/env python

import shelve
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

options = { 'new':'creates a new contact',
           'search': 'searches for an existing contact',
           'delete': 'deletes a contact',
           'edit': 'edits an existing contact' }

class PhonebookGUI(QtGui.QWidget):
    def __init__(self):
        super(PhonebookGUI, self).__init__()
        self.initUI()
    
    def initUI(self):
        
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.label = QtGui.QLabel("Choose action:", self)
        self.options = QtGui.QComboBox(self)
        self.options.addItem('Select')
        self.options.addItem('Add new contact')
        self.options.addItem('Edit existing contact')
        self.options.addItem('Delete contact')
        self.options.addItem('Search contact')
        self.options.move(50, 50)
        self.label.move(50, 10)
        
        self.options.activated[str].connect(self.onActivated)
        self.move(300, 300)
        self.setFixedSize(300, 175)
        self.setWindowTitle('Phonebook')
        self.show()
        
    def onActivated(self, text):
        if text == 'Add new contact':
            self.showNewDialog()
        elif text == 'Edit existing contact':
            self.showEditDialog()
        elif text == 'Delete contact':
            self.showDeleteDialog()
        elif text == 'Search contact':
            self.showSearchDialog()

    def showNewDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'New contact', 'Enter new name:')
        if ok:
            new_contact = str(text).strip()
            if new_contact == '':
                self.showEmptyErrorDialog()
                return
            phonebook = shelve.open('phonebook.shelve')
            for contact in phonebook:
                if contact == new_contact:
                    QtGui.QMessageBox.information(self, 'Error', 'Contact already exists. To edit, try the edit option')
                    phonebook.close()
                    return
            text, ok = QtGui.QInputDialog.getText(self, 'New number', 'Enter new number:')
            if ok:
                new_number = str(text).strip()
                if new_number == '':
                    self.showEmptyErrorDialog()
                    phonebook.close()
                    return
                phonebook[new_contact] = new_number
                QtGui.QMessageBox.information(self, 'Result', 'Contact successfully added')
                phonebook.close()
                return
        
    def showSearchDialog(self):
        phonebook = shelve.open('phonebook.shelve')
        text, ok = QtGui.QInputDialog.getText(self, 'Search contact', 'Enter name of contact')
        if ok:
            search_contact = str(text).strip()
            if search_contact == '':
                self.showEmptyErrorDialog()
                return
            phonebook = shelve.open('phonebook.shelve')
            for contact in phonebook:
                if contact == search_contact:
                    QtGui.QMessageBox.information(self, 'Number', phonebook[contact])
                    phonebook.close()
                    return
            QtGui.QMessageBox.information(self, 'Error', 'Contact not found')
            phonebook.close()
            return

    def showDeleteDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Delete contact', 'Enter name of contact')
        if ok:
            delete_contact = str(text).strip()
            if delete_contact == '':
                self.showEmptyErrorDialog()
                return
            phonebook = shelve.open('phonebook.shelve')
            for contact in phonebook:
                if contact == delete_contact:
                    del phonebook[delete_contact]
                    QtGui.QMessageBox.information(self, 'Result', 'Contact successfully deleted')
                    phonebook.close()
                    return
            QtGui.QMessageBox.information(self, 'Error', 'Contact not found')
            phonebook.close()
            return

    def showEditDialog(self):
        phonebook = shelve.open('phonebook.shelve')
        text, ok = QtGui.QInputDialog.getText(self, 'Edit contact', 'Enter name of contact')
        if ok:
            edit_contact = str(text).strip()
            if edit_contact == '':
                self.showEmptyErrorDialog()
                return
            phonebook = shelve.open('phonebook.shelve')
            for contact in phonebook:
                if contact == edit_contact:
                    old_number = phonebook[contact]
                    text, ok = QtGui.QInputDialog.getText(self, 'New number', 'Enter new number:', text=old_number)
                    if ok:
                        new_number = str(text).strip()
                        if new_number == '':
                            self.showEmptyErrorDialog()
                            phonebook.close()
                            return
                        phonebook[edit_contact] = new_number
                        QtGui.QMessageBox.information(self, 'Result', 'Contact successfully edited')
                        phonebook.close()
                    return
            QtGui.QMessageBox.information(self, 'Error', 'Contact not found')
            phonebook.close()
            return
            
    def showEmptyErrorDialog(self):
        QtGui.QMessageBox.information(self, 'Error', 'The field cannot be empty')
            
class InvalidOptionError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def get_user_option():
    """Get the option from the user."""
    try:
        arg = sys.argv[1]
        try:
            if arg[0] == '-' and arg[1:] in options.keys():
                return arg[1:]
            else:
                raise InvalidOptionError("Sorry, wrong option. Please try again.")
        except InvalidOptionError as e:
            print e
    except IndexError:
        return 'gui'

def new():
    """Create a new contact."""
    phonebook = shelve.open('phonebook.shelve')
    name = raw_input("Enter name of contact: ")
    for contact in phonebook:
        if contact == name:
            print "Contact already exists."
            print "To edit this contact, try the 'edit' option"
            phonebook.close()
            return
    num = raw_input("Enter contact number: ")
    phonebook[name] = num
    print "Contact successfully created."
    phonebook.close()

def search():
    """Search for an existing contact."""
    phonebook = shelve.open('phonebook.shelve')
    name = raw_input("Enter name of contact to get contact number: ")
    for contact in phonebook:
        if contact == name:
            print phonebook[contact]
            phonebook.close()
            return
    print "Contact not found."
    phonebook.close()

def delete():
    """Delete a contact."""
    phonebook = shelve.open('phonebook.shelve')
    name = raw_input("Enter name of contact to delete: ")
    for contact in phonebook:
        if contact == name:
            del phonebook[name]
            print "Contact successfully deleted."
            phonebook.close()
            return
    print "Contact not found."
    phonebook.close()

def edit():
    """Edit an existing contact"""
    phonebook = shelve.open('phonebook.shelve')
    name = raw_input("Enter name of contact to edit: ")
    for contact in phonebook:
        if contact == name:
            new_num = raw_input("Enter new number: ")
            phonebook[name] = new_num
            print "Contact successfully edited."
            phonebook.close()
            return
    print "Contact not found."
    phonebook.close()

def main():
    option = get_user_option()
    if option == "gui":
        app = QtGui.QApplication(sys.argv)
        gui = PhonebookGUI()
        sys.exit(app.exec_())
    elif option == "new": new()
    elif option == "search": search()
    elif option == "delete": delete()
    elif option == "edit": edit()

if __name__ == "__main__": main()