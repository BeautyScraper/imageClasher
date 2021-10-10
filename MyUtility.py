from pathlib import Path
import sys
import pandas as pd
from random import shuffle
import random
import numpy as np
import os
import re

def listToFile(l,filename='D:\\ListFile.txt'):
    k = [x.strip('\n')+'\n' for x in l]
    k = list(set(k))
    with open(filename,'w') as fp:
        fp.writelines(k)

def inputWithinTime(inputString='',timelimit=10):
    import time
    print(inputString)
    for i in range(timelimit):
        time.sleep(1)
        print(i+1)
        
def moveByFastCopy(txtFileName,dstination,action='move'):
    fastCopyLocation = 'C:\\app\\FastCopyPortable\\FastCopyPortable.exe'
    cmdTemplate = '''%0 /log /cmd="%3" /auto_close /force_close /srcfile=%1 /to=%2 '''
    cmd = cmdTemplate.replace('%0',fastCopyLocation)
    cmd = cmd.replace('%1',txtFileName)
    cmd = cmd.replace('%2',dstination)
    cmd = cmd.replace('%3',action)
    print(cmd)
    # import pdb;pdb.set_trace()
    os.system(cmd)
        