import re


def writeToFile(lines, fileName):
    file = open(fileName, 'w')
    count = 0
    for line in lines:
        curLine = line.rstrip()
        # Get email
        # if re.search(r"@", curLine) == None:
        #     continue
        # str2 = re.sub(r"(.*?：.*?) \['.*?'([\w\d]*\@.*?)\'.*", r"\1 \2", curLine)
        # print(str2)
        # Get phone
        pattern = r"(.*?) \['.*?'(1\d{10})'.*"
        if re.match(pattern, curLine):
            count = count + 1
            replace = re.sub(pattern, r"\1 \2", curLine)
            print(replace)
            print(replace, file=file)
        else:
            continue
    file.close()
    print('Total: ' + str(count))
