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
from random import choice

randCmd1 = '--order rand'
randCmd2 = '--rand'

image_categories = ['porn', 'corn', 'Desi']
ic = choice(image_categories)
# cmd = f'python "D:\Developed\Automation\imageClasher\heap_clash.py" --inputDir "C:\Heaven\YummyBaker" --outputDir "D:\paradise\stuff\essence\Pictures\Heap" --time 30 '
cmd = f'python "D:\Developed\Automation\imageClasher\heap_clash.py" --inputDir "C:\Heaven\ToBeHeaps\{ic}" --outputDir "D:\paradise\stuff\essence\Pictures\Heap\{ic}" --time 30 '
# cmd = 'python "D:\Developed\Automation\imageClasher\heap_clash.py" --inputDir "D:\paradise\stuff\essence\Pictures\heap\heapTest" --outputDir "D:\paradise\stuff\essence\Pictures\Heap" --time 30 '

x = random.randint(1,100)

print(x)

if x < 50:
    cmd = cmd + randCmd1
else:
    cmd = cmd + randCmd2
    # cmd 
print(cmd)
os.system(cmd)