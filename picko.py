from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from pathlib import Path
import sys


import shutil
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
parser.add_argument('--cfgfile', type=dir_path,default='pickoactions.cfg')
# parser.add_argument('--championsDir', type=dir_path)
# parser.add_argument('--MidCardDir', type=dir_path)
parser.add_argument('--DeletablePath', type=dir_path,default=r'C:\temp\deleatble')
# parser.add_argument('--time', type=int)
# parser.add_argument('--winRate', type=int,default=20)
parser.add_argument('--order', choices=['rand', 'date', 'name'],default='name')
parser.add_argument('--rand', dest='rand', action='store_true')
parser.add_argument('--no-rand', dest='rand', action='store_false')
parser.set_defaults(rand=False)

args = parser.parse_args()



def openInBrowser(fileName):
    import webbrowser
    template = 'https://www.picnob.com/post/@@/'

    try: 
        postId = re.search('\((\d{3,}?)\)', fileName)[0].strip('()')
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
    def __init__(self,keys,targetDir,actiontype='move'):
        self.keys = keys
        self.notedownfile = str(hash(targetDir))+ '.txt'
        self.targetDir = targetDir
        self.actiontype = actiontype
        
        

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    CtrlClicked = QtCore.pyqtSignal()
    Rclicked = QtCore.pyqtSignal()
    CtrlRclicked = QtCore.pyqtSignal()
    winningCount = 0
    timeToWin = 5000
    def getThisFile(self,sourceFile,parentDir,srclistFilePath=r'D:\Developed\Automation\fnr\TargetDirs.opml'):
        with open(srclistFilePath,'r') as fp:
            srcFileList = fp.readlines()
        # srcFileList.append(r'C:\bekar')
        for srcDir in srcFileList:
            dirP = Path(srcDir.rstrip())
            srcPath = dirP / parentDir / sourceFile
            # import pdb;pdb.set_trace()
            if srcPath.is_file():
                return srcPath
        return None
    def noteItDownre(self,fileName,repattern='',subpattern='',srclistFile=r'D:\Developed\Automation\fnr\TargetDirs.opml'):
        tk = self.Imagelist[self.currentIndex]
        # print(tk)
        try:
            dirName = re.search('(.*) @hudengi (.*) W1t81N (.*)',str(tk))[2]
            filename = re.search('(.*) @hudengi (.*) W1t81N (.*)',str(tk))[3]
        except:
            return
        if re.sub('_\d+\.','.',filename) is not None:
            filename = re.sub('_\d+\.','.',filename)        
        srcPath = self.getThisFile(filename,dirName)
        if srcPath is None:
            return
        with open(str(fileName), 'a+') as fp:
            fp.write(str(srcPath) + '\n')
        
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
        # self.resize(1900,1080)
        
        self.setScaledContents(False)
    
    def changeColor(self,redIntensity=50,wi=-1):
        # self.setStyleSheet("background-color: rgb(%s, 0, 0);border: 2px solid red;" % redIntensity) 
        self.setStyleSheet("background-color: rgb(%s, 0, 0);border: 5px solid rgb(%s, 0, 0);" % (redIntensity,redIntensity)) 
        # print("background-color: rgb(%s, 0, 0);border: 5px solid green;" % redIntensity, wi)
        # self.setStyleSheet("")
        # print(wi)
        self.timers[wi].stop()
    
    def bringNextContenderOut(self):
        
        # self.timer.timeout.connect(self.changeColor)
        if self.currentIndex < len(self.Imagelist) - 1:
            self.currentIndex += 1
        else: 
            return
        self.redhotmap = QtGui.QPixmap(self.Imagelist[self.currentIndex])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height() * self.rightOne,1,1)
        self.setPixmap(self.redhotmap)
        # self.resize(1900,1080)
        # self.setAlignment(QtCore.Qt.AlignTop)
        # self.winningCount = 0 
        # [x.stop() for x in self.timers]
        # self.setStyleSheet("background-color: black") 
        # [x.start(y.time*1000) for x,y in zip(self.timers,self.actions)]
    
    def itWon(self,by=0):
        self.timer.stop()
        self.winningCount += 1 + by
        self.setStyleSheet("background-color: lightgreen") 
    
    def getWinningCount(self):
        return self.winningCount
    
    def bringPreviousContenderOut(self):
        # [x.stop() for x in self.timers]
        self.setStyleSheet("background-color: black") 
        # [x.start(y.time*1000) for x,y in zip(self.timers,self.actions)]
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
        if args.order == 'date':
            print('sorting according to the date')
            self.listI.sort(key=lambda x: os.path.getmtime(x),reverse=True)
        listOfName =  [Path(x).stem for x in self.listI]
            
            
        # shuffle(self.listI)
        self.ActionList = []
        # weightM = np.zeros((len(listOfName),len(listOfName)))
        self.listOfName = listOfName
        self.filecount = len(listOfName)
        
    def showTheWinner(self,MainWindow):



        template = 'start "C:\Program Files\IrfanView\i_view64.exe\" /slideshow=%s' %  str(p)
        os.system(template)

        
    def afterMath(self):
        Aftermath.main(Path(self.path))
    def openTargetDir(self,pathToopen=''):
        if pathToopen == '':
            pathToopen = self.path
        os.system('start "" "%s"' % pathToopen)
        
    def showTheLoser(self,MainWindow):


        norm = lambda x: str(Path(self.path) / (x + '.jpg')) + '\n' 
        fileList = [norm(x) for x in lf]
        myPicsListCatalog = Path.cwd() /  'myPics.txt'
        with open(myPicsListCatalog,'w') as fp:
            fp.writelines(fileList)

        template = '\"C:\Program Files\IrfanView\i_view64.exe\" /slideshow=%s' %  str(myPicsListCatalog)
        print(template)
        os.system(template)

    def moveFiles(self,txtFile = 'listdnbh.txt.opml', moveToDit = 'dnbh',relative=True,moveAction='force_copy'):
        dels = Path(txtFile)
        if dels.is_file():
            dstPath =Path(moveToDit)
            if relative:
                dstPath = Path(self.path) / moveToDit
            moveByFastCopy(txtFile,str(dstPath),moveAction)
            dels.unlink()
    def movecorrFiles(self,txtFile = 'listdnbh.txt.opml', moveToDit = 'dnbh',relative=True,moveAction='force_copy'):
        if not Path(txtFile).is_file():
            return
        filestoMove = []
        with open(txtFile, 'r') as fp:
            for pths in fp.readlines():
                fpath = Path(pths.strip())
                if not fpath.is_file():
                    continue
                updatedName = fpath.parent.name + ' me chudi ' + fpath.name
                upath = fpath.parent / updatedName
                shutil.copy(fpath,upath)
                # print(fpath,upath)
                filestoMove.append(str(upath)+ '\n')
        with open(txtFile,'w') as fp:
            fp.writelines(filestoMove)
        self.moveFiles(txtFile,moveToDit,relative,moveAction)
            
                
    def closingActions(self,event):
        for tb in self.actions:
            if tb.actiontype == 'corr_move': 
                # print(tb.targetDir)
                self.movecorrFiles(tb.notedownfile,tb.targetDir,False,'move')
                continue
            self.moveFiles(tb.notedownfile,tb.targetDir,False,'force_copy')
        # breakpoint()
        
        self.moveFiles(self.defaultaction.notedownfile,self.defaultaction.targetDir,False,'move')
        # self.moveFiles()
        # self.moveFiles('listchampions.txt.opml',args.championsDir,False)
        # self.moveFiles('listmidCard.txt.opml',r'C:\Heaven\YummyBaked\midCard',False)
        # self.moveFiles('listmidCard.txt.opml',args.MidCardDir,False)
        # self.moveFiles('del.txt',args.DeletablePath,False)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        cfgfilename = args.cfgfile
        self.actions = []
        with open(cfgfilename,'r') as fp:
            for acts in fp.readlines():
                acts = acts.strip('\\\n')
                if 'default' in acts:
                    self.defaultaction = action(acts.split(',')[0],acts.split(',')[1]) 
                    continue
                act_key = acts.split(',')[0]
                k = acts.split(',')[1] 
                # k = acts.split(',')[2]
                act_type = 'move'
                if '@' in acts:
                    act_type = 'corr_move'
                    
                self.actions.append(action(act_key,k,act_type))
        # self.actions = [
        # action('a','midcard',r'C:\temp\midCard'),
        # action('s','champions',r'C:\temp\champion'),
        # action('d','ultra',r'C:\temp\Ultra'),
        
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
        
        self.textlabel = ClickableLabel(self.horizontalLayoutWidget)
        self.textlabel.setObjectName("textlabel")
        # self.textlabel.setAlignment(QtCore.Qt.AlignLeft)
        self.textlabel.setAlignment(QtCore.Qt.AlignRight)
        self.textlabel.setWordWrap(True)

        self.textlabel.setFont(QtGui.QFont('Arial', 8))
        with open(args.cfgfile,'r') as fp:
            # import pdb;pdb.set_trace()
            self.textlabel.setText(fp.read())
        self.textlabel.setStyleSheet("color: lightgreen")
        # self.horizontalLayout.addWidget(self.textlabel)
        
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.resize(w,h)
        self.label.setList(self.listI,self.actions)
        
        
        # self.label.actions = 
        fullScreenFlag = [False]
        # self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.textlabel)
        def toggleFulScreen():
            MainWindow.setWindowState(QtCore.Qt.WindowFullScreen) if not fullScreenFlag[0] else MainWindow.setWindowState(QtCore.Qt.WindowMaximized)
            fullScreenFlag[0] = not fullScreenFlag[0]
        MainWindow.setCentralWidget(self.centralwidget)
        # self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.arraowEvent())
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.skipEvent(10))
        # QtWidgets.QShortcut(QtGui.QKeySequence('Down'), MainWindow, activated=lambda :self.arraowEvent())
        for acts in self.actions:
            if acts.actiontype == 'move':
                QtWidgets.QShortcut(QtGui.QKeySequence(acts.keys), MainWindow, activated=lambda x=acts.notedownfile:self.label.noteItDown(x))
            if acts.actiontype == 'corr_move': 
               QtWidgets.QShortcut(QtGui.QKeySequence(acts.keys), MainWindow, activated=lambda x=acts.notedownfile:self.label.noteItDownre(x)) 
            QtWidgets.QShortcut(QtGui.QKeySequence('Shift+' + acts.keys), MainWindow, activated=lambda x=acts.targetDir:self.openTargetDir(x))
            QtWidgets.QShortcut(QtGui.QKeySequence('Alt+' + acts.keys), MainWindow, activated=lambda x=acts.targetDir:self.runSicko(x))
        QtWidgets.QShortcut(QtGui.QKeySequence('Alt+Left'), MainWindow, activated=lambda x=args.inputDir:self.runSicko(x))
        # QtWidgets.QShortcut(QtGui.QKeySequence('Alt+' + acts.keys), MainWindow, activated=lambda x=acts.targetDir:self.runIfVSlideshow(x))
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.opendstdir())
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up), MainWindow, activated=lambda :MainWindow.setWindowState(QtCore.Qt.WindowMinimized) == MainWindow.close())
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down), MainWindow, activated=lambda :self.showTheLoser(MainWindow))
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), MainWindow, activated=lambda :openInBrowser(self.label.getCurrentcontenderName()))
        # QtWidgets.QShortcut(QtGui.QKeySequence("Shift+Left"), MainWindow, activated=self.openTargetDir)
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), MainWindow, activated=self.afterMath)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_M), MainWindow, activated= toggleFulScreen)
        # QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_Left).toString()
        # breakpoint()
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_I), MainWindow, activated=lambda :self.openFileIrfanView(self.label.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_I), MainWindow, activated=lambda :self.openSrcFileIrfanview(self.label.getCurrentcontenderName()))

        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_T), MainWindow, activated=self.startTime)
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.openFileIrfanView(self.LeftImage.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.label.bringPreviousContenderOut())
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.LeftImage.bringPreviousContenderOut())
        
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_1), MainWindow, activated=lambda :self.label.noteItDown('dnbh.txt'))
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_2), MainWindow, activated=lambda :self.LeftImage.noteItDown('dnbh.txt'))
        
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_1), MainWindow, activated=lambda :self.label.noteItDown('del.txt'))
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_2), MainWindow, activated=lambda :self.LeftImage.noteItDown('del.txt'))
        

        # self.timestamp = time.time()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def startTime(self):
        print('hello')
        rd = QTimer()
        rd.timeout.connect(self.arraowEvent)
        rd.start(1000)
    def runSicko(self,Filepath):
    
        MainWindow.setWindowState(QtCore.Qt.WindowMinimized)
        MainWindow.close()
        pyfile =  Path(__file__).parent / 'sicko.py'
        pyfile = str(pyfile)
        template = 'Python "%s" --inputDir "%s" --cfgfile "%s" --rand' %  (pyfile,Filepath,args.cfgfile)
        print(template)
        os.system(template)
        

    def runIfVSlideshow(self,Filepath):
        # if not Path(filePath).is_absolute():
            # p = Path(self.path) / ( filePath + '.jpg')
        MainWindow.setWindowState(QtCore.Qt.WindowMinimized)
        MainWindow.close()
        template = 'start "" "C:\Program Files (x86)\IrfanView\i_view32.exe" /slideshow="%s"' %  str(Filepath)
        print(template)
        os.system(template)
    def openFileIrfanView(self,filePath):
        if not Path(filePath).is_absolute():
            p = Path(self.path) / ( filePath + '.jpg')

        template = 'start "C:\Program Files (x86)\IrfanView\i_view32.exe\" "%s"' %  str(p)
        os.system(template)
    def openSrcFileIrfanview(self,fileName):
        tk = self.label.Imagelist[self.label.currentIndex]
        # print(tk)
        try:
            dirName = re.search('(.*) @hudengi (.*) W1t81N (.*)',str(tk))[2]
            # breakpoint()
            filename = re.search('(.*) @hudengi (.*) W1t81N (.*)',str(tk))[3]
        except Exception as e:
            print(e)
            return
        if re.sub('_\d+\.','.',filename) is not None:
            filename = re.sub('_\d+\.','.',filename)
        srcPath = self.label.getThisFile(filename,dirName)
        if srcPath is None:
            return
        template = 'start "C:\Program Files (x86)\IrfanView\i_view32.exe\" "%s"' %  str(srcPath)
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
    def skipEvent(self,count = 10):
        i = -1 if count <= 0 else -1 
        for _ in range(abs(count)):
            self.label.currentIndex += i
            self.label.noteItDown(self.defaultaction.notedownfile) 
        self.arraowEvent()
        
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
        # deliberationTime = time.time() - self.timestamp
        # timeboundries = [5,10,15]
        # for tb in self.actions[::-1]:
            # print(deliberationTime)
            # if deliberationTime > tb.time:
                # break
        # else:
            # self.label.noteItDown('del.txt')
        # print(Winner.getWinningCount(), ' winnin', loserName)
        # if deliberationTime < self.losersTime and Loser.getWinningCount() <= 0:
            # Loser.noteItDown('del.txt')
        # else:
           # Loser.noteItDown('midCard.txt') 
        # if Winner.getWinningCount() >= self.topCard:
           # Winner.setStyleSheet("border: 5px solid black;")
           # Winner.noteItDown('champions.txt') 
        # for _ in range(count):
        self.label.noteItDown(self.defaultaction.notedownfile) 
        self.label.bringNextContenderOut()
        self.statusbar.showMessage(self.label.getCurrentcontenderName())
        self.label.resize(self.w, self.h)
        # Loser.bringNextContenderOut()
        # self.horizontalLayout.addStretch(1)
        # self.timestamp = time.time()

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
