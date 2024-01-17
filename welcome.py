#Welcome.py
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
        pass
    
    #######################################################################
    ##       FUNCTION THAT TAKES YOU TO THE CREATEACCOUNT SCREEN         ##
    #######################################################################
    def gotoCreateAccountScreen(self):
        pass



