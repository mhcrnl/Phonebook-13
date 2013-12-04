#!/usr/bin/env python

import shelve
import sys

phonebook = shelve.open("phonebook.shelve")

options = { 'new':'creates a new contact',
           'search': 'searches for an existing contact',
           'delete': 'deletes a contact',
           'edit': 'edits an existing contact' }

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
        print "Error: no option entered"

def new():
    """Create a new contact."""
    name = raw_input("Enter name of contact: ")
    for contact in phonebook:
        if contact == name:
            print "Contact already exists."
            print "To edit this contact, try the 'edit' option"
            return
    num = raw_input("Enter contact number: ")
    phonebook[name] = num
    print "Contact successfully created."

def search():
    """Search for an existing contact."""
    name = raw_input("Enter name of contact to get contact number: ")
    for contact in phonebook:
        if contact == name:
            print phonebook[contact]
            return
    print "Contact not found."

def delete():
    """Delete a contact."""
    name = raw_input("Enter name of contact to delete: ")
    for contact in phonebook:
        if contact == name:
            del phonebook[name]
            print "Contact successfully deleted."
            return
    print "Contact not found."
    
def edit():
    """Edit an existing contact"""
    name = raw_input("Enter name of contact to edit: ")
    for contact in phonebook:
        if contact == name:
            new_num = raw_input("Enter new number: ")
            phonebook[name] = new_num
            print "Contact successfully edited."
            return
    print "Contact not found."

def main():
    option = get_user_option()
    if option == "new": new()
    elif option == "search": search()
    elif option == "delete": delete()
    elif option == "edit": edit()

if __name__ == "__main__": main()