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

#change abc node path
def replaceABCNodePath(abcNode,dir):
    # print(cm.getAttr('%s.abc_File'%abcNode))
    # print(cm.getAttr('%s.abc_layerFiles'%abcNode))
    try:
        abcFile = cm.getAttr('%s.abc_File'%abcNode)
        abcFileDir = os.path.dirname(abcFile)
        abcFileBaseName = os.path.basename(abcFile)
        newAbcFile = os.path.join(dir,abcFileBaseName).replace('\\','/')
        # print(newAbcFile)
        #os.path.dirname()
        #set attr
        cm.setAttr('%s.abc_File'%abcNode,newAbcFile,type = 'string')
        cm.setAttr('%s.abc_layerFiles'%abcNode,1,newAbcFile,type = 'stringArray')
    except:
        pass

def getAlembicNodeList(objList):
    abcNodeList = list()
    for obj in objList:
        historyList = cm.listHistory(obj)
        if historyList:
            abcNode = None
            for history in historyList:
                if cm.nodeType(history) == 'AlembicNode':
                    abcNode = history
                    break
            if abcNode:
                if not abcNode in abcNodeList:
                    abcNodeList.append(abcNode)
    return abcNodeList

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
        self.setFixedSize(150, 100)

class BatchReplaceAbcPathWidget(QWidget):
    def __init__(self,parent = None):
        super(BatchReplaceAbcPathWidget,self).__init__(parent)

        self.scriptJobId = -10001

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'批量替换abc文件夹工具')
        self.resize(300,100)
        layout = QVBoxLayout(self)
        margin = 5
        layout.setContentsMargins(margin,margin,margin,margin)
        layout.setSpacing(3)
        self.setLayout(layout)

        textBrowser = QTextBrowser(self)
        # infoLabel.setFixedHeight(100)
        # infoLabel.setAlignment(Qt.AlignCenter)
        self.textBrowser = textBrowser
        layout.addWidget(textBrowser)
        # print(infoLabel.sizePolicy())

        # pathLayout = QHBoxLayout(self)
        # layout.addLayout(pathLayout)
        # pathLineEdit = QLineEdit(self)
        # pathLayout.addWidget(pathLineEdit)
        # selectFolderButton = QPushButton(u'selectFolder',self)
        # pathLayout.addWidget(selectFolderButton)
        
        self.infoLabel = QLabel(self)
        layout.addWidget(self.infoLabel)
        
        selectAllAlembicNodeBtn = QPushButton(u'选择所有abc节点',self)
        selectAllAlembicNodeBtn.clicked.connect(self.selectAllAbcNodes)
        layout.addWidget(selectAllAlembicNodeBtn)

        replaceButton = QPushButton(u'替换文件夹',self)
        replaceButton.clicked.connect(self.replaceAbcPathDialog)
        layout.addWidget(replaceButton)
        # print(replaceButton.sizePolicy())

        #styleSheet
        styleSheet = u'''
            *{
                font-size:12px;
                font-family:"Microsoft YaHei";
            }
            QTextBrowser{
                font-size:14px;
            }
        '''
        self.setStyleSheet(styleSheet)

        self.selectionChanged()

    def selectAllAbcNodes(self):
        abcNodeList = cm.ls(type = 'AlembicNode')
        cm.select(abcNodeList,r = True)

    def selectionChanged(self):
        abcNodeList = getAlembicNodeList(cm.ls(sl = True))
        # print(getAlembicNodeList(cm.ls(sl = True)))
        self.textBrowser.clear()
        if not abcNodeList:
            self.textBrowser.append(u'请选择物体\n或选择abc节点')
        else:
            abcText = ''
            for abcNode in abcNodeList:
                abcText += u'abc node:  <font color=white>%s</font><br>'%abcNode
                abcText += u'abc path:  <b><font color=yellow>%s</font></b><br><br>'%cm.getAttr('%s.abc_File'%abcNode)
            self.textBrowser.append(abcText)
        self.infoLabel.setText(u'%d 个abc节点被选择'%len(abcNodeList))

    def replaceAbcPathDialog(self):
        u'''
        选择alembic文件路径窗口
        '''
        basicFilter = "folder"
        abcPathList = cm.fileDialog2( fileFilter=basicFilter,dialogStyle = 2,fileMode = 3,
            caption = u'选择文件夹',okCaption = u'替换文件夹',cancelCaption = u'取消')
        if abcPathList:
            # print(abcPathList)
            abcNodeList = getAlembicNodeList(cm.ls(sl = True))
            if abcNodeList:
                for abcNode in abcNodeList:
                    replaceABCNodePath(abcNode,abcPathList[0])
                msgBox = EaMessageBox(getMayaWin())
                msgBox.setText(u'替换完毕，\n请保存后重新打开文件！')
                msgBox.setWindowTitle(u'结果')
                msgBox.setStyleSheet(u'font-size:12px;font-family:"Microsoft YaHei";')
                msgBox.exec_()
            #self.pathLineEdit.setText(abcPathList[0])
            #self.changeAlembicPath()
        self.selectionChanged()
        

    def showEvent(self,event):
        if not cm.scriptJob(ex = self.scriptJobId):
            self.scriptJobId = cm.scriptJob(event = ['SelectionChanged',self.selectionChanged])

    def hideEvent(self,event):
        if cm.scriptJob(ex = self.scriptJobId):
            cm.scriptJob(k = self.scriptJobId)



def mainUI():
    winName = u'batch_replace_abc_path_tool'
    if cm.window(winName,q = True,exists = True):
        cm.deleteUI(winName)

    win = BatchReplaceAbcPathWidget(getMayaWin())
    win.setObjectName(winName)
    win.show()


if __name__ == '__main__':
    mainUI()
    # replaceABCNodePath(cm.ls(sl = True)[0],'D:\\project\\0714\\B')
