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

ipath = r'C:\Heaven\YummyBaked'
clashFilep = r'D:\Developed\Automation\imageClasher\picko.py'
cpd = r'C:\Heaven\YummyBaked\champions'
mpd = r'C:\Heaven\YummyBaked\midCard'
# breakpoint()
sp = [dp for dp in Path(ipath).glob('*/')]
random.shuffle(sp)
dp = sp[0]
cmd = 'python "%s" --inputDir "%s" ' % (clashFilep, str(dp))
print(cmd)
os.system(cmd)
# for dp in Path(ipath).glob('*/'):