#Mainpage.py

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidget, QLineEdit, QPushButton, QTimeEdit, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
import sqlite3
import allimages
import arrowimages


class MainScreen(QMainWindow):
    def __init__(self, username="", email="", password="", age="", phonenumber="", location="", gender=""):
        super(MainScreen, self).__init__()
        loadUi("Mainpage.ui", self)
        self.username = username
        self.email = email
        self.password = password
        self.age = age
        self.phonenumber = phonenumber
        self.location = location
        self.gender = gender
        self.user_image = None
        self.current_index = 0  # Keep track of the current user index
        self.loadUser(self.current_index)

        ### ASSIGNING EACH BUTTON TO A PAGE IN THE STACKED WIDGET IN THE MAIN ###
        self.Home_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.HomePage))
        self.Find_match_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Match_Page))
        self.Others_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Others_page))
        self.Date_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Date_page))
        self.Account_Button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Account_page))

        # ACTION TO OPEN FILE IMAGE AND UPLOAD ON THE ACOUNT PAGE ##
        self.Upload_image_button.clicked.connect(self.updateProfilePicture)

        ## SETTING THE TEXT LABEL FIELD IN MAINPAGE UI TO THE USERNAME OF THE USER ##
        self.username_label.setText(self.username)

        ## BUTTON THAT UPDATES THE USER PROFILE AUTOMATICALLY AS HE ENTERS THE MAINPAGE ##
        self.Save_button.clicked.connect(self.UpdateProfile)

        ## BUTTON THAT HELPS VIEW SUGGESTIONS ##
        self.View_suggestions_button.clicked.connect(self.viewSuggestions)
        
        ## BUTTON THAT MOVES TO THE NEXT USER IN THE OTHER PROFILES PAGE ##
        self.Right_arrow_button.clicked.connect(self.nextUser)

        ## BUTTON THAT MOVES TO THE PREVIOUS USER IN THE OTHER PROFILES PAGE ##
        self.Left_arrow_button.clicked.connect(self.previousUser)

        # Connect calendar widget click event to set event date
        self.calendarWidget.clicked.connect(self.setEventDate)

        # Connect save button to save event function
        self.Event_save_button.clicked.connect(self.saveEvent)

        

    ###########################################################################################
    ##    METHOD THAT AUTOMATICALLY SETS UP THE USERPROFILE ON LOGIN OR CREATE ACCOUNT       ##
    ###########################################################################################
 
    def setUserProfile(self):
        try:
            conn = sqlite3.connect("usersInfo.db")
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT Username, Password, Age, Email, Location, PhoneNumber, Gender, Image
                            FROM Users
                            WHERE Username = ?
                            ''', (self.username,))
            user_data = cursor.fetchone()
            conn.close()

            if user_data:
                self.username, self.password, self.age, self.email, self.location, self.phonenumber, self.gender, image_data = user_data
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.user_image = pixmap
                self.Account_image_Input.setPixmap(pixmap)

                self.Account_username_Input.setText(self.username)
                self.Account_password_Input.setText(self.password)
                self.Account_age_Input.setText(str(self.age))
                self.Account_email_Input.setText(self.email)
                self.Account_location_Input.setText(self.location)
                self.Account_Phone_number_Input.setText(str(self.phonenumber))
                self.Account_gender_Input.setText(self.gender)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch user profile: {str(e)}")

    ######################################################################################################
    ##                    FUNCTION THAT ALLOWS USER TO UPDATE HIS PROFILE PICTURE                       ##
    ######################################################################################################

    def updateProfilePicture(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            try:
                pixmap = QPixmap(filename)
                self.Account_image_Input.setPixmap(pixmap.scaled(self.Account_image_Input.width(), self.Account_image_Input.height()))
                self.user_image = pixmap
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update profile picture: {str(e)}")
            
    #####################################################################################################
    ##                   FUNCTION THAT ALLOWS USER TO UPDATE HIS PROFILE                               ##
    #####################################################################################################

    def UpdateProfile(self):
        updated_username = self.Account_username_Input.text()
        updated_password = self.Account_password_Input.text()
        updated_age = self.Account_age_Input.text()
        updated_email = self.Account_email_Input.text()
        updated_location = self.Account_location_Input.text()
        updated_phonenumber = self.Account_Phone_number_Input.text()
        updated_gender = self.Account_gender_Input.text()

        try:
            conn = sqlite3.connect("usersInfo.db")
            cursor = conn.cursor()

            if self.user_image:
                # Convert QPixmap to bytes for storage in the database
                img_bytes = QByteArray()
                buffer = QBuffer(img_bytes)
                buffer.open(QIODevice.ReadWrite)
                self.user_image.save(buffer, "PNG")  # Adjust format based on your preference

                cursor.execute('''
                                UPDATE Users 
                                SET Username = ?, Email = ?, Password = ?, PhoneNumber = ?, Age = ?, Location = ?, Gender = ?, Image = ?
                                WHERE Username = ?
                                ''', (updated_username, updated_email, updated_password, updated_phonenumber, updated_age, updated_location, updated_gender, img_bytes, self.username))
            else:
                cursor.execute('''
                                UPDATE Users 
                                SET Username = ?,Email = ?, Password = ?,PhoneNumber = ? Age = ?,  Location = ?, Gender = ? 
                                WHERE Username = ?
                                ''', (updated_username, updated_email, updated_password, updated_phonenumber, updated_age, updated_location,updated_gender,  self.username))

            conn.commit()
            conn.close()

            self.username = updated_username
            self.password = updated_password
            self.age = updated_age
            self.email = updated_email
            self.location = updated_location
            self.phonenumber = updated_phonenumber
            self.gender = updated_gender

            QMessageBox.information(self, "Success", "Profile updated successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update profile: {str(e)}")
            print(f"Failed to update profile: {str(e)}")



    #####################################################################################################
    ##                   FUNCTION THAT ALLOWS USER IN THE HOME TO SEE SUGGESTIONS                      ##
    #####################################################################################################

    def viewSuggestions(self):
        conn = sqlite3.connect("usersInfo.db")
        cur = conn.cursor()
        sql_query = "SELECT Image, Username, Age, Location, Gender FROM Users WHERE Username != ? LIMIT 10"

        rows = cur.execute(sql_query, (self.username,)).fetchall()

        self.tableWidget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            image_data = row[0]
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            label = QtWidgets.QLabel()
            label.setPixmap(pixmap.scaled(100, 100))  # Set your desired size for the image

            label.setAlignment(QtCore.Qt.AlignCenter)

            self.tableWidget.setRowHeight(i, 120)  # Increase row height to accommodate the image

            self.tableWidget.setCellWidget(i, 0, label)  # Display image in column 0

            for j in range(1, len(row)):
                item = QtWidgets.QTableWidgetItem(str(row[j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)

        conn.close()

    #############################################################################################################
    ##        FUNCTION THAT ALLOWS YOU TO LOAD A USERS PROFILE ON THE OTHER PROFILES PAGE FROM THE DATA BASE   ##
    #####################################################################################################
    
    def loadUser(self, index):
        conn = sqlite3.connect("usersInfo.db")
        cur = conn.cursor()
        cur.execute("SELECT Image, Username, Age, Location, Gender FROM Users LIMIT 10 OFFSET ?", (index,))
        user_data = cur.fetchone()
        conn.close()

        if user_data:
            image_data, username, age, location, gender = user_data

            # Load the image into the label
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(image_data)
            self.Other_Profiles_Image_Label.setPixmap(pixmap.scaled(200, 200))

            # Set user details in other labels
            self.Other_Profiles_name_label.setText(username)
            self.Other_Profiles_age_label.setText(f"{age}")
            self.Other_Profiles_location_label.setText(location)
            self.Other_Profiles_Gender_label.setText(gender)

    #####################################################################################################
    ##        FUNCTION THAT ALLOWS USER TO MOVE TO THE NEXT USER IN THE OTHER PROFILES PAGE             ##
    #####################################################################################################

    def nextUser(self):
        self.current_index += 1
        self.loadUser(self.current_index) 

    #####################################################################################################
    ##        FUNCTION THAT ALLOWS USER TO MOVE TO THE PREVIOUS USER IN THE OTHER PROFILES PAGE        ##
    #####################################################################################################

    def previousUser(self):
        if self.current_index > 0: 
            self.current_index -= 1  
            self.loadUser(self.current_index)

    #####################################################################################################
    ##        FUNCTION THAT ALLOWS USER TO SAVE AN EVENT IN THE EVENT PAGE                             ##
    #####################################################################################################

    def saveEvent(self):
        event_name = self.event_name_line_edit.text()
        start_time = self.Start_time_edit.time().toString()
        end_time = self.End_time_edit.time().toString()
        description = self.Description_text_edit.toPlainText()
        event_date = self.event_date_edit.text()  # Get the date set on the calendar
        username = self.username  # Get the username of the logged-in user

        try:
            conn = sqlite3.connect("Event.db")
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Events (
                    EventID INTEGER PRIMARY KEY AUTOINCREMENT,
                    EventName TEXT,
                    StartTime TEXT,
                    EndTime TEXT,
                    Description TEXT,
                    EventDate TEXT,
                    Username TEXT
                )
            ''')

            cursor.execute('''
                INSERT INTO Events (EventName, StartTime, EndTime, Description, EventDate, Username)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (event_name, start_time, end_time, description, event_date, username))

            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Event saved successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save event: {str(e)}")

    #####################################################################################################
    ##     FUNCTION THAT ALLOWS USER TO SAVE THE EVENT FIELDS FOR A SPECIFIC USER FROM THE DATABASE    ##
    #####################################################################################################
    
    def setEventFields(self, event_data):
        if event_data:
            event_name, start_time, end_time, description = event_data
            self.event_name_line_edit.setText(event_name)
            self.Start_time_edit.setTime(QtCore.QTime.fromString(start_time))
            self.End_time_edit.setTime(QtCore.QTime.fromString(end_time))
            self.Description_text_edit.setPlainText(description)

    #####################################################################################################
    ##        FUNCTION THAT ALLOWS USER TO LOAD EVENT FROM THE DATA BASE                               ##
    #####################################################################################################

    def loadEvent(self):
        event_date = self.event_date_edit.text()
        username = self.username

        try:
            conn = sqlite3.connect("Event.db")
            cursor = conn.cursor()

            cursor.execute('''
                SELECT EventName, StartTime, EndTime, Description
                FROM Events
                WHERE EventDate = ? AND Username = ?
            ''', (event_date, username))

            event_data = cursor.fetchone()

            conn.close()

            self.setEventFields(event_data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load event: {str(e)}")

    #####################################################################################################
    ##        FUNCTION THAT SETS THE DATE EDIT TO THE SELECTED DATE ON TEH CALENDAR WIDGET             ##
    #####################################################################################################

    def setEventDate(self):
        selected_date = self.calendarWidget.selectedDate()
        self.event_date_edit.setDate(selected_date)

        # Clear other event fields
        self.event_name_line_edit.clear()
        self.Start_time_edit.clear()
        self.End_time_edit.clear()
        self.Description_text_edit.clear()

        # Load event data for the selected date and user
        self.loadEvent()


    


        