from Crypto.Cipher import Salsa20 as sal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QAction, qApp
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
import json, os, glob, sys
import functionTest as ft

nowPath = str(os.getcwd())
jsonPath = nowPath
#jsonPath = os.getenv('ProgramFiles') + '\\PasswordManager'
jsonName = 'PasswordManager.json'
print(jsonPath)
os.chdir(jsonPath)

'''
Password Manager for Windows
'''


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('testing')

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        settingAction = QAction(QIcon('\\setting.png'), 'Exit', self)
        settingAction.setShortcut('Esc')
        settingAction.setStatusTip('Open Setting Window')
        #settingAction.triggered.connect(qApp.)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)
        filemenu.addAction(settingAction)

        '''
        btn = QPushButton('Quit', self)
        btn.move(900, 400)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)
        '''

        self.setWindowTitle('PasswordManager')
        #self.move(300, 300)
        self.resize(1000,500)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
