from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
import sys

class QtVideoPlayer(QWidget):
    def __init__(self,parent = None):
        super(QtVideoPlayer,self).__init__(parent)
        self.setWindowTitle("Basic Media Player Demo") #set window title
        self.vWidget = QVideoWidget() #mediaplayer will be displayed here
        self.mPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface) #create mediaplayer
        self.mPlayer.setVideoOutput(self.vWidget) #set mediaplayer Video Output
        #self.mPlayer.stateChanged.connect(self.mediaStateChanged)
        #self.mPlayer.positionChanged.connect(self.positionChanged)
        #self.mPlayer.durationChanged.connect(self.durationChanged)
        self.vWidget.setStyleSheet('background-color: black;')

        self.mainLayout = QVBoxLayout() #create main layout
        self.commandLayout = QHBoxLayout() #create HBoxLayout for insert commands
        

        self.openFileBtn = QPushButton("Select and Open Video File") #create button for select file
        self.openFileBtn.clicked.connect(self.selectFile) #connect openFileBtn clicked

        self.commandLayout.addWidget(self.openFileBtn) #add openFileBtn in commandLayout
        
        
        self.mainLayout.addWidget(self.vWidget) #add Video Widget in main Layout
        self.mainLayout.addLayout(self.commandLayout) #add commandLayout in main Layout

        self.setLayout(self.mainLayout) #set main layout

    def selectFile(self):
        filesTypes = "MPEG-4 Video File (*.mp4);;Audio Video Interleave File (*.avi);;Matroska Video File (*.mkv);;MPEG Video (*.mpeg);;Windows Media Video (*.wmv);;MPEG Video File (*.mpg);;All Files (*.*)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Select and Open Video", "/",filesTypes)
        if fileName != '':
            self.mPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.mPlayer.play()
        #fileName = QFileDialog.getOpenFileName(self, "Select and Open Video", "/",filesTypes)[0]
        #print(fileName)
        #if self.fileName != '':
            #self.mPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName))) #set mediaplayer file
            #self.mPlayer.play()

    
if __name__ == '__main__':

    myapp=QApplication(sys.argv) #create application
    myplayer=QtVideoPlayer() #create mediaplayer object
    myplayer.resize(640,480) #set size of mediaplayer object
    myplayer.show() #show mediaplayer object

    sys.exit(myapp.exec_())
                      
