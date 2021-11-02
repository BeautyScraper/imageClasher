from pathlib import Path
import sys
import pandas as pd
from random import shuffle
import random
import numpy as np
import os
import re
import shutil
from tqdm import tqdm
import argparse

randCmd1 = '--order rand'
randCmd2 = '--rand'

cmd = 'python "D:\Developed\Automation\imageClasher\icko.py" --inputDir "C:\Heaven\YummyBaker" --outputDir "D:\paradise\stuff\essence\Pictures\\ranked2" --time 30 '

x = random.randint(1,100)

print(x)

if x < 50:
    cmd = cmd + randCmd1
else:
    cmd = cmd + randCmd2
    # cmd 
print(cmd)
os.system(cmd)