# coding:utf-8
import maya.mel as mel
import maya.cmds as cmds
import sys,os,re
import maya.api.OpenMaya as om


from imp import reload
def initializePlugin(*args):
    from maya import mel
    if not mel.eval('$gMainWindow=$gMainWindow'):
        return

    try:
        reload (LugwitMayaPlugStart)
    except:
        import LugwitMayaPlugStart
 
    LugwitMayaPlugStart.install()


def uninitializePlugin(*args):
    try:
        reload (LugwitMayaPlugStart)
    except:
        import LugwitMayaPlugStart
    LugwitMayaPlugStart.uninstall()

'''
这个文件夹只有一个python文件,否则在插件目录会有两个python文件
'''
