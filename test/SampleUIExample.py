import sys
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic

class UI_Sample(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI_Sample, self).__init__()
        uic.loadUi('./ui/test.ui', self)
        self.mainWindow = self.findChild(QtWidgets.QMainWindow, 'MainWindow')
        self.setWindowTitle("Basic Qt Window Example")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.show()

        self.submitButton = self.findChild(QtWidgets.QPushButton, 'submitButton')
        self.submitButton.clicked.connect(self.submitClick)
        
        self.showLabel=self.findChild(QtWidgets.QLabel, 'showLabel')

        self.textEdit=self.findChild(QtWidgets.QLineEdit, 'textEdit')
        
        self.openMenu = self.findChild(QtWidgets.QAction, 'actionOpen')
        self.openMenu.triggered.connect(self.openMenuClick)

        self.saveMenu = self.findChild(QtWidgets.QAction, 'actionSave')
        self.saveMenu.triggered.connect(self.saveMenuClick)

        self.printerMenu = self.findChild(QtWidgets.QAction, 'actionPrinter')
        self.printerMenu.triggered.connect(self.printerMenuClick)
        
        self.emailMenu = self.findChild(QtWidgets.QAction, 'actionE_Mail')
        self.emailMenu.triggered.connect(self.emailMenuClick)

        self.exitMenu = self.findChild(QtWidgets.QAction, 'actionExit')
        self.exitMenu.triggered.connect(self.exitMenuClick)
        
    def submitClick(self):
        self.showLabel.setText(self.textEdit.text())
    
    def openMenuClick(self):
        self.statusBar.showMessage("Open menu clicked...")

    def saveMenuClick(self):
        self.statusBar.showMessage("Save menu clicked...")

    def printerMenuClick(self):
        self.statusBar.showMessage("Printer menu clicked...")
        
    def emailMenuClick(self):
        self.statusBar.showMessage("E-Mail menu clicked...")
        
    def exitMenuClick(self):
        sys.exit(app.exec_())


app = QtWidgets.QApplication(sys.argv)
mainWindow = UI_Sample()
app.exec_()
