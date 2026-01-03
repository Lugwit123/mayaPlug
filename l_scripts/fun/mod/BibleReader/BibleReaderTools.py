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



def getMayaWin():
    ptr = omui.MQtUtil.mainWindow()
    mayaWin = wrapInstance(long(ptr), QWidget)
    return mayaWin

def getQssPath(qssFile):
    u"""
    :param qssFile: 'xxx.qss'
    :return: str
    """
    thisPath = __file__
    scriptsPath = os.path.dirname(thisPath)
    qssFolderPath = os.path.join(scriptsPath,'qss')
    qssPath = os.path.join(qssFolderPath,qssFile).replace('\\','/')
    return qssPath.decode('gbk')

def getStyleSheet(qssFile):
    thisPath = __file__
    styleSheet = ''
    qssPath = getQssPath(qssFile)
    if qssPath:
        qss = QFile(qssPath)
        qss.open(QFile.ReadOnly)
        styleSheet = qss.readAll().data().decode('utf-8')     
        styleSheet = styleSheet.replace(u':/images/',
            os.path.join(os.path.dirname(thisPath).decode('gbk'),u'images/'))
        styleSheet = styleSheet.replace('\\','/')
        qss.close()
    return styleSheet

def getUIPath(uiName):
    u"""
    :param uiName: 'xxx.ui'
    :return: str
    """
    thisPath = __file__
    scriptsPath = os.path.dirname(thisPath).decode('gbk')
    uiFolderPath = os.path.join(scriptsPath,'ui')
    uiPath = os.path.join(uiFolderPath,uiName).replace('\\','/')
    return uiPath

def getBiblePath():
    thisPath = __file__
    scriptsPath = os.path.dirname(thisPath)
    return os.path.join(scriptsPath,'bible')