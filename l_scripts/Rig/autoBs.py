# -*- coding: utf8
import sys,os
from PySide2.QtWidgets import *
from PySide2 import QtCore
from PySide2.QtGui import QMovie
from PySide2.QtCore import *

instructions=u'''
**使用说明**
1. 手动创建BS:如果有不能自动创建BS的物体,可以使用插件手动创建
2. 检查失败的物体:如果有部分模型没有创建BS,插件提供检查哪些物体没有创建BS的功能
3. 删除BS:如果你要删除BS历史,插件提了此功能
'''
        
class L_ProgressDialog(QProgressDialog):
    def __init__(self,title=u'生成BS',processList=[]):
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

def isMatch(BsObj,BsTarget,FaceNum_BsObj,edgeToFaceMatchList_BsObj,vertexNum_BsObj,YanGeSample,area_BsObj,IsYange,sameObj):
    
    import maya.cmds as cmds
    edgeToFaceMatchList_BsTarget=[]
    
    for YanGeSample_index in range(YanGeSample):
        topoInfo=sorted(str(cmds.polyInfo(BsTarget+'.vtx[{}]'.format(YanGeSample_index),vertexToFace=1)[0]).split(' '))
        edgeToFaceMatchList_BsTarget.append(topoInfo)

    FaceNum_BsTarget=cmds.polyEvaluate(BsTarget,face=1)

    vertexNum_BsTarget=cmds.polyEvaluate(BsTarget,vertex=1)

    area_BsTarget=cmds.polyEvaluate(BsTarget,area=1)


    if FaceNum_BsObj==FaceNum_BsTarget and vertexNum_BsObj==vertexNum_BsTarget:
        if edgeToFaceMatchList_BsObj!=edgeToFaceMatchList_BsTarget and IsYange:
            print (edgeToFaceMatchList_BsObj,edgeToFaceMatchList_BsTarget,'拓扑不匹配')
            return

        xx=0.8 if sameObj else 0.9
        if abs(area_BsObj/area_BsTarget)<xx or abs(area_BsObj/area_BsTarget)>2-xx:
            print ('area_BsObj,area_BsTarget:',area_BsObj,area_BsTarget,area_BsObj/area_BsTarget)
            print (u'面积相差过大,跳过')
            return


        bsNode = cmds.blendShape(BsObj,before=1 )[0]
        cmds.blendShape(bsNode, edit=True, t=(
            BsObj, 0, BsTarget , 1), w=(0, 1))
        return True
                
def autoCreateBS(IsYange=True,YanGeSample=1):
    import maya.cmds as cmds
    sels=cmds.ls(sl=1)
    cmds.select(sels[0])
    cmds.SelectHierarchy()
    BsTargetList=cmds.ls(cmds.filterExpand(cmds.ls(sl=1),sm=12))
    BsTargetList=[x for x in BsTargetList if cmds.getAttr(x+'.visibility')]
    BsTargetList=list(set(BsTargetList))
    cmds.select(sels[1])
    cmds.SelectHierarchy()
    BsObjList=cmds.ls(cmds.filterExpand(cmds.ls(sl=1),sm=12))
    BsObjList=[x for x in BsObjList if cmds.getAttr(x+'.visibility')]
    BsObjList=list(set(BsObjList))
    cmds.select(cl=1)
    BsObjProcessedList=[]
    BsTargetProcessedList=[]
    amount=len(BsObjList)
    process=L_ProgressDialog(processList=[str(x) for x in range(amount)])
    YanGeSample=int(YanGeSample)
    Progress_index=0
    for BsObj in BsObjList:
        boundingBox_BsObj=cmds.polyEvaluate(BsObj,boundingBox=1)
        area_BsObj=cmds.polyEvaluate(BsObj,area=1)
        vertexNum_BsObj=cmds.polyEvaluate(BsObj,vertex=1)
        MidPoint_Pos_BsObj=cmds.polyEditUV(BsObj+'.map[{}]'.format(int(vertexNum_BsObj/2)),q=1)
        ZeroPoint_Pos_BsObj=cmds.polyEditUV(BsObj+'.map[0]',q=1)
        FaceNum_BsObj=cmds.polyEvaluate(BsObj,face=1)
        baseName_BsObj=BsObj.rsplit('|',1)[-1].rsplit(':',1)[-1]
        
        edgeToFaceMatchList_BsObj=[]
        for YanGeSample_index in range(YanGeSample):
            topoInfo=sorted(str(cmds.polyInfo(BsObj+'.vtx[{}]'.format(YanGeSample_index),vertexToFace=1)[0]).split(' '))
            edgeToFaceMatchList_BsObj.append(topoInfo)

        if process.ProgressDialog_Procecss(index=Progress_index)=='stop':
            return 
        Progress_index+=1
            
        for BsTarget in BsTargetList:

            Continue=0
            if BsObj in BsObjProcessedList:
                print (u'已经创建BS,跳过BsObj-{}'.format(BsObj))
                continue
            if not cmds.getAttr(BsTarget+'.visibility'):
                print (u'隐藏物体,跳过BsTarget-{}'.format(BsTarget))
                continue
            if BsTarget in BsTargetProcessedList:
                print (u'已经创建BS,跳过BsTarget-{}'.format(BsTarget))
                continue
            baseName_BsTarget=BsTarget.rsplit('|',1)[-1].rsplit(':',1)[-1]
            
            if baseName_BsObj==baseName_BsTarget:
                sameObj=1
                matchResult=isMatch(BsObj,BsTarget,FaceNum_BsObj,edgeToFaceMatchList_BsObj,vertexNum_BsObj,YanGeSample,area_BsObj,IsYange,sameObj)
                if matchResult :
                    BsObjProcessedList.append(BsObj)
                    BsTargetProcessedList.append(BsTarget)
                    
        for BsTarget in BsTargetList:

            Continue=0
            if BsObj in BsObjProcessedList:
                continue
            if not cmds.getAttr(BsTarget+'.visibility'):
                print (u'隐藏物体,跳过BsTarget-{}'.format(BsTarget))
                continue
            if BsTarget in BsTargetProcessedList:
                continue
            baseName_BsTarget=BsTarget.rsplit('|',1)[-1].rsplit(':',1)[-1]
            sameObj=0
            matchResult=isMatch(BsObj,BsTarget,FaceNum_BsObj,edgeToFaceMatchList_BsObj,vertexNum_BsObj,YanGeSample,area_BsObj,IsYange,sameObj)
            if matchResult :
                BsObjProcessedList.append(BsObj)
                BsTargetProcessedList.append(BsTarget)
                    
        


    cmds.select([BsObj])
    
def findSameObj():
    import maya.cmds as cmds
    sels=cmds.ls(sl=1)
    cmds.select(sels[0])
    cmds.SelectHierarchy()
    BsTargetList=cmds.ls(cmds.filterExpand(cmds.ls(sl=1),sm=12))
    BsTargetList=[x for x in BsTargetList if cmds.getAttr(x+'.visibility')]
    BsTargetList=list(set(BsTargetList))
    cmds.select(sels[1])
    cmds.SelectHierarchy()
    BsObjList=cmds.ls(cmds.filterExpand(cmds.ls(sl=1),sm=12))
    BsObjList=[x for x in BsObjList if cmds.getAttr(x+'.visibility')]
    BsObjList=list(set(BsObjList))
    cmds.select(cl=1)
    BsObjProcessedList=[]
    BsTargetProcessedList=[]
    amount=len(BsObjList*len(BsTargetList))
    process=L_ProgressDialog(processList=[str(x) for x in range(amount)])
    import copy
    noBsObjList=[]
    noBsTargetList=[]
    Progress_index=0
    for BsObj in BsObjList:
        vertexNum_BsObj=cmds.polyEvaluate(BsObj,vertex=1)
        FaceNum_BsObj=cmds.polyEvaluate(BsObj,face=1)
        for BsTarget in BsTargetList:
            if process.ProgressDialog_Procecss(index=Progress_index)=='stop':
                return 
            Progress_index+=1
            Continue=0
            if BsObj in BsObjProcessedList:
                continue
            if not cmds.getAttr(BsTarget+'.visibility'):
                print (u'隐藏物体,跳过BsTarget-{}'.format(BsTarget))
                continue
            if BsTarget in BsTargetProcessedList:
                continue
            FaceNum_BsTarget=cmds.polyEvaluate(BsTarget,face=1)
            
            vertexNum_BsTarget=cmds.polyEvaluate(BsTarget,vertex=1)

            
            if FaceNum_BsObj==FaceNum_BsTarget and vertexNum_BsObj==vertexNum_BsTarget:
                hisList=cmds.listHistory(BsObj)
                HasBs=0
                for his in hisList:
                    if not cmds.objExists(his):
                        continue
                    if cmds.nodeType(his)=='blendShape':
                        source=cmds.listConnections(his,d=0,type='mesh',sh=1)
                        source_source=cmds.listConnections(source,d=0,sh=1)
                        if source_source:
                            if cmds.nodeType(source_source[0])=='AlembicNode':
                                HasBs=1
                                break
                if HasBs==0:
                    noBsObjList.append(BsObj)
                    noBsTargetList.append(BsTarget)
                    


    cmds.select(noBsObjList+noBsTargetList)

def deleteBS(*args):
    import maya.cmds as cmds
    cmds.SelectHierarchy()
    PolyList=cmds.ls(cmds.filterExpand(cmds.ls(sl=1),sm=12))
    PolyList=[x for x in PolyList if cmds.getAttr(x+'.visibility')]
    PolyList=list(set(PolyList))
    for Poly in PolyList:
        hisList=cmds.listHistory(Poly)
        for his in hisList:
            if not cmds.objExists(his):
                continue
            if cmds.nodeType(his)=='blendShape':
                source=cmds.listConnections(his,d=0,type='mesh',sh=1)
                source_source=cmds.listConnections(source,d=0,sh=1)
                # if source_source:
                #     if cmds.nodeType(source_source[0])=='AlembicNode':
                #         print (u'从{}删除BS--{}'.format(Poly,his))
                #         cmds.delete(his)
                if ':' not in  his:
                    print (u'从{}删除BS--{}'.format(Poly,his))
                    cmds.delete(his)


def shouDongBS_Fucn(*args):
    import maya.cmds as cmds
    sels=cmds.ls(sl=1)
    cmds.blendShape(sels[1],before=1)[0]
    cmds.blendShape(bsNode, edit=True, t=(
        sels[1], 0, sels[0] , 1), w=(0, 1))
    
    for i in range(4,8):
        node='modelPanel{}ViewSelectedSet'.format(i)
        if cmds.objExists(node):
            cmds.sets(sels,rm=node)

class UI(QWidget):
    def __init__(self):
        super(UI,self).__init__()
        self.setFixedWidth(800)
        self.setWindowTitle(u'传递BS')
        self.resize(500, 200)
        self.topLay=QVBoxLayout(self)
        
        self.yange_ck=QCheckBox(u'拓扑匹配严格模式,匹配不上不勾选,匹配错乱就勾选这个')
        self.yange_ck.setChecked(True)
        
        yangeSampleLay=QHBoxLayout()
        yangeSampleLabelWgt=QLabel(u'拓扑匹配严格程度:数字越大,匹配越慢,也不容易匹配出错')
        self.yangeSampleLineEditWgt=QLineEdit('2')
        self.yangeSampleLineEditWgt.setReadOnly(1)
        self.yangeSampleSliderWgt=QSlider(Qt.Horizontal)
        self.yangeSampleSliderWgt.setMinimum(2) #设置最小值
        self.yangeSampleSliderWgt.setMaximum(10) #设置最大值
        yangeSampleLay.addWidget(yangeSampleLabelWgt)
        yangeSampleLay.addWidget(self.yangeSampleLineEditWgt)
        yangeSampleLay.addWidget(self.yangeSampleSliderWgt,20)
        self.yangeSampleSliderWgt.valueChanged.connect(
            lambda *args:self.yangeSampleLineEditWgt.setText(str(self.yangeSampleSliderWgt.value())))
        
        
        self.topLay.addWidget(self.yange_ck)
        self.topLay.addLayout(yangeSampleLay)
        
        MatchBS_Btn=QPushButton(u'先选择abc大组,再选择引用文件的大组,创建BS')
        
        shouDongBS_Btn=QPushButton(u'先选择ABC物体,再选择引用文件,手动创建BS')
        shouDongBS_Btn.clicked.connect(shouDongBS_Fucn)
        
        CheckBS_Btn=QPushButton(u'先选择abc大组,再选择引用文件的大组,选择从ABC文件找到了相同拓扑的模型,但是没有匹配上的模型')
        CheckBS_Btn.clicked.connect(findSameObj)
        
        ClearBS_Btn=QPushButton(u'选择资产文件,删除变形目标为ABC文件的BS')
        
        ClearBS_Btn.clicked.connect(deleteBS)
        MatchBS_Btn.clicked.connect(
            lambda *args:autoCreateBS(  IsYange=self.yange_ck.isChecked(),
                                        YanGeSample=self.yangeSampleSliderWgt.value(),
                                        
                                        ))
        
        self.topLay.addWidget(MatchBS_Btn)
        self.topLay.addWidget(shouDongBS_Btn)
        self.topLay.addWidget(CheckBS_Btn)
        self.topLay.addWidget(ClearBS_Btn)
        
        instructionsWgt=QLabel(instructions)


        self.topLay.addWidget(instructionsWgt)
        
        
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint |   # 使能最小化按钮
                        Qt.WindowType.WindowCloseButtonHint |      # 使能关闭按钮
                        Qt.WindowType.WindowStaysOnTopHint)
        
def main(*args):
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
if __name__=='autoBs' or __name__=='__main__':
    main()

'''
#cmds.select ('yzyd_ep01_sc010_sh0200_xzz36_c002001xzz_h_rg36_warp')
#cmds.select (' c002001xzz_h_rg36:Group',add=1)
# 先选择abc大组,再选择引用文件的大组
import os
pyFilePath=r'D:\plug_in\Lugwit_plug\mayaPlug\l_scripts\Rig\autoBs.py'
moduleName=os.path.basename(pyFilePath).split('.')[0]
moduleDir=os.path.dirname(pyFilePath)
sys.path.append(moduleDir)
if moduleName in sys.modules:
    del sys.modules[moduleName]
    exec('import {}'.format(moduleName))
else:
    exec('import {}'.format(moduleName))
'''