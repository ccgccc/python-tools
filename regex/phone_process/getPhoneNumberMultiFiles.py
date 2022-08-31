import re
from os import listdir
from os.path import isfile, join
from getPhoneNumber import *

# 这里定义批量处理文件路径
mypath = './files/'


files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
lines = []
for fileName in files:
    getPhoneNumber(fileName.split('.')[0])
