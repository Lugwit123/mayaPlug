# -*- coding: utf-8 -*-
import codecs
import json
import sys,os,re
from functools import partial

from l_scripts import L_GV

os.environ['QT_API'] = 'PySide2'

LugwitToolDir=os.environ.get('LugwitToolDir')
sys.path.append(LugwitToolDir+'/Lib')
print("LugwitToolDir",LugwitToolDir)
from LQtLib import L_showQtWin,L_QtToolLib
from IOLib import exFbx
qttool=L_QtToolLib
reload(qttool)
reload(L_showQtWin)
reload(exFbx)
reload(L_GV)

import Lugwit_Module as LM
lprint=LM.lprint
lprint.max_prints_per_line = 100
if LM.isMayaEnv():
    import maya.cmds as cmds
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin



from PySide2.QtWidgets import (QApplication, QMainWindow,QPushButton,QLabel,
                               QGridLayout,QComboBox,QLineEdit,QPushButton)
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
if "ui_helper" in sys.modules:
    del sys.modules['ui_helper']
import ui_helper
reload(ui_helper)
import data_center
reload(data_center)
            
            
            

class MainWindow(MayaQWidgetDockableMixin,QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # 删除已存在的UI界面
        if LM.isMayaEnv():
            try:
                cmds.deleteUI("BatchExAbcWorkspaceControl")
            except RuntimeError:
                pass
        
        self.nameSplaceInfoDictFromJSonFile = {}
        self.qttool = qttool  # 将qttool作为实例属性，供helper使用
        self.load_ui()
        self.connectSigals()
        
        # 创建数据中心和UI助手作为成员变量 (单例模式)
        self.data_center = data_center.DataCenter(self)
        self.ui_helper = ui_helper.MainWindowHelper(self)
        
        # 将UI助手注册到数据中心
        self.data_center.ui_helper = self.ui_helper
        self.ui_helper.data_center = self.data_center
        self.ui_helper.register_to_data_center(self.data_center)

        # 初始化UI填充（无JSON数据的基础填充）
        self.ui_helper.initial_ui_fill()
        
        # 数据中心主导数据初始化
        self.data_center.initialize_data()
        
        self.setWindowTitle('选择的组如果没有名称空间，请手动输入(不会导出隐藏物体和中间对象物体'+
                            'Maya文件存储为项目名_集_场_镜会自动识别项目名_集_场_镜)')
        self.setMinimumWidth(1100)
        
        # 设置对象名称，这将影响WorkspaceControl的命名
        self.setObjectName("BatchExAbc")
    


    def load_ui(self):
        loader = QUiLoader()
        ui_file = QFile(LM.Lugwit_mayaPluginPath+r"\l_scripts\IOLib\BatchExAbc\exAbc.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)  # 加载 .ui 文件
        ui_file.close()
        self.ui.projectCombo.clear()
        self.ui.projectCombo.addItems(["BLDTD","TBZZXKX"])
    

        

    def connectSigals(self):
        self.ui.refreshBtn.clicked.connect(self.refresh)
        self.ui.exAbc_btn.clicked.connect(self.exAbc)
        self.ui.openActualDirWgt.clicked.connect(lambda: self.ui_helper.file_operation_helper.open_actual_directory())
        self.ui.brower_preset_path_wgt.clicked.connect(lambda: self.ui_helper.file_operation_helper.browse_json_file())
        self.ui.open_preset_path_btn.clicked.connect(lambda: self.ui_helper.file_operation_helper.open_preset_directory())
        # self.ui.jsonPreset_Combo.currentTextChanged.connect(self.onJsonPresetChanged)
        self.ui.guess_shot_wgt.clicked.connect(lambda: self.ui_helper.auto_fill_helper.guess_shot_from_maya_filename())
        if LM.hostName!="PC-20240202CTEU":
            self.ui.guess_shot_wgt.setVisible(False)


    

    
    def refresh(self):
        """刷新界面 - 委托给RefreshHelper处理"""
        if hasattr(self, 'ui_helper') and self.ui_helper.refresh_helper:
            self.ui_helper.refresh_helper.perform_full_refresh()


                        
                        
    def selectExGroup(self, rowIndex):
        """选择导出组 - 委托给RefreshHelper处理"""
        if hasattr(self, 'ui_helper') and self.ui_helper.refresh_helper:
            self.ui_helper.refresh_helper.select_export_group(rowIndex)

    def exAbc(self):
        rowNum=self.ui.exListGridLay.count()/5
        exPathList=[];exNodeList=[]
        acturalDir=self.ui.actualDirWgt.currentText()
        for i in range(1,rowNum+1):
            exGroupList=self.ui.exListGridLay.itemAtPosition(i,2).widget().text()
            if not exGroupList:
                continue
            selObj=self.ui.exListGridLay.itemAtPosition(i,0).widget().text()
            if ':' not in selObj:
                namespace=""
            else:
                namespace=selObj.split(':')[0]
            exGroupList=eval(exGroupList)
            exGroupList=[':'.join([namespace,x]) for x in exGroupList]
            exName=self.ui.exListGridLay.itemAtPosition(i,3).widget().currentText()+'.abc'
            exPath='/'.join([acturalDir,exName,])
            exPathList.append(exPath.replace('\\','/'))
            exNodeList.append(exGroupList)
        exFbx.batch_exABCfromGroup(exPathList=exPathList,
                                    rootList=exNodeList,
                                    Triangulate=self.ui.triFace_ckb.isChecked(),
                                    FrameRange='{},{}'.format(self.ui.sf_wgt.value(),
                                                self.ui.ef_wgt.value()))
        if os.path.exists(acturalDir) and exNodeList:
            os.startfile(acturalDir)

def showWin(*args):
    # 创建并显示可停靠窗口
    if LM.isMayaEnv():
        # 在Maya环境中使用可停靠窗口
        window = MainWindow()
        window.show(dockable=True)
        return window
    else:
        # 在非Maya环境中使用普通Qt窗口
        L_showQtWin.shouQtWin(QApplication,MainWindow,)

if __name__ == "__main__":
    showWin()
'''
from IOLib import BatchExAbc

'''

