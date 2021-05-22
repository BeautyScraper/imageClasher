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
import re
import os
from notSoRand import main

class FileAction():
    
    def __init__(self,ActionString,srcFile,*param):
        self.ActionString = ActionString
        self.srcFile = srcFile
        
    def movesrcLsttoDstPath(self,srcFileName,DstPath):
        pass
    def perform():
        if not Path(self.srcFile).is_file():
            return
        if self.ActionString == 'move':
            p = Path(param[0])
            assert p.is_dir()
            self.movesrcLsttoDstPath(self.srcFile,p)
            
def openInBrowser(fileName):
    import webbrowser
    template = 'https://www.instagram.com/p/@@/'
    # fileName = 'estellemorain(B3-FYpcBMcE).jpg'
    try: 
        postId = re.search('\((.*?)\)',fileName).group(1)
    except:
        print('Not a correctly Formated File')
        return
    urlToOpen =  template.replace('@@', postId)
    print(urlToOpen)
    webbrowser.open(urlToOpen, new=2)
    
    


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    CtrlClicked = QtCore.pyqtSignal()
    Rclicked = QtCore.pyqtSignal()
    CtrlRclicked = QtCore.pyqtSignal()
    def setList(self,List):
        self.Imagelist = List
        self.currentIndex = 0
        self.redhotmap = QtGui.QPixmap(self.Imagelist[0])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height(),1,1)
        self.setPixmap(self.redhotmap)
    
    def bringNextContenderOut(self):
        self.currentIndex += 1
        self.redhotmap = QtGui.QPixmap(self.Imagelist[self.currentIndex])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height(),1,1)
        self.setPixmap(self.redhotmap)
        self.resize(self.redhotmap.width(),self.redhotmap.height())
        
    def bringPreviousContenderOut(self):
        self.currentIndex -= 1
        self.redhotmap = QtGui.QPixmap(self.Imagelist[self.currentIndex])
        self.redhotmap = self.redhotmap.scaled(self.geometry().width(),self.geometry().height(),1,1)
        self.setPixmap(self.redhotmap)
        self.resize(self.redhotmap.width(),self.redhotmap.height())
        # .setAlignment(QtCore.Qt.AlignLeft)
        # self.Text(self.Imagelist[self.currentIndex])
        # print('New Image Allocated',self.Imagelist[self.currentIndex],self.currentIndex)
        
        
    def getCurrentcontenderName(self):
        try :
            p = Path(self.Imagelist[self.currentIndex]).stem
        except:
            self.setStyleSheet("QLabel"
                            "{"
                            "background-color : lightgreen;"
                            "}")
            p = Path(self.Imagelist[-1]).stem
            
        return p
        
        
    def mouseReleaseEvent(self, QMouseEvent):
        # print(QMouseEvent)
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        # import pdb; pdb.set_trace()
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
    path = sys.argv[1]
    def setupList(self):
        self.listI = [str(x) for x in Path(self.path).glob('*.jpg')]
        listOfName =  [Path(x).stem for x in self.listI]
        shuffle(self.listI)
        self.dffilename = Path(self.path) / 'MatchRecord.csv'
        self.ActionList = []
        # self.ActionDict = [(filename, 'Move', DstDirPath)]
        weightM = np.zeros((len(listOfName),len(listOfName)))
        df = pd.DataFrame(weightM,columns=listOfName,index=listOfName)
        # assert len(listOfName) != len(self.listI)
        if self.dffilename.is_file():
            df1 = pd.read_csv(str(self.dffilename))
            df1 = df1.set_index(df1.columns[0])
            # import pdb;pdb.set_trace()
            df = df1 + df
            df = df[listOfName].filter(items=listOfName,axis=0)
            df = df.fillna(0.)
        self.df = df

    def showTheWinner(self,MainWindow):
        print('current champion score is:' , self.df.sum(1).max())
        p = Path(self.path) / (self.df.sum(1).idxmax() + '.jpg')
        # template = 'start "C:\Program Files\IrfanView\i_view64.exe\" "%s"' %  str(p)
        template = 'start "C:\Program Files\IrfanView\i_view64.exe\" /slideshow=%s' %  str(p)
        os.system(template)
        # print(p)
        
    def showTheLoser(self,MainWindow):
        # print('current champion score is:' , self.df.sum(1).min())
        lf = self.df.sum(1).sort_values(0,ascending=False).index
        norm = lambda x: str(Path(self.path) / (x + '.jpg')) + '\n' 
        fileList = [norm(x) for x in lf]
        myPicsListCatalog = Path.cwd() /  'myPics.txt'
        with open(myPicsListCatalog,'w') as fp:
            fp.writelines(fileList)
        # p = Path(self.path) / (self.df.sum(1).idxmin() + '.jpg')
        template = '\"C:\Program Files\IrfanView\i_view64.exe\" /slideshow=%s' %  str(myPicsListCatalog)
        print(template)
        os.system(template)
        # print(p)
        

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1000)
        MainWindow.closeEvent = lambda e: self.df.to_csv(self.dffilename)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.h = MainWindow.geometry().height()
        h = self.h
        self.w = MainWindow.geometry().width()
        w = self.w
        self.setupList()
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, w, h))
        # MainWindow.setWindowState(QtCore.Qt.WindowFullScreen)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.label = ClickableLabel(self.horizontalLayoutWidget)
        # self.label.setGeometry(QtCore.QRect(0, 0, w, h))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.resize(w/2,h)
        self.label.setList(self.listI[0::2])
        # print(self.listI[223])
        # redhotmap = QtGui.QPixmap(self.listI[223])
        # redhotmap = QtGui.QPixmap("D:/paradise/stuff/Images/walls/juggernaut1_huc656199de66b421ef22ad489780ef428_234989_1920x1080_resize_q75_box.jpg")
        # redhotmap = redhotmap.scaled(200,200,0)
        # self.label.setPixmap(redhotmap)
        self.label.setScaledContents(False)
        self.horizontalLayout.addWidget(self.label)
        self.LeftImage = ClickableLabel(self.horizontalLayoutWidget)
        self.LeftImage.resize(w/2,h)
        self.LeftImage.setList(self.listI[1::2])
        self.LeftImage.setObjectName("LeftImage")
        # self.LeftImage.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.horizontalLayout.addWidget(self.LeftImage)
        MainWindow.setCentralWidget(self.centralwidget)
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.arraowEvent(1))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.arraowEvent(0))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up), MainWindow, activated=lambda :MainWindow.setWindowState(QtCore.Qt.WindowMinimized) == MainWindow.close())
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down), MainWindow, activated=lambda :self.showTheLoser(MainWindow))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), MainWindow, activated=lambda :openInBrowser(self.label.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_G), MainWindow, activated=lambda :openInBrowser(self.LeftImage.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.openFileIrfanView(self.label.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.openFileIrfanView(self.LeftImage.getCurrentcontenderName()))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Left), MainWindow, activated=lambda :self.label.bringPreviousContenderOut())
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.LeftImage.bringPreviousContenderOut())
        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Right), MainWindow, activated=lambda :self.openFileIrfanView(self.LeftImage.getCurrentcontenderName()))

        # QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), MainWindow, activated=self.label.bringNextContenderOut)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def openFileIrfanView(self,filePath):
        if not Path(filePath).is_absolute():
            p = Path(self.path) / ( filePath + '.jpg')
        # template = 'start "C:\Program Files\IrfanView\i_view64.exe\" "%s"' %  str(p)
        template = 'start "C:\Program Files\IrfanView\i_view64.exe\" "%s"' %  str(p)
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
        if rng:
           self.DoMoves()
        else:
            self.AssignRole()
    
    def arraowEvent(self,WinningSide):
        self.statusbarManipulation()
        Winner = self.label
        Loser = self.LeftImage
        if WinningSide == 0:
            Winner = self.LeftImage
            Loser = self.label
        winnerName = Winner.getCurrentcontenderName()
        loserName = Loser.getCurrentcontenderName()
        Loser.resize(MainWindow.geometry().width()/2,MainWindow.geometry().height()-30)
        
        # self.close()
        # print(self.df[winnerName][loserName])
        flag = False
        if True:
            # print('df corrrectness')
            df = self.df
            df.loc[winnerName,:] += df.loc[loserName,:].replace(-1,0)
            df.loc[winnerName,:] = df.loc[winnerName,:].replace(2,1)
            
            df[loserName] += df[winnerName].replace(1,0)
            df[loserName] = df[loserName].replace(-2,-1)
            # import pdb;pdb.set_trace()
        self.df[loserName][winnerName] = 1
        self.df[winnerName][loserName] = -1
        # print('Change Start',Loser.currentIndex)
        
        while self.df[loserName][winnerName] != 0 and self.df[winnerName][loserName] != 0:
            if flag:
                pass
                # print( loserName,'Already Done')
            flag = True
            Loser.currentIndex += 1
            if loserName != Loser.getCurrentcontenderName():
                loserName = Loser.getCurrentcontenderName()
            else:
                # print('Last One')
                return
        # print('Change Over',Loser.currentIndex)
        Loser.currentIndex -= 1
        Loser.bringNextContenderOut()
        self.horizontalLayout.addStretch(1)
        # print('Change Over')
        # self.df.to_csv(self.dffilename)
    
    # def getCurrentChampion(self):
        # pass

        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ClickOnTheWinner"))
        # self.label.setText(_translate("MainWindow", "TextLabel"))
        # self.LeftImage.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # print('Hello')
    # ui.df.to_csv(ui.dffilename)
    sys.exit(app.exec_())
