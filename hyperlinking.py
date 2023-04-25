import os
import re
from termcolor import colored, cprint

filePaths = []
classDict = {}

folderPath = "/home/me/Documents/folder"

for root, dirs, files in os.walk(folderPath):
    for name in files:
        if name.endswith('.md'):
            filePaths.append(os.path.join(root, name))
            ### create index of written class names matching the corresponding doc file###
            className = re.search("[0-9A-Za-z]+(?=.md)", name)
            if className:
                classDict[className.group(0).lower()] = name


for filePath in filePaths:
    cprint('\t\t##Processing file '+filePath, "grey")
    if not os.path.isfile(filePath):
        print('File does not exist.')
        continue
    with open(filePath, 'r') as fileR:
        lines = fileR.readlines()
    with open(filePath, 'w') as fileW:
        for line in lines:
            if not re.match("#", line):# regex is more simple with this exception (titles)
                for match in re.findall(r"(?<=`)\w+(?=`)", line):
                    targetFileName = classDict.get(match.lower())
                    cprint('\t'+line.strip(), "grey")
                    if not targetFileName:
                        cprint(f'WARNING no mapping found for {match}', "red")
                        input()
                        continue
                    inp = input(f'Hyperlink {match} to {targetFileName} ? (Enter:oui // autreTouche:non)')
                    if not inp:#no input means enter typed
                        hyperlink = f'[`{match}`]({targetFileName})'
                        line = re.sub("`"+match+"`", hyperlink, line)
                        cprint(line, "green")
            fileW.write(line)


