from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget, QMessageBox, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QFont, QEnterEvent, QPixmap
from PyQt5.QtCore import *
import sys
import os
from os.path import exists
import time
import threading

class ALP_AboutUs(QtWidgets.QMainWindow):
    X=7
    Y=270
    def __init__(self, parent=None):
        super().__init__()
        #self.uis = uic.loadUi(os.path.join(os.path.dirname(__file__), "About.ui"),self)
        self.uis = uic.loadUi('./Settings/AboutUs.ui',self)
        self.setMainWindow = self.findChild(QtWidgets.QMainWindow, 'setMainForm')
        self.setWindowTitle("Ambilight Media Player - About Us")
        ##Windows Seetings
        self.setTitleWidget = self.findChild(QtWidgets.QWidget, 'setTitleWidget')
        # Set the form without borders
        self.setWindowFlags(Qt.FramelessWindowHint)
        #Set _drag_status and MouseTracking
        self._drag_status = False
        self.setMouseTracking(True)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.moveCenter()
        ##End Windows Seetings
        
        ##Connection Settings
        self.CloseButton = self.findChild(QtWidgets.QPushButton, 'CloseButton')
        self.CloseButton.clicked.connect(self.CloseButtonClicked)

        self.marqueeLabel = self.findChild(QtWidgets.QLabel, 'marqueeLabel')
        self.t1 = threading.Thread(target=self.setLabelCoord, daemon=True)
        self.t1.start()
        ##End Connection Settings
        
    ##Main Form Event Functions
    
    def moveCenter(self):
        #Positions the window in the center of the screen
        fg = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(centerpoint)
        self.move(fg.topLeft())
        
    def eventFilter(self, obj, event):
        # Setting standard mouse style after entering other controls
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(ALP_Settings, self).eventFilter(obj, event)
 
    def mousePressEvent(self, event):
        # If left click on the title bar area
        if (event.button() == Qt.LeftButton) and (event.y() < self.setTitleWidget.height()):
            self._drag_status = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self._drag_status:
            # Title bar drag and drop window position
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()
 
    def mouseReleaseEvent(self, QMouseEvent):
        # Reset _drag_status
        self._drag_status = False
    ##End Main Form Event Functions    

    ##Functions
    
    def setLabelCoord(self):
      while True:  
          self.marqueeLabel.move(self.X,self.Y)
          self.Y=self.Y-1
          time.sleep(0.1)
          self.marqueeLabel.repaint()
          if self.Y<-394:
              self.Y=270
          
    def CloseButtonClicked(self):
        self.close()  
  
    ##End Functions
