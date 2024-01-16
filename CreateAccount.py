#CreateAccount.py
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import re # for regular expressions and used to validate email
from PyQt5.uic import loadUi
from Mainpage import MainScreen
import sqlite3


class CreateAccountScreen(QMainWindow):
    def __init__(self, widget):
        super(CreateAccountScreen, self).__init__()
        loadUi("CreateAccount.ui", self)
        self.widget = widget

        #### HIDING PASSWORD FIELD IN THE CREATEACCOUNT PAGE ####
        self.Password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        #### SUBMIT BUTTON THAT LEADS TO THE MAINPAGE ####
        self.submit_Button.clicked.connect(self.Submit)

        ## BUTTTON TO UPLOAD A PICTURE ###
        self.Upload_Picture_button.clicked.connect(self.uploadImage)

    #########################################################################################
    ##      METHOD THAT VERIFIES IF THE USERNAME THE USER IS ENTERING IS NOT YET TAKEN     ##
    #########################################################################################
    def isUsernameTaken(self, username):
        pass


    ########################################################################################
    ##     METHOD TO CHECK IF THE USER INFO IS ENTERED IN THE CORRECT FORMAT              ##
    ########################################################################################
    def CheckInfo(self, username, email, password, age, phonenumber, location, gender):
        # Check if the information is in the correct format
        pass
    
    #############################################################################################
    ##      METHOD THAT STORES USER INFO IN THE DATABASE AFTER VALIDATION                      ##
    #############################################################################################

    def storeInDataBase(self, username, email, password, age, phonenumber, location,gender, image_path):
        pass

    ##############################################################################################
    ##        METHOD THAT ALLOWS USER TO UPLOAD AN IMAGE FOR HIS PROFILE                        ##
    ##############################################################################################

    def uploadImage(self):
        pass

    ####################################################################################################
    ##    THE FINAL SUBMIT BUTTON THAT VERIFIES ALL THE OTHER METHODS, THEN MOVES TO THE MAINPAGE     ##
    ####################################################################################################

    def Submit(self):
        pass