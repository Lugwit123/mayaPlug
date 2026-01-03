# -*- coding:utf-8 -*-
import maya.cmds as cm
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

def selectBorderFromSelected(*argvs):
    objList = cm.ls(sl = True)
    selectBorder(objList)


def selectBorder(meshes):
    cm.select(meshes,r = True)
    cm.polySelectConstraint(m = 3,t = 0x8000,w = True)
    borderEdges = cm.ls(sl = True,fl = True)
    cm.polySelectConstraint(dis = True)

'''
def getOverlappingVertices(meshes):
    Lvertices = []
    for mesh in meshes:
            
        numverts = int(cm.polyEvaluate(mesh, v=1))
        
        # store vertex positions and indices in a dict
        # in the form {(x,y,z):[index,], }
        Dindex = {}
        Ddups = {}
        for i in range(numverts):
            #t = tuple(cm.xform('%s.vtx[%d]' % (mesh, i), query=True, worldSpace=True, translation=True))
            # pointPosition is twice as fast as xform
            t = cm.pointPosition('%s.vtx[%d]' % (mesh, i))
            for j in range(len(t)):
                v = t[j]
                t[j] = round(v,3)
            t = tuple(t)
            if t in Dindex.keys():
                Dindex[t].append(i)
            else:
                Dindex[t] = [i]
                 
            # we now have something like
            # {(-1.0, 0.0, 1.0): [1], (-1.0, 0.0, -1.0): [0], (1.0, 0.0, -1.0): [2, 3]} 
        
        # find vertex positions that are duplicates
        Ddups = dict((k, v) for k, v in Dindex.iteritems() if len(v) > 1)      
        numberofdups = len(Ddups.keys())
        # this is the filtered version of the dict and looks like
        # {(1.0, 0.0, -1.0): [2, 3]}
        if numberofdups > 0:
            # fail the test
            result = True
            
            for v in Ddups.values():
                Ltmpvtx = []
                # every entry in the dic has at least >1 vertices
                for vtx in v:
                    Ltmpvtx.append('%s.vtx[%d]' % (mesh, vtx))
                # 
                Lvertices.extend(Ltmpvtx)
        
            # flatten the list
            # sel = [item for sublist in Lvertices for item in sublist]
    return(Lvertices)
'''

# def selectOverlappingVertices(*argvs):
#     time1 = time.time()
#     meshes = cm.ls(sl = True)
#     lvertices = getOverlappingVertices(meshes)
#     cm.select(lvertices)
#     time2 = time.time()
#     print(time2 - time1)

def loadOverlappingVerticesPlugin():
    plugin = 'PolyOverlappingVertices'
    if not cm.pluginInfo(plugin,l = True,q = True):
        cm.loadPlugin(plugin)

def selectOverlappingVertices(objList):
    loadOverlappingVerticesPlugin()
    time1 = time.time()
    # objList = cm.ls(sl = True)
    allVertList = list()
    OverlappingVerticesObjList = list()
    if objList:
        for obj in objList:
            # cm.select(obj,r = True)
            vertList = cm.PolyOverlappingVertices(obj,p = -4)
            if vertList:
                OverlappingVerticesObjList.append(obj)
                for vertIndex in vertList:
                    edge = '%s.vtx[%d]'%(obj,vertIndex)
                    allVertList.append(edge)
    time2 = time.time()
    print(time2 - time1)
    print(len(allVertList))
    cm.select(allVertList,r = True)
    return OverlappingVerticesObjList

def selectOverlappingVerticesFromSelected(*argvs):
    meshList = cm.listRelatives(cm.ls(sl = True),type="mesh", ad=1)
    polygons = list()
    if meshList:
        polygons = list(set(cm.listRelatives(mesh,p = True,pa = True)[0] for mesh in meshList))
    return selectOverlappingVertices(polygons)
    
def polyProblemUI():
    winName = u'polyProblemWin'
    if cm.window(winName,q = True,exists = True):
        cm.deleteUI(winName)
    cm.window(winName,title = u'模型检测')
    cm.window(winName,e = True,w = 250,h = 100)
    cm.columnLayout(adj = True)
    h = 40
    cm.button(l = u'检测border',h = h,c = selectBorderFromSelected)
    cm.button(l = u'检测重叠的点',h = h,c = selectOverlappingVerticesFromSelected)
    cm.showWindow(winName)


if __name__ == '__main__':
    # winName = 'hyws_asset_browser'
    # if cm.window(winName,q = True,exists = True):
    #     cm.deleteUI(winName)

    # win = UIWin(uitools.getMayaWin())
    # win.setObjectName(winName)
    # win.show()
    polyProblemUI()