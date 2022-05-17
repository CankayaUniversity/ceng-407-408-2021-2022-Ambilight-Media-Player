from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget, QMessageBox, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QFont, QEnterEvent, QPixmap
from PyQt5.QtCore import *
import sys
import os
from os.path import exists
import time
from configparser import ConfigParser
from Bulbs import *

class ALP_Settings(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.uis = uic.loadUi('./Settings/Settings.ui',self)
        self.setMainWindow = self.findChild(QtWidgets.QMainWindow, 'setMainForm')
        self.setWindowTitle("Ambilight Media Player - Settings")
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
        self.firstWidget = self.findChild(QtWidgets.QWidget, 'firstWidget')
        self.secondWidget = self.findChild(QtWidgets.QWidget, 'secondWidget')
        self.thirdWidget = self.findChild(QtWidgets.QWidget, 'thirdWidget')
        self.fourthWidget = self.findChild(QtWidgets.QWidget, 'fourthWidget')

        self.firstChkLabel = self.findChild(QtWidgets.QLabel, 'firstChkLabel')
        self.secondChkLabel = self.findChild(QtWidgets.QLabel, 'secondChkLabel')
        self.thirdChkLabel = self.findChild(QtWidgets.QLabel, 'thirdChkLabel')
        self.fourthChkLabel = self.findChild(QtWidgets.QLabel, 'fourthChkLabel')

        self.setLabel(self.firstChkLabel,"")
        self.setLabel(self.secondChkLabel,"")
        self.setLabel(self.thirdChkLabel,"")
        self.setLabel(self.fourthChkLabel,"")
        
        self.firstEdit=self.findChild(QtWidgets.QLineEdit, 'firstEdit')
        self.secondEdit=self.findChild(QtWidgets.QLineEdit, 'secondEdit')
        self.thirdEdit=self.findChild(QtWidgets.QLineEdit, 'thirdEdit')
        self.fourthEdit=self.findChild(QtWidgets.QLineEdit, 'fourthEdit')

        self.videodelaySpin=self.findChild(QtWidgets.QSpinBox, 'videodelaySpin')
        
        
        self.countBulbBox = self.findChild(QtWidgets.QComboBox, 'countBulbBox')
        self.countBulbBox.currentIndexChanged.connect(self.countBulbBoxIndexChanged)
        self.countBulbBox.setCurrentIndex(-1)
        
        
        self.setCloseButton = self.findChild(QtWidgets.QPushButton, 'setCloseButton')
        self.setCloseButton.clicked.connect(self.CloseButtonClicked)

        self.setCButton = self.findChild(QtWidgets.QPushButton, 'setCButton')
        self.setCButton.clicked.connect(self.CloseButtonClicked)

        self.saveButton = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.saveButton.clicked.connect(self.saveSettings)
        
        self.discoverButton = self.findChild(QtWidgets.QPushButton, 'discoverButton')
        self.discoverButton.clicked.connect(self.discoverButtonClicked)

        self.testLampButton = self.findChild(QtWidgets.QPushButton, 'testLampButton')
        self.testLampButton.clicked.connect(self.testLampButtonClicked)
        
        self.loadSettings()
        
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
    def setLabel(self,label,char):
        label.setText(char)
        label.repaint()
        
    def loadSettings(self):
        if exists('./Settings/Settings.ini') :
            
            try:
                getSettingObj = ConfigParser()
                getSettingObj.read('./Settings/Settings.ini')
                
                countBulb= getSettingObj["COUNTBULB"]
                self.countBulbBox.setCurrentIndex(int(countBulb["count"]))
                
                ipBulbs= getSettingObj["BULBS"]
                
                self.firstEdit.setText(ipBulbs["firstIp"])
                self.secondEdit.setText(ipBulbs["secondIp"])
                self.thirdEdit.setText(ipBulbs["thirdIp"])
                self.fourthEdit.setText(ipBulbs["fourthIp"])

                vDelay = getSettingObj["DELAY"]
                self.videodelaySpin.setValue(int(vDelay["vdelay"]))
            except:
                pass
            
        else:
            popup= QMessageBox()
            popup.setWindowTitle("Adjustment Issue")
            popup.setText("Settings file not found!!!\nPlease check your Bulb settings...")
            popup.setIcon(QMessageBox.Warning)
            res= popup.exec_()    

    
    def countBulbBoxIndexChanged(self,value):
        if value==0:
            self.secondWidget.setVisible(False)
            self.thirdWidget.setVisible(False)
            self.fourthWidget.setVisible(False)
            
        elif value==1:
            self.secondWidget.setVisible(True)
            self.thirdWidget.setVisible(False)
            self.fourthWidget.setVisible(False)
            
        elif value==2:
            self.secondWidget.setVisible(True)
            self.thirdWidget.setVisible(True)
            self.fourthWidget.setVisible(True)
            
    def CloseButtonClicked(self):
        self.close()
        
    def discoverButtonClicked(self):
        discoverBulbs(self)

    def testLampButtonClicked(self):
        index = self.countBulbBox.currentIndex()
        if index==0:
            res=testBulb(self,self.firstEdit.text())
            if res:
                self.setLabel(self.firstChkLabel,"P")
            else:
                self.setLabel(self.firstChkLabel,"O")
                
        elif index==1:
            res1=testBulb(self,self.firstEdit.text())
            if res1:
                self.setLabel(self.firstChkLabel,"P")
            else:
                self.setLabel(self.firstChkLabel,"O")

            res2=testBulb(self,self.secondEdit.text())
            if res2:
                self.setLabel(self.secondChkLabel,"P")
            else:
                self.setLabel(self.secondChkLabel,"O")

        elif index==2:
            res1=testBulb(self,self.firstEdit.text())
            if res1:
                self.setLabel(self.firstChkLabel,"P")
            else:
                self.setLabel(self.firstChkLabel,"O")

            res2=testBulb(self,self.secondEdit.text())
            if res2:
                self.setLabel(self.secondChkLabel,"P")
            else:
                self.setLabel(self.secondChkLabel,"O")

            res3=testBulb(self,self.thirdEdit.text())
            if res3:
                self.setLabel(self.thirdChkLabel,"P")
            else:
                self.setLabel(self.thirdChkLabel,"O")

            res4=testBulb(self,self.fourthEdit.text())
            if res4:
                self.setLabel(self.fourthChkLabel,"P")
            else:
                self.setLabel(self.fourthChkLabel,"O")
                
    def saveSettings(self):
        setSettingObj = ConfigParser()
        
        setSettingObj["COUNTBULB"] = {
        "count": self.countBulbBox.currentIndex()
        }
        
        setSettingObj["BULBS"] = {
        "firstIp": self.firstEdit.text(),
        "secondIp": self.secondEdit.text(),
        "thirdIp": self.thirdEdit.text(),
        "fourthIp": self.fourthEdit.text()
        }
        setSettingObj["DELAY"] = {
        "vdelay": self.videodelaySpin.value()
        }
        with open('./Settings/Settings.ini', 'w') as set:
            setSettingObj.write(set)
        
        popup= QMessageBox()
        popup.setWindowTitle("Settings are saved")
        popup.setText("Your settings are saved.\nPlease restart the program." )
        popup.setIcon(QMessageBox.Information)
        res= popup.exec_()
        time.sleep(1)
        sys.exit()
    ##End Functions
