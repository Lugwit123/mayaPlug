# coding:utf-8
import os
try:
    from PySide2.QtCore import * 
    from PySide2.QtGui import * 
    from PySide2.QtWidgets import *
    from PySide2 import __version__
except:
    try:
        from PySide.QtWidgets import *
    except:
        class QWidget:
            pass
        pass
import sys,re
from functools import partial
executable=sys.executable
print ('executable',executable)

HorizontalHeaderLabels=[u'是否加载',u'是否替换',u'是否高模',u'参考节点',u'文件路径']
try:
    import maya.cmds as cmds
except:
    pass

def getrefInfoDict():
    import re
    def findRefDict():
        rfNodeList=cmds.ls(type='reference')
        cmds.select(rfNodeList)
        rfNodeDict={'chr':[],'porp':[],'set':[]}
        for rfNode in rfNodeList:
            try:
                refFile=cmds.referenceQuery( rfNode, f=True )
                refFileisLoad=cmds.referenceQuery( rfNode,il=1)
                isHigMod='LowMod' not in refFile
            except Exception as e:
                print (e)
                continue

            for key,val in rfNodeDict.items():
                if re.search('/'+key+'/',refFile,flags=re.I):
                    rfNodeDict[key].append((rfNode,refFile,refFileisLoad,isHigMod))
        with open (os.environ['Temp']+'/aa.txt','w') as f:
            f.write(  str(rfNodeDict)  )
        return rfNodeDict
    print (findRefDict())
    

    
def replaceModel(toggleToMod=['/LowMod','/Texture'],rfNodeList=[]):
    print ('toggleToMod:',toggleToMod)
    processRefNodeList=[]
    processRefFileList=[]
    HigFile=[]
    for rfNode in rfNodeList:
        try:
            refFile=cmds.referenceQuery( rfNode, f=True )
        except Exception as e:
            continue
            print (e)
        fileDir,fileName=os.path.split(refFile)
        print ('toggleToMod[0],refFile,toggleToMod[0] in refFile',toggleToMod[0],refFile,toggleToMod[0] in refFile)
        if toggleToMod[0] in refFile:
            
            HigFileDir=fileDir.replace(toggleToMod[0],toggleToMod[1])
            if os.path.exists(HigFileDir) :
                for file in os.listdir(HigFileDir):
                    if file.endswith('.ma'):
                        HigFile=HigFileDir+'/'+file
                        try:
                            cmds.file(HigFile, loadReference=rfNode,
                                    type="mayaAscii", options="v=0",f=1,iv=1)
                        except Exception as e:
                            print (e)
                        processRefNodeList.append(rfNode)
                        processRefFileList.append(HigFile)
    cmds.select(processRefNodeList)
    return processRefFileList
    print (processRefNodeList,processRefFileList)


    
    
class UI(QWidget):
    def __init__(self, parent = None):
        super(UI, self).__init__( parent)
        self.setWindowFlags(Qt.Window) 
        self.resize(1300, 800)
        self.setWindowTitle(u'替换高低模')
        
        if re.search('maya.*.exe',executable):
            getrefInfoDict()
        
        with open (os.environ['Temp']+'/aa.txt','r') as f:
            RefDict=eval(f.read())
            print (RefDict)
            
        self.layout = QVBoxLayout()
        self.allRefList=RefDict['chr']+RefDict['porp']+RefDict['set']
        self.layout.addWidget(self.table())
        self.layout.addLayout(self.btnLay())
        self.setLayout(self.layout)
        self.setStyleSheet('''
                        QPushButton {
                            color: #1de9b6;
                            background-color: #31363b;
                            border: 2px solid #1de9b6;
                            border-radius: 4px;
                            height: 32px;}

                        QCheckBox,
                        QGroupBox {
                                    color: #1de9b6;}
                        QCheckBox::indicator:checked,
                        QGroupBox::indicator:checked, {
                                        color: #ffff00;
                                        border: 3px  solid #d80707;
                                        margin : 10;
                                        border-top-left-radius: 4px;}
                            ''')
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint |   # 使能最小化按钮
                            Qt.WindowType.WindowCloseButtonHint |      # 使能关闭按钮
                            Qt.WindowType.WindowStaysOnTopHint)
        
    def table(self):
        
        self.tableWidget = QTableWidget(len(self.allRefList),len(HorizontalHeaderLabels))
        self.tableWidget.setHorizontalHeaderLabels(HorizontalHeaderLabels)
        self.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.ContextMenuFunc)
        #self.tableWidget.setVerticalHeaderLabels(aovList)
        chr_porp_setList=[]
        for i,(RefNode,RefFile,refFileisLoad,isHigMod) in enumerate(self.allRefList):
            chr_porp_set=re.search('/chr/|/porp/|/set/', RefFile,flags=re.I)
            print (chr_porp_set, RefFile)
            chr_porp_setList.append(chr_porp_set.group().replace('/',''))
            for j,label in enumerate(HorizontalHeaderLabels):
                if j<3 :
                    widget=QCheckBox()
                    #widget.setFixedWidth(20)
                    self.tableWidget.horizontalHeader().resizeSection(j, 60)
                    self.tableWidget.setCellWidget(i, j,widget)
                    
                    widget.setStyleSheet('''
                                        color: #d80707;
                                        line-height: 14px;
                                        height: 36px;
                                        padding-left: 15px;
                                        spacing: 12px;
                                        background-color: #646f7b;
                                        ''')
                    if j==0:
                        widget.setChecked(refFileisLoad)
                        widget.setAttribute(Qt.WA_TransparentForMouseEvents)
                        widget.setFocusPolicy(Qt.NoFocus)
                        widget.setStyleSheet('color: #833912;')
                        
                    elif j==2:
                        widget.setChecked(isHigMod)
                        widget.setAttribute(Qt.WA_TransparentForMouseEvents)
                        widget.setFocusPolicy(Qt.NoFocus)
                        widget.setStyleSheet('color: #833912;')
                    widget.setGeometry(150, 120, 30, 40)
                if j==3:
                    widgetItem=QTableWidgetItem(RefNode)
                    self.tableWidget.setItem(i, j, widgetItem)
                    self.tableWidget.horizontalHeader().resizeSection(j, 220)
                if j==4:
                    widgetItem=QTableWidgetItem(RefFile)
                    self.tableWidget.setItem(i, j, widgetItem)
                    self.tableWidget.horizontalHeader().resizeSection(j, 750)
                    widgetItem.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled )
                widget.setGeometry(150, 120, 30, 40)
        self.tableWidget.setVerticalHeaderLabels(chr_porp_setList)
        return self.tableWidget
    
    def btnLay(self):
        btnLay=QHBoxLayout()
        chrCheckBox=QCheckBox('chr');btnLay.addWidget(chrCheckBox)
        chrCheckBox.clicked.connect(lambda *args:self.chr_porp_setCkb_ChangeFucn(chrCheckBox))
        porpCheckBox=QCheckBox('porp');btnLay.addWidget(porpCheckBox)
        porpCheckBox.clicked.connect(lambda *args:self.chr_porp_setCkb_ChangeFucn(porpCheckBox))
        setCheckBox=QCheckBox('set');btnLay.addWidget(setCheckBox)
        setCheckBox.clicked.connect(lambda *args:self.chr_porp_setCkb_ChangeFucn(setCheckBox))
        self.ignoreUnLoadFileCheckBox=QCheckBox(u'忽略未加载文件')
        btnLay.addWidget(self.ignoreUnLoadFileCheckBox)
        
        replacetoHigMod=QPushButton(u'替换为高模')
        replacetoHigMod.setFixedWidth(200)
        replacetoHigMod.clicked.connect(lambda *args:self.replaceHigRig(toggleToMod=['/LowMod','/Texture']))
        replacetoLowMod=QPushButton(u'替换为低模')
        replacetoLowMod.setFixedWidth(200)
        replacetoLowMod.clicked.connect(lambda *args:self.replaceHigRig(toggleToMod=['/Texture','/LowMod']))
        btnLay.addWidget(self.ignoreUnLoadFileCheckBox)
        btnLay.addWidget(replacetoHigMod)
        btnLay.addWidget(replacetoLowMod)
        btnLay.addStretch(5)
        return btnLay
    
    def ContextMenuFunc(self,pos):
        columnNum=-1
        for i in self.tableWidget.selectionModel().selection().indexes():
            columnNum=i.column()
        selectedItem=self.tableWidget.selectedItems()
        if columnNum==4:
            menu=QMenu()
            menu1_Action=menu.addAction(u'复制路径')
            path=selectedItem[0].text()
            import pyperclip
            menu1_Action.triggered.connect(
                        lambda *args:(pyperclip.copy(path)))
            screenPos = self.tableWidget.mapToGlobal(pos)
            action = menu.exec_(screenPos)

            
    def chr_porp_setCkb_ChangeFucn(self,checkBox):
        CheckBoxName=checkBox.text()
        val=checkBox.isChecked()
        for i,(RefNode,RefFile,refFileisLoad,isHigMod) in enumerate(self.allRefList):
            chr_porp_set=re.search('/chr/|/porp/|/set/', RefFile,flags=re.I)
            chr_porp_set=chr_porp_set.group().replace('/','')
            for j,label in enumerate(HorizontalHeaderLabels):
                if chr_porp_set.lower()==CheckBoxName.lower():
                    if j==1:
                        self.tableWidget.cellWidget(i, j).setChecked(val)
                        
    def replaceHigRig(self,toggleToMod=['/LowMod','/Texture']):
        for i,(RefNode,RefFile,refFileisLoad,isHigMod) in enumerate(self.allRefList):
            for j,label in enumerate(HorizontalHeaderLabels):
                if j==1:
                    if self.ignoreUnLoadFileCheckBox.isChecked():
                        if not self.tableWidget.cellWidget(i, 0).isChecked():
                            continue
                    isReplace=self.tableWidget.cellWidget(i, j).isChecked()
                    if isReplace:
                        rfNode=self.tableWidget.item(i, 3).text()
                        processRefFileList=replaceModel(toggleToMod,rfNodeList=[rfNode])
                        print ('processRefNodeList:',processRefFileList)
                        if processRefFileList:
                            rfNode=self.tableWidget.item(i, 4).setText(processRefFileList[0])
                            self.tableWidget.cellWidget(i, 2).setChecked(toggleToMod==['/LowMod','/Texture'])
        
        
global win
def main(*args):
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
    win.show()
    if not re.search('maya.*.exe',executable):
        sys.exit(app.exec_())
        
if __name__=='__main__':
    main()