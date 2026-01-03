#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import maya.cmds as mc
import maya.cmds as cmds
import json,os,sys
from Lugwit_Module import *

import codecs

Lugwit_mayaPluginPath=os.environ['Lugwit_mayaPluginPath']
if sys.version_info[0]==2:
    sys.path.append(Lugwit_mayaPluginPath+r'\materialPlug\python_library')
try:
    import numpy as np
except:
    pass

import random

import datetime,math, time,maya

try:
    import os,sys
    sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
    import load_pymel
    pm=load_pymel.pm
except:
    pass



def get_shading_groups(polygon):
    u"""
        返回模型的shading_groups
    :param polygon: polygon (pymel)
    :return: shading group list (pymel)
    """
    sgs = polygon.shadingGroups()
    sgs.extend(polygon.outputs(type="shadingEngine"))
    if polygon.type() == "transform":
        sgs.extend(polygon.getShape().outputs(type="shadingEngine"))
    return sgs
    
    
def make_dirs(path):
    path = os.path.normpath(path)
    os.system(u'cmd /c mkdir {}'.format(path))

def getSGs(obj):
    try:
        obj=pm.listRelatives(obj,s=1)
    except:
        pass
    shader=pm.listConnections(obj,type='shadingEngine')
    return list(set(shader))  

def getPath(*args):
    global pathName
    pathName = fileDialog2(fileMode=3, caption="Import Image")[0]
    textFieldButtonGrp(u'exchangeFile', e=1, tx=pathName)
    
def export_mat_json(selObj='', path='',Key='Sg|Obj',writeBBoxInfo=1,
                    writeTopoInfo=1,openMayaFile='',mayaFile=''):
    
    lprint (locals())
    
    if openMayaFile:
        try:
            cmds.file(mayaFile, f=True, o=True,ignoreVersion=True)
        except:
            pass
        
    if not selObj:
        selObj=cmds.ls(type='mesh')
        print (u'因为你没有选择任何物体,所有选择所有物体导出材质配置文件')
    # selObj 选择的一个或者节点
    # path 生成的数据存储的完整名称
    #selObj = pm.ls(selObj)
    pathStartDir=os.path.dirname(cmds.file(q=1,sn=1))
    if not path:
        path=cmds.fileDialog2(fileMode=0,fileFilter='*.json' ,caption="MatJsonFile",startingDirectory=pathStartDir)[0]
    
    data = {};
    cmds.select(selObj)
    lprint (cmds.ls(sl=1))
    cmds.SelectHierarchy()
    
    selObj=cmds.ls(sl=1)
    selMesh=pm.filterExpand(selObj,sm=12)
    selMesh_pm=pm.ls(selMesh)
    if selMesh_pm:
        selMesh_pm=set(selMesh_pm)
        for sel in selMesh_pm:
            #break
            sgs = getSGs(sel)
            # prefix = len("|".join(re.split("\|\w+:", sel.fullPath())))
            #lprint ("sgs",sgs)
            meshNode_pm=sel.getShapes()[0]
            meshNode=str(meshNode_pm)
            
            if cmds.nodeType(str(meshNode_pm))!='mesh':
                continue
            
            trNode=str(sel)
            if writeBBoxInfo:
                vol=pm.polyEvaluate(meshNode_pm,worldArea=1)
            if writeTopoInfo:
                faceNum=meshNode_pm.numFaces()
                vtxNum=meshNode_pm.numVertices()
            breakUpperLoop=0
            for sg in sgs:
                #fanhui 
                elements = sg.elements()
                #lprint ('sg.elements()',sg.elements())
                if not elements:
                    continue
                    # return False
                #lprint('meshNode_pm',meshNode_pm)   
                for element in elements:
                    # element要么是面,要么是mesh
                    
                    isMultiMat=isinstance(element, pm.general.MeshFace)
                    #lprint ('element,element.node()',element,element.node())
                    if element.node()!=meshNode_pm:
                        continue
                    
                    #其实这里只会有一个mesh
                    if Key=='Sg':
                        data.setdefault(sg.name(), {}).setdefault(trNode, []).extend(element.indices())
                    elif Key=='Obj':
                        if  isMultiMat:
                            data.setdefault(trNode,{}).setdefault('SG',{}).setdefault(sg.name(),element.indices())
                        else:
                            data.setdefault(trNode,{}).setdefault('SG',sg.name())
                            
            if breakUpperLoop==0:
                data.setdefault(trNode,{}).setdefault('topo',[faceNum,vtxNum])
                data.setdefault(trNode,{}).setdefault('visibility',cmds.getAttr(trNode+'.visibility'))
                lprint (trNode,meshNode_pm, faceNum)
                data.setdefault(trNode,{}).setdefault('vol',vol)
                # 导出形态节点的arnold属性
                aiAttrs=cmds.listAttr(meshNode)
                for aiAttr in aiAttrs:
                    try:
                        attrValue=cmds.getAttr(meshNode+'.'+aiAttr)
                        attrType=cmds.getAttr(meshNode+'.'+aiAttr,type=1)
                        data.setdefault(trNode,{}).setdefault('ShapeNode',{}).setdefault(aiAttr,[attrValue,attrType])
                    except Exception as e:
                        lprint (e)
                # OpaqueValue=meshNode_pm.attr('aiOpaque').get()
                # data.setdefault(trNode,{}).setdefault('aiOpaque',OpaqueValue)
                # AiSubType=meshNode_pm.attr('aiSubdivType').get()
                # AiSub=meshNode_pm.attr('aiSubdivIterations').get()
                # data.setdefault(trNode,{}).setdefault('arnold',{}).setdefault('AiSubdivIterations',{'AiSubType':AiSubType,'AiSubdivIterations':AiSub})
    #导出头发材质
    Descs=cmds.ls(type='xgmDescription')
    sgs=[]
    for desc in Descs:
        if desc in  selObj :
            sg=cmds.listConnections(desc,type='shadingEngine')[0]
            desc=cmds.listRelatives(desc,p=1)[0]
            data.setdefault('xgenNode__'+desc,{}).setdefault('SG',sg)

    
    make_dirs(os.path.dirname(path))
    #lprint(data)
    # json_file = os.path.join(path + ".json")
    for poly, polyInfo in data.items():
        try:
            sg = polyInfo['SG']
        except:
            lprint (poly, polyInfo)
        if isinstance(sg,dict):
            for sg, ids in polyInfo['SG'].items():
                slices = []
                while ids:
                    _slice = [ids[0], ids.pop(0)]
                    slices.append(_slice)
                    while True:
                        if not ids:
                            break
                        if _slice[1] + 1 == ids[0]:
                            _slice[1] = ids.pop(0)
                        else:
                            break
                    data[poly]['SG'][sg] = slices
    with open(path, "w") as write:
        json.dump(data,write,ensure_ascii=False,indent=4)
    cmds.select(cl=1)
    cmds.warning(u'导出完毕')
        
'''
import IOLib.mat as mat
reload(mat)
mat.export_mat_json(cmds.ls(sl=1),
                            path='e:\BUG_Project\B003_S78\Asset_work\chars\Rig\B003_S78_chars_wuji_Mat.json',
                            Key='Obj')
'''

def exSgNet(exPath='D:/bb/bb.ma',openMayaFile=''):
    pathStartDir=os.path.dirname(cmds.file(q=1,sn=1))
    if not exPath:
        exPath=cmds.fileDialog2(fileMode=0, fileFilter='*.ma',
            caption=u"Maya材质文件",startingDirectory=pathStartDir)[0]
    sels=cmds.ls(type='shadingEngine')
    sels.remove(u'initialShadingGroup')
    sels.remove(u'initialParticleSE')
    allShaderNodeList = list()
    for sg in sels:
        shaderNodeList = cmds.listHistory(sg,pdo = True)
        shaderNodeList = [shader for shader in shaderNodeList if cmds.nodeType(shader) != 'uvChooser']
        allShaderNodeList.extend(shaderNodeList)
    
    cmds.select(allShaderNodeList,r = True,noExpand = True)
    cmds.file(exPath,force = True,
        options = 'v=0;',type = 'mayaAscii',pr = False,es = True,
        constructionHistory = False)
    cmds.confirmDialog(title=u'导出成功',message=u'导出成功{}'.format(exPath),button=u'确定')

def exmatJsonAndSgNode(mayaFile='',
                       matJsonExFile='',
                       SgNodeExPath='',
                       openMayaFile=''):
    if openMayaFile:
        try:
            cmds.file(mayaFile, f=True, o=True,ignoreVersion=True)
        except:
            pass
    export_mat_json( path=matJsonExFile,Key='Obj')
    exSgNet(SgNodeExPath)
'''
import autoTransferUV
reload(autoTransferUV)
import IOLib
reload(IOLib)

print autoTransferUV.sameObj(sourceObj='pTorus2', targetObj='pTorus3',
                       useJsonFile='D:/bb/bb.json')



IOLib.export_mat_json(cmds.ls(sl=1),
                             path='D:/bb/bb.json',
                             Key='Obj')
                             
                            
                             
                      
                             
exportMatJson.assignMat(cmds.ls(sl=1,)[0],jsonFile=r'D:\bb\bb.json',)
'''