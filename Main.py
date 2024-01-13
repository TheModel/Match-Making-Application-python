import sys
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication
from welcome import WelcomeScreen

##########################################
##  RUNNING THE APPLICATION             ##
##########################################

app = QApplication(sys.argv)
widget = QStackedWidget()
welcomewindow = WelcomeScreen(widget)
widget.addWidget(welcomewindow)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
sys.exit(app.exec_())


# This is from MaximusAy127

# There are a lot of things I still need to know about github for real.

#Really this is some parallel code or something.
