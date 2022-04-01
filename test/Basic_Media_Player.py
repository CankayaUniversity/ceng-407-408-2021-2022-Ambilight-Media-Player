from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QSlider, QStyle
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt
import sys

class QtVideoPlayer(QWidget):
    def __init__(self,parent = None):
        super(QtVideoPlayer,self).__init__(parent)
        self.setWindowTitle("Basic Media Player Demo") #set window title
        self.vWidget = QVideoWidget() #mediaplayer will be displayed here
        self.mPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface) #create mediaplayer
        self.mPlayer.setVideoOutput(self.vWidget) #set mediaplayer Video Output
        
        self.mPlayer.stateChanged.connect(self.mediaStateChanged) #connect media state change
        self.mPlayer.positionChanged.connect(self.positionChanged) #connect media player position change
        self.mPlayer.durationChanged.connect(self.durationChanged) #connect media player duration change
        
        self.vWidget.setStyleSheet('background-color: black;') #set videoWidget Background color 

        self.posSlider = QSlider(Qt.Horizontal) #create media player position slider
        self.posSlider.setRange(0,0) #set slider range
        self.posSlider.sliderMoved.connect(self.setPosition)#connect position of slider change

        self.mainLayout = QVBoxLayout() #create main layout
        self.commandLayout = QHBoxLayout() #create HBoxLayout for insert commands
        

        self.openFileBtn = QPushButton("Open") #create button for select file
        self.openFileBtn.clicked.connect(self.selectFile) #connect openFileBtn clicked

        self.playPauseBtn = QPushButton() #create button for play and pause action
        self.playPauseBtn.setEnabled(False) #set enable of playPauseBtn is false

        #set icon of playPauseBtn - We can use standard icons inside the QStyle class
        #For details, see https://doc.qt.io/qt-5/qstyle.html.
        self.playPauseBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay)) 
        self.playPauseBtn.clicked.connect(self.playPauseClick) #connect playPauseBtn clicked

        self.commandLayout.addWidget(self.openFileBtn) #add openFileBtn in commandLayout
        self.commandLayout.addWidget(self.playPauseBtn) #add playPauseBtn in commandLayout
        self.commandLayout.addWidget(self.posSlider) #add posSlider in commandLayout
        
        self.mainLayout.addWidget(self.vWidget) #add Video Widget in main Layout
        self.mainLayout.addLayout(self.commandLayout) #add commandLayout in main Layout

        self.setLayout(self.mainLayout) #set main layout

    def selectFile(self):
        filesTypes = "MPEG-4 Video File (*.mp4);;Audio Video Interleave File (*.avi);;Matroska Video File (*.mkv);;MPEG Video (*.mpeg);;Windows Media Video (*.wmv);;MPEG Video File (*.mpg);;All Files (*.*)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Select and Open Video", "/",filesTypes)
        if fileName != '':
            self.mPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playPauseBtn.setEnabled(True)

    def playPauseClick(self):
        if self.mPlayer.state() == QMediaPlayer.PlayingState:
            self.mPlayer.pause()
        else:
            self.mPlayer.play()
    def positionChanged(self, position):
        self.posSlider.setValue(position)

    def durationChanged(self, duration):
        self.posSlider.setRange(0, duration)
        
    def setPosition(self, position):
        self.mPlayer.setPosition(position)

    def mediaStateChanged(self, state):
        if self.mPlayer.state() == QMediaPlayer.PlayingState:
            self.playPauseBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playPauseBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

if __name__ == '__main__':

    myapp=QApplication(sys.argv) #create application
    myplayer=QtVideoPlayer() #create mediaplayer object
    myplayer.resize(640,480) #set size of mediaplayer object
    myplayer.show() #show mediaplayer object
    sys.exit(myapp.exec_())
                      
