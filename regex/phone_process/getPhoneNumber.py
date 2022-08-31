from common import *

# 在这里定义文件名
fileName = '河南'


def getPhoneNumber(fileName):
    lines = []
    with open('./files/' + fileName + '.txt', 'r') as f:
        for line in f:
            lines.append(line.rstrip())
    writeToFile(lines, 'results/' + fileName + '-phone.txt')


getPhoneNumber(fileName)
