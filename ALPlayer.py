
#from ALPlayer import myPlayer
import cv2
import sys
import os
from os.path import exists
from configparser import ConfigParser
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from threading import Thread
import yeelight
import time
from yeelight.main import Bulb



class AL_Player(QtWidgets.QMainWindow):
    def __init__(self):
        super(AL_Player, self).__init__()
        uic.loadUi('407.ui', self)
        self.mainWindow = self.findChild(QtWidgets.QMainWindow, 'MainWindow')
        self.settingsBox = self.findChild(QtWidgets.QGroupBox, 'settingsBox')
        #self.mainWindow.setFixedWidth(self.mainWindow.width())
        #self.mainWindow.setFixedHeight(self.mainWindow.height()-self.settingsBox.height())
       
        #self.settingsBox = self.findChild(QtWidgets.QGroupBox, 'settingsBox')

        self.settingsBox.setVisible(False)
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.videoWidget.setStyleSheet("background-color: black")
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        #self.mediaPlayer.stateChanged.connect(self.StateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.volumeChanged.connect(self.volumeChanged)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self.vLayout = self.findChild(QtWidgets.QVBoxLayout, 'playvideoLayout')
        self.vLayout.addWidget(self.videoWidget)
        self.setFixedWidth(594)
        self.setFixedHeight(500)
        self.show()

        self.LeftTopLamp = self.findChild(QtWidgets.QPushButton, 'LeftTopLamp')
        self.LeftBottomLamp = self.findChild(QtWidgets.QPushButton, 'LeftBottomLamp')
        self.RightTopLamp = self.findChild(QtWidgets.QPushButton, 'RightTopLamp')
        self.RightBottomLamp = self.findChild(QtWidgets.QPushButton, 'RightBottomLamp')



        self.openmenu = self.findChild(QtWidgets.QAction, 'actionOpen')
        self.openmenu.triggered.connect(self.openFile)

        self.savesettingmenu = self.findChild(QtWidgets.QAction, 'actionSettings')
        self.savesettingmenu.triggered.connect(self.saveSettings)

        self.openmenu = self.findChild(QtWidgets.QAction, 'actionExit')
        self.openmenu.triggered.connect(self.exitFun)
        
        self.openbutton = self.findChild(QtWidgets.QPushButton, 'openButton')
        self.openbutton.clicked.connect(self.openFile)

        self.playbutton = self.findChild(QtWidgets.QPushButton, 'playButton')
        self.playbutton.clicked.connect(self.playclick)

        self.pausebutton = self.findChild(QtWidgets.QPushButton, 'pauseButton')
        self.pausebutton.clicked.connect(self.pauseclick)

        self.stopButton = self.findChild(QtWidgets.QPushButton, 'stopButton')
        self.stopButton.clicked.connect(self.stopclick)

        self.fullscrbutton = self.findChild(QtWidgets.QPushButton, 'fullscrButton')
        self.fullscrbutton.clicked.connect(self.fullscreen)

        self.firstButton = self.findChild(QtWidgets.QPushButton, 'firstButton')
        self.firstButton.clicked.connect(self.setFirst)

        self.lastButton = self.findChild(QtWidgets.QPushButton, 'lastButton')
        self.lastButton.clicked.connect(self.setLast)

        self.preButton = self.findChild(QtWidgets.QPushButton, 'preButton')
        self.preButton.clicked.connect(self.setPrev)

        self.nextButton = self.findChild(QtWidgets.QPushButton, 'nextButton')
        self.nextButton.clicked.connect(self.setNext)

        self.testButton = self.findChild(QtWidgets.QPushButton, 'testButton')
        self.testButton.clicked.connect(self.testLamp)

        self.settingsButton = self.findChild(QtWidgets.QPushButton, 'settingsButton')
        self.settingsButton.clicked.connect(self.showSettings)
        
        self.saveSetButton = self.findChild(QtWidgets.QPushButton, 'saveSetButton')
        self.saveSetButton.clicked.connect(self.saveSettings)
        
        self.progressSlider = self.findChild(QtWidgets.QSlider, 'progressSlider')
        self.progressSlider.sliderMoved.connect(self.setPosition)

        self.volumeSlider = self.findChild(QtWidgets.QSlider, 'volumeSlider')
        self.volumeSlider.sliderMoved.connect(self.setVolume)

        self.LeftTopBox = self.findChild(QtWidgets.QCheckBox,'LeftTopBox')
        self.RightTopBox = self.findChild(QtWidgets.QCheckBox,'RightTopBox')
        self.LeftBottomBox = self.findChild(QtWidgets.QCheckBox,'LeftBottomBox')
        self.RightBottomBox = self.findChild(QtWidgets.QCheckBox,'RightBottomBox')

        self.LeftTopIpEdit = self.findChild(QtWidgets.QLineEdit,'LeftTopIpEdit')
        self.RightTopIpEdit = self.findChild(QtWidgets.QLineEdit,'RightTopIpEdit')
        self.LeftBottomIpEdit = self.findChild(QtWidgets.QLineEdit,'LeftBottomIpEdit')
        self.RightBottomIpEdit = self.findChild(QtWidgets.QLineEdit,'RightBottomIpEdit')

        if exists('settings.ini') :
            print("Var")
            try:
                getObject = ConfigParser()
                getObject.read("settings.ini")
            
                lTop = getObject["LEFTTOP"]
                
                if lTop["checked"]=="True":
                    self.LeftTopBox.setChecked(True)
                else:
                    self.LeftTopBox.setChecked(False)
                self.LeftTopIpEdit.setText(lTop["ip"])

                lBottom = getObject["LEFTBOTTOM"]
                if lBottom["checked"]=="True":
                    self.LeftBottomBox.setChecked(True)
                else:
                    self.LeftBottomBox.setChecked(False)
                self.LeftBottomIpEdit.setText(lBottom["ip"])

                rTop = getObject["RIGHTTOP"]
                if rTop["checked"]=="True":
                    self.RightTopBox.setChecked(True)
                else:
                    self.RightTopBox.setChecked(False)
                self.RightTopIpEdit.setText(rTop["ip"])

                rBottom = getObject["RIGHTBOTTOM"]
                if rBottom["checked"]=="True":
                    self.RightBottomBox.setChecked(True)
                else:
                    self.RightBottomBox.setChecked(False)
                self.RightBottomIpEdit.setText(rBottom["ip"])
            except:
                pass

    def showSettings(self):
        self.settingsBox.setVisible(not self.settingsBox.isVisible())
        if self.settingsBox.isVisible():
            self.setFixedWidth(594)
            self.setFixedHeight(610)
        else:
            self.setFixedWidth(594)
            self.setFixedHeight(500)

    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Select and Open Video", "/home")[0]
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.statusBar.showMessage(fileName)
            self.playbutton.setEnabled(True)
            self.volumeSlider.setValue(self.mediaPlayer.volume())

    def playclick(self):
        self.mediaPlayer.play()
        #if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
        #    self.mediaPlayer.pause()
        #else:
    
    def pauseclick(self):
        self.mediaPlayer.pause()

    def stopclick(self):
        self.mediaPlayer.stop()

    def fullscreen(self):
        self.videoWidget.setFullScreen(True)

    def mouseDoubleClickEvent(self, event):
        self.videoWidget.setFullScreen(not self.videoWidget.isFullScreen())
        event.accept()

    def positionChanged(self, position):
        self.progressSlider.setValue(position)

    def durationChanged(self, duration):
        self.progressSlider.setRange(0, duration)

    def volumeChanged(self, volume):
        self.volumeSlider.setValue(volume)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def setVolume(self, volume):
        self.mediaPlayer.setVolume(volume)

    def setPrev(self,position):
        self.mediaPlayer.setPosition(self.mediaPlayer.position()-1000)

    def setNext(self,position):
        self.mediaPlayer.setPosition(self.mediaPlayer.position()+1000)

    def setFirst(self):
        self.mediaPlayer.setPosition(0)

    def setLast(self, duration):
        self.mediaPlayer.setPosition(self.mediaPlayer.duration())
    
    def exitFun(self):
        sys.exit(app.exec_())
    
    def lampCheckFun(self,ip):
        bulb = Bulb(ip, effect="smooth")
        try:
            try:
                bulb.stop_music()
            except:
                pass
            time.sleep(1)
            bulb.start_music(2000)
            bulb.turn_on()
            bulb.set_default()
            time.sleep(1)
            bulb.turn_off()
            time.sleep(1)
            bulb.turn_on()
            return True
        except:
            return False


    def testLamp(self):
        if self.LeftTopBox.isChecked():
            st1=self.lampCheckFun(self.LeftTopIpEdit.text())
            if st1:
                self.LeftTopLamp.setEnabled(True)
            else:
                self.LeftTopLamp.setEnabled(False)

        if self.RightTopBox.isChecked():
            st2=self.lampCheckFun(self.RightTopIpEdit.text())
            if st2:
                self.RightTopLamp.setEnabled(True)
            else:
                self.RightTopLamp.setEnabled(False)

        if self.LeftBottomBox.isChecked():
            st3=self.lampCheckFun(self.LeftBottomIpEdit.text())
            if st3:
                self.LeftBottomLamp.setEnabled(True)
            else:
                self.LeftBottomLamp.setEnabled(False)

        if self.RightBottomBox.isChecked():
            st4=self.lampCheckFun(self.RightBottomIpEdit.text())
            if st4:
                self.RightBottomLamp.setEnabled(True)
            else:
                self.RightBottomLamp.setEnabled(False)

    def saveSettings(self):

        settingObject = ConfigParser()
        settingObject["LEFTTOP"] = {
        "checked": self.LeftTopBox.isChecked(),
        "ip": self.LeftTopIpEdit.text()
        }

        settingObject["LEFTBOTTOM"] = {
        "checked": self.LeftBottomBox.isChecked(),
        "ip": self.LeftBottomIpEdit.text()
        }

        settingObject["RIGHTTOP"] = {
        "checked": self.RightTopBox.isChecked(),
        "ip": self.RightTopIpEdit.text()
        }

        settingObject["RIGHTBOTTOM"] = {
        "checked": self.RightBottomBox.isChecked(),
        "ip": self.RightBottomIpEdit.text()
        }

        with open('settings.ini', 'w') as set:
            settingObject.write(set)
        
        self.statusBar.showMessage("Settings are saved")

app = QtWidgets.QApplication(sys.argv)
mainWindow = AL_Player()
app.exec_()
