#Welcome.py
import sys
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PyQt5.uic import loadUi
from login import LoginScreen
from CreateAccount import CreateAccountScreen
import myimages


class WelcomeScreen(QMainWindow):
    def __init__(self, widget):
        super(WelcomeScreen, self).__init__()
        loadUi("Welcome.ui", self)
        self.widget = widget

        ### CONNECTING THE LOGIN BUTTON THAT LEADS TO THE LOGIN SCREEN ###
        self.Login_pushButton.clicked.connect(self.gotologinScreen)

        ### CONNECTING THE LOGIN BUTTON THAT LEADS TO THE LOGIN SCREEN ###
        self.CreateAccount_pushButton.clicked.connect(self.gotoCreateAccountScreen)

    #######################################################################
    ##            FUNCTION THAT TAKES YOU TO THE LOGIN SCREEN            ##
    #######################################################################
    def gotologinScreen(self):
        loginscreen = LoginScreen(self.widget)
        self.widget.addWidget(loginscreen)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    
    #######################################################################
    ##       FUNCTION THAT TAKES YOU TO THE CREATEACCOUNT SCREEN         ##
    #######################################################################
    def gotoCreateAccountScreen(self):
        createaccountscreen = CreateAccountScreen(self.widget)
        self.widget.addWidget(createaccountscreen)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)



