# -*- coding: utf8
import sys,os,re
from PySide2.QtWidgets import *
from PySide2 import QtCore
from PySide2.QtGui import QMovie
from PySide2.QtCore import *
import maya.cmds as cmds


instructions=u'''
**使用说明**
1. 如何贴图连接到材质球的属性带有"color"关键字被视为颜色贴图
2. 如何贴图名称带有"color"关键字的"File"节点被视为颜色贴图
'''
        
class L_ProgressDialog(QProgressDialog):
    def __init__(self,title=u'设置颜色空间',processList=[]):
        self.title=title;self.processList=processList
        self.listLen=len(self.processList)
        #QProgressDialog(u"正在{},请稍等{}".format(self.title,self.listLen), "Cancel", 0,self.listLen)
        super(L_ProgressDialog, self).__init__(u"正在{},请稍等{}".format(self.title,self.listLen), "Cancel", 0,self.listLen)
        self.setWindowTitle(title)
        self.setFixedSize(650,170)
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint |   # 使能最小化按钮
                            Qt.WindowType.WindowCloseButtonHint |      # 使能关闭按钮
                            Qt.WindowType.WindowStaysOnTopHint) 
        self.open()

    def ProgressDialog_Procecss(self,index):
        if self.wasCanceled():
            return 'stop'
        self.setValue(index+1)
        self.setLabelText(u'已完成{}/{}'.format(index,self.listLen))
        QCoreApplication.processEvents()


class UI(QWidget):
    def __init__(self):
        super(UI,self).__init__()
        self.setFixedWidth(800)
        self.setWindowTitle(u'设置颜色空间')
        self.resize(500, 200)
        self.topLay=QVBoxLayout(self)
        colorSpaceList=cmds.colorManagementPrefs(q=True, inputSpaceNames=True) 
        
        colorQH=QHBoxLayout()
        self.topLay.addLayout(colorQH)
        colorLabelWgt=QLabel(u'颜色贴图颜色空间')
        self.colorFileNodeWgt=QComboBox()
        self.colorFileNodeWgt.addItems(colorSpaceList)
        self.colorFileNodeWgt.currentTextChanged.connect(lambda:self.setColorSpace(NodeType='Color'))
        
        colorQH.addWidget(colorLabelWgt,1)
        colorQH.addWidget(self.colorFileNodeWgt,10)
        
        otherQH=QHBoxLayout()
        self.topLay.addLayout(otherQH)
        otherLabelWgt=QLabel(u'其他贴图颜色空间')
        self.otherFileNodeWgt=QComboBox()
        self.otherFileNodeWgt.addItems(colorSpaceList)
        self.otherFileNodeWgt.currentTextChanged.connect(lambda:self.setColorSpace(NodeType='Grey'))
        
        otherQH.addWidget(otherLabelWgt,1)
        otherQH.addWidget(self.otherFileNodeWgt,10)

        
        # 颜色空间转换A  》》》》》》》》》》》》》
        colorSpaceConvetQHA=QHBoxLayout()
        self.srcColorSpaceWgtA=QComboBox()
        self.tgtColorSpaceWgtA=QComboBox()
        
        self.srcColorSpaceWgtA.addItems(colorSpaceList)
        self.srcColorSpaceWgtA.setEditable(1)
        self.tgtColorSpaceWgtA.addItems(colorSpaceList)
        self.tgtColorSpaceWgtA.setEditable(1)

        colorSpaceConvetQHA.addWidget(QLabel(u'原始颜色空间'),1)
        colorSpaceConvetQHA.addWidget(self.srcColorSpaceWgtA,10)
        colorSpaceConvetQHA.addWidget(QLabel(u'>>>转换到>>>'),1)
        colorSpaceConvetQHA.addWidget(QLabel(u'目标颜色空间'),1)
        colorSpaceConvetQHA.addWidget(self.tgtColorSpaceWgtA,10)
        # 颜色空间转换A  《《《《《《《《《《《《
        
        # 颜色空间转换B  》》》》》》》》》》》》》
        colorSpaceConvetQHB=QHBoxLayout()
        self.srcColorSpaceWgtB=QComboBox()
        self.tgtColorSpaceWgtB=QComboBox()
        
        self.srcColorSpaceWgtB.addItems(colorSpaceList)
        self.srcColorSpaceWgtB.setEditable(1)
        self.tgtColorSpaceWgtB.addItems(colorSpaceList)
        self.tgtColorSpaceWgtB.setEditable(1)

        colorSpaceConvetQHB.addWidget(QLabel(u'原始颜色空间'),1)
        colorSpaceConvetQHB.addWidget(self.srcColorSpaceWgtB,10)
        colorSpaceConvetQHB.addWidget(QLabel(u'>>>转换到>>>'),1)
        colorSpaceConvetQHB.addWidget(QLabel(u'目标颜色空间'),1)
        colorSpaceConvetQHB.addWidget(self.tgtColorSpaceWgtB,10)
        # 颜色空间转换B  《《《《《《《《《《《《
        
        
        self.topLay.addLayout(colorSpaceConvetQHA)
        self.topLay.addLayout(colorSpaceConvetQHB)
        converColorSpaceBtn=QPushButton(u'执行颜色空间转换')
        converColorSpaceBtn.clicked.connect(self.toggleColorSpace)

        self.topLay.addWidget(converColorSpaceBtn)

        self.topLay.addLayout(colorSpaceConvetQHA)

        instructionsWgt=QLabel(instructions)
        self.topLay.addWidget(instructionsWgt)
        
        
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint |   # 使能最小化按钮
                        Qt.WindowType.WindowCloseButtonHint |      # 使能关闭按钮
                        Qt.WindowType.WindowStaysOnTopHint)
    
    def toggleColorSpace(self):
        srcColorSpaceA=self.srcColorSpaceWgtA.currentText()
        tgtColorSpaceA=self.tgtColorSpaceWgtA.currentText()
        srcColorSpaceB=self.srcColorSpaceWgtB.currentText()
        tgtColorSpaceB=self.tgtColorSpaceWgtB.currentText()
        allFileNode=cmds.ls(type='file')
        for file in allFileNode:
            getSrcColorSpace=cmds.getAttr(file+'.colorSpace')
            if getSrcColorSpace==srcColorSpaceA:
                cmds.setAttr(file+'.colorSpace',tgtColorSpaceA,type='string')
            elif getSrcColorSpace==srcColorSpaceB:
                cmds.setAttr(file+'.colorSpace',tgtColorSpaceB,type='string')

    
    def setColorSpace(self,NodeType='Color|Grey'):
        allFileNode=cmds.ls(type='file')
        colorMapColorSpace=self.colorFileNodeWgt.currentText()
        for file in allFileNode:
            isColorSpace=False
            TexName=cmds.getAttr(file+'.ftn')
            colorCon=cmds.listConnections(file+'.outColor',plugs=1)
            if colorCon:
                if re.search('color',str(colorCon),flags=re.I):
                    isColorSpace=True
            if NodeType=='Color':
                if re.search('color',TexName,flags=re.I) or isColorSpace:
                    cmds.setAttr(file+u'.colorSpace',colorMapColorSpace,type=u'string')
                    #print (u'设置节点{}颜色空间属性为{}'.format(file,colorMapColorSpace))
            elif  NodeType=='Grey':
                 cmds.setAttr(file+'.colorSpace',self.otherFileNodeWgt.currentText(),type='string')
    
def main():
    if sys.executable.endswith('maya.exe'):
        pass
    else:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    global win
    win=UI()
    win.show()
    if not sys.executable.endswith('maya.exe'):
        sys.exit(app.exec_())
        
print (__name__) 
if __name__=='SetColorSpace' or __name__=='__main__':
    try:
        if __file__.replace('/','\\')==r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\Rig\SetColorSpace.py':
            print (u'复制文件')
            import shutil
            targetPath=u"A:\\TD\\常用工具\\Maya脚本小工具\\SetColorSpace.py"
            shutil.copy2("D:\\TD_Depot\\plug_in\\Lugwit_plug\\mayaPlug\\l_scripts\\Rig\\SetColorSpace.py", targetPath)
    except:
        pass
    main()

'''
#cmds.select ('yzyd_ep01_sc010_sh0200_xzz36_c002001xzz_h_rg36_warp')
#cmds.select (' c002001xzz_h_rg36:Group',add=1)
# 先选择abc大组,再选择引用文件的大组
import os
pyFilePath=r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\Rig\SetColorSpace.py'
moduleName=os.path.basename(pyFilePath).split('.')[0]
moduleDir=os.path.dirname(pyFilePath)
sys.path.append(moduleDir)
if moduleName in sys.modules:
    del sys.modules[moduleName]
    exec('import {}'.format(moduleName))
else:
    exec('import {}'.format(moduleName))
'''