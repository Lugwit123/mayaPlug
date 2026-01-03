# coding:utf-8
import os
import maya.cmds as cmds

def getBlendControlDict():
    blendControlDict={}
    blendShapeNode=cmds.ls(type='blendShape')
    for blendShapeNode_A in  blendShapeNode:
        userAttr=cmds.listAttr(blendShapeNode_A+'.w',m=1)
        #cmds.select(blendShapeNode_A)
        for  userAttr_A in  userAttr:
            blendControlDict[userAttr_A]=blendShapeNode_A.split('_blendShapes')[0]
        return blendControlDict


def exPhiz(maxIter=10000):
    blendControlDict=getBlendControlDict()
    clNode='CTRL_expressions'
    outPort=cmds.listAttr(clNode,ud=1)
    print (outPort)
    exPath=r'E:\BUG_Project\B014\reference\chars\XiaoYang\MetaHumanPhiz'
    exPath=exPath.replace('\\','/')
    
    for index,outPort_A in  enumerate(outPort):
        if index>maxIter:
            break
        exNode=blendControlDict[outPort_A]
        inputAttrList=clNode+'.'+outPort_A
        inputNodeAttr=cmds.listConnections(inputAttrList,p=1,s=1,d=0)[0]
        cmds.select(inputNodeAttr)
        print (inputAttrList,inputNodeAttr)
        cmds.disconnectAttr(inputNodeAttr,inputAttrList)
        cmds.setAttr(clNode+'.'+outPort_A,1)
        exFile=exPath+'/'+exNode+'_'+outPort_A+'.obj'
        cmds.select(exNode)
        cmds.file(exFile,force=1,options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1",typ="OBJexport",
        pr=1,es=1)
        cmds.setAttr(clNode+'.'+outPort_A,0)
        cmds.connectAttr(inputNodeAttr,inputAttrList)
        break
    
#给新的初始模型添加Orgi形态节点

def genOrgiShape():
    newTrNode='pSphere1'
    newShapeNode=cmds.listRelatives(newTrNode,s=1)[0]
    oriTrNode='pSphere3'
    oriShapeNode=cmds.listRelatives(oriTrNode,s=1)[0]
    oriOrgiNode=cmds.listRelatives(oriTrNode,s=1)[1]
    copyNewTrNode=cmds.duplicate(newShapeNode)
    copyNewShapeNode=cmds.listRelatives(copyNewTrNode,s=1)[0]
    nameNewShapeNode=cmds.rename(copyNewShapeNode,newShapeNode+'Orig')
    cmds.setAttr(nameNewShapeNode+'.visibility',0)
    cmds.parent(nameNewShapeNode,newTrNode,s=1,add=1)
    cmds.delete(copyNewTrNode)
    return  nameNewShapeNode

def transBlend():  
    blendNode=cmds.listConnections(oriShapeNode+'.inMesh',p=1,d=0)[0]
    cmds.connectAttr(blendNode,newShapeNode+'.inMesh',f=1)
    groupPartNode=cmds.listConnections(oriOrgiNode+'.worldMesh',p=1,s=0)[0]
    cmds.connectAttr(genOrgiShape()+'.inMesh',groupPartNode,f=1)
    
