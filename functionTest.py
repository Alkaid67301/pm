import json, os, glob, binascii
from Crypto.Hash import SHA256
from Crypto.Cipher import Salsa20
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

nowPath = str(os.getcwd())
jsonPath = nowPath
#jsonPath = os.getenv('ProgramFiles') + '\\PasswordManager'
jsonName = 'PasswordManager.json'
print(jsonPath)
os.chdir(jsonPath)
'''

with open(jsonName, 'r', encoding = 'utf-8') as json_file:
    data = json.load(json_file)

masterPW = data["master"]
'''

def existMPW(jsonName):
    with open(jsonName, 'r', encoding = 'utf-8') as json_file:
        data = json.load(json_file)

    print(data)
    masterPW = data["master"]
    print(masterPW)
    a = True

    if masterPW == '':
        #print('타 사용자의 접근을 막기 위한 비밀번호를 설정합니다.')
        a = False

    return a

        #while a == True:
'''
            pw = input('설정할 비밀번호를 입력해주세요: ')
            pwRe = input('다시 한 번 입력해주세요: ')
            if pw == pwRe:
                a = False
            else:
                print('비밀번호가 일치하지 않습니다.')
'''

print(existMPW(jsonName))

def SaveMPW(jsonName, mpw):
#pw = 'masterpw'
    with open(jsonName, 'r', encoding = 'utf-8') as json_file:
        data = json.load(json_file)
    h = SHA256.new()
    h.update(bytearray(mpw, encoding = 'utf-8'))
    #print(h.hexdigest())
    h.update(h.digest())
    #print(h.hexdigest())
    hashed = h.hexdigest()
    data["master"] = hashed
    with open(jsonName, 'w', encoding = 'utf-8') as json_f:
        json.dump(data, json_f, indent=4, sort_keys=True)


#print(data)

def makeJSON(jsonPath, jsonName):
    exist = False
    for i in glob.glob(jsonPath + '\\*'):
        #print(i[len(jsonPath)+1:])
        if i[len(jsonPath)+1:] == jsonName:
            exist = True
            break
    #print(exist)

    if not exist:
        #print('makedir')
        pwData = {
        "master" : "",
        "mode" : "num",
        "min" : "60000",
        "num" : "1",
        "viewtime" : "30000",
        "test" : {},
        "view" : {},
        }
        with open(jsonName, 'w', encoding = 'utf-8') as json_file:
            json.dump(pwData, json_file, indent=4, sort_keys=True)

def checkMPW(readData, inPW):
    vaildPwHash = readData["master"]
    pwHash = SHA256.new()
    pwHash.update(bytearray(inPW, encoding = 'utf-8'))
    pwHash.update(pwHash.digest())
    if vaildPwHash == pwHash.hexdigest():
        return True
    return False

#print(checkMPW(data, 'master'))

#readMode = 't', 'b'
#'t' == testMode only 'b' = both testMode and viewMode
def input_password(readData, inputMPW, readMode, siteName, siteID, sitePW):
    pwBin = bytearray(sitePW, encoding = 'utf-8')
    mpwHash = SHA256.new()
    mpwHash.update(bytearray(inputMPW, encoding = 'utf-8'))

    sal = Salsa20.new(key = mpwHash.digest())
    pwEnc = sal.nonce + sal.encrypt(pwBin)

    idpwDict = {"id" : siteID, "pw" : pwEnc.hex()}
    readData["test"][siteName] = idpwDict
    if readMode == 'b':
        readData["view"][siteName] = idpwDict
    print(readData)

    with open(jsonName, 'w', encoding = 'utf-8') as json_f:
        json.dump(readData, json_f, ensure_ascii = False, indent=4, sort_keys=True)

#input_password(data, 'masterpw', 'b', "ThisisTest", "ThisisID", "ThisisPW")



def read_password(readData, inputMPW, siteName):
    mpwHash = SHA256.new()
    mpwHash.update(bytearray(inputMPW, encoding = 'utf-8'))

    pw = readData["view"][siteName]["pw"]
    binpw = binascii.unhexlify(pw)

    pw_nonce = binpw[:8]
    pw_enc = binpw[8:]
    sal = Salsa20.new(key = mpwHash.digest(), nonce = pw_nonce)
    plainpw = sal.decrypt(pw_enc).decode('utf-8')
    print(plainpw)

#read_password(data, 'masterpw', 'ThisisTest')
