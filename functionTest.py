import json, os, glob
from Crypto.Hash import SHA256
#고통받기위해서태어난인생같아.. .. . . .. .. .. .
#목표
#여기서 우선 커널 창에서 이용할 수 있게 프로그래밍 하기
#시간이 되면 main.py 파일에서 이 파일 import 해서 gui화
#시간 안 되면.,.. . . . .. ... ..수시지원전까지는만들수있겠지뭐<ㅋㅋ\

nowPath = str(os.getcwd())
jsonPath = nowPath
#jsonPath = os.getenv('ProgramFiles') + '\\PasswordManager'
jsonName = 'PasswordManager.json'
print(jsonPath)
os.chdir(jsonPath)

with open(jsonName, 'r', encoding = 'utf-8') as json_file:
    data = json.load(json_file)
    masterPW = data["master"]
    if masterPW == "":
        print('타 사용자의 접근을 막기 위한 비밀번호를 설정합니다.')
        a = True
        while a == True:
            pw = input('설정할 비밀번호를 입력해주세요: ')
            pwRe = input('다시 한 번 입력해주세요: ')
            if pw == pwRe:
                a = False
            else:
                print('비밀번호가 일치하지 않습니다.')
