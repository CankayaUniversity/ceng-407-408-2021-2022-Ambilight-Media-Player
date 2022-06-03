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
        self.firstLabel=self.findChild(QtWidgets.QLabel, 'label_4')
        self.secondLabel=self.findChild(QtWidgets.QLabel, 'label_5')
        
        self.firstWidget = self.findChild(QtWidgets.QWidget, 'firstWidget')
        self.secondWidget = self.findChild(QtWidgets.QWidget, 'secondWidget')
        self.thirdWidget = self.findChild(QtWidgets.QWidget, 'thirdWidget')
        self.fourthWidget = self.findChild(QtWidgets.QWidget, 'fourthWidget')

        self.t1Button = self.findChild(QtWidgets.QPushButton, 't1Button')
        self.t2Button = self.findChild(QtWidgets.QPushButton, 't2Button')
        self.t3Button = self.findChild(QtWidgets.QPushButton, 't3Button')
        self.t4Button = self.findChild(QtWidgets.QPushButton, 't4Button')
        
        self.setIcon(self.t1Button,12)
        self.setIcon(self.t2Button,12)
        self.setIcon(self.t3Button,12)
        self.setIcon(self.t4Button,12)

        self.t1Button.clicked.connect(lambda:self.testLamp(0))
        self.t2Button.clicked.connect(lambda:self.testLamp(1))
        self.t3Button.clicked.connect(lambda:self.testLamp(2))
        self.t4Button.clicked.connect(lambda:self.testLamp(3))
        
        
        self.firstIpCombo = self.findChild(QtWidgets.QComboBox, 'firstIpCombo')
        self.secondIpCombo = self.findChild(QtWidgets.QComboBox, 'secondIpCombo')
        self.thirdIpCombo = self.findChild(QtWidgets.QComboBox, 'thirdIpCombo')
        self.fourthIpCombo = self.findChild(QtWidgets.QComboBox, 'fourthIpCombo')
    
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
    def setIcon(self,obj,icon):
        #12=SP_MessageBoxQuestion, 45=SP_DialogApplyButton, 40=SP_DialogCancelButton, 68=SP_MediaVolume, 69=SP_MediaVolumeMuted
        obj.setIcon(self.style().standardIcon(icon))
        
    def loadSettings(self):
        if exists('./Settings/Settings.ini') :
            
            try:
                getSettingObj = ConfigParser()
                getSettingObj.read('./Settings/Settings.ini')
                
                countBulb= getSettingObj["COUNTBULB"]
                self.countBulbBox.setCurrentIndex(int(countBulb["count"]))
                
                ipBulbs= getSettingObj["BULBS"]
                self.firstIpCombo.addItem(ipBulbs["firstIp"])
                self.secondIpCombo.addItem(ipBulbs["secondIp"])
                self.thirdIpCombo.addItem(ipBulbs["thirdIp"])
                self.fourthIpCombo.addItem(ipBulbs["fourthIp"])
                '''
                self.firstIpCombo.setCurrentText(ipBulbs["firstIp"])
                self.secondIpCombo.setCurrentText(ipBulbs["secondIp"])
                self.thirdIpCombo.setCurrentText(ipBulbs["thirdIp"])
                self.fourthIpCombo.setCurrentText(ipBulbs["fourthIp"])
                '''
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
            self.firstWidget.setVisible(False)
            self.secondWidget.setVisible(False)
            self.thirdWidget.setVisible(False)
            self.fourthWidget.setVisible(False)
            
            
        if value==1:
            self.firstLabel.setText("Ip Number of Bulb")
            self.firstWidget.setVisible(True)
            self.secondWidget.setVisible(False)
            self.thirdWidget.setVisible(False)
            self.fourthWidget.setVisible(False)
            
        elif value==2:
            self.firstLabel.setText("Ip Number of Left Bulb")
            self.secondLabel.setText("Ip Number of Right Bulb")
            self.firstWidget.setVisible(True)
            self.secondWidget.setVisible(True)
            self.thirdWidget.setVisible(False)
            self.fourthWidget.setVisible(False)
            
        elif value==3:
            self.firstLabel.setText("Ip Number of Left Top Bulb")
            self.secondLabel.setText("Ip Number of Right Top Bulb")
            self.firstWidget.setVisible(True)
            self.secondWidget.setVisible(True)
            self.thirdWidget.setVisible(True)
            self.fourthWidget.setVisible(True)
            
    def CloseButtonClicked(self):
        self.close()
        
    def discoverButtonClicked(self):
        bList=[]
        bList=discoverBulbs(self)
        for b in bList:
            self.firstIpCombo.addItem(b)
            self.secondIpCombo.addItem(b)
            self.thirdIpCombo.addItem(b)
            self.fourthIpCombo.addItem(b)
            
    def testLamp(self,lampNum):
        if lampNum==0:
            res=testBulb(self,self.firstIpCombo.currentText())
            if res:
                self.setIcon(self.t1Button,45)
            else:
                self.setIcon(self.t1Button,40)
        elif lampNum==1:
            res=testBulb(self,self.secondIpCombo.currentText())
            if res:
                self.setIcon(self.t2Button,45)
            else:
                self.setIcon(self.t2Button,40)

        elif lampNum==2:
            res=testBulb(self,self.thirdIpCombo.currentText())
            if res:
                self.setIcon(self.t3Button,45)
            else:
                self.setIcon(self.t3Button,40)
                
        elif lampNum==3:
            res=testBulb(self,self.fourthIpCombo.currentText())
            if res:
                self.setIcon(self.t4Button,45)
            else:
                self.setIcon(self.t4Button,40)        
              
    def saveSettings(self):
        setSettingObj = ConfigParser()
        
        setSettingObj["COUNTBULB"] = {
        "count": self.countBulbBox.currentIndex()
        }
        
        setSettingObj["BULBS"] = {
        "firstIp": self.firstIpCombo.currentText(),
        "secondIp": self.secondIpCombo.currentText(),
        "thirdIp": self.thirdIpCombo.currentText(),
        "fourthIp": self.fourthIpCombo.currentText()
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
