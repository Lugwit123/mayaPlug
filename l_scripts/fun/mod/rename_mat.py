# -*- coding:utf-8 -*-
import maya.cmds as cmds
import os
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import re
import functools
import time
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import *
    from PySide import __version__
    from shiboken import wrapInstance
except:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtUiTools import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance


def getMayaWin():
    ptr = omui.MQtUtil.mainWindow()
    mayaWin = wrapInstance(long(ptr), QWidget)
    return mayaWin

def paintEvent(self,event):
    opt = QStyleOption()
    opt.initFrom(self)
    p = QPainter(self)
    self.style().drawPrimitive(QStyle.PE_Widget,opt,p,self)

        
class TestWidget(QWidget):
    def __init__(self,parent = None):
        super(TitleWidget,self).__init__(parent)
        
TestWidget.paintEvent = paintEvent


class RenameMat(QWidget):
    def __init__(self,parent = None):
        super(RenameMat,self).__init__(parent)

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'材质球批量命名')
        layout = QVBoxLayout(self)  
        margin = 5
        layout.setContentsMargins(margin,margin,margin,margin)
        layout.setSpacing(0)  
        self.setLayout(layout)

        title_label = QLabel(u'选择模型然后修改',self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        sub_layout = QHBoxLayout(self)
        
        sub_layout.setContentsMargins(0,0,0,0)
        sub_layout.setSpacing(3)
        name_text_edit = QLineEdit(self)
        self.name_text_edit = name_text_edit
        btn = QPushButton(u'修改',self)
        btn.setFixedWidth(60)
        sub_layout.addWidget(name_text_edit)
        sub_layout.addWidget(btn)
        btn.clicked.connect(self.rename)

        layout.addLayout(sub_layout)

        styleSheet = u'''
            *{
                font-size:12px;
                font-family:"Microsoft YaHei";
            }
            QLabel{font-size:20px;}

        '''
        self.setStyleSheet(styleSheet)

        self.resize(300,150)
        
    def rename(self):
        name = self.name_text_edit.text()
        if name:
            rename_selection_shaders(name = name)


def get_sg(obj):
    u"""物体的sg列表"""
    sg_list = list()
    t_sg_list = cmds.listConnections(obj, s=False, type='shadingEngine')
    shape_list = cmds.listRelatives(obj, s=True, pa=True, ni=True)
    if t_sg_list:
        sg_list.extend(t_sg_list)
    if shape_list:
        for shape in shape_list:
            shape_sg_list = cmds.listConnections(shape, s=False, type='shadingEngine')
            if shape_sg_list:
                sg_list.extend(shape_sg_list)
    return list(set(sg_list))

def rename_selection_shaders(name = 'a'):
    u"""
    把所选的物体的sg和sg的材质球名字更改：
    sg: [name]_a_shadingEngine
    shader: [name]_a_[节点类型]
    会按选择顺序让材质节点从a-z命名
    """
    objs = cmds.ls(sl = True)
    ord_index = ord('a')
    for obj in objs:
        sgs = get_sg(obj)        
        for sg in sgs:
            shaders = cmds.listConnections(sg + '.surfaceShader')
            cmds.rename(sg,'%s_%s_%s'%(name,chr(ord_index),'shadingEngine'))
            for shader in shaders:
                cmds.rename(shader,'%s_%s_%s'%(name,chr(ord_index),cmds.nodeType(shader)))
            ord_index+=1



def mainUI():
    winName = 'batch_rename_mat'
    if cmds.window(winName,q = True,exists = True):
        cmds.deleteUI(winName)

    win = RenameMat(getMayaWin())
    win.setObjectName(winName)
    win.show()

if __name__ == '__main__':
    mainUI()