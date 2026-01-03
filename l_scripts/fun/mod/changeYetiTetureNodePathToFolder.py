# -*- coding:utf-8 -*-
import maya.cmds as cm
import os
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import re
import functools
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance
except:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance

def getAllYetiMayaTransformNodeList():
    yetiShapeList = cm.ls(type = 'pgYetiMaya')
    yetiTransformList = list()
    if yetiShapeList:        
        for yetiShape in yetiShapeList:
            transformList = cm.listRelatives(yetiShape,p = True,pa = True)
            if transformList:
                yetiTransformList.append(transformList[0])
    return yetiTransformList
    
def changeTetureNodePathToFolder(yetiTransformList,dir):                
    for yetiTransform in yetiTransformList:
        textureNodeList = cm.pgYetiGraph(yetiTransform,listNodes = True,type = 'texture')
        if textureNodeList:
            for textureNode in textureNodeList:
                try:
                    filePath = cm.pgYetiGraph(yetiTransform,node = textureNode,param = 'file_name',getParamValue = True)
                    fileDir = os.path.dirname(filePath)
                    fileBaseName = os.path.basename(filePath)
                    newFilePath = os.path.join(dir,fileBaseName).replace('\\','/')
                    cm.pgYetiGraph(yetiTransform,node = textureNode,param = 'file_name',setParamValueString = newFilePath)
                    print(u'change %s %s file_name from %s to %s'%(yetiTransform,textureNode,filePath,newFilePath))
                except:
                    pass


#ui
def getMayaWin():
    ptr = omui.MQtUtil.mainWindow()
    mayaWin = wrapInstance(long(ptr), QWidget)
    return mayaWin

class EaMessageBox(QMessageBox):
    def __init__(self, parent = None):
        super(EaMessageBox, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose,True)

    def resizeEvent(self,event):
        super(EaMessageBox, self).resizeEvent(event)
        self.setFixedSize(120, 100)

class ChangeYetiTetureNodePathToFolderWidget(QWidget):
    def __init__(self,parent = None):
        super(ChangeYetiTetureNodePathToFolderWidget,self).__init__(parent)

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'批量替换yeti贴图路径工具')
        self.resize(300,100)
        layout = QVBoxLayout(self)
        margin = 5
        layout.setContentsMargins(margin,margin,margin,margin)
        layout.setSpacing(3)
        self.setLayout(layout)


        replaceButton = QPushButton(u'选择文件夹替换',self)
        replaceButton.setFixedHeight(30)
        replaceButton.clicked.connect(self.replaceAbcPathDialog)
        layout.addWidget(replaceButton)
        # print(replaceButton.sizePolicy())

        #styleSheet
        styleSheet = u'''
            *{
                font-size:12px;
                font-family:"Microsoft YaHei";
            }
            QLabel{
                font-size:14px;
            }
        '''
        self.setStyleSheet(styleSheet)


    def replaceAbcPathDialog(self):
        u'''
        选择alembic文件路径窗口
        '''
        basicFilter = "folder"
        abcPathList = cm.fileDialog2( fileFilter=basicFilter,dialogStyle = 2,fileMode = 3,
            caption = u'选择文件夹',okCaption = u'替换',cancelCaption = u'取消')
        if abcPathList:
            # print(abcPathList)
            nodeList = getAllYetiMayaTransformNodeList()
            if nodeList:
                changeTetureNodePathToFolder(nodeList,abcPathList[0])
                msgBox = EaMessageBox(getMayaWin())
                msgBox.setText(u'替换完毕！')
                msgBox.setWindowTitle(u'结果')
                msgBox.setStyleSheet(u'font-size:12px;font-family:"Microsoft YaHei";')
                msgBox.exec_()
            #self.pathLineEdit.setText(abcPathList[0])
            #self.changeAlembicPath()



def mainUI():
    winName = u'changeTetureNodePathToFolderWin'
    if cm.window(winName,q = True,exists = True):
        cm.deleteUI(winName)

    win = ChangeYetiTetureNodePathToFolderWidget(getMayaWin())
    win.setObjectName(winName)
    win.show()


if __name__ == '__main__':
    mainUI()
