from PyQt5.QtGui import QColor, qGray, QImage, QPainter, QPalette
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt
import sys
class VideoWidget(QVideoWidget):
    mPlayer=None
    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_PaintOnScreen, True)
        palette = self.palette()
        palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(palette)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       
        '''
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(40, 44, 51, 255), stop:1 rgba(76, 47, 50, 255));
        '''
    def setMediaPlayer(self, mp):
        self.mPlayer=mp
        
    def closeEvent(self, event):
        sys.exit()
        #event.ignore()  #if we want the program not to close
        
    def keyPressEvent(self, event):
        #Set keyPressEvent
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.setFullScreen(False)
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            
        elif event.key() == Qt.Key_F:
            if self.mPlayer.state() == 1:
                self.setFullScreen(not self.isFullScreen())
                if self.isFullScreen():
                    self.setCursor(Qt.BlankCursor)
                else:
                    self.setCursor(Qt.ArrowCursor)
            else:
                pass
            event.accept()
            
        elif event.key() == Qt.Key_Space:
            if self.mPlayer.state() == 1:
                self.mPlayer.pause()
            else:
                self.mPlayer.play()
            event.accept()
        elif event.key() == Qt.Key_M:
            self.mPlayer.setMuted(not self.mPlayer.isMuted())
            event.accept()
        else:
            super(VideoWidget, self).keyPressEvent(event)
           
    def mouseDoubleClickEvent(self, event):
        #Set mouseDoubleClickEvent
        try:
            if self.mPlayer.state() == 1:
                self.setFullScreen(not self.isFullScreen())
                if self.isFullScreen():
                    self.setCursor(Qt.BlankCursor)
                else:
                    self.setCursor(Qt.ArrowCursor)
                event.accept()
        except:
            pass
    
