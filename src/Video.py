from PyQt5.QtGui import QColor, qGray, QImage, QPainter, QPalette
from PyQt5.QtMultimedia import (QAbstractVideoBuffer, QMediaContent, QMediaMetaData, QMediaPlayer, QMediaPlaylist, QVideoFrame, QVideoProbe)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog, QFormLayout, QHBoxLayout, QLabel, QListView, QMessageBox, QPushButton,
        QSizePolicy, QSlider, QStyle, QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtCore import QUrl, Qt

class VideoWidget(QVideoWidget):
    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        plt = self.palette()
        plt.setColor(QPalette.Window, Qt.black)
        self.setPalette(plt)
        self.setAttribute(Qt.WA_OpaquePaintEvent,False)

    def keyPressEvent(self, event):
        #Set keyPressEvent
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.setFullScreen(False)
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        elif event.key() == Qt.Key_F:
            if self.mediaObject().state() == QMediaPlayer.PlayingState:
                self.setFullScreen(not self.isFullScreen())
                if self.isFullScreen():
                    self.setCursor(Qt.BlankCursor)
                else:
                    self.setCursor(Qt.ArrowCursor)
            event.accept()
        elif event.key() == Qt.Key_Space:
            if self.mediaObject().state() == QMediaPlayer.PlayingState:
                self.mediaObject().pause()
            else:
                self.mediaObject().play()
            event.accept()
        elif event.key() == Qt.Key_M:
            self.mediaObject().setMuted(not self.mediaObject().isMuted())
            event.accept()
        else:
            super(VideoWidget, self).keyPressEvent(event)
            
    def mouseDoubleClickEvent(self, event):
        #Set mouseDoubleClickEvent
        try:
            if self.mediaObject().state() == QMediaPlayer.PlayingState:
                self.setFullScreen(not self.isFullScreen())
                if self.isFullScreen():
                    self.setCursor(Qt.BlankCursor)
                else:
                    self.setCursor(Qt.ArrowCursor)
            event.accept()
        except:
            pass
