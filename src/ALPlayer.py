import sys
import os
from os.path import exists
from configparser import ConfigParser

import time
import colorsys
from PIL import Image

import numpy as np
import numpy
import math
import cv2

from sklearn.cluster import KMeans
from collections import Counter
import wcag_contrast_ratio as contrast


import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
#from PyQt5.QtCore import QUrl, Qt
from PyQt5 import QtWidgets
#from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QMainWindow, QWidget, QDialog, QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QVideoFrame, QAbstractVideoSurface, QAbstractVideoBuffer, QVideoSurfaceFormat
#from PyQt5.QtWidgets import QMessageBox

#from PyQt5.QtCore import pyqtSlot, Qt, QPoint
#from PyQt5.QtGui import QFont, QEnterEvent, QPixmap
#from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
#from PyQt5 import QtCore

#from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget

import yeelight
from yeelight.main import Bulb, discover_bulbs
#from yeelight.main import discover_bulbs
from yeelight import enums

from Settings import ALP_Settings
from Video import VideoWidget
from VideoGrabber import VideoFrameGrabber
from Dominant import DominantColors


class AL_Player(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AL_Player, self).__init__(parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "ALPlayer.ui"),self)
        self.mainWindow = self.findChild(QtWidgets.QMainWindow, 'MainForm')
        self.mediaPlayer =None
        ##Read Settings and Initilaze Bulb
        self.firstBulbIp=None
        self.secondBulbIp=None
        self.thirdBulbIp=None
        self.fourthBulbIp=None
        self.bulbCount=None
        self.AMLStatus=False
        self.delay=0
        
        self.singleBulb=None
        
        self.leftBulb=None
        self.rightBulb=None
        
        self.leftTopBulb=None
        self.rightTopBulb=None
        self.leftBottomBulb=None
        self.rightBottomBulb=None
        
        if exists('settings.ini') :
            try:
                getSettingObj = ConfigParser()
                getSettingObj.read("settings.ini")
                countBulb= getSettingObj["COUNTBULB"]
                self.bulbCount=int(countBulb["count"])
                ipBulbs= getSettingObj["BULBS"]
                self.firstBulbIp=ipBulbs["firstIp"]
                self.secondBulbIp=ipBulbs["secondIp"]
                self.thirdBulbIp=ipBulbs["thirdIp"]
                self.fourthBulbIp=ipBulbs["fourthIp"]
                vDelay = getSettingObj["DELAY"]
                self.delay=int(vDelay["vdelay"])

                if self.bulbCount==0:
                    self.singleBulb = Bulb(self.firstBulbIp, effect="smooth")
                    try:
                        self.singleBulb.stop_music()
                    except:
                        pass
                    time.sleep(1)
                    try:
                        self.singleBulb.start_music(20000)
                    except:
                        pass
                elif self.bulbCount==1:
                    self.leftBulb = Bulb(self.firstBulbIp, effect="smooth")
                    self.rightBulb = Bulb(self.secondBulbIp, effect="smooth")
                    try:
                        self.leftBulb.stop_music()
                        self.rightBulb.stop_music()
                    except:
                        pass
                    time.sleep(1)
                    try:
                        self.leftBulb.start_music(20000)
                        self.rightBulb.start_music(20000)
                    except:
                        pass
                    
                elif self.bulbCount==2:
                    self.leftTopBulb = Bulb(self.firstBulbIp, effect="smooth")
                    self.rightTopBulb = Bulb(self.secondBulbIp, effect="smooth")
                    self.leftBottomBulb = Bulb(self.thirdBulbIp, effect="smooth")
                    self.rightBottomBulb = Bulb(self.fourthBulbIp, effect="smooth")
                    try:
                        self.leftTopBulb.stop_music()
                        self.rightTopBulb.stop_music()
                        self.leftBottomBulb.stop_music()
                        self.rightBottomBulb.stop_music()
                    except:
                        pass
                    time.sleep(1)
                    try:
                        self.leftTopBulb.start_music(20000)
                        self.rightTopBulb.start_music(20000)
                        self.leftBottomBulb.start_music(20000)
                        self.rightBottomBulb.start_music(20000)
                    except:
                        pass
                self.AMLStatus=True
            except:
                self.AMLStatus=False
                pass
        else:
            popup= QMessageBox()
            popup.setWindowTitle("Adjustment Issue")
            popup.setText("Settings file not found!!!\nPlease check your Bulb settings...")
            popup.setIcon(QMessageBox.Warning)
            res= popup.exec_()
        ##End Read Settings and Initilaze Bulb

        ##Windows Seetings
        self.centralWidget = self.findChild(QtWidgets.QWidget, 'centralWidget')
        self.titleWidget = self.findChild(QtWidgets.QWidget, 'titleWidget')
        self.setWindowTitle("Ambilight Media Player")
        
        # Set the form without borders
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Set the default value of mouse tracking judgment trigger
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self.setMouseTracking(True)
        self.centralWidget.installEventFilter(self)  # Initialize event filter
        self.titleWidget.installEventFilter(self)  # Initialize event filter
        self.moveCenter()
        ##End Windows Seetings


        ##Connection Settings
        self.minButton = self.findChild(QtWidgets.QPushButton, 'minButton')
        self.minButton.clicked.connect(self.minButtonClicked)

        self.maxButton = self.findChild(QtWidgets.QPushButton, 'maxButton')
        self.maxButton.clicked.connect(self.maxButtonClicked)

        self.closeButton = self.findChild(QtWidgets.QPushButton, 'closeButton')
        self.closeButton.clicked.connect(self.closeButtonClicked)

        
        self.volumeSlider = self.findChild(QtWidgets.QSlider, 'volumeSlider')
        self.volumeSlider.valueChanged.connect(self.setVolume)


        self.positionSlider = self.findChild(QtWidgets.QSlider, 'positionSlider')
        self.positionSlider.sliderMoved.connect(self.setPosition)

        
        self.menuButton = self.findChild(QtWidgets.QPushButton, 'menuButton')
        self.menuButton.clicked.connect(self.showMenu)
        
        
        self.playbutton = self.findChild(QtWidgets.QPushButton, 'playpauseButton')
        self.playbutton.clicked.connect(self.playclick)

        self.preButton = self.findChild(QtWidgets.QPushButton, 'fwdButton')
        self.preButton.clicked.connect(self.setPrev)

        self.nextButton = self.findChild(QtWidgets.QPushButton, 'bwdButton')
        self.nextButton.clicked.connect(self.setNext)
        
        self.fullscrbutton = self.findChild(QtWidgets.QPushButton, 'fullScrButton')
        self.fullscrbutton.clicked.connect(self.fullscreen)
        
        
        self.muteButton = self.findChild(QtWidgets.QPushButton, 'muteButton')
        self.muteButton.clicked.connect(self.mutePlayer)

        self.playingLabel=self.findChild(QtWidgets.QLabel, 'playingLabel')
        
        self.reclistWidget=self.findChild(QtWidgets.QListWidget, 'reclistWidget')
        self.reclistWidget.itemDoubleClicked.connect(self.recListDblClick)
        
        ##End Connection Settings

        ##Create VideoWidget
        self.videoWidget = VideoWidget()
        self.videoLayout = self.findChild(QtWidgets.QVBoxLayout, 'playvideoLayout')
        self.videoLayout.addWidget(self.videoWidget)
        ##End VideoWidget
        
        self.createMenu()
        self.show()
        
    ##Menu Functions
    def createMenu(self):
        self.myMenu = QtWidgets.QMenu(self)
        openAction=QtWidgets.QAction('Open Video File', self)
        openAction.triggered.connect(self.openFile)
        self.myMenu.addAction(openAction)

        settingsAction=QtWidgets.QAction('Show Settings', self)
        settingsAction.triggered.connect(self.openSettings)
        self.myMenu.addAction(settingsAction)
        
        
        self.myMenu.addSeparator()
        self.myMenu.addAction(QtWidgets.QAction('About Me', self))
        self.myMenu.addSeparator()
        closeAction=QtWidgets.QAction('Exit', self)
        closeAction.triggered.connect(self.closeButtonClicked)
        self.myMenu.addAction(closeAction)
        self.myMenu.setStyleSheet('''
                                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(59, 65, 65, 255), stop:1 rgba(40, 44, 51, 255));
                                    font: 75 10pt "Arial";
                                    border-style: solid;
                                    border-color: #050a0e;
                                    border-width: 1px;
                                    padding: 2px;
                                ''')
    def showMenu(self):
        self.myMenu.exec_(QCursor.pos())
    ##End Menu Functions    

    ##Min_Max_Close Functions    
    def minButtonClicked(self):
        self.showMinimized()
        
    def maxButtonClicked(self):
        if self.isMaximized():
            self.showNormal()
            self.maxButton.setText('1')  # Toggle enlarge button icon
            self.maxButton.setToolTip("<html><head/><body><p>Maximize</p></body></html>")
        else:
            self.showMaximized()
            self.maxButton.setText('2')
            self.maxButton.setToolTip("<html><head/><body><p>Normal</p></body></html>")

    def closeButtonClicked(self):
        self.close()
    ##End Min_Max_Close Functions

    ##Main Form Event Functions
    def moveCenter(self):
        fg = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(centerpoint)
        self.move(fg.topLeft())
        
    def eventFilter(self, obj, event):
        # Event filter, used to solve the problem that the mouse returns to the standard mouse style after entering other controls
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(AL_Player, self).eventFilter(obj, event)  # Note that MyWindow is the name of your class
        # return QWidget.eventFilter(self, obj, event)  # This is fine, but be careful to change the window type

    def resizeEvent(self, QResizeEvent):
        # Custom window sizing events
        # Change the window size by three coordinate ranges
        self._right_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 5)
                            for y in range(self.titleWidget.height() + 20, self.height() - 5)]
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - 5)
                             for y in range(self.height() - 5, self.height() + 1)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 1)
                             for y in range(self.height() - 5, self.height() + 1)]

    def mousePressEvent(self, event):
        # Override mouse click events
        if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
            # Left click the border area in the lower right corner
            self._corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            # Left click on the right border area
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            # Click the lower border area with the left mouse button
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() < self.titleWidget.height()):
            # Left click on the title bar area
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        # Determine mouse position and switch mouse gesture
        if QMouseEvent.pos() in self._corner_rect:  # QMouseEvent.pos() get relative position
            self.setCursor(Qt.SizeFDiagCursor)
        elif QMouseEvent.pos() in self._bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self._right_rect:
            self.setCursor(Qt.SizeHorCursor)

        # When the left mouse button click and meet the requirements of the click area, different window adjustments are realized
        # There is no definition of the left and top five directions, mainly because the implementation is not difficult, but the effect is very poor. When dragging and dropping, the window flickers, and then study whether there is a better implementation
        if Qt.LeftButton and self._right_drag:
            # Right adjust window width
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
            # Lower adjustment window height
            self.resize(self.width(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._corner_drag:
            #  Because my window is set with rounded corners, this size adjustment is useless
            # Adjust the height and width at the same time in the lower right corner
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            # Title bar drag and drop window position
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        # After the mouse is released, each trigger is reset
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
    ##End Main Form Event Functions
        
    
    ##Media Player Functions
    def openFile(self):
        files_types = "MPEG-4 Video File (*.mp4);;Audio Video Interleave File (*.avi);;Matroska Video File (*.mkv);;MPEG Video (*.mpeg);;Windows Media Video (*.wmv);;MPEG-4 Playlist (*.m4u);;MPEG Video File (*.mpg);;All Files (*.*)"
        self.fileName = QFileDialog.getOpenFileName(self, "Select and Open Video", "/",files_types)[0]
        if self.fileName != '':
            if self.mediaPlayer ==None:
                self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
                self.mediaPlayer2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
                self.videoWidget2 = VideoWidget()
                self.grabber = VideoFrameGrabber(self.videoWidget2, self)
                self.mediaPlayer.setVideoOutput(self.videoWidget)
                self.mediaPlayer2.setVideoOutput(self.grabber)
                self.grabber.frameAvailable.connect(self.process_frame)
                self.mediaPlayer2.setMuted(True)
                self.mediaPlayer.stateChanged.connect(self.StateChanged)
                self.mediaPlayer.positionChanged.connect(self.positionChanged)
                self.mediaPlayer.durationChanged.connect(self.durationChanged)
                self.mediaPlayer.volumeChanged.connect(self.volumeChanged)
            self.mediaPlayer.stop()    
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
            self.mediaPlayer2.stop()    
            self.mediaPlayer2.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
            self.playingLabel.setText("Playing: "+self.fileName)
            QListWidgetItem(self.fileName,self.reclistWidget)
            self.reclistWidget.setCurrentItem(self.reclistWidget.currentItem())
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)

    def openSettings(self):
        if self.mediaPlayer!=None:
            self.mediaPlayer.pause()
            self.mediaPlayer2.pause()
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)
        self.settingsWindow = ALP_Settings(self)
        self.settingsWindow.show()
        
    def playclick(self):
        if self.mediaPlayer!=None:
            if self.playbutton.isChecked():
                self.mediaPlayer.play()
                self.mediaPlayer2.play()
                self.playbutton.setText(";")
            else:
                self.mediaPlayer.pause()
                self.mediaPlayer2.pause()
                self.playbutton.setText("4")
        
    def mutePlayer(self):
        if self.mediaPlayer!=None:
            self.mediaPlayer.setMuted(not self.mediaPlayer.isMuted())
            if self.mediaPlayer.isMuted():
                self.muteButton.setText("X")
            else:
                self.muteButton.setText("Xð")
    
    def fullscreen(self):
        self.videoWidget.setFullScreen(True)

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.mediaPlayer2.setPosition(position+self.delay)
        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def volumeChanged(self, volume):
        if self.mediaPlayer!=None:
            self.volumeSlider.setValue(volume)

    def setPosition(self, position):
        if self.mediaPlayer!=None:
            self.mediaPlayer.setPosition(position)
        
    def setVolume(self, volume):
        if self.mediaPlayer!=None:
            self.mediaPlayer.setVolume(volume)

    def setPrev(self,position):
        if self.mediaPlayer!=None:
            self.mediaPlayer.setPosition(self.mediaPlayer.position()-1000)

    def setNext(self,position):
        if self.mediaPlayer!=None:
            self.mediaPlayer.setPosition(self.mediaPlayer.position()+1000)

    def recListDblClick(self,item):
        if self.mediaPlayer !=None:
            self.mediaPlayer.stop()
            self.mediaPlayer2.stop()
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(item.text())))
            self.mediaPlayer2.setMedia(QMediaContent(QUrl.fromLocalFile(item.text())))
            self.playingLabel.setText("Playing: "+item.text())
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)

    def StateChanged(self,status):
        if status in [QMediaPlayer.EndOfMedia,QMediaPlayer.StoppedState]: 
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)
            
    def process_frame(self, image):
        if self.AMLStatus:
            img_list=self.divideImage(self.convertQImageToMat(image))
            self.sendColor(img_list)
            #print (self.AMLStatus)

    def divideImage(self,img):
        image_list=list()
        if self.bulbCount==0:
            image_list.append(img)
            return image_list
        elif self.bulbCount==1:
            height = img.shape[0]
            width = img.shape[1]
            width_cutoff = width // 2
            left = img[:, :width_cutoff]
            right = img[:, width_cutoff:]
            image_list.append(left)
            image_list.append(right)
            return image_list
        elif self.bulbCount==2:
            height = img.shape[0]
            width = img.shape[1]
            width_cutoff = width // 2
            left1 = img[:, :width_cutoff]
            right1 = img[:, width_cutoff:]
            img = cv2.rotate(left1, cv2.ROTATE_90_CLOCKWISE)
            height = img.shape[0]
            width = img.shape[1]
            width_cutoff = width // 2
            l2 = img[:, :width_cutoff]
            l1 = img[:, width_cutoff:]
            l2 = cv2.rotate(l2, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_list.append(l2)
            l1 = cv2.rotate(l1, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_list.append(l1)
            img = cv2.rotate(right1, cv2.ROTATE_90_CLOCKWISE)
            height = img.shape[0]
            width = img.shape[1]
            width_cutoff = width // 2
            r4 = img[:, :width_cutoff]
            r3 = img[:, width_cutoff:]
            r4 = cv2.rotate(r4, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_list.append(r4)
            r3 = cv2.rotate(r3, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_list.append(r3)
            return image_list

    def convertQImageToMat(self,incomingImage):
        '''  Converts a QImage into an opencv MAT format  '''
        incomingImage = incomingImage.convertToFormat(4)
        width = incomingImage.width()
        height = incomingImage.height()
        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
        return arr
    
    def sendColor(self,list):
        if self.bulbCount==0:
            img = list[0]
            clusters = 1
            dc = DominantColors(img, clusters)
            singleColors = dc.dominantColors()
            singleR=int(singleColors[0,0])
            singleG=int(singleColors[0,1])
            singleB=int(singleColors[0,2])
            try:
                if singleR<10 and singleG<10 and singleB<10:
                    self.singleBulb.turn_off()
                else:
                    self.singleBulb.turn_on()
                    self.singleBulb.set_rgb(singleR,singleG,singleB)
            except:
                pass
            
        elif self.bulbCount==1:
            leftimg = list[0]
            rightimg = list[1]
            clusters = 1
            dc = DominantColors(leftimg, clusters) 
            doubleColors = dc.dominantColors()
            
            leftR=int(doubleColors[0,0])
            leftG=int(doubleColors[0,1])
            leftB=int(doubleColors[0,2])

            dc = DominantColors(rightimg, clusters) 
            doubleColors = dc.dominantColors()
            rightR=int(doubleColors[0,0])
            rightG=int(doubleColors[0,1])
            rightB=int(doubleColors[0,2])

            try:
                if leftR<10 and leftG<10 and leftB<10:
                    self.leftBulb.turn_off()
                else:
                    self.leftBulb.turn_on()
                    self.leftBulb.set_rgb(leftR,leftG,leftB)
                    
                if rightR<10 and rightG<10 and rightB<10:
                    self.rightBulb.turn_off()
                else:
                    self.rightBulb.turn_on()
                    self.rightBulb.set_rgb(rightR,rightG,rightB)
            except:
                pass
        
        elif self.bulbCount==2:
            
            leftTopimg = list[1]
            rightTopimg = list[3]
            leftBotimg = list[0]
            rightBotimg = list[2]
            clusters = 1
            
            dc = DominantColors(leftTopimg, clusters) 
            fourColors = dc.dominantColors()
            
            leftTopR=int(fourColors[0,0])
            leftTopG=int(fourColors[0,1])
            leftTopB=int(fourColors[0,2])

            dc = DominantColors(rightTopimg, clusters) 
            fourColors = dc.dominantColors()
            rightTopR=int(fourColors[0,0])
            rightTopG=int(fourColors[0,1])
            rightTopB=int(fourColors[0,2])

            dc = DominantColors(leftBotimg, clusters) 
            fourColors = dc.dominantColors()
            leftBotR=int(fourColors[0,0])
            leftBotG=int(fourColors[0,1])
            leftBotB=int(fourColors[0,2])

            dc = DominantColors(rightBotimg, clusters) 
            fourColors = dc.dominantColors()
            rightBotR=int(fourColors[0,0])
            rightBotG=int(fourColors[0,1])
            rightBotB=int(fourColors[0,2])

            try:
                if leftTopR<10 and leftTopG<10 and leftTopB<10:
                    self.leftTopBulb.turn_off()
                else:
                    self.leftTopBulb.turn_on()
                    self.leftTopBulb.set_rgb(leftTopR,leftTopG,leftTopB)
                    
                if rightTopR<10 and rightTopG<10 and rightTopB<10:
                    self.rightTopBulb.turn_off()
                else:
                    self.rightTopBulb.turn_on()
                    self.rightTopBulb.set_rgb(rightTopR,rightTopG,rightTopB)
                    
                if leftBotR<10 and leftBotG<10 and leftBotB<10:
                    self.leftBottomBulb.turn_off()
                else:
                    self.leftBottomBulb.turn_on()
                    self.leftBottomBulb.set_rgb(leftBotR,leftBotG,leftBotB)

                if rightBotR<10 and rightBotG<10 and rightBotB<10:
                    self.rightBottomBulb.turn_off()
                else:
                    self.rightBottomBulb.turn_on()
                    self.rightBottomBulb.set_rgb(rightBotR,rightBotG,rightBotB)
            except:
                pass
        
        
    ##End Media Player Functions

if __name__ == '__main__':
    
    # Suitable for 2k high resolution screen, low resolution screen can be default
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)    
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = AL_Player()
    sys.exit(app.exec_())
