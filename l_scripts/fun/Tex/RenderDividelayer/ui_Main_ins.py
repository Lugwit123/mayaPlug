# -*- coding: utf8


import sys,os,re,math
curDir=os.path.dirname(__file__)
sys.path.append(curDir)
import ui_Main
os.environ['QT_API']='PySide2'
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools



import sys
import glob
import codecs
from Lugwit_Module import *

from Lugwit_Module.l_src.UILib.QTLib import styleSheet
if sys.version_info[0]==3:
    from importlib import reload
reload (styleSheet)

import glob

if isMayaEnv():
    try:
        import mtoa.aovs as aovs
    except:
        lprint (u'arnold 未加载')
    
fileDir=os.path.dirname(__file__)

# 获取配置文件

jsonFileDir=fileDir+'/Config'

jsonFileList=glob.glob(jsonFileDir+'/*.json')

with codecs.open(jsonFileList[0], 'r', 'utf-8') as f:
    f_read=f.read()
    configDict=eval(f_read)

from Lugwit_Module.l_src.UILib.QTLib import PySideLib


pyFile= fileDir+r'\ui_Main.py'

# import mtoa.aovs as aovs;print  (aovs.getBuiltinAOVs())
aovList=\
['P', 'Z', 'N', 'opacity', 'motionvector', 'Pref', 'raycount', 'cputime', 'ID', 'RGBA', 'direct', 'indirect', 'emission', 'background', 'diffuse', 'specular', 'transmission', 'sss', 'volume', 'albedo', 'diffuse_direct', 'diffuse_indirect', 'diffuse_albedo', 'specular_direct', 'specular_indirect', 'specular_albedo', 'coat', 'coat_direct', 'coat_indirect', 'coat_albedo', 'sheen', 'sheen_direct', 'sheen_indirect', 'sheen_albedo', 'transmission_direct', 'transmission_indirect', 'transmission_albedo', 'sss_direct', 'sss_indirect', 'sss_albedo', 'volume_direct', 'volume_indirect', 'volume_albedo', 'volume_opacity', 'volume_Z', 'shadow_matte', 'AA_inv_density','AO']

usualAovList=\
['AO','N','RGBA','Z','crypto_asset','crypto_material','crypto_objecy',
'diffuse','direct','emission','indirect','specular','tranmission']
charAovList=['Pref','sss']
SetAovList=['P']
PropAovList=[]

    
    
    
aovList=sorted(aovList, key=lambda x: x.lower())

def addAovs(aovList):
    if aov in aovNodeNameList:
        aovs.AOVInterface().addAOV(aov,)
        
def getAllAOVs():
    # 获取所有的AOV
    aov_interface = aovs.AOVInterface()
    all_aovs = aov_interface.getAOVs()
        
def load_ui(ui_file):
    u"""加载UI文件"""
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(ui_file)
    ui_file.open(QtCore.QFile.ReadOnly)
    ui = loader.load(ui_file)
    ui_file.close()
    return ui
        
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__( QApplication.activeWindow())
        # 加载Qt Designer生成的UI文件
        ui_file =fileDir+'/main.ui'
        self.ui = load_ui(ui_file)
        self.setCentralWidget(self.ui)
        
        self.yuSeLPathSelFunc()
        self.aovListFunc()
        #self.setLayout(self.ui.topLay)
        self.ui.setStyleSheet(styleSheet.self_qss)
        self.setWindowTitle(u'渲染层AOV工具')
        self.connectCommandFunc()
        self.setMinimumSize(739, 900)
        self.setMaximumSize(739, 900)
        # 在此处添加您的其他代码
        
    def connectCommandFunc(self):
        func=lambda:self.addAovsFunc()
        self.ui.buildAovBtn.clicked.connect(func)
        self.ui.BuildRenderLayBtn.clicked.connect(self.buildRenderLayer)
        self.ui.CreateTerRefObjBtn.clicked.connect(self.CreateTextureReferenceObject)
        self.ui.LightDirBtn.clicked.connect(self.openStardardLightDir)
        self.ui.switchModeBtn.clicked.connect(self.switchMode)
        
    def CreateTextureReferenceObject(self):
        cmds.CreateTextureReferenceObject()
        
    def yuSeLPathSelFunc(self):
        self.yuSeLPathSelWgt=PySideLib.LPathSel(par=self.ui.topLay,l_lab=u'',DialogCommit=u'预设文件',fileType="*.json",buttonName=u'另存为',chooseFunc=u'getSaveFileName',defaultPath=jsonFileList[0])
        self.ui.yuSeLPathSel_lay.replaceWidget(self.ui.yuSeLPathSel, self.yuSeLPathSelWgt)
        # 删除 QLabel
        self.ui.yuSeLPathSel.deleteLater()
        
    def aovListFunc(self):
        #self.ui.usualAovList_GB.setMinimumHeight(300)
        aovListAppendSpace=aovList+['']
        while self.ui.usualAovList_GL_1.count():
            child = self.ui.usualAovList_GL_1.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for index,item in enumerate(aovListAppendSpace):
            row=int(index/6)
            colunm=index%6
            if item:
                checkBox=QCheckBox(item)
                checkBox.setMinimumHeight(20)
                self.ui.usualAovList_GL_1.addWidget(checkBox,row,colunm)
                if item in usualAovList:
                    checkBox.setChecked(True)
        #self.ui.usualAovList_GB_1.setMinimumHeight(80)
        
        # 角色
        while self.ui.usualAovList_GL_2.count():
            child = self.ui.usualAovList_GL_2.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        for index,item in enumerate(range(5)):
            ComboBox=QComboBox()
            ComboBox.addItems(aovListAppendSpace)
            self.ui.usualAovList_GL_2.addWidget(ComboBox)
            try:
                lprint (charAovList[index])
                ComboBox.setCurrentText(charAovList[index])
            except Exception as e:
                ComboBox.setCurrentText('')
                lprint (index,e)

        # 道具
        while self.ui.usualAovList_GL_3.count():
            child = self.ui.usualAovList_GL_3.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for index,item in enumerate(range(5)):
            ComboBox=QComboBox()
            ComboBox.addItems(aovList+[''])
            self.ui.usualAovList_GL_3.addWidget(ComboBox)
            try:
                lprint (PropAovList[index])
                ComboBox.setCurrentText(PropAovList[index])
            except Exception as e:
                ComboBox.setCurrentText('')
                lprint (index,e)
            
        while self.ui.usualAovList_GL_4.count():
            child = self.ui.usualAovList_GL_4.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for index,item in enumerate(range(5)):
            ComboBox=QComboBox()
            ComboBox.addItems(aovList+[''])
            self.ui.usualAovList_GL_4.addWidget(ComboBox)
            try:
                lprint (SetAovList[index])
                ComboBox.setCurrentText(SetAovList[index])
            except Exception as e:
                ComboBox.setCurrentText('')
                lprint (index,e)
                
    def addAovsFunc(self):
        # 已经存在的AOV
        existAllAOVs=getAllAOVs()
        existNameList=[]
        if existAllAOVs:
            existNameList=[x.name for x in existAllAOVs ]
        all_children = self.ui.usualAovList_GB.findChildren(QWidget)
        AOVNameList=[]
        for child in all_children:
            if isinstance(child,QCheckBox):
                if child.isChecked():
                    label=child.text()
                    if label in existNameList:
                        continue
                    AOVNameList.append(label)
                    if label !='AO':
                        aovs.AOVInterface().addAOV(label)
 
                    
            elif isinstance(child,QComboBox):
                label=child.currentText()
                if label:
                    AOVNameList.append(label)
                    if label !='AO':
                        aovs.AOVInterface().addAOV(label)

        #设置N通道的过滤模式为gaussian
        # 获取所有的AOV
        aov_interface = aovs.AOVInterface()
        all_aovs = aov_interface.getAOVs()

        # 打印所有的AOV名称
        for aov in all_aovs:
            aov_name=aov.name
            aov_node=aov.node
            if aov_name=='N':
                filterNode_Old=cmds.listConnections(aov_node+'.outputs[0].filter')[0]
                cmds.disconnectAttr(filterNode_Old+'.message',aov_node+'.outputs[0].filter')
                filterNode_New=cmds.createNode('aiAOVFilter')
                cmds.setAttr(filterNode_New+'.aiTranslator','gaussian',type='string')
                cmds.connectAttr(filterNode_New+'.message',aov_node+'.outputs[0].filter',f=1)
        
        
        if 'AO' in AOVNameList:
            if 'AO' in existNameList:
                return 
            self.createAOAov()
                    
    def createAOAov(self,aovNode=''):
        SceneAOV=aovs.AOVInterface().addAOV('AO')
        aovNode=SceneAOV.node

        aiOCCNode=cmds.createNode('aiAmbientOcclusion')
        cmds.setAttr('{}.samples'.format(aiOCCNode),4)
        cmds.select(aovNode)
        cmds.connectAttr(aiOCCNode+'.outColor','{}.defaultValue'.format(aovNode))

        # 创建shading group节点
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
        cmds.connectAttr(aiOCCNode + '.outColor', shading_group + '.surfaceShader')
    
    def openStardardLightDir(self):
        os.startfile(self.ui.LightDirLineEdit.text())
    
    def buildRenderLayer(self):
        selObj=cmds.ls(sl=True)
        AssetType_RadioButton=self.ui.AssetType_BtnGrp.checkedButton()
        CharDir=self.ui.CharDirMarkWgt.text()
        PropDir=self.ui.PropDirMarkWgt.text()
        SetDir=self.ui.SetDirMarkWgt.text()
        DirMarkWgtList=[self.ui.CharDirMarkWgt,self.ui.PropDirMarkWgt,self.ui.SetDirMarkWgt]
        
        CharRenderLayerName=self.ui.CharRenderLayerNameWgt.text()
        PropRenderLayerName=self.ui.PropRenderLayerNameWgt.text()
        SetRenderLayerName=self.ui.SetRenderLayerNameWgt.text()
        AssetTypeDirDict={u'角色':CharDir,u'道具':PropDir,u'场景':SetDir}
        
        AssetTypeRenderLayerNameDict={u'角色':CharRenderLayerName,
                                      u'道具':PropRenderLayerName,
                                      u'场景':SetRenderLayerName}
        AssetType=''
        for node in selObj:
            try:
                reference_file = cmds.referenceQuery(node, filename=True)
            except:
                reference_file = node
                
            print(u"{} 的引用文件为：{}".format(node, reference_file))
            AssetType_RadioButton_toolTip=AssetType_RadioButton.toolTip()
            AssetType_RadioButton_Text=AssetType_RadioButton.text()
            lprint (AssetType_RadioButton_Text)
            if AssetType_RadioButton_Text==u'自动':
                for asset_dirmark_wgt in DirMarkWgtList:
                    asset_dirmark=asset_dirmark_wgt.text()
                    if reference_file:
                        RegText=asset_dirmark.replace(',','/|/')
                        RegText='/'+RegText+'/'
                    else:
                        RegText=asset_dirmark.replace(',','|')
                    lprint (RegText)
                    RegResult=re.search(RegText,reference_file,flags=re.I)
                    if RegResult:
                        AssetType=asset_dirmark_wgt.toolTip()
                        break
            else:
                AssetType=AssetType_RadioButton.text()

        if not AssetType:
            global electAssetTypeUI_ins
            SelectAssetTypeUI_ins=SelectAssetTypeUI(self)
            SelectAssetTypeUI_ins.show()
            lprint (SelectAssetTypeUI_ins)
            SelectAssetTypeUI_ins.exec_()
            SelectAssetTypeUI_ins.close()
            AssetType=self.assetType
        
        lprint (AssetType)
        renderLayName=AssetTypeRenderLayerNameDict[AssetType]
        
        polygons=cmds.filterExpand(selObj,sm=12)
        
        cmds.createRenderLayer(polygons,name=renderLayName,noRecurse=False,makeCurrent=True)
        
        self.specialSetCode(AssetType)
        
            
    def specialSetCode(self,assetType=''):
        # 通用设置代码,设置N通道的过滤模式为gaussian
        usualSetingCode=self.ui.usualSeting_Wgt.toPlainText()
        if usualSetingCode:
            exec (usualSetingCode)
            
        # 角色设置代码 # 角色关掉灯光组,关掉AOV[P]
        CharSetingCode=self.ui.CharSeting_Wgt.toPlainText()
        if CharSetingCode and assetType ==u'角色':
            exec (CharSetingCode)
            
        # 道具设置代码
        PropSetingCode=self.ui.PropSeting_Wgt.toPlainText()
        if PropSetingCode and assetType ==u'道具':
            exec (PropSetingCode)
            
        # 场景设置代码 # 关掉AOV [sss,Pref]
        SetSetingCode=self.ui.SetSeting_Wgt.toPlainText()
        if SetSetingCode and assetType ==u'场景':
            exec (SetSetingCode)
            
    def switchMode(self):
        usualAovList_GB_visible=self.ui.usualAovList_GB.isVisible()
        self.ui.usualAovList_GB.setVisible(not usualAovList_GB_visible)
        self.ui.SpeciSetGB.setVisible(not self.ui.SpeciSetGB.isVisible())
        if usualAovList_GB_visible:
            self.setMinimumSize(100, 100)
            self.setMaximumSize(739, 400)
        else:
            self.setMinimumSize(739, 900)
        
        
        self.adjustSize()
        print (self.sizeHint())
        #self.setMaxmumSize(self.sizeHint())
        #Qself.setMaxnummSize(200)
        
class SelectAssetTypeUI(QDialog):
    def __init__(self,parent=None):
        super(SelectAssetTypeUI,self).__init__(parent)
        self.setWindowTitle(u'没有找到对应的类型,请手动确定')
        self.setMinimumSize(300, 100)
        # 创建三个QRadioButton，并设置其文本
        self.parent=parent
        self.role_radio = QRadioButton(u"角色")
        self.role_radio.setChecked(True)
        self.prop_radio = QRadioButton(u"道具")
        self.scene_radio = QRadioButton(u"场景")

        # 创建一个QButtonGroup，并将三个QRadioButton添加到该组中
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.role_radio)
        self.button_group.addButton(self.prop_radio)
        self.button_group.addButton(self.scene_radio)

        # 创建一个QVBoxLayout，并将三个QRadioButton添加到该布局中
        layout = QHBoxLayout()
        layout.addWidget(self.role_radio)
        layout.addWidget(self.prop_radio)
        layout.addWidget(self.scene_radio)

        # 创建一个“确定”按钮，并将其点击事件与get_selection()方法绑定
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.get_selection)

        # 将布局和按钮添加到主窗口中
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.ok_button)

    def get_selection(self):
        # 获取选中的QRadioButton
        if self.role_radio.isChecked():
            selection = u"角色"
        elif self.prop_radio.isChecked():
            selection = u"道具"
        elif self.scene_radio.isChecked():
            selection = u"场景"
        else:
            selection = "Unknown"
        print("Selected item:", selection)
        self.parent.assetType=selection
        self.close()
    
print (__name__ == '__main__' or __name__ == 'ui_Main_ins' )

def show_Main(*args):
    if isMayaEnv():
        pass
    else:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    global win
    win=Main()
    win.show()
    if not isMayaEnv():
        sys.exit(app.exec_())
    
if __name__ == '__main__' or __name__ == 'ui_Main_ins':
    if isMayaEnv():
        pass
    else:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    global win
    win=Main()
    win.show()
    
    if not isMayaEnv():
        sys.exit(app.exec_())
        
r'''
import os
pyFilePath=r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\fun\Tex\RenderDividelayer\ui_Main_ins.py'
moduleName=os.path.basename(pyFilePath).split('.')[0]
moduleDir=os.path.dirname(pyFilePath)
sys.path.append(moduleDir)
if moduleName in sys.modules:
    del sys.modules[moduleName]
    exec('import {}'.format(moduleName))
else:
    exec('import {}'.format(moduleName))
'''