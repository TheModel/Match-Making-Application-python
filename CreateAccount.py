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
        conn = sqlite3.connect("usersInfo.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Username FROM Users WHERE Username = ?", (username,))
        result = cursor.fetchone()

        conn.close()

        return result is not None  # Return True if the username exists, False otherwise '''


    ########################################################################################
    ##     METHOD TO CHECK IF THE USER INFO IS ENTERED IN THE CORRECT FORMAT              ##
    ########################################################################################
    def CheckInfo(self, username, email, password, age, phonenumber, location, gender):
        # Check if the information is in the correct format
        if (
            len(username) == 0
            or len(password) == 0
            or len(email) == 0
            or len(age) == 0
            or len(phonenumber) == 0
            or len(location) == 0
            or len(gender) == 0
        ):
            return "Please fill in all input fields!"
        elif not len(username) >= 4:
            return "Username should have at least 4 characters!"
        elif self.isUsernameTaken(username):
           return "Username is already taken!"  
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return "Incorrect email!"
        elif not len(password) >= 5:
            return "Password length must be at least 5 characters"
        elif not phonenumber.isdigit():
            return "Invalid phone number!"
        elif not age.isdigit():
            return "Invalid age!"
        elif gender.lower() not in ['male', 'female']:
            return "Gender should be Male or Female"
        else:
            return None  # Return None if all checks pass
    
    #############################################################################################
    ##      METHOD THAT STORES USER INFO IN THE DATABASE AFTER VALIDATION                      ##
    #############################################################################################

    def storeInDataBase(self, username, email, password, age, phonenumber, location,gender, image_path):
        self.conn = sqlite3.connect("usersInfo.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT 
            EXISTS Users (
                        UserId INTEGER PRIMARY KEY AUTOINCREMENT,
                        Username TEXT,
                        Email TEXT,
                        Password TEXT,
                        PhoneNumber TEXT,
                        Age INTEGER,
                        Location TEXT,
                        Gender TEXT,
                        Image BLOB  -- Store the image.
            )
            '''
        )
        self.conn.commit()

        self.cursor.execute(
            '''
            INSERT INTO Users(Username, Email, Password, PhoneNumber, Age, Location,Gender, Image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
            ''', (username, email, password, phonenumber, age, location, gender, image_path)
        )
        self.conn.commit()
        self.conn.close()

    ##############################################################################################
    ##        METHOD THAT ALLOWS USER TO UPLOAD AN IMAGE FOR HIS PROFILE                        ##
    ##############################################################################################

    def uploadImage(self):
        # Open a file dialog to select an image file
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.jpg *.png *.jpeg)')
        if self.image_path:  # Check if an image was selected
            # Display the selected image in a label, if needed
            pixmap = QPixmap(self.image_path)
            self.Picture_label.setPixmap(pixmap)
            self.Picture_label.setScaledContents(True)  # Optional: Scale image to fit label
            self.Picture_label.show()

    ####################################################################################################
    ##    THE FINAL SUBMIT BUTTON THAT VERIFIES ALL THE OTHER METHODS, THEN MOVES TO THE MAINPAGE     ##
    ####################################################################################################

    def Submit(self):
        username = self.username_LineEdit.text()
        email = self.Email_LineEdit.text()
        password = self.Password_LineEdit.text()
        age = self.Age_LineEdit.text()
        phonenumber = self.PhoneNo_lineEdit.text()
        location = self.Location_LineEdit.text()
        gender = self.Gender_LineEdit.text()

        # Check the information format
        error_message = self.CheckInfo(username, email, password, age, phonenumber, location, gender)
        if error_message:
            self.error_label.setText(error_message)
        else:
            if hasattr(self, 'image_path'):
                # Read the image file and convert it to binary
                with open(self.image_path, 'rb') as file:
                    image_binary = file.read()
                self.storeInDataBase(username, email, password, age, phonenumber, location,gender,  image_binary)
            else:
                self.storeInDataBase(username, email, password, age, phonenumber, location, gender,  None)

            mainpage = MainScreen(username, email, password, age, phonenumber, location, gender)
            mainpage.setUserProfile()
            self.widget.addWidget(mainpage)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)