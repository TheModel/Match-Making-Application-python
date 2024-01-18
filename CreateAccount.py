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
        
    try:
        # Step 1: Establish a connection to the SQLite database named "usersInfo.db"
        conn = sqlite3.connect("usersInfo.db")

        # Step 2: Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Step 3: Execute an SQL query to check if the username already exists in the Users table
        cursor.execute("SELECT Username FROM Users WHERE Username = ?", (username,))
        
        # Step 4: Fetch the result of the query
        result = cursor.fetchone()

        # Step 5: Close the database connection to free up resources
        conn.close()

        # Step 6: Return True if the username exists, False otherwise
        return result is not None

    except Exception as e:
        # Step 7: Handle any exceptions that might occur during the process and return False
        print(f"Error checking username existence: {str(e)}")
        return False

        pass


    ########################################################################################
    ##     METHOD TO CHECK IF THE USER INFO IS ENTERED IN THE CORRECT FORMAT              ##
    ########################################################################################
    def CheckInfo(self, username, email, password, age, phonenumber, location, gender):
        # Check if the information is in the correct format
        
    try:
        # Step 1: Check if any of the required input fields is empty
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

        # Step 2: Check if the username has at least 4 characters
        elif not len(username) >= 4:
            return "Username should have at least 4 characters!"

        # Step 3: Check if the username is already taken
        elif self.isUsernameTaken(username):
            return "Username is already taken!"

        # Step 4: Check if the email is in the correct format
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return "Incorrect email!"

        # Step 5: Check if the password length is at least 5 characters
        elif not len(password) >= 5:
            return "Password length must be at least 5 characters"

        # Step 6: Check if the phone number consists of digits only
        elif not phonenumber.isdigit():
            return "Invalid phone number!"

        # Step 7: Check if the age consists of digits only
        elif not age.isdigit():
            return "Invalid age!"

        # Step 8: Check if the gender is either 'male' or 'female'
        elif gender.lower() not in ['male', 'female']:
            return "Gender should be Male or Female"

        # Step 9: If all checks pass, return None (indicating successful validation)
        else:
            return None

    except Exception as e:
        # Step 10: Handle any exceptions that might occur during the process and return an error message
        print(f"Error checking user info format: {str(e)}")
        return "An error occurred during user info validation."

        pass
    
    #############################################################################################
    ##      METHOD THAT STORES USER INFO IN THE DATABASE AFTER VALIDATION                      ##
    #############################################################################################

    def storeInDataBase(self, username, email, password, age, phonenumber, location,gender, image_path):
        
    try:
        # Step 1: Connect to the database
        self.conn = sqlite3.connect("usersInfo.db")
        self.cursor = self.conn.cursor()

        # Step 2: Create the Users table if it does not exist
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Users (
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

        # Step 3: Insert user information into the Users table
        self.cursor.execute(
            '''
            INSERT INTO Users(Username, Email, Password, PhoneNumber, Age, Location, Gender, Image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
            ''', (username, email, password, phonenumber, age, location, gender, image_path)
        )
        self.conn.commit()

        # Step 4: Close the database connection
        self.conn.close()

    except Exception as e:
        # Step 5: Handle any exceptions that might occur during the process
        print(f"Error storing user info in the database: {str(e)}")
        pass

    ##############################################################################################
    ##        METHOD THAT ALLOWS USER TO UPLOAD AN IMAGE FOR HIS PROFILE                        ##
    ##############################################################################################

    def uploadImage(self):
        
    try:
        # Step 1: Open a file dialog to select an image file
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.jpg *.png *.jpeg)')

        # Step 2: Check if an image was selected
        if self.image_path:
            # Step 3: Display the selected image in a label
            pixmap = QPixmap(self.image_path)
            self.Picture_label.setPixmap(pixmap)

            # Optional: Scale the image to fit the label
            self.Picture_label.setScaledContents(True)

            # Optional: Show the label with the selected image
            self.Picture_label.show()

    except Exception as e:
        # Step 4: Handle any exceptions that might occur during the process
        print(f"Error uploading image: {str(e)}")

        pass

    ####################################################################################################
    ##    THE FINAL SUBMIT BUTTON THAT VERIFIES ALL THE OTHER METHODS, THEN MOVES TO THE MAINPAGE     ##
    ####################################################################################################

    def Submit(self):
        
    try:
        # Step 1: Get user input from the input fields
        username = self.username_LineEdit.text()
        email = self.Email_LineEdit.text()
        password = self.Password_LineEdit.text()
        age = self.Age_LineEdit.text()
        phonenumber = self.PhoneNo_lineEdit.text()
        location = self.Location_LineEdit.text()
        gender = self.Gender_LineEdit.text()

        # Step 2: Check the information format using the CheckInfo method
        error_message = self.CheckInfo(username, email, password, age, phonenumber, location, gender)

        # Step 3: Display error message if there is any issue with the information format
        if error_message:
            self.error_label.setText(error_message)
        else:
            # Step 4: Check if an image path is available
            if hasattr(self, 'image_path'):
                # Step 5: Read the image file and convert it to binary
                with open(self.image_path, 'rb') as file:
                    image_binary = file.read()

                # Step 6: Store user information in the database using storeInDataBase method
                self.storeInDataBase(username, email, password, age, phonenumber, location, gender, image_binary)
            else:
                # Step 7: If no image is selected, store user information with a None image
                self.storeInDataBase(username, email, password, age, phonenumber, location, gender, None)

            # Step 8: Create an instance of the MainScreen and set the user profile
            mainpage = MainScreen(username, email, password, age, phonenumber, location, gender)
            mainpage.setUserProfile()

            # Step 9: Add the MainScreen to the widget and move to the MainScreen
            self.widget.addWidget(mainpage)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    except Exception as e:
        # Step 10: Handle any exceptions that might occur during the process
        print(f"Error in the Submit method: {str(e)}")

        pass
