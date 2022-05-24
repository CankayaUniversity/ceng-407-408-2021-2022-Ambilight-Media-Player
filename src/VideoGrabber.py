from PyQt5.QtWidgets import QPushButton, QStyle, QVBoxLayout, QWidget, QFileDialog, QLabel, QSlider, QHBoxLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os

class GrabVideoSurface(QAbstractVideoSurface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentFrame = QImage()
    @property
    def getCurrentFrame(self):
        return self.currentFrame

    def supportedPixelFormats(self, handleType=QAbstractVideoBuffer.NoHandle):
        formats = [QVideoFrame.PixelFormat()]
        if handleType == QAbstractVideoBuffer.NoHandle:
            for f in [
                QVideoFrame.Format_RGB32,
                QVideoFrame.Format_ARGB32,
                QVideoFrame.Format_ARGB32_Premultiplied,
                QVideoFrame.Format_RGB565,
                QVideoFrame.Format_RGB555,
                QVideoFrame.Format_ARGB32,
                QVideoFrame.Format_ARGB32_Premultiplied,
                QVideoFrame.Format_RGB32,
                QVideoFrame.Format_RGB24,
                QVideoFrame.Format_RGB565,
                QVideoFrame.Format_RGB555,
                QVideoFrame.Format_ARGB8565_Premultiplied,
                QVideoFrame.Format_BGRA32,
                QVideoFrame.Format_BGRA32_Premultiplied,
                QVideoFrame.Format_BGR32,
                QVideoFrame.Format_BGR24,
                QVideoFrame.Format_BGR565,
                QVideoFrame.Format_BGR555,
                QVideoFrame.Format_BGRA5658_Premultiplied,
                QVideoFrame.Format_AYUV444,
                QVideoFrame.Format_AYUV444_Premultiplied,
                QVideoFrame.Format_YUV444,
                QVideoFrame.Format_YUV420P,
                QVideoFrame.Format_YV12,
                QVideoFrame.Format_UYVY,
                QVideoFrame.Format_YUYV,
                QVideoFrame.Format_NV12,
                QVideoFrame.Format_NV21,
                QVideoFrame.Format_IMC1,
                QVideoFrame.Format_IMC2,
                QVideoFrame.Format_IMC3,
                QVideoFrame.Format_IMC4,
                QVideoFrame.Format_Y8,
                QVideoFrame.Format_Y16,
                QVideoFrame.Format_Jpeg,
                QVideoFrame.Format_CameraRaw,
                QVideoFrame.Format_AdobeDng,
            ]:
                formats.append(f)
        return formats

    def present(self, frame):
        self.currentFrame = frame.image()
        return True
    
