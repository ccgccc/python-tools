import re
from os import listdir
from os.path import isfile, join
from common import *


# 这里定义批量处理文件路径
mypath = './files/'


files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
lines = []
for f in files:
    print(f)
    for line in open(mypath + f, 'r'):
        lines.append(line.rstrip())

writeToFile(lines, 'results/batch-phone.txt')
