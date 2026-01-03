# coding:utf-8


import traceback
import os,sys
import maya.cmds as cmds
tempDir=os.environ['Temp']


class pm_class():
    def __init__(self):
        pass
    def __getattr__(self,name):
        global pm
        sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
        import load_pymel
        pm=load_pymel.pm
        func=eval('pm.{}'.format(name))
        return func
pm=pm_class()

def list_all_Nurbs_children(nodes):
    """Fast, but slow when nesting is very deep."""
    
    result = set()
    children = set(cmds.listRelatives(nodes, fullPath=True) or [])
    while children:
        result.update(children)
        children = set(cmds.listRelatives(children, fullPath=True) or []) - result
    result=list(result)
    cmds.select(result)
    nurbs=cmds.filterExpand(sm=9)
    cmds.select(cl=1)
    return cmds.listRelatives(nurbs,p=1)
    
# 清除引用修改中关于材质的部分
def cleanMatFromRef_MethodA(*args):
    from pymel.core.system import exportEdits
    sels=cmds.ls(sl=1)
    for sel in sels:
        # try:
        #     shNode=cmds.listRelatives(sel,s=1)[0]
        # except Exception as e:
        #     cmds.select(sel)
        #     print (e)
        #     continue
        # mats=[]
        # sgs=cmds.listConnections(shNode,type='shadingEngine')
        # mats+=[cmds.listConnections(x+'.surfaceShader')[0] for x in sgs]
        refNode = pm.referenceQuery(sel, referenceNode=True)
        refNode=pm.FileReference(refnode=refNode)
        # if 'chars' not in str(refNode) :
        #     continue
        #refNode.unload()
        referenceEdits=pm.referenceQuery(refNode, editStrings=True )
        print (referenceEdits)
        try:
            for referenceEdit in referenceEdits:
                str_referenceEdit=str(referenceEdit)
                A='instObjGroups' in str_referenceEdit
                B='.oig' in str_referenceEdit
                C='mo.v"' in str_referenceEdit
                #D = any([mat in str_referenceEdit for mat in mats])
                split_str_referenceEdit=str_referenceEdit.split('"')
                if A or B or C:
                    try:
                        try:
                            referenceEdit.remove(force=1)
                        except:
                            cmds.referenceEdit(split_str_referenceEdit[1],split_str_referenceEdit[3],removeEdits=1,editCommand='connectAttr',failedEdits=True,successfulEdits=True)
                        print (u'移除编辑{}成功'.format(referenceEdit))
                    except:
                        
                        print(traceback.format_exc())
        except:
            print(traceback.format_exc())
        refNode.load()
    
    
def cleanMatFromRef_MethodB(ExMofify=1,importMofifyWithoutSG=0,):
    allRef=pm.listReferences()
    for ref in allRef:
        if 'chars' not in str(ref) :
            continue
        refNode=ref.refNode
        refLogFile=tempDir+'\\'+refNode.split(':')[-1]+'.editMA'
        fullNamespace=refNode.longName()
        #导出编辑
        NewrefLogFile=refLogFile.replace('.editMA','_New_.editMA')
        if ExMofify:
            exportEdits(refLogFile,
                        f=1,
                        orn=refNode.longName(),
                        includeSetAttrs=1,
                        includeShaders=0,
                        includeAnimation=1,
                        includeNetwork=1,
                        includeConstraints=1,
                        includeDeformers=1,
                        includeSetDrivenKeys=1,
                        type="editMA")
            
            with open(refLogFile,'r') as f:
                lines=f.readlines()
            with open(NewrefLogFile,'w') as f:
                newLines=[]
                replaceList=[]
                for i,line in enumerate(lines):
                    replaceList.append(0)
                    if '.instObjGroups' in line or '.iog' in line or 'mo.v"' in line:
                        replaceList[i]=1
                        continue
                    if replaceList[i-1]==1:
                        print (i,lines[i-1])
                        continue
                    #B003_S78_props_DT_rig:Main_Mov B003_S78_chars_wuji_lay1:MainExtra1
                    f.write(line)

            
        
        if importMofifyWithoutSG:
            #卸载参考
            ref.unload()
            #清理参考编辑
            ref.clean()
            #导入参考编辑
            ref.load()
            print (u'加载参考')
            cmds.file(NewrefLogFile,i=1,type="editMA" ,
            namespace=fullNamespace,
            applyTo=refNode.longName(),
            force=1)
        
            print (u'移除结束')