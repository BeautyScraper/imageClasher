import random
import re
import os
from pathlib import Path

def randomLine(fileName, pf):
    currentfile = pf / fileName
    if not currentfile.is_file():
        selectedLine = 'fileNotExist'
        currentfile.touch()
        return selectedLine.rstrip('\n')
    
        # print("opening " + fileName)
    with open(currentfile,"r") as inF:
        curentfileslines = inF.readlines()
        if len(curentfileslines) == 0:
            selectedLine = 'Empty Line'
        else:
            selectedLine = random.choice(curentfileslines).rstrip('\n')
        # os.system('start "" "files\%s"' % (fileName))
        # print("Selected Lines is " + selectedLine)
        while(re.search("\[(.*?)\]",selectedLine)):
            replaceMentStr = randomLine(re.search("\[(.*?)\]",selectedLine)[1] + ".txt", pf)
            selectedLine = re.sub("(\[.*?\])",replaceMentStr,selectedLine,1)
    return selectedLine.rstrip('\n')
    # print("Returning " + selectedLine)
    
def main(fg='files'):
    if not Path(fg).is_dir():
        Path(fg).mkdir(parents=True, exist_ok=True)
    return randomLine('start.txt',Path(fg))
    
if __name__ == '__main__':
    os.system("md files")
    line = randomLine("Static.txt")
    with open("result.txt","w") as file:
        file.write(line)

