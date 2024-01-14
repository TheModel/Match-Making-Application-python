#Login.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from Mainpage import MainScreen
import sqlite3



class LoginScreen(QMainWindow):
    def __init__(self, widget):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)
        self.widget = widget

        ### HIDING THE PASSWORD FIELD ###
        self.Password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        ###### LOGIN BUTTON TRIGGER THAT LEADS TO MAINPAGE ####
        self.login_pushButton.clicked.connect(self.Login)
        

    ####################################################################################
    ##          FUNCTION THAT CHECKS IF THE USER INFO IS FOUND IN THE DATABASE        ##
    ####################################################################################

    def checkInfoinDatabase(self, username, password):
        self.conn = sqlite3.connect("usersInfo.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            SELECT Username, Email, Password, PhoneNumber, Age, Location, Gender from Users WHERE Username = ? AND Password = ?
                            ''',(username, password))
        result = self.cursor.fetchone()
        self.conn.close()
        return result
    

    #####################################################################################
    ##             FUNCTION CHECKS IF THE INPUT FIELD HAVE BEEN ENTERED ALL            ##
    #####################################################################################

    def checkInputFields(self, username, password):
        if not username or not password:
            if not username:
                self.login_error_label.setText("Username is required!")
            elif not password:
                self.login_error_label.setText("Password is required!")
            return False
        return True
    

    #####################################################################################
    ##                  LOGIN FUNCTION THAT LEADS TO THE MAINPAGE                      ##
    #####################################################################################

    def Login(self):
        username = self.Username_LineEdit.text()
        password = self.Password_LineEdit.text()

        if self.checkInputFields(username, password):
            result = self.checkInfoinDatabase(username, password)
            if result:
                mainpage = MainScreen(*result)
                mainpage.setUserProfile()
                self.widget.addWidget(mainpage)
                self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
            else:
                self.login_error_label.setText("Incorrect Username or Password")