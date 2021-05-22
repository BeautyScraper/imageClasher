# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import sys
# from KeyAssigningWidget import Ui_Form
import pandas as pd
from random import shuffle
import random
import numpy as np
import os
from notSoRand import main
import shutil

def main(ImageDir):
    csvFileName = ImageDir / 'MatchRecord.csv'
    
    df = pd.read_csv(csvFileName)
    # ImageDir = Path.cwd()
    ImageFilePaths = [x for x in ImageDir.glob('*.jp*g')]
    df = df.set_index(df.columns[0])
    totalImages = len(ImageFilePaths)
    sdf = df.replace(-1,0).sum(1)
    cdf = df[df != 0].count()
    ddf = sdf[cdf > (totalImages/5)]
    
    print('current Threshhold is :' ,totalImages/5)
    Jobbers = ddf[ddf <= 0]
    filesToMove = [ImageDir / (x+'.jpg') for x in Jobbers.index]
    JobberPath = ImageDir / ('Jobbers%d' % len(filesToMove))
    print(Jobbers)
    # import pdb;pdb.set_trace()
    if not JobberPath.is_dir():
        JobberPath.mkdir()
    for file in filesToMove:
        if file.is_file():
            shutil.move(str(file), str(JobberPath))
    shutil.copy(csvFileName, JobberPath)
    
    
if __name__ == '__main__':
    main(Path.cwd())