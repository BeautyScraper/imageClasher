from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from pathlib import Path

import sys

from img_heap import MaxHeap, Candidate
import pandas as pd
from random import shuffle
import random
import numpy as np
import re
import os
from notSoRand import main
import Aftermath
from MyUtility import moveByFastCopy
import argparse
import shutil

from csvheap_ops import main as rain

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
# set a new parameter stringFiles with default value same as inputDir 
parser.add_argument('--stringDir', type=dir_path, default=None)
# parser.add_argument('--championsDir', type=dir_path)
parser.add_argument('--outputDir', type=dir_path)
parser.add_argument('--DeletablePath', type=dir_path,default=r'C:\temp\deleatble')
parser.add_argument('--time', type=int)
parser.add_argument('--winRate', type=int,default=20)
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

def openDirectoryUI(upi:str):
    os.system('start "" "%s"' % upi)

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    CtrlClicked = QtCore.pyqtSignal()
    Rclicked = QtCore.pyqtSignal()
    CtrlRclicked = QtCore.pyqtSignal()
    winningCount = 0
    timeToWin = 5000

    def noteItDown(self, fileName):
        with open(fileName, 'a+') as fp:
            fp.write(self.Imagelist[self.currentIndex] + '\n')
    def setList(self,List,ra = 1):
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
    
    def bringNextContenderOut(self):
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
        self.winningCount = 0 
        self.setStyleSheet("background-color: black") 
        # self.timer.start(ClickableLabel.timeToWin)
    
    def itWon(self,fp_path):
        pass

    def getWinningCount(self):
        return self.winningCount
    
    def bringPreviousContenderOut(self):
        self.timer.stop()
        self.setStyleSheet("background-color: black") 
        self.timer.start(ClickableLabel.timeToWin)
        self.currentIndex -= 1
        self.redhotmap = QtGui.QPixmap(self.Imagelist[self.currentIndex])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height() * self.rightOne ,1,1)
        self.setPixmap(self.redhotmap)
        self.resize(self.redhotmap.width(),self.redhotmap.height())
        self.setAlignment(QtCore.Qt.AlignTop)

    def getfullpathname(self):
        return self.Imagelist[self.currentIndex]
    
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

class HeapLabel(ClickableLabel):
    def setList(self, ra = 1):
        if args.stringDir is None:
            args.stringDir = args.inputDir
        Path(args.outputDir).mkdir(parents=True, exist_ok=True)
        self.im_heap_gen = MaxHeap(Path(args.outputDir)/'clash_records.csv')

        self.imgListGen = self.im_heap_gen.traverse_heap()
        # if len(self.imgListGen) <= 0:
        #     breakpoint()
            # first = Candidate()
        self.worths = 5000
        # super().setList(imgList,ra)
        self.rightOne = ra
        self.Imagelist = next(self.imgListGen).filepath
        self.currentIndex = 0
        self.redhotmap = QtGui.QPixmap(self.Imagelist)
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height(),1,1)
        self.setPixmap(self.redhotmap)
        self.w = self.geometry().width()
        self.h = self.geometry().height()

    def getCurrentcontenderName(self):
        try :
            p = Path(self.Imagelist).stem
        except:
            self.setStyleSheet("QLabel"
                            "{"
                            "background-color : red;"
                            "}")
            print('xdf566 error lies here')
            # p = Path(self.Imagelist[-1]).stem
            
        return p


    def bringNextContenderOut(self):
        # self.currentIndex += 1
        self.Imagelist = next(self.imgListGen).filepath
        try:
            self.redhotmap = QtGui.QPixmap(self.Imagelist)
        except:
            self.redhotmap = QtGui.QPixmap(self.Imagelist)
            self.im_heap_gen.heap_to_csv()
            # self.currentIndex -= 1
            
        self.redhotmap = self.redhotmap.scaled(self.w, self.h, 1, 1)
        self.setPixmap(self.redhotmap)
        self.resize(self.redhotmap.width(),self.redhotmap.height())
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setStyleSheet("background-color: black") 
        # self.timer.start(ClickableLabel.timeToWin)



    def itWon(self,fp_path):
        out_dir = Path(args.outputDir)
        out_dir.mkdir(exist_ok=True,parents=True)
        out_file = out_dir / Path(fp_path).name
        shutil.move(fp_path,out_file)
        print(f'{out_file.stem} lost to {Path(self.Imagelist).name}' )
        new_contender = Candidate(2000,str(out_file))
        parent = Candidate(2000,self.Imagelist)
        self.im_heap_gen.insert_child_to_parent(parent,new_contender)
        self.reset()

    def reset(self):
        self.imgListGen = self.im_heap_gen.traverse_heap()
        # self.Imagelist =  next(self.imgListGen).filepath
        # self.worths = next(self.imgListGen).key_worth
        # self.worths = [x.key_worth for x in self.im_heap_gen.traverse_heap()]
        # self.im_heap_gen.heap_to_csv()
        self.currentIndex = -1
        self.bringNextContenderOut()
        # self.timer.start(ClickableLabel.timeToWin)
 



class Ui_MainWindow(object):
    path = args.inputDir
    def setupList(self):
        self.dffilename = Path(args.inputDir) / 'winningRecords.csv'
        self.listI = [str(x) for x in Path(self.path).glob('*.jpg')] + [str(x) for x in Path(self.path).glob('*.webp')]
        if args.rand:
            cyclePoint = random.randint(0, len(self.listI))
            self.listI = self.listI[cyclePoint::] + self.listI[:cyclePoint:]
        if args.order == 'rand':
            random.shuffle(self.listI)
            
        listOfName =  [Path(x).stem for x in self.listI]
        weightM = np.zeros((len(listOfName),1))
        df = pd.DataFrame(weightM,columns=['filename'],index=listOfName)
        print(self.path)
        self.df = csvReadFile(df,self.dffilename,listOfName)
        # shuffle(self.listI)
        self.ActionList = []
        weightM = np.zeros((len(listOfName),len(listOfName)))
        self.listOfName = listOfName
        self.filecount = len(listOfName)
        
    def showTheWinner(self,MainWindow):
        template = 'start "C:\Program Files\IrfanView\i_view64.exe\" /slideshow=%s' %  str(p)
        os.system(template)

        
    def afterMath(self):
        print(f'xcc {self.path=}')
        Aftermath.main(Path(self.path))
    def openTargetDir(self):
        os.system('start "" "%s"' % args.outputDir)
        
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
        # self.moveFiles()
        # self.moveFiles('listchampions.txt.opml',args.championsDir,False)
        # self.moveFiles('listmidCard.txt.opml',r'C:\Heaven\YummyBaked\midCard',False)
        # self.moveFiles('listmidCard.txt.opml',args.MidCardDir,False)
        # self.moveFiles('listdel.txt.opml',args.DeletablePath,False)
        self.label.im_heap_gen.heap_to_csv()
        print('Closing heap')
        outputDir = r'D:\paradise\stuff\essence\Pictures\Action'
        rain(args.outputDir)
        if not Path('dnbh.txt').is_file():
            return
        with open('dnbh.txt') as fp:
            for filepathstr in fp.readlines():
                # import pdb;pdb.set_trace()
                fpname = Path(filepathstr.strip()).stem 
                try:
                    # outDir = Path(outputDir) / (Path(filepathstr.strip()).stem + ' Won_' + str(int(self.df.loc[fpname][0])) + Path(filepathstr.strip()).suffix)
                    outDir = Path(outputDir) / str(int(self.df.loc[fpname][0])) / Path(filepathstr.strip()).name
                    if not outDir.parent.is_dir():
                        outDir.parent.mkdir(parents=True)
                    # print(outDir)
                except:
                    # print('Some problem')
                    continue
                if Path(filepathstr.strip()).is_file():
                    shutil.move(filepathstr.strip(), outDir)
        Path('dnbh.txt').unlink()
        pass
        
        self.df.to_csv(self.dffilename)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1000)
        
        MainWindow.closeEvent = self.closingActions
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.h = MainWindow.geometry().height()
        h = self.h
        self.w = MainWindow.geometry().width()
        w = self.w
        
        self.setupList()
        
        
        self.topCard = args.winRate
        self.losersTime = args.time
        ClickableLabel.timeToWin = self.losersTime * 1000
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, w, h))
        self.timer=QTimer()
        self.timer.timeout.connect(self.DoMoves)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.label = HeapLabel(self.horizontalLayoutWidget)
        
        self.textlabel = ClickableLabel(self.horizontalLayoutWidget)
        self.textlabel.setObjectName("textlabel")
        self.textlabel.setAlignment(QtCore.Qt.AlignLeft)
        self.textlabel.setWordWrap(True)
        self.textlabel.setFont(QtGui.QFont('Arial', 15))
        self.textlabel.setText("Hello World")
        
        
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.resize(int(w/2),h)
        if len(self.listI) == 0:
            return
        self.label.setList()
        fullScreenFlag = [False]
        
        def toggleFulScreen():
            MainWindow.setWindowState(QtCore.Qt.WindowFullScreen) if not fullScreenFlag[0] else MainWindow.setWindowState(QtCore.Qt.WindowMaximized)
            fullScreenFlag[0] = not fullScreenFlag[0]
        
        self.label.setScaledContents(False)
        self.horizontalLayout.addWidget(self.label)
        self.LeftImage = ClickableLabel(self.horizontalLayoutWidget)
        self.LeftImage.resize(int(w/2),int(h))
        self.LeftImage.setList(self.listI,0.75)
        self.LeftImage.setObjectName("LeftImage")
        
        
        
        self.horizontalLayout.addWidget(self.LeftImage)
        self.horizontalLayout.addWidget(self.textlabel)
        MainWindow.setCentralWidget(self.centralwidget)
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # breakpoint()
        # self.field_joystick_up_button = QtGui.QToolButton()
        # self.field_joystick_up_button.setArrowType(QtCore.Qt.UpArrow)
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.arraowEvent(1))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.arraowEvent(0))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up), MainWindow, activated=lambda :MainWindow.setWindowState(QtCore.Qt.WindowMinimized) == MainWindow.close())
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down), MainWindow, activated=lambda :self.showTheLoser(MainWindow))
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), MainWindow, activated=lambda :openInBrowser(self.label.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_G), MainWindow, activated=lambda :openInBrowser(self.LeftImage.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_S), MainWindow, activated=lambda :openDirectoryUI(args.stringDir))
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_O), MainWindow, activated=self.openTargetDir)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), MainWindow, activated=self.afterMath)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_M), MainWindow, activated= toggleFulScreen)
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.openFileIrfanView(self.label.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.openFileIrfanView(self.LeftImage.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.label.bringPreviousContenderOut())
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.LeftImage.bringPreviousContenderOut())
        
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_1), MainWindow, activated=lambda :self.label.noteItDown('dnbh.txt'))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_2), MainWindow, activated=lambda :self.LeftImage.noteItDown('dnbh.txt'))
        
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_1), MainWindow, activated=lambda :self.label.noteItDown('del.txt'))
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_2), MainWindow, activated=lambda :self.LeftImage.noteItDown('del.txt'))
        


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def openFileIrfanView(self,filePath):
        if not Path(filePath).is_absolute():
            p = Path(self.path) / ( filePath + '.jpg')

        template = 'start "C:\Program Files (x86)\IrfanView\i_view32.exe\" "%s"' %  str(p)
        os.system(template)

    
    def DoMoves(self):
        movefppath = Path(r'D:\Developed\Automation\imageClasher\lunchers\files\MoveName.txt')
        with open(movefppath,'r') as fp:
            fc = fp.readlines()
        wrestler = ['LeftOne \U00002B05', 'RightOne \U000027A1']#https://unicode-table.com/en/sets/arrow-symbols/#right-arrows
        shuffle(wrestler)

        moveStr = '%s %sed %s' % (wrestler[0],random.choice(fc).strip(),wrestler[1])
        i = 1
        counter = random.randint(0,5) > 2
        if counter:
            moveStr += ' but %s countered with %s' % (wrestler[i%2],random.choice(fc).strip())
            i += 1
        pinned = random.randint(0,10) < 2
        if pinned and not counter:
            moveStr += 'and %s pinneded %s' % (wrestler[0],wrestler[1])
            self.timer.stop()
            
        if pinned and counter:
            moveStr += 'and %s pinneded %s' % (wrestler[i%2],wrestler[(i+1)%2])
            self.timer.stop()
            
        
        # print(moveStr)
        # self.statusbar.showMessage(moveStr)
        self.textlabel.setText(moveStr)
        if not pinned:
            self.timer.start(200 * len(moveStr))
        
    def AssignRole(self):
        temp_path = Path(args.stringDir) / 'files'
        temp_path.mkdir(exist_ok=True,parents=True)
        moveStr = main(str(temp_path))
        # print(moveStr)
        self.textlabel.setText(moveStr)
    
    def statusbarManipulation(self):
        rng = 2 > random.randint(0,15)
        if rng:
            self.DoMoves()
        else:
            self.timer.stop()
            self.AssignRole()
    
    def arraowEvent(self,WinningSide):
        
        
        self.statusbarManipulation()
        Winner = self.label
        Loser = self.LeftImage
        self.statusbar.showMessage(f'{Winner.im_heap_gen.size} out of {str(512)}')
        if WinningSide == 0:
            Winner = self.LeftImage
            Loser = self.label
        winnerName = Winner.getCurrentcontenderName()
        loserName = Loser.getCurrentcontenderName()
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
        print(loserName , 'lost to', winnerName)
        # Winner.bringNextContenderOut()
        # if random.randint(1,100) < 80:
        Winner.itWon(Loser.getfullpathname())
        Loser.bringNextContenderOut()
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
