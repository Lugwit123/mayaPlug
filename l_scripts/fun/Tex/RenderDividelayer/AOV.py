# -*- coding: utf8
try:
    from PySide2.QtCore import * 
    from PySide2.QtGui import * 
    from PySide2.QtWidgets import *
    from PySide2 import __version__
except:
    from PySide.QtWidgets import *
import sys,re
import maya.cmds as cmds
from functools import partial
from imp import reload
aovList=['col','dsk','id','msk','shw']
aovListALias=['_C_|_col','_dis|_dsk','_id','_m|_ramp','_shw']
sgs=cmds.ls(type='shadingEngine')
#sgs=['g37ssrydcg_c001001yd_JS_SG']
import mtoa.aovs as aovs
aovNodeList=aovs.AOVInterface().getAOVNodes(names=True)
aovNodeNameList=[x[0] for x in aovNodeList]
print (aovNodeList)
for i,aov in enumerate(aovList):
    if aov in aovNodeNameList:
        continue
    aovs.AOVInterface().addAOV(aov,)
    
def getMainWindowPtr(): 
    mayaMainWindowPtr = maya.OpenMayaUI.MQtUtil.mainWindow() 
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget) 
    return mayaMainWindow 

class UI(QWidget):
    def __init__(self, parent = None):
        super(UI, self).__init__( parent)
        self.setWindowFlags(Qt.Window) 
        self.resize(1000, 300)
        self.setWindowTitle(u'链接AOV')
        self.layout = QVBoxLayout()
        qh,self.aovMatchWidgetList=self.aovNameList()
        self.tabs = QTabWidget()
        applyListSgsList=[]
        for sg in sgs:
            NodeList = cmds.listHistory(sg,pdo = True)
            fileNodeList=[];fileTextureNameList=[]
            for node in NodeList:
                if cmds.nodeType(node)=='file':
                    fileTextureName=cmds.getAttr(node+'.fileTextureName')
                    fileNodeList.append([node,fileTextureName])
                if cmds.nodeType(node)=='ramp':
                    fileNodeList.append([node,""])
            if fileNodeList :
                self.tabs.addTab(self.table(fileNodeList,sg), sg)
                applyListSgsList.append(sg)
        self.tabs.currentChanged.connect(partial(self.selectCurrenSG,applyListSgsList))
        self.layout.addWidget(self.tabs)
        self.layout.addLayout(qh)
        selSgBtn=QPushButton('选择当前sg')
        selSgBtn.clicked.connect(partial(self.selectCurrenSG,applyListSgsList))
        self.layout.addWidget(selSgBtn)
        self.setLayout(self.layout)
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint |   # 使能最小化按钮
                            Qt.WindowType.WindowCloseButtonHint |      # 使能关闭按钮
                            Qt.WindowType.WindowStaysOnTopHint)
    def table(self,fileNodeList,sg):
        aovDict={}
        for x in range(1000):
            attr=cmds.listAttr(sg+'.aiCustomAOVs[{}].aovName'.format(x))[0]
            if attr!='aiCustomAOVs[{}].aovName'.format(x):
                aovDict[attr.rsplit('_')[-1]]='aiCustomAOVs[{}]'.format(x)
            attr=cmds.aliasAttr(sg+'.aiCustomAOVs[{}]'.format(x),q=1)
            if attr!='aiCustomAOVs[{}].aovName'.format(x):
                aovDict[attr]='aiCustomAOVs[{}]'.format(x)
        tableWidget = QTableWidget(len(aovList),2)
        HeaderLabels=[u'节点命名',u'贴图路径']
        tableWidget.setHorizontalHeaderLabels(HeaderLabels)
        tableWidget.setVerticalHeaderLabels(aovList)
        for i in range(len(aovList)):
            for j in range(len(HeaderLabels)):
                if j==0:
                    widget=QComboBox()
                    tableWidget.horizontalHeader().resizeSection(j, 250)
                    tableWidget.setCellWidget(i, 0,widget)
                    widget.addItems([x[0] for x in fileNodeList]+[""])
                        
                elif j==1:
                    tableWidget.horizontalHeader().resizeSection(j, 670)
                    widgetItem= QTableWidgetItem()
                    tableWidget.setItem(i, j, widgetItem)
                    widget.currentTextChanged.connect(partial(self.QComboBoxChangeFunc,widgetItem,widget,i,sg,aovDict))
                    widget.setCurrentText("")
                    for fileNode,filePath in fileNodeList:
                        if re.search(self.aovMatchWidgetList[i].text(),filePath+fileNode,flags=re.I):
                            print (self.aovMatchWidgetList[i].text(),filePath)
                            print re.search(self.aovMatchWidgetList[i].text(),filePath+fileNode,flags=re.I)
                            if cmds.nodeType(fileNode)=='file':
                                widgetItem.setText(cmds.getAttr(fileNode+'.fileTextureName'))
                            widget.setCurrentText(fileNode)

        return tableWidget
    def QComboBoxChangeFunc(self,widgetItem,widget,i,sg,aovDict,*args):
        currentText=widget.currentText()
        print (currentText)
        if currentText:
            if cmds.nodeType(currentText)=='file':
                widgetItem.setText(cmds.getAttr(currentText+'.fileTextureName'))
            cmds.connectAttr(currentText+'.outColor',sg+'.'+aovDict[aovList[i]]+'.aovInput',f=1)
        else:
            try:
                attr=cmds.listConnections(sg+'.'+aovDict[aovList[i]]+'.aovInput',p=1)
                if attr:
                    cmds.disconnectAttr(attr[0],sg+'.'+aovDict[aovList[i]]+'.aovInput')
            except Exception as e:
                print (e)

    def aovNameList(self):
        qh=QHBoxLayout()
        aovMatchWidgetList=[]
        for i,aov in enumerate(aovList):
            aovLabel=QLabel(aov)
            aovName=QLineEdit(aovListALias[i])
            qh.addWidget(aovLabel)
            qh.addWidget(aovName)
            aovMatchWidgetList.append(aovName)
        return qh,aovMatchWidgetList
    
    def selectCurrenSG(self,applyListSgsList,*args):
        cmds.select(applyListSgsList[self.tabs.currentIndex()],ne=1)
        

executable=sys.executable
print ('executable',executable)
if re.search('maya.*.exe',executable):
    try:
        app = QApplication([])
    except:
        app = QApplication.instance()
else:
    print (u'独立运行')
    app = QApplication(sys.argv)
#有空试试setObjectName关闭存在UI
try:
    win.close()
except:
    pass
win = UI()
def winShow(*args):
    global win
    win.show()
winShow()
if not re.search('maya.*.exe',executable):
    sys.exit(app.exec_())
'''
import sys
sys.path.append(r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\mayaPlug\scripts')
try:
    reload(exABC)
except:
    import exABC
'''
