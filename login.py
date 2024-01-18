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
        pass
    

    #####################################################################################
    ##             FUNCTION CHECKS IF THE INPUT FIELD HAVE BEEN ENTERED ALL            ##
    #####################################################################################

    def checkInputFields(self, username, password):
        try:   
            if not username or not password:
                if not username:
                    self.login_error_label.setText("Username is required!")
                elif not password:
                    self.login_error_label.setText("Password is required!")
                    return False
                return True
        except Exception as e:
            print(f"Error in checkInputFields method: {str(e)}")
            return False

    #####################################################################################
    ##                  LOGIN FUNCTION THAT LEADS TO THE MAINPAGE                      ##
    #####################################################################################

    def Login(self):
        pass
