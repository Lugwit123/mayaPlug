# coding:utf-8
import re
import maya.mel as mm
import maya.cmds as cmds
from Lugwit_Module import *
from usualLib import *
def getSGs(obj):
    try:
        try:
            obj=cmds.listRelatives(obj,s=1,f=1)
        except:
            pass
        shader=cmds.listConnections(obj,type='shadingEngine')
        if shader:
            return list(set(shader))
    except:
        cmds.select(obj)
        cmds.error ('getSGs error:{}'.format(obj))
	#shader=listConnections(shader)
	#mat=list(set(ls(shader,mat=1)))
 
def genUdimPreview(*args):
    sl=cmds.ls(sl=1,l=1)
    if not sl:
        ok=cmds.confirmDialog(title=u'你没有选择物体',message=u'没选择物体将会刷新所有udim贴图',button=[u'要得',u'要不得,我要选择物体在操作'],
                           defaultButton=u'要得', cancelButton=u'要不得,我要选择物体在操作')
        if ok==u'要不得,我要选择物体在操作':
            return
        selObjs=cmds.ls(tr=1,l=1)
    else:
        selObjs=sl
    FileNodeList=[]
    for obj in selObjs:
        shNode=cmds.listRelatives(obj,s=1,f=1)
        if not shNode:
            continue
        shNode=shNode[0]
        if cmds.nodeType(shNode)=='mesh':
            sgs=getSGs(obj)
            if not sgs:
                continue
            for sg in sgs:
                mat=cmds.listConnections(sg+'.surfaceShader')[0]
                outColor_Input=cmds.listHistory(mat+'.outColor')
                for inputNode in outColor_Input:
                    if cmds.nodeType(inputNode)=='file':
                        imageNameAtrrValue=cmds.getAttr(inputNode+'.ftn')
                        if re.search('[0-9]{4}',imageNameAtrrValue,flags=re.I):
                            print (inputNode)
                            if inputNode in FileNodeList:
                                continue
                            mm.eval('generateUvTilePreview  {}'.format(inputNode))
                            FileNodeList.append(inputNode)
    cmds.confirmDialog(title=u'你好',message=u'一共对{}个文件节点进行了UDIM预览'.format(len(FileNodeList)),button=[u'要得'],)
