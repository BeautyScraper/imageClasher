from tkinter.messagebox import NO
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
import shutil

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
# parser.add_argument('--outputDir', type=dir_path)
parser.add_argument('--cfgfile', type=dir_path,default='pickoactions.cfg')
# parser.add_argument('--DeletablePath', type=dir_path,default=r'C:\temp\deleatble')
parser.add_argument('--rows', type=int,default=4)
parser.add_argument('--columns', type=int,default=5)
# parser.add_argument('--winRate', type=int,default=20)
parser.add_argument('--rand', dest='rand', action='store_true')
parser.add_argument('--no-rand', dest='rand', action='store_false')
parser.add_argument('--order', choices=['rand', 'date', 'name'],default='name')
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
        # print(df)
        # import pdb;pdb.set_trace()
        # df = df[listOfName].filter(items=listOfName,axis=0)
        df = df.filter(items=listOfName,axis=0)
        df = df.fillna(0.)
    return df


class action:
    def __init__(self,keys,targetDir,actiontype='move'):
        self.keys = keys
        self.notedownfile = keys + '.txt'
        self.targetDir = targetDir
        self.actiontype = actiontype
        
 

class ClickableLabel(QtWidgets.QLabel):
    CtrlClicked = QtCore.pyqtSignal()
    CtrlRclicked = QtCore.pyqtSignal()
    winningCount = 0
    # timeToWin = 5000

    def noteItDown(self, fileName,bolor=None):
        # print(self.Imagelist[self.currentIndex])
        if bolor is None: 
            self.setStyleSheet("background-color: lightgreen")
        else:
            self.setStyleSheet("background-color: " + bolor)
        with open(fileName, 'a+') as fp:
            fp.write(self.Imagelist[self.currentIndex] + '\n')
    def setList(self,List,ra = 1):
        self.clicked = QtCore.pyqtSignal()
        self.Rclicked = QtCore.pyqtSignal()
        self.timer=QTimer()
        self.rightOne = ra
        self.Imagelist = List
        self.currentIndex = 0
        self.redhotmap = QtGui.QPixmap(self.Imagelist[0])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height(),1,1)
        self.setPixmap(self.redhotmap)
        self.w = self.geometry().width()
        self.h = self.geometry().height()
    def changeColor(self):
        self.setStyleSheet("background-color: lightgreen;border: 5px solid green;") 
        print('dont worry it loser will not be delated')
        # self.setStyleSheet("")
        self.timer.stop()
    
    def bringNextContenderOut(self):
        self.timer.timeout.connect(self.changeColor)
        self.currentIndex += 1
        try:
            self.redhotmap = QtGui.QPixmap(self.Imagelist[self.currentIndex])
        except:
            self.redhotmap = QtGui.QPixmap(self.Imagelist[self.currentIndex-1])
            self.currentIndex -= 1
            
        self.redhotmap = self.redhotmap.scaled(self.w, self.h, 1, 1)
        self.setPixmap(self.redhotmap)
        self.resize(self.redhotmap.width(),self.redhotmap.height())
        self.setAlignment(QtCore.Qt.AlignTop)
        # self.winningCount = 0 
        # self.timer.stop()
        self.setStyleSheet("background-color: black") 
        # self.timer.start(ClickableLabel.timeToWin)
    def search_inlastline(self,pattern):
        file_list = ['l.txt', 'r.txt']
        fl_valid = []
        for fl in file_list: 
            if not Path(fl).is_file():
                continue
            with open(fl,'r') as fp:
                for lines in fp.readlines():
                    # if re.search(pattern,lines):
                    # print(f'{pattern} is in {lines}')
                    if pattern in lines:
                        fl_valid.append(fl)
                        break
        return fl_valid


    def skipNextnContender(self,pattern):
        list_of_files_to_write_in = self.search_inlastline(pattern)
        while pattern in self.getCurrentcontenderName():
            for fps in list_of_files_to_write_in:
                self.noteItDown(fps)
            self.noteItDown('default.txt')
            self.currentIndex += 1
        self.currentIndex -= 1
        self.bringNextContenderOut()

    def itWon(self,by=0):
        self.timer.stop()
        self.winningCount += 1 + by
        self.setStyleSheet("background-color: lightgreen") 
    
    def getWinningCount(self):
        return self.winningCount
    
    def bringPreviousContenderOut(self):
        # self.timer.stop()
        # self.setStyleSheet("background-color: black") 
        # self.timer.start(ClickableLabel.timeToWin)
        self.currentIndex -= 1
        self.redhotmap = QtGui.QPixmap(self.Imagelist[self.currentIndex])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height() * self.rightOne ,1,1)
        self.setPixmap(self.redhotmap)
        self.resize(self.redhotmap.width(),self.redhotmap.height())
        self.setAlignment(QtCore.Qt.AlignTop)
    
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
            # print('left button pressed')
            
            self.noteItDown('l.txt')
            # self.clicked.emit()
        if rightPressed and not ctrlPressed :
            self.noteItDown('r.txt','blue')
            # self.Rclicked.emit()
        if leftPressed and ctrlPressed:
            pass
            # self.CtrlClicked.emit()
        if rightPressed and ctrlPressed:
            pass
            # self.CtrlRclicked.emit()

class Ui_MainWindow(object):
    path = args.inputDir
    def setupList(self):
        self.dffilename = Path(args.inputDir) / 'winningRecords.csv'
        self.listI = [str(x) for x in Path(self.path).glob('*.jpg')]
        if args.rand:
            cyclePoint = random.randint(0, len(self.listI))
            self.listI = self.listI[cyclePoint::] + self.listI[:cyclePoint:]
        if args.order == 'rand':
            random.shuffle(self.listI)
        elif args.order == 'date':
            self.listI = sorted(self.listI, key=lambda x: Path(x).stat().st_mtime)
            # start_time = time.time()
            # end_time = start_time + args.time * 60
            # while time.time() < end_time:
            #     time.sleep(1)
            
        listOfName =  [Path(x).stem for x in self.listI]
        # weightM = np.zeros((len(listOfName),1))
        # df = pd.DataFrame(weightM,columns=['filename'],index=listOfName)
        # print(self.path)
        # self.df = csvReadFile(df,self.dffilename,listOfName)
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
    def openTargetDir(self,directory_path):
        os.system('start "" "%s"' % directory_path)
        
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
    def closingActions(self,event):
        # self.moveFiles()
        # self.moveFiles('listchampions.txt.opml',args.championsDir,False)
        # self.moveFiles('listmidCard.txt.opml',r'C:\Heaven\YummyBaked\midCard',False)
        # self.moveFiles('listmidCard.txt.opml',args.MidCardDir,False)
        # self.moveFiles('listdel.txt.opml',args.DeletablePath,False)
        # outputDir = args.outputDir
        for tb in self.actions:
            if tb.actiontype == 'corr_move': 
                # print(tb.targetDir)
                self.movecorrFiles(tb.notedownfile,tb.targetDir,False,'force_copy')
                continue
            self.moveFiles(tb.notedownfile,tb.targetDir,False,'force_copy')
        # breakpoint()
        
        self.moveFiles(self.defaultaction.notedownfile,self.defaultaction.targetDir,False,'move')
        
        
        # self.df.to_csv(self.dffilename)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        screenw = 1920
        screenh = 1000
        MainWindow.resize(screenw, screenh)
        self.scannedFiles = 0
        rows = args.rows
        columns = args.columns
        self.picInWin = rows * columns
        cellArea = (screenw * screenh) / self.picInWin
        self.cellheight = screenh / rows
        self.cellwidth = screenw / columns
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
        self.horizontalLayout = QtWidgets.QGridLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        # self.label = ClickableLabel(self.horizontalLayoutWidget)
        
        # self.textlabel = ClickableLabel(self.horizontalLayoutWidget)
        # self.textlabel.setObjectName("textlabel")
        # self.textlabel.setAlignment(QtCore.Qt.AlignLeft)
        # self.textlabel.setWordWrap(True)
        # self.textlabel.setFont(QtGui.QFont('Arial', 15))
        # self.textlabel.setText("Hello World")
        
        
        # self.label.setText("")
        # self.label.setObjectName("label")
        # self.label.resize(int(w/2),h)
        if len(self.listI) == 0:
            return
        # self.label.setList(self.listI[0::2])
        fullScreenFlag = [False]
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up), MainWindow, activated=lambda :MainWindow.setWindowState(QtCore.Qt.WindowMinimized) == MainWindow.close())
        
        def toggleFulScreen():
            MainWindow.setWindowState(QtCore.Qt.WindowFullScreen) if not fullScreenFlag[0] else MainWindow.setWindowState(QtCore.Qt.WindowMaximized)
            fullScreenFlag[0] = not fullScreenFlag[0]
        
        # self.label.setScaledContents(False)
        # self.horizontalLayout.addWidget(self.label)
        i = 0
        self.cells = []
        for r in range(rows):
            for c in range(columns):
                if (r+1) * (c+1) >= self.picInWin:
                    break
                LeftImage = ClickableLabel(self.horizontalLayoutWidget)
                # LeftImage.resize(self.cellwidth,self.cellheight)
                LeftImage.resize(self.cellwidth,self.cellheight)
                LeftImage.setList(self.listI[i::self.picInWin-1])
                LeftImage.setObjectName("LeftImage")
                # LeftImage.clicked.connect(lambda :LeftImage.noteItDown('l.txt'))
                # LeftImage.Rclicked.connect(lambda :LeftImage.noteItDown('r.txt'))
                self.horizontalLayout.addWidget(LeftImage,r,c)
                self.cells.append(LeftImage)
                i += 1
        r_keys_list = [
                    QtCore.Qt.Key_4, 
                    QtCore.Qt.Key_5,
                    QtCore.Qt.Key_6,
                    ]
        for r_key,r_cell in zip(r_keys_list,self.cells[::int(len(self.cells)/len(r_keys_list))]):
            QtWidgets.QShortcut(QtGui.QKeySequence(r_key), r_cell, activated=lambda x=r_cell:x.noteItDown('r.txt','blue'))
        # self.LeftImage.clicked.connect(lambda x=acts.notedownfile:self.label.noteItDownre(x))
        l_keys_list = [
                    QtCore.Qt.Key_1, 
                    QtCore.Qt.Key_2, 
                    QtCore.Qt.Key_3, 
                    ]
        for r_key,r_cell in zip(l_keys_list,self.cells[::int(len(self.cells)/len(l_keys_list))]):
            QtWidgets.QShortcut(QtGui.QKeySequence(r_key),r_cell, activated=lambda x=r_cell:x.noteItDown('l.txt'))
        # self.LeftImage.clicked.connect(lambda x=acts.notedownfile:self.label.noteItDownre(x))
        
        
        
        b1 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        b1.setText("next")
        for acts in self.actions:
            QtWidgets.QShortcut(QtGui.QKeySequence('Shift+' + acts.keys), MainWindow, activated=lambda x=acts.targetDir:self.openTargetDir(x))    
        b1.setGeometry(MainWindow.geometry().width()-self.cellwidth,MainWindow.geometry().height()-self.cellheight,int(self.cellwidth/2),self.cellheight)  
        b1.clicked.connect(self.arraowEvent)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left),MainWindow, activated=self.arraowEvent)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), MainWindow, activated=self.previousall)
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_X), MainWindow, activated=self.skip_ahead)
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Period), MainWindow, activated=self.skip_ahead)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_0), MainWindow, activated=self.skip_ahead)
        # self.horizontalLayout.addWidget(self.textlabel)
        MainWindow.setCentralWidget(self.centralwidget)
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        lastlayout = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget)
        quit_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        countbtn = 1
        quit_btn.setText('quit')
        quit_btn.clicked.connect(lambda :MainWindow.setWindowState(QtCore.Qt.WindowMinimized) == MainWindow.close())
        r1 = QtCore.QRect(b1.geometry().right(),b1.geometry().top(),int(self.cellwidth/2),self.cellheight/countbtn)
        quit_btn.setGeometry(r1)
        lastlayout.setGeometry(r1)
        lastlayout.addWidget(quit_btn)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # breakpoint()
        # self.field_joystick_up_button = QtGui.QToolButton()
        # self.field_joystick_up_button.setArrowType(QtCore.Qt.UpArrow)
        

        # self.timestamp = time.time()

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
        self.textlabel.setText(moveStr)
        
    def AssignRole(self):
        
        moveStr = main()
        print(moveStr)
        self.statusbar.showMessage(moveStr)
        self.textlabel.setText(moveStr)
    
    def statusbarManipulation(self):
        rng = 3 > random.randint(0,15)
        if rng and False:
           self.DoMoves()
        else:
            self.AssignRole()
    
    def previousall(self):
        
        # print('its executinh')
        for cell in self.cells:
            # cell.noteItDown(self.defaultaction.notedownfile)
            cell.bringPreviousContenderOut()
        
        self.scannedFiles -= self.picInWin - 1 
        self.statusbar.showMessage(str(self.scannedFiles) + '/'+ str(len(self.listI)) )
    
    def skip_ahead(self):
        patterns = []
        for cell in self.cells:
            skip_p = cell.getCurrentcontenderName()
            skip_p = skip_p.split('-Scene-')[0] + '-Scene-'
            patterns.append(skip_p)
        for cell in self.cells:
            for pp in patterns:
                cell.skipNextnContender(pp)


    def arraowEvent(self):
        # print('its executinh')
        for cell in self.cells:
            cell.noteItDown(self.defaultaction.notedownfile)
            cell.bringNextContenderOut()
            # print(cell.geometry())  
        
        self.scannedFiles += self.picInWin - 1 
        self.statusbar.showMessage(str(self.scannedFiles) + '/'+ str(len(self.listI)) )
        # Loser.resize(MainWindow.geometry().width()/2,MainWindow.geometry().height()-30)
        # flag = False
        # Winner.itWon(Loser.getWinningCount())
        # deliberationTime = time.time() - self.timestamp
        # print(Winner.getWinningCount(), ' winnin', loserName)
        # Loser.noteItDown('del.txt')
        # if deliberationTime < self.losersTime and Loser.getWinningCount() <= 0:
            # Loser.noteItDown('del.txt')
        # else:
           # Loser.noteItDown('midCard.txt') 
        # if Winner.getWinningCount() >= self.topCard:
           # Winner.setStyleSheet("border: 5px solid black;")
           # Winner.noteItDown('champions.txt') 
        # self.df.loc[winnerName] = self.df.loc[winnerName] + self.df.loc[loserName] + 1
        # print(loserName , 'lost to', winnerName)
        # Winner.bringNextContenderOut()
        # if random.randint(1,100) < 80:
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
