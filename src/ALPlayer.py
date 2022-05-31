#Dominat Color Modülü değiştirildi, cluster sayısı artıtırıldı,
#koyu renk tonlarında lamba davranışları geliştirildi.
import sys
import os
from os.path import exists
from configparser import ConfigParser
import time
import numpy as np
import numpy
import cv2

import PyQt5
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QVideoFrame, QAbstractVideoSurface, QAbstractVideoBuffer, QVideoSurfaceFormat
from PyQt5.QtMultimediaWidgets import QVideoWidget

import yeelight
from yeelight.main import Bulb, discover_bulbs
from yeelight import enums

from Settings import ALP_Settings
from AboutUs import ALP_AboutUs
from Video import VideoWidget
from VideoGrabber import GrabVideoSurface
from Dominant import FindDominantColors

class AL_Player(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AL_Player, self).__init__(parent)
        self.ui = uic.loadUi('./Settings/ALPlayer.ui',self)
        self.mainWindow = self.findChild(QtWidgets.QMainWindow, 'MainForm')
        self.setStyleSheet('background-color: black;')
        self.mediaPlayer =None
        ##Read Settings and Initilaze Bulb
        self.firstBulbIp=None
        self.secondBulbIp=None
        self.thirdBulbIp=None
        self.fourthBulbIp=None
        self.bulbCount=None
        self.AMLStatus=False

        self.singleBulb=None
        
        self.leftBulb=None
        self.rightBulb=None
        
        self.leftTopBulb=None
        self.rightTopBulb=None
        self.leftBottomBulb=None
        self.rightBottomBulb=None
        
        if exists('./Settings/Settings.ini') :
                        
           getSettingObj = ConfigParser()
           getSettingObj.read('./Settings/Settings.ini')
           countBulb= getSettingObj["COUNTBULB"]
           self.bulbCount=int(countBulb["count"])
           ipBulbs= getSettingObj["BULBS"]
           self.firstBulbIp=ipBulbs["firstIp"]
           self.secondBulbIp=ipBulbs["secondIp"]
           self.thirdBulbIp=ipBulbs["thirdIp"]
           self.fourthBulbIp=ipBulbs["fourthIp"]
           self.createBulb()
           #print(self.AMLStatus)
           if not self.AMLStatus:
               popup= QMessageBox()
               popup.setWindowTitle("Connection Issues")
               popup.setText("Unexpected error occurred in lamp connections.\nPlease check your connection settings.")
               popup.setIcon(QMessageBox.Critical)
               self.AMLStatus=False
               res= popup.exec_()
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
        self.playbutton.clicked.connect(self.playClick)

        self.fwdButton = self.findChild(QtWidgets.QPushButton, 'fwdButton')
        self.fwdButton.clicked.connect(self.setFwd)

        self.bwdButton = self.findChild(QtWidgets.QPushButton, 'bwdButton')
        self.bwdButton.clicked.connect(self.setBwd)

        self.nextButton = self.findChild(QtWidgets.QPushButton, 'nextButton')
        self.nextButton.clicked.connect(self.setNext)

        self.prevButton = self.findChild(QtWidgets.QPushButton, 'prevButton')
        self.prevButton.clicked.connect(self.setPrev)

        self.fullscrbutton = self.findChild(QtWidgets.QPushButton, 'fullScrButton')
        self.fullscrbutton.clicked.connect(self.fullScreen)
        
        
        self.muteButton = self.findChild(QtWidgets.QPushButton, 'muteButton')
        self.muteButton.clicked.connect(self.mutePlayer)

        self.playingLabel=self.findChild(QtWidgets.QLabel, 'playingLabel')
        
        self.reclistWidget=self.findChild(QtWidgets.QListWidget, 'reclistWidget')
        self.reclistWidget.itemDoubleClicked.connect(self.recListDblClick)

        self.shortCut = QShortcut(QKeySequence("F"), self)
        self.shortCut.activated.connect(self.fullScreen)
        self.shortCut = QShortcut(QKeySequence("Esc"), self)
        self.shortCut.activated.connect(self.normalScreen)
        
        
        ##End Connection Settings

        ##Create VideoWidget
        self.videoWidget = VideoWidget(self)
        self.grabVideoSurface = GrabVideoSurface(self)
        self.videoWidget.setAutoFillBackground(True)
        self.videoLayout = self.findChild(QtWidgets.QVBoxLayout, 'playvideoLayout')
        self.videoLayout.addWidget(self.videoWidget)
        ##End VideoWidget
        
        self.createMenu()
        self.show()
        
    ##Menu Functions
    def createBulb(self):
        if self.bulbCount==0:
            if self.singleBulb is None:
                try:
                    self.singleBulb = Bulb(self.firstBulbIp, effect="smooth", auto_on=True)
                    #self.singleBulb.turn_on()
                    music=self.singleBulb.get_properties()
                    if music['music_on']=='0':
                        self.singleBulb.start_music(2023)
                    else:
                        self.singleBulb.stop_music()
                        time.sleep(1)
                        self.singleBulb.start_music(2023)
                    self.singleBulb.set_color_temp(6500)
                    self.AMLStatus=True
                except:
                    self.AMLStatus=False    
        elif self.bulbCount==1:
            if self.leftBulb is None:
                try:
                    self.leftBulb = Bulb(self.firstBulbIp, effect="smooth", auto_on=True)
                    #self.leftBulb.turn_on()
                    music=self.leftBulb.get_properties()
                    if music['music_on']=='0':
                        self.leftBulb.start_music(65443)
                    else:
                        self.leftBulb.stop_music()
                        time.sleep(1)
                        self.leftBulb.start_music(65443)
                    self.leftBulb.set_color_temp(6500)
                    self.AMLStatus=True
                except:
                    self.AMLStatus=False
            if self.rightBulb is None:
                try:
                    self.rightBulb = Bulb(self.secondBulbIp, effect="smooth", auto_on=True)
                    #self.rightBulb.turn_on()
                    music=self.rightBulb.get_properties()
                    if music['music_on']=='0':
                        self.rightBulb.start_music(65443)
                    else:
                        self.rightBulb.stop_music()
                        time.sleep(1)
                        self.rightBulb.start_music(65443)
                    self.rightBulb.set_color_temp(6500)
                    self.AMLStatus=True
                except:
                    self.AMLStatus=False
        elif self.bulbCount==2:
            if self.leftTopBulb is None:
                try:
                    self.leftTopBulb = Bulb(self.firstBulbIp, effect="smooth", auto_on=True)
                    #self.leftTopBulb.turn_on()
                    music=self.leftTopBulb.get_properties()
                    if music['music_on']=='0':
                        self.leftTopBulb.start_music(2023)
                    else:
                        self.leftTopBulb.stop_music()
                        time.sleep(1)
                        self.leftTopBulb.start_music(2023)
                    self.leftTopBulb.set_color_temp(6500)
                    self.AMLStatus=True
                except:
                    self.AMLStatus=False
            if self.rightTopBulb is None:
                try:
                    self.rightTopBulb = Bulb(self.secondBulbIp, effect="smooth", auto_on=True)
                    #self.rightTopBulb.turn_on()
                    music=self.rightTopBulb.get_properties()
                    if music['music_on']=='0':
                        self.rightTopBulb.start_music(2023)
                    else:
                        self.rightTopBulb.stop_music()
                        time.sleep(1)
                        self.rightTopBulb.start_music(2023)
                    self.rightTopBulb.set_color_temp(6500)
                    self.AMLStatus=True
                except:
                    self.AMLStatus=False
            if self.leftBottomBulb is None:
                try:
                    self.leftBottomBulb = Bulb(self.thirdBulbIp, effect="smooth", auto_on=True)
                    #self.leftBottomBulb.turn_on()
                    music=self.leftBottomBulb.get_properties()
                    if music['music_on']=='0':
                        self.leftBottomBulb.start_music(2023)
                    else:
                        self.leftBottomBulb.stop_music()
                        time.sleep(1)
                        self.leftBottomBulb.start_music(2023)
                    self.leftBottomBulb.set_color_temp(6500)
                    self.AMLStatus=True
                except:
                    self.AMLStatus=False
            if self.rightBottomBulb is None:
                try:
                    self.rightBottomBulb = Bulb(self.fourthBulbIp, effect="smooth", auto_on=True)
                    #self.rightBottomBulb.turn_on()
                    music=self.rightBottomBulb.get_properties()
                    if music['music_on']=='0':
                        self.rightBottomBulb.start_music(2023)
                    else:
                        self.rightBottomBulb.stop_music()
                        time.sleep(1)
                        self.rightBottomBulb.start_music(2023)
                    self.rightBottomBulb.set_color_temp(6500)
                    self.AMLStatus=True
                except:
                    self.AMLStatus=False
        
    def closeBulb(self):
        if self.bulbCount==0:
               self.singleBulb.turn_off()
        elif self.bulbCount==1:
               self.leftBulb.turn_off() 
               self.rightBulb.turn_off()
        elif self.bulbCount==2:
               self.leftTopBulb.turn_off() 
               self.rightTopBulb.turn_off()
               self.leftBottomBulb.turn_off()
               self.rightBottomBulb.turn_off()
               
    def openBulb(self):
        if self.bulbCount==0:
               self.singleBulb.turn_on()
        elif self.bulbCount==1:
               self.leftBulb.turn_on() 
               self.rightBulb.turn_on()
        elif self.bulbCount==2:
               self.leftTopBulb.turn_on() 
               self.rightTopBulb.turn_on()
               self.leftBottomBulb.turn_on()
               self.rightBottomBulb.turn_on()

    def createMenu(self):
        self.myMenu = QtWidgets.QMenu(self)
        openAction=QtWidgets.QAction('Open Video File', self)
        openAction.triggered.connect(self.openFile)
        self.myMenu.addAction(openAction)

        settingsAction=QtWidgets.QAction('Show Settings', self)
        settingsAction.triggered.connect(self.openSettings)
        self.myMenu.addAction(settingsAction)
        
        
        self.myMenu.addSeparator()
        aUsAction=QtWidgets.QAction('About Us', self)
        aUsAction.triggered.connect(self.aboutUs)
        self.myMenu.addAction(aUsAction)
        
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
            self.maxButton.setText('1')  
            self.maxButton.setToolTip("Maximize")
        else:
            self.showMaximized()
            self.maxButton.setText('2')
            self.maxButton.setToolTip("Normal")

    def closeButtonClicked(self):
        if self.AMLStatus == True:
            self.closeBulb()
        sys.exit()
    ##End Min_Max_Close Functions

    ##Main Form Event Functions
    #In this part of the code, examples
    #from https://www.fatalerrors.org/a/0N921Q.html were used.
    
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
        if self.windowState()in[QtCore.Qt.WindowMinimized]:
           # Window is minimised. Restore it.
           self.setAttribute(Qt.WA_Mapped)
        return super(AL_Player, self).eventFilter(obj, event)
        

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
            self._corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() < self.titleWidget.height()):
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.pos() in self._corner_rect:  
            self.setCursor(Qt.SizeFDiagCursor)
        elif QMouseEvent.pos() in self._bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self._right_rect:
            self.setCursor(Qt.SizeHorCursor)
        if Qt.LeftButton and self._right_drag:
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
            self.resize(self.width(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._corner_drag:
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        
    def changeEvent(self,event):
        if event.type() == QEvent.WindowStateChange:
            if not(self.isMinimized()):
                self.setAttribute(Qt.WA_Mapped)
                self.videoWidget.updateGeometry()
    
    ##End Main Form Event Functions
        
    
    ##Media Player Functions
    def openFile(self):
        files_types = "MPEG-4 Video File (*.mp4);;Audio Video Interleave File (*.avi);;Matroska Video File (*.mkv);;MPEG Video (*.mpeg);;Windows Media Video (*.wmv);;MPEG-4 Playlist (*.m4u);;MPEG Video File (*.mpg);;All Files (*.*)"
        self.fileName = QFileDialog.getOpenFileName(self, "Select and Open Video", "/",files_types)[0]
        if self.fileName != '':
            if self.mediaPlayer ==None:
                self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
                self.videoWidget.setMediaPlayer(self.mediaPlayer)
                self.mediaPlayer.setVideoOutput([self.videoWidget.videoSurface(), self.grabVideoSurface])
                self.mediaPlayer.stateChanged.connect(self.stateChanged)
                self.mediaPlayer.positionChanged.connect(self.positionChanged)
                self.mediaPlayer.durationChanged.connect(self.durationChanged)
                self.mediaPlayer.volumeChanged.connect(self.volumeChanged)
                
            self.mediaPlayer.stop()    
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
            
            self.playingLabel.setText("Playing: "+self.fileName)
            QListWidgetItem(self.fileName,self.reclistWidget)
            self.reclistWidget.setCurrentRow(self.reclistWidget.count()-1)
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)

    def openSettings(self):
        if self.mediaPlayer!=None:
            self.mediaPlayer.pause()
            
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)
        self.settingsWindow = ALP_Settings(self)
        self.settingsWindow.show()
        
    def aboutUs(self):
        if self.mediaPlayer!=None:
            self.mediaPlayer.pause()
            
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)
        
        self.aUsWindow = ALP_AboutUs(self)
        self.aUsWindow.show()
        
    def playClick(self):
        if self.mediaPlayer!=None:
            if self.playbutton.isChecked():
                self.mediaPlayer.play()
            else:
                self.mediaPlayer.pause()
       
    def mutePlayer(self):
        if self.mediaPlayer!=None:
            self.mediaPlayer.setMuted(not self.mediaPlayer.isMuted())
            if self.mediaPlayer.isMuted():
                self.muteButton.setText("X")
            else:
                self.muteButton.setText("Xð")
    
    def fullScreen(self):
        if self.mediaPlayer!=None:
            if self.mediaPlayer.state()in [QMediaPlayer.PausedState, QMediaPlayer.PlayingState]:
                self.videoWidget.setFullScreen(True)
                self.videoWidget.setCursor(Qt.BlankCursor)
                
    def normalScreen(self):
        if self.mediaPlayer!=None:
            if self.mediaPlayer.state()in [QMediaPlayer.PausedState, QMediaPlayer.PlayingState]:
                self.videoWidget.setFullScreen(False)
                self.videoWidget.setCursor(Qt.ArrowCursor)
                    
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        if self.AMLStatus == True:
            image = self.grabVideoSurface.getCurrentFrame
            if not image.isNull():
                img_list=self.divideImage(self.convertQImageToMat(image))
                self.sendColor(img_list)
        
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

    def setFwd(self,position):
        if self.mediaPlayer!=None:
            self.mediaPlayer.setPosition(self.mediaPlayer.position()-1000)

    def setBwd(self,position):
        if self.mediaPlayer!=None:
            self.mediaPlayer.setPosition(self.mediaPlayer.position()+1000)

    def setNext(self):
        current=self.reclistWidget.currentRow()
        total=self.reclistWidget.count()-1
        if current<total:
            current+=1
            self.reclistWidget.setCurrentRow(current)
            if self.mediaPlayer!=None:
                self.mediaPlayer.stop()
                
                file=self.reclistWidget.currentItem().text()
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
                
                self.playingLabel.setText("Playing: "+file)
                self.playbutton.setText("4")
                self.playbutton.setChecked(False)
            
    def setPrev(self):
        current=self.reclistWidget.currentRow()
        if current>0:
            current-=1
            self.reclistWidget.setCurrentRow(current)
            if self.mediaPlayer!=None:
                self.mediaPlayer.stop()
                
                file=self.reclistWidget.currentItem().text()
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
                
                self.playingLabel.setText("Playing: "+file)
                self.playbutton.setText("4")
                self.playbutton.setChecked(False)
        
    def recListDblClick(self,item):
        if self.mediaPlayer !=None:
            self.mediaPlayer.stop()
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(item.text())))
            self.playingLabel.setText("Playing: "+item.text())
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)

    def stateChanged(self,status):
        if status in [QMediaPlayer.EndOfMedia,QMediaPlayer.StoppedState]:
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)
            self.mediaPlayer.setPosition(0)
            if self.AMLStatus == True:
                self.closeBulb()
        if status in [QMediaPlayer.PausedState]:
            self.playbutton.setText("4")
            self.playbutton.setChecked(False)
        if status in [QMediaPlayer.PlayingState]:
            self.playbutton.setText(";")
            self.playbutton.setChecked(True)
            if self.AMLStatus == True:
                self.openBulb()
            
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
            left12 = img[:, :width_cutoff]
            left11 = img[:, width_cutoff:]
            left12 = cv2.rotate(left12, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_list.append(left12)
            left11 = cv2.rotate(left11, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_list.append(left11)
            img = cv2.rotate(right1, cv2.ROTATE_90_CLOCKWISE)
            height = img.shape[0]
            width = img.shape[1]
            width_cutoff = width // 2
            right12 = img[:, :width_cutoff]
            right11 = img[:, width_cutoff:]
            right12 = cv2.rotate(right12, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_list.append(right12)
            right11 = cv2.rotate(right11, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_list.append(right11)
            return image_list

    def convertQImageToMat(self,sourceImage):
        #Converts QImage to MAT format
        sourceImage = sourceImage.convertToFormat(4)
        width = sourceImage.width()
        height = sourceImage.height()
        ptr = sourceImage.bits()
        ptr.setsize(sourceImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)
        return arr
    
    def sendColor(self,list):
        if self.bulbCount==0:
            img = list[0]
            clusters = 5
            dc = FindDominantColors(img, clusters)
            singleColors = dc.dominantColors()
            try:
                if dc.MAXINDEX > -1:
                    self.singleBulb.set_rgb(int(singleColors[dc.MAXINDEX][0]), int(singleColors[dc.MAXINDEX][1]), int(singleColors[dc.MAXINDEX][2]))
                    self.singleBulb.set_brightness(dc.BRIGHTNESS)
                else:
                    self.singleBulb.turn_off()
            except:
                pass
            
        elif self.bulbCount==1:
            leftimg = list[0]
            rightimg = list[1]
            clusters = 5
            dc = FindDominantColors(leftimg, clusters)
            doubleColors = dc.dominantColors()
            leftBrightness=dc.BRIGHTNESS
            leftMaxindex=dc.MAXINDEX
            leftR=int(doubleColors[leftMaxindex][0])
            leftG=int(doubleColors[leftMaxindex][1])
            leftB=int(doubleColors[leftMaxindex][2])
            dc = FindDominantColors(rightimg, clusters) 
            doubleColors = dc.dominantColors()
            rightBrightness=dc.BRIGHTNESS
            rightMaxindex=dc.MAXINDEX
            rightR=int(doubleColors[rightMaxindex][0])
            rightG=int(doubleColors[rightMaxindex][1])
            rightB=int(doubleColors[rightMaxindex][2])
            try:
                if leftMaxindex > -1:
                    self.leftBulb.turn_on()
                    self.leftBulb.set_rgb(leftR,leftG,leftB)
                    self.leftBulb.set_brightness(leftBrightness)
                else:
                    self.leftBulb.turn_off()

                if rightMaxindex > -1:
                    self.rightBulb.turn_on()
                    self.rightBulb.set_rgb(rightR,rightG,rightB)
                    self.rightBulb.set_brightness(rightBrightness)
                else:
                    self.rightBulb.turn_off()
            except:
                pass
        
        elif self.bulbCount==2:
            
            leftTopimg = list[1]
            rightTopimg = list[3]
            leftBotimg = list[0]
            rightBotimg = list[2]
            clusters = 5
            
            dc = FindDominantColors(leftTopimg, clusters)
            fourColors = dc.dominantColors()
            leftTopBrightness=dc.BRIGHTNESS
            leftTopMaxindex=dc.MAXINDEX
            leftTopR=int(fourColors[leftTopMaxindex][0])
            leftTopG=int(fourColors[leftTopMaxindex][1])
            leftTopB=int(fourColors[leftTopMaxindex][2])
            
            dc = FindDominantColors(rightTopimg, clusters) 
            fourColors = dc.dominantColors()
            rightTopBrightness=dc.BRIGHTNESS
            rightTopMaxindex=dc.MAXINDEX
            rightTopR=int(fourColors[rightTopMaxindex][0])
            rightTopG=int(fourColors[rightTopMaxindex][1])
            rightTopB=int(fourColors[rightTopMaxindex][2])

            dc = FindDominantColors(leftBotimg, clusters)
            fourColors = dc.dominantColors()
            leftBotBrightness=dc.BRIGHTNESS
            leftBotMaxindex=dc.MAXINDEX
            leftBotR=int(fourColors[leftBotMaxindex][0])
            leftBotG=int(fourColors[leftBotMaxindex][1])
            leftBotB=int(fourColors[leftBotMaxindex][2])
            
            dc = FindDominantColors(rightBotimg, clusters) 
            fourColors = dc.dominantColors()
            rightBotBrightness=dc.BRIGHTNESS
            rightBotMaxindex=dc.MAXINDEX
            rightBotR=int(fourColors[rightBotMaxindex][0])
            rightBotG=int(fourColors[rightBotMaxindex][1])
            rightBotB=int(fourColors[rightBotMaxindex][2])

            try:
                if leftTopMaxindex > -1:
                    self.leftTopBulb.turn_on()
                    self.leftTopBulb.set_rgb(leftTopR,leftTopG,leftTopB)
                    self.leftTopBulb.set_brightness(leftTopBrightness)
                else:
                    self.leftTopBulb.turn_off()

                if rightTopMaxindex > -1:
                    self.rightTopBulb.turn_on()
                    self.rightTopBulb.set_rgb(rightTopR,rightTopG,rightTopB)
                    self.rightTopBulb.set_brightness(rightTopBrightness)
                else:
                    self.rightTopBulb.turn_off()

                if leftBotMaxindex > -1:
                    self.leftBottomBulb.turn_on()
                    self.leftBottomBulb.set_rgb(leftBotR,leftBotG,leftBotB)
                    self.leftBottomBulb.set_brightness(leftBotBrightness)
                else:
                    self.leftBottomBulb.turn_off()

                if rightBotMaxindex > -1:
                    self.rightBottomBulb.turn_on()
                    self.rightBottomBulb.set_rgb(rightBotR,rightBotG,rightBotB)
                    self.rightBottomBulb.set_brightness(rightBotBrightness)
                else:
                    self.rightBottomBulb.turn_off()
            except:
                pass
            
    ##End Media Player Functions

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)    
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('./Settings/images/logo.gif'))
    mainWindow = AL_Player()
    sys.exit(app.exec_())
