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

        sumbitButton.clicked.connect(self.inputMPW)

    def loadComboBox(self):
        with open(jsonName, 'r', encoding = 'utf-8') as json_file:
            data = json.load(json_file)

        siteNameList = list(data["test"].keys())
        for i in siteNameList:
            siteNameCB.addItem(i)

    def inputMPW(self):
        mPW, ok = QInputDialog.getText(self, 'Input MasterPassword', 'Enter Password:')

        with open(jsonName, 'r', encoding = 'utf-8') as json_file:
            data = json.load(json_file)

        a = ft.checkMPW(data, mPW)
        if a:
            self.tryWindow(mPW)
        else:
            QMessageBox.question(self, '실패', '비밀번호가 일치하지 않습니다.', QMessageBox.Yes)

    def tryWindow(self, mPW):
        key = ft.encKey(mPW)

        k = True
        while k:
            trypw, ok =  QInputDialog.getText(self, '입력', 'Password: ')
            if ok == QMessageBox.No:
                QMessageBox.question(self, '실패', '해당 작업을 중지합니다.', QMessageBox.Yes)
                k = False
            else:
                siteName = siteNameCB.activated[str]
                TorF = ft.check_password(data, trypw, siteName, key)
                if TorF:
                    id = data["test"][siteName]["id"]
                    QMessageBox.question(self, '성공', 'id: ' + id + '\npw: ' + trypw, QMessageBox.Yes)
                    k = False
                else:
                    QMessageBox.question(self, '실패', '비밀번호가 일치하지 않습니다.', QMessageBox.Yes)
                    self.tryWindow(mPW)


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
        h1 = QLabel('Password Manager for Windows\n')
        h2 = QLabel('아이디와 비밀번호를 사이트 제목 등으로 분류하여 저장합니다.\n\n입력 시도 탭: 비밀번호를 잊어버렸을 때, 맞는 번호인지 입력해서 시험해봅니다.\n공인인증서 비밀번호 등 입력 횟수 제한이 있고, 공개될 때의 리스크가 큰 것들에 적합합니다.')
        h3 = QLabel('비밀번호 확인 탭: 비밀번호를 잊어버렸을 때, 직접 확인해봅니다.\n포탈 사이트 비밀번호 등에 적합합니다.\n')
        h4 = QLabel('입력 탭: 사이트 이름, id, pw를 입력할 수 있습니다.\n입력 시 비밀번호 확인 탭의 활성화 여부를 결정합니다.\n입력 시도 탭은 언제나 활성화됩니다.\n이미 존재하는 사이트 이름은 다시 사용할 수 없습니다.\n')
        h5 = QLabel('설정 탭: ')

        grid = QGridLayout()
        grid.addWidget(h1, 0, 0)
        grid.addWidget(h2, 1, 0)
        grid.addWidget(h3, 2, 0)
        grid.addWidget(h4, 3, 0)
        grid.addWidget(h5, 4, 0)
        self.setLayout(grid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
