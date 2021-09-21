from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from pathlib import Path
import sys

import pandas as pd
from random import shuffle
import random
import numpy as np
import re
import time
import os
from notSoRand import main
import Aftermath
from MyUtility import moveByFastCopy
import argparse

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        try:
            _ = Path(string)
        except:
            raise NotADirectoryError(string)
    return string

parser = argparse.ArgumentParser()

parser.add_argument('--inputDir', type=dir_path)
# parser.add_argument('--championsDir', type=dir_path)
# parser.add_argument('--MidCardDir', type=dir_path)
parser.add_argument('--DeletablePath', type=dir_path,default=r'C:\temp\deleatble')
# parser.add_argument('--time', type=int)
# parser.add_argument('--winRate', type=int,default=20)
parser.add_argument('--rand', dest='rand', action='store_true')
parser.add_argument('--no-rand', dest='rand', action='store_false')
parser.set_defaults(rand=False)

args = parser.parse_args()

def openInBrowser(fileName):
    import webbrowser
    template = 'https://www.instagram.com/p/@@/'

    try: 
        postId = re.search('\((.*?)\)',fileName).group(1)
    except:
        print('Not a correctly Formated File')
        return
    urlToOpen =  template.replace('@@', postId)
    print(urlToOpen)
    webbrowser.open(urlToOpen, new=2)
    
def csvReadFile(df,dffilename,listOfName):
    if dffilename.is_file():
        df1 = pd.read_csv(str(dffilename))
        df1 = df1.set_index(df1.columns[0])

        df = df1 + df
        df = df[listOfName].filter(items=listOfName,axis=0)
        df = df.fillna(0.)
    return df

class action:
    def __init__(self,time,notedownfile,targetDir):
        self.time = time
        self.notedownfile = notedownfile
        self.targetDir = targetDir
        
        

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    CtrlClicked = QtCore.pyqtSignal()
    Rclicked = QtCore.pyqtSignal()
    CtrlRclicked = QtCore.pyqtSignal()
    winningCount = 0
    timeToWin = 5000

    def noteItDown(self, fileName):
        with open(str(fileName), 'a+') as fp:
            fp.write(self.Imagelist[self.currentIndex] + '\n')
    def setList(self,List,actions,ra = 1):
        self.actions = actions
        self.timers = []
        i = 0
        for act in actions:
            rd = QTimer()
            # print(i,'wf')
            pr = lambda i=i: self.changeColor(i * int(255/len(actions)),i)
            rd.timeout.connect(pr)
            self.timers.append(rd)
            i += 1
        # i = 1
        self.rightOne = ra
        self.Imagelist = List
        self.currentIndex = 0
        self.redhotmap = QtGui.QPixmap(self.Imagelist[0])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height(),1,1)
        self.setPixmap(self.redhotmap)
    
    def changeColor(self,redIntensity=50,wi=-1):
        # self.setStyleSheet("background-color: rgb(%s, 0, 0);border: 2px solid red;" % redIntensity) 
        self.setStyleSheet("background-color: rgb(%s, 0, 0);border: 5px solid rgb(%s, 0, 0);" % (redIntensity,redIntensity)) 
        # print("background-color: rgb(%s, 0, 0);border: 5px solid green;" % redIntensity, wi)
        # self.setStyleSheet("")
        # print(wi)
        self.timers[wi].stop()
    
    def bringNextContenderOut(self):
        
        # self.timer.timeout.connect(self.changeColor)
        self.currentIndex += 1
        self.redhotmap = QtGui.QPixmap(self.Imagelist[self.currentIndex])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height() * self.rightOne,1,1)
        self.setPixmap(self.redhotmap)
        # self.resize(self.redhotmap.width(),self.redhotmap.height())
        self.setAlignment(QtCore.Qt.AlignTop)
        self.winningCount = 0 
        [x.stop() for x in self.timers]
        self.setStyleSheet("background-color: black") 
        [x.start(y.time*1000) for x,y in zip(self.timers,self.actions)]
    
    def itWon(self,by=0):
        self.timer.stop()
        self.winningCount += 1 + by
        self.setStyleSheet("background-color: lightgreen") 
    
    def getWinningCount(self):
        return self.winningCount
    
    def bringPreviousContenderOut(self):
        [x.stop() for x in self.timers]
        self.setStyleSheet("background-color: black") 
        [x.start(y.time*1000) for x,y in zip(self.timers,self.actions)]
        self.currentIndex -= 1
        self.redhotmap = QtGui.QPixmap(self.Imagelist[self.currentIndex])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height() * self.rightOne ,1,1)
        self.setPixmap(self.redhotmap)
        # self.resize(self.redhotmap.width(),self.redhotmap.height())
        # self.setAlignment(QtCore.Qt.AlignTop)
    
    def getCurrentcontenderName(self):
        try :
            p = Path(self.Imagelist[self.currentIndex]).stem
        except:
            self.setStyleSheet("QLabel"
                            "{"
                            "background-color : red;"
                            "}")
            p = Path(self.Imagelist[-1]).stem
            
        return p
        
        
    def mouseReleaseEvent(self, QMouseEvent):

        modifiers = QtWidgets.QApplication.keyboardModifiers()

        leftPressed = QMouseEvent.button() == QtCore.Qt.LeftButton
        rightPressed = QMouseEvent.button() == QtCore.Qt.RightButton
        ctrlPressed = modifiers == QtCore.Qt.ControlModifier
        if leftPressed and not ctrlPressed:
            self.clicked.emit()
        if rightPressed and not ctrlPressed :
            self.Rclicked.emit()
        if leftPressed and ctrlPressed:
            self.CtrlClicked.emit()
        if rightPressed and ctrlPressed:
            self.CtrlRclicked.emit()

class Ui_MainWindow(object):
    path = args.inputDir
    def setupList(self):
        
        self.listI = [str(x) for x in Path(self.path).glob('*.jpg')]
        if args.rand:
            random.shuffle(self.listI)
        listOfName =  [Path(x).stem for x in self.listI]
        # shuffle(self.listI)
        self.ActionList = []
        weightM = np.zeros((len(listOfName),len(listOfName)))
        self.listOfName = listOfName
        self.filecount = len(listOfName)
        
    def showTheWinner(self,MainWindow):



        template = 'start "C:\Program Files\IrfanView\i_view64.exe\" /slideshow=%s' %  str(p)
        os.system(template)

        
    def afterMath(self):
        Aftermath.main(Path(self.path))
    def openTargetDir(self):
        os.system('start "" "%s"' % self.path)
        
    def showTheLoser(self,MainWindow):


        norm = lambda x: str(Path(self.path) / (x + '.jpg')) + '\n' 
        fileList = [norm(x) for x in lf]
        myPicsListCatalog = Path.cwd() /  'myPics.txt'
        with open(myPicsListCatalog,'w') as fp:
            fp.writelines(fileList)

        template = '\"C:\Program Files\IrfanView\i_view64.exe\" /slideshow=%s' %  str(myPicsListCatalog)
        print(template)
        os.system(template)

    def moveFiles(self,txtFile = 'listdnbh.txt.opml', moveToDit = 'dnbh',relative=True):
        dels = Path(txtFile)
        if dels.is_file():
            dstPath =Path(moveToDit)
            if relative:
                dstPath = Path(self.path) / moveToDit
            moveByFastCopy(txtFile,str(dstPath))
            dels.unlink()
    def closingActions(self,event):
        for tb in self.actions:
            self.moveFiles(tb.notedownfile,tb.targetDir,False)
        # self.moveFiles()
        # self.moveFiles('listchampions.txt.opml',args.championsDir,False)
        # self.moveFiles('listmidCard.txt.opml',r'C:\Heaven\YummyBaked\midCard',False)
        # self.moveFiles('listmidCard.txt.opml',args.MidCardDir,False)
        self.moveFiles('del.txt',args.DeletablePath,False)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1000)
        cfgfilename = 'actions.cfg'
        self.actions = []
        with open(cfgfilename,'r') as fp:
            for acts in fp.readlines():
                t = int(acts.split(',')[0])
                n = acts.split(',')[1] 
                k = acts.split(',')[2]
                self.actions.append(action(t,n,k))
        # self.actions = [
        # action(5,'midcard',r'C:\Heaven\YummyBaked\midCard'),
        # action(10,'champions',r'C:\Heaven\YummyBaked\champion'),
        # action(15,'ultra',r'C:\Heaven\YummyBaked\Ultra'),
        
        # ]
        MainWindow.closeEvent = self.closingActions
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.h = MainWindow.geometry().height()
        h = self.h
        self.w = MainWindow.geometry().width()
        w = self.w
        
        self.setupList()
        # self.topCard = args.winRate
        # self.losersTime = args.time
        # ClickableLabel.timeToWin = self.losersTime * 1000
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, w, h))

        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.label = ClickableLabel(self.horizontalLayoutWidget)

        self.label.setText("")
        self.label.setObjectName("label")
        self.label.resize(w,h)
        self.label.setList(self.listI,self.actions)
        # self.label.actions = 
        fullScreenFlag = [False]
        
        def toggleFulScreen():
            MainWindow.setWindowState(QtCore.Qt.WindowFullScreen) if not fullScreenFlag[0] else MainWindow.setWindowState(QtCore.Qt.WindowMaximized)
            fullScreenFlag[0] = not fullScreenFlag[0]
        
        # self.label.setScaledContents(False)
        # self.horizontalLayout.addWidget(self.label)
        # self.LeftImage = ClickableLabel(self.horizontalLayoutWidget)
        # self.LeftImage.resize(w/2,h)
        # self.LeftImage.setList(self.listI[1::2],0.75)
        # self.LeftImage.setObjectName("LeftImage")

        # self.horizontalLayout.addWidget(self.LeftImage)
        MainWindow.setCentralWidget(self.centralwidget)
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.arraowEvent())
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.opendstdir())
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up), MainWindow, activated=lambda :MainWindow.setWindowState(QtCore.Qt.WindowMinimized) == MainWindow.close())
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down), MainWindow, activated=lambda :self.showTheLoser(MainWindow))
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), MainWindow, activated=lambda :openInBrowser(self.label.getCurrentcontenderName()))
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_G), MainWindow, activated=lambda :openInBrowser(self.LeftImage.getCurrentcontenderName()))
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_O), MainWindow, activated=self.openTargetDir)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), MainWindow, activated=self.afterMath)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_M), MainWindow, activated= toggleFulScreen)
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.openFileIrfanView(self.label.getCurrentcontenderName()))
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.openFileIrfanView(self.LeftImage.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.label.bringPreviousContenderOut())
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.LeftImage.bringPreviousContenderOut())
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_1), MainWindow, activated=lambda :self.label.noteItDown('dnbh.txt'))
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_2), MainWindow, activated=lambda :self.LeftImage.noteItDown('dnbh.txt'))
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_1), MainWindow, activated=lambda :self.label.noteItDown('del.txt'))
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_2), MainWindow, activated=lambda :self.LeftImage.noteItDown('del.txt'))
        

        self.timestamp = time.time()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def openFileIrfanView(self,filePath):
        if not Path(filePath).is_absolute():
            p = Path(self.path) / ( filePath + '.jpg')

        template = 'start "C:\Program Files (x86)\IrfanView\i_view32.exe\" "%s"' %  str(p)
        os.system(template)

    
    def DoMoves(self):
        with open('moves.txt','r') as fp:
            fc = fp.readlines()
        wrestler = ['LeftOne', 'RightOne']
        shuffle(wrestler)
        moveStr = '%s %sed %s' % (wrestler[0],random.choice(fc).strip(),wrestler[1])
        i = 1
        while random.randint(0,5) > 2:
            moveStr += ' but %s countered with %s' % (wrestler[i%2],random.choice(fc).strip())
            i += 1
        print(moveStr)
        self.statusbar.showMessage(moveStr)
        
    def AssignRole(self):
        
        moveStr = main()
        print(moveStr)
        self.statusbar.showMessage(moveStr)
    
    def statusbarManipulation(self):
        rng = 3 > random.randint(0,15)
        if rng and False:
           self.DoMoves()
        else:
            self.AssignRole()
    
    def opendstdir(self):
        deliberationTime = time.time() - self.timestamp
        # timeboundries = [5,10,15]
        for tb in self.actions[::-1]:
            # print(deliberationTime)
            if deliberationTime > tb.time:
                os.system('start "" "%s"' % tb.targetDir) 
                break
        else:
            os.system('start "" "%s"' % args.DeletablePath)
            
    def arraowEvent(self):
        
        
        # self.statusbarManipulation()
        # Winner = self.label
        # Loser = self.LeftImage
        # if WinningSide == 0:
            # Winner = self.LeftImage
            # Loser = self.label
        # winnerName = Winner.getCurrentcontenderName()
        # loserName = Loser.getCurrentcontenderName()
        # Loser.resize(MainWindow.geometry().width()/2,MainWindow.geometry().height()-30)
        # flag = False
        # Winner.itWon(Loser.getWinningCount())
        deliberationTime = time.time() - self.timestamp
        # timeboundries = [5,10,15]
        for tb in self.actions[::-1]:
            # print(deliberationTime)
            if deliberationTime > tb.time:
                self.label.noteItDown(tb.notedownfile) 
                break
        else:
            self.label.noteItDown('del.txt')
        # print(Winner.getWinningCount(), ' winnin', loserName)
        # if deliberationTime < self.losersTime and Loser.getWinningCount() <= 0:
            # Loser.noteItDown('del.txt')
        # else:
           # Loser.noteItDown('midCard.txt') 
        # if Winner.getWinningCount() >= self.topCard:
           # Winner.setStyleSheet("border: 5px solid black;")
           # Winner.noteItDown('champions.txt') 
        self.label.bringNextContenderOut()
        self.statusbar.showMessage(self.label.getCurrentcontenderName())
        # Loser.bringNextContenderOut()
        self.horizontalLayout.addStretch(1)
        self.timestamp = time.time()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ClickOnTheWinner"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()


    sys.exit(app.exec_())
