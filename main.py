from Crypto.Cipher import Salsa20 as sal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication
import json, os, glob, sys

nowPath = str(os.getcwd())
jsonPath = nowPath
#jsonPath = os.getenv('ProgramFiles') + '\\PasswordManager'
jsonName = 'PasswordManager.json'
print(jsonPath)
os.chdir(jsonPath)

'''
Password Manager for Windows
'''

exist = False
for i in glob.glob(jsonPath + '\\*'):
    print(i[len(jsonPath)+1:])
    if i[len(jsonPath)+1:] == jsonName:
        exist = True
        break
#print(exist)

if not exist:
    print('makedir')
    pwData = {
    "master" : "",
    "mode" : "num",
    "min" : "60000",
    "num" : "1",
    "viewtime" : "30000",
    "test" : [{"샘플사이트" : {"id" : "example", "pw" : "example"}}],
    "view" : [{"샘플사이트" : {"id" : "example", "pw" : "example"}}],
    }
    with open(jsonName, 'w', encoding = 'utf-8') as json_file:
        json.dump(pwData, json_file, indent=4, sort_keys=True)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn = QPushButton('Quit', self)
        btn.move(900, 400)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setWindowTitle('PasswordManager')
        #self.move(300, 300)
        self.resize(1000,500)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
