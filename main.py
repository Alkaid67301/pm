from Crypto.Hash import SHA256
from Crypto.Cipher import Salsa20 as sal
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.checkJsonExist()
        self.checkMPWexist()
        self.initUI()

    def initUI(self):
        tab_test = TryTab()
        tab_view = ViewTab()
        tab_input = InputTab()
        tab_setting = SettingTab()
        tab_help = HelpTab()

        tabs = QTabWidget()
        tabs.addTab(tab_test, '입력 시도')
        tabs.addTab(tab_view, '비밀번호 확인')
        tabs.addTab(tab_input, '새로 입력')
        tabs.addTab(tab_setting, '설정')
        tabs.addTab(tab_help, '도움말')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        self.setWindowTitle('PasswordManager')
        #self.move(300, 300)
        self.resize(500, 400)
        self.center()
        self.show()

    def checkJsonExist(self):
        ft.makeJSON(jsonPath, jsonName)

    def checkMPWexist(self):
        with open(jsonName, 'r', encoding = 'utf-8') as json_file:
            data = json.load(json_file)

        exist = ft.existMPW(jsonName)
        print(ft.existMPW(jsonName))
        print(exist)

        while exist == False:
            newPW, ok = QInputDialog.getText(self, '비밀번호 입력', '사용할 프로그램 비밀번호를 입력하세요:')
            PWagain, ok = QInputDialog.getText(self, '비밀번호 입력', '다시 입력해주세요:')
            if newPW == '':
                QMessageBox.question(self, '실패', '비밀번호는 공백일 수 없습니다.', QMessageBox.Yes)
                continue
            elif newPW == PWagain:
                QMessageBox.question(self, '성공', '비밀번호를 설정했습니다.', QMessageBox.Yes)
                ft.SaveMPW(jsonName, newPW)
                exist = True
            else:
                reply = QMessageBox.question(self, '실패', '비밀번호가 일치하지 않습니다. \n비밀번호를 설정하지 않으면 프로그램이 종료됩니다. \n비밀번호를 설정하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.No:
                    sys.exit()
                else:
                    continue

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', '정말 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class TryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        sitename = QLabel('사이트 이름:')
        siteNameCB = QComboBox(self)
        self.loadComboBox()
        sumbitButton = QPushButton('Sumbit')

        grid = QGridLayout()
        grid.addWidget(sitename, 0, 0)
        grid.addWidget(siteNameCB, 0, 1)
        grid.addWidget(sumbitButton, 1, 1)

        self.setLayout(grid)

    def loadComboBox(self):
        with open(jsonName, 'r', encoding = 'utf-8') as json_file:
            data = json.load(json_file)

        siteNameList = list(data["test"].keys())
        for i in siteNameList:
            siteNameCB.addItem(i)

    def inputMPQ(self):
        mPW, ok = QInputDialog.getText(self, 'Input MasterPassword', 'Enter Password:')

class ViewTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

class InputTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

class SettingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
