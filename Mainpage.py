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
            conn=sqlite3.connect("userInfo.db")
            cursor=conn.cursor()
            cursor.execute('''SELECT Username,Password,Age,Email,Location,Phone Number,Gender,Image
                           FROM Users
                           WHERE Username=?''',(self.username,))
            user_data=cursor.fetchone()
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
        pass
            
    #####################################################################################################
    ##                   FUNCTION THAT ALLOWS USER TO UPDATE HIS PROFILE                               ##
    #####################################################################################################

    def UpdateProfile(self):
        pass



    #####################################################################################################
    ##                   FUNCTION THAT ALLOWS USER IN THE HOME TO SEE SUGGESTIONS                      ##
    #####################################################################################################

    def viewSuggestions(self):
        pass
    #############################################################################################################
    ##        FUNCTION THAT ALLOWS YOU TO LOAD A USERS PROFILE ON THE OTHER PROFILES PAGE FROM THE DATA BASE   ##
    #####################################################################################################
    
    def loadUser(self, index):
        pass
    #####################################################################################################
    ##        FUNCTION THAT ALLOWS USER TO MOVE TO THE NEXT USER IN THE OTHER PROFILES PAGE             ##
    #####################################################################################################

    def nextUser(self):
        pass

    #####################################################################################################
    ##        FUNCTION THAT ALLOWS USER TO MOVE TO THE PREVIOUS USER IN THE OTHER PROFILES PAGE        ##
    #####################################################################################################

    def previousUser(self):
        pass

    #####################################################################################################
    ##        FUNCTION THAT ALLOWS USER TO SAVE AN EVENT IN THE EVENT PAGE                             ##
    #####################################################################################################

    def saveEvent(self):
            
        event_name = self.event_name_line_edit.text()
        start_time = self.Start_time_edit.time().toString()
        end_time = self.End_time_edit.time().toString()
        description = self.Description_text_edit.toPlainText()
        
        event_date = self.event_date_edit.text()
        
        username= self.username

        try:

            conn=sqlite3.connect("Event.db")

            cursor=conn.cursor()
            cursor.execute('''
   
              CREATE TABLE IF NOT EXISTS Events(
                EventID INTEGER PRIMARY KEY AUTOINCREMENT,
                EventName TEXT,
                StartTime TEXT,
                EndTime TEXT,
                Description TEXT,
                EventDate TEXT,
                Username TEXT,
               )
             ''')

            cursor.execute('''
              INSERT INTO Events (EventName, StartTime, EndTime, Description, EventDate, Username)
              VALUES (?,?,?,?,?,?)
            ''', (event_name,start_time,end_time,description,event_date,username))

            conn.commit()

            conn.close
    
            QMessageBox.information(self,"Success","Event saved successfully!")
        except Exception as e:

            QMessageBox.critical(self,"Error",f"Failed to save event:{str(e)}")

        
    

    #####################################################################################################
    ##     FUNCTION THAT ALLOWS USER TO SET THE EVENT FIELDS FOR A SPECIFIC USER FROM THE DATABASE     ##
    #####################################################################################################
    
    def setEventFields(self, event_data):
        pass

    #####################################################################################################
    ##        FUNCTION THAT ALLOWS USER TO LOAD EVENT FROM THE DATA BASE TO THE CALENDAR               ##
    #####################################################################################################

    def loadEvent(self):
        pass

    #####################################################################################################
    ##        FUNCTION THAT SETS THE DATE EDIT TO THE SELECTED DATE ON THE CALENDAR WIDGET             ##
    #####################################################################################################

    def setEventDate(self):
        pass

    


        
