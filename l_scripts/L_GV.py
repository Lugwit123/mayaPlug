# -*- coding: utf-8 -*-
import subprocess,math,os
import traceback
from Lugwit_Module import *
import time

import Lugwit_Module as LM
import maya.mel as mm
import maya.cmds as cmds
from maya.cmds import *
import maya
import sys

import maya.api.OpenMaya as om
import maya.cmds as cmds

# 限制递归深度
RECURSION_DEPTH_LIMIT = 1000

def allOrSel(tr=0):
    proObjList=[]
    if cmds.checkBox('allOrSel',q=1,value=1)==1:
        if tr==1:
            allObj=cmds.ls(filterExpand(cmds.ls(tr=1),sm=12))
        if tr==0:
            allObj=[]
            for x in cmds.filterExpand(ls(tr=1),sm=12):
                if cmds.nodeType(x)=='mesh':
                    allObj.append(x)
                else:
                    x=cmds.listRelatives(x,s=1)[0] 
                    allObj.append(x)
        proObjList=allObj
    if cmds.checkBox('allOrSel',q=1,value=1)==0:
        if cmds.ls(sl=1)!=[]:
            if tr==1:
                selObj=cmds.ls(filterExpand(cmds.ls(sl=1),sm=12))
            if tr==0:
                selObj=[]
                for x in cmds.filterExpand(cmds.ls(sl=1),sm=12):
                    if cmds.nodeType(x)=='mesh':
                        selObj.append(x)
                    else:
                        x=cmds.listRelatives(x,s=1)[0] 
                        selObj.append(x)
            proObjList=selObj
    return list(set(proObjList))

def get_allPoly(tr=0):
    if tr==1:
        allObj=cmds.ls(cmds.filterExpand(cmds.ls(tr=1),sm=12),l=1)
    elif tr==0:
        allObj=[]
        for x in cmds.filterExpand(cmds.ls(tr=1),sm=12):
            if cmds.nodeType(x)=='mesh':
                allObj.append(x)
            else:
                x=cmds.listRelatives(x,s=1)[0] 
                allObj.append(x)
    return list(set(allObj))

def getSameMatObj(selected_objects=[]):
    if not selected_objects:
        selected_objects = cmds.ls(selection=True,l=1)
    shNode=cmds.listRelatives(selected_objects,s=1,f=1)
    shading_groups = cmds.listConnections(shNode, type='shadingEngine')

    mat = cmds.listConnections(sg + ".surfaceShader")[0]
    orginalMat=mat.replace('_dup_mat','')
    orginalSg=cmds.listConnections(orginalMat,type='shadingEngine')[0]
    
    cmds.select(shading_groups)
    cmds.pickWalk(d='up')
    sel=cmds.ls(sl=1,l=1)
    return sel


def getSameMatObj(selected_objects=[]):
    if not selected_objects:
        selected_objects = cmds.ls(selection=True,l=1)
    shNode=cmds.listRelatives(selected_objects,s=1,f=1)
    shading_groups = cmds.listConnections(shNode, type='shadingEngine')


    
    cmds.select(shading_groups)
    cmds.pickWalk(d='up')
    sel=cmds.ls(sl=1,l=1)
    return sel




def select_objects_by_material(material,*args):
    cmds.select(get_objects_by_material(material))

def allNode():
    proObjList=[]
    if cmds.checkBox('allOrSel',q=1,value=1)==1:
        proObjList=cmds.ls()
    elif cmds.checkBox('allOrSel',q=1,value=1)==0:
        proObjList=cmds.ls(sl=1)
    return proObjList
def getClosestPointF(obj,pos1):#getClosestPoint(cmds.ls(sl=1)[0],[20,20,20])
    distance=[]
    reNormalprecision=float(cmds.intFieldGrp( 'reNormalprecision',q=1,v1=1))
    vervexNum=obj.numVertices()
    interval=int(math.ceil(vervexNum/50.0))
    for i in range(0,vervexNum,interval):
        vec=Array(pos1)-Array(xform(obj.vtx[i],t=1,q=1,ws=1))
        distance.append(vec.length())
    print (distance.index(max(distance)))
    index=distance.index(max(distance))*interval
    #select(obj.vtx[index])
    return distance[distance.index(max(distance))],index  
        
def Process_old():
    
    start=u'''
minPro=0
import maya
global gMainProgressBar,proStatus
proStatus=''
if 'forceAll' not in locals().keys():
    if cmds.ls(sl=1)==[] and cmds.checkBox('allOrSel',q=1,value=1)==0:
        cmds.confirmDialog(message=u"请先选择物体或者勾选所有物体选项",button=u"确定",defaultButton=u"确定",cancelButton=u"确定",dismissString=u"确定")
        sys.exit(1)
import time,math
global exExplain,leng,starttime,_pro,gMainProgressBar
exExplain='';leng=0
try:
    leng=len(Obj)
except:
    pass
_pro=0
starttime=time.time()
global gMainProgressBar 
gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')
cmds.progressBar( gMainProgressBar,
        edit=True,
        beginProgress=True,
        isInterruptable=True,
        maxValue=100 )
'''

    pro=u'''
global gMainProgressBar,proStatus,_pro
import subprocess
_pro+=1
timeDiff=time.time()-starttime
v=_pro/((timeDiff)+0.001)

pro=int(math.ceil (100.0*_pro/  leng  )   )
proStatus=u'剩余时间: '+str( leng/v-(timeDiff))+u'秒 '+u'循环次数: '+str(_pro)+'/'+str(leng)+u' 附加说明：'+str(exExplain)
cmds.progressBar( gMainProgressBar, edit=True, pr=pro ,status=proStatus )
if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ) and timeDiff>4:
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    cmds.error(u'结束进程')
    sys.exit(1)
'''

    end=u'''
cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
print( u'elapsed time--{}s'.format(time.time()-starttime))
'''
    editexExplain='''
minPro+=0.5
cmds.progressBar( gMainProgressBar, edit=True ,status=proStatus ,pr=pro+minPro)
minPro-=0.5'''
    return start,pro,end,editexExplain

class Process():
    def __init__(self,getdefault='btn',proList=[]):
        try:
            self.gMainProgressBar = mm.eval('$tmp = $gMainProgressBar')
        except RuntimeError:
            # 如果Maya GUI未完全初始化或在批处理模式下，$gMainProgressBar可能不存在
            # 在这种情况下设置为None，后续代码中检查时跳过进度条功能
            self.gMainProgressBar = None
            lprint("警告: $gMainProgressBar变量不存在，可能在批处理模式下运行")
        self.proList=proList
        try:
            self.start()
        except Exception as e:
            lprint("启动进程时出错: {}".format(e))

    def start(self):
        self.minPro=0
        self.proStatus=''
        if not self.proList:
            if 'forceAll' not in locals().keys():
                if cmds.ls(sl=1)==[] and cmds.checkBox('allOrSel',q=1,value=1)==0:
                    cmds.confirmDialog(message=u"请先选择物体或者勾选所有物体选项",button=u"确定",defaultButton=u"确定",cancelButton=u"确定",dismissString=u"确定")
                    return
        import time,math
        self.exExplain='';self.leng=0
        self.leng=len(self.proList)

        self._pro=0
        self.starttime=time.time()
        self.process=0
        if self.gMainProgressBar:
            cmds.progressBar( self.gMainProgressBar,
                    edit=True,
                    beginProgress=True,
                    isInterruptable=True,
                    maxValue=100 )
        else:
            lprint("开始处理进度，总数: {}".format(self.leng))


    def pro(self,exExplain=""):
        try:
            import subprocess
            self._pro+=1
            if exExplain:
                self.exExplain=exExplain
            timeDiff=time.time()-self.starttime
            v=self._pro/((timeDiff)+0.001)

            self.process=int(math.ceil (100.0*self._pro/self.leng  )   )
            
            
            self.proStatus=u'剩余时间: '+str( self.leng/v-(timeDiff))+u'秒 '+u'循环次数: '+str(self._pro)+'/'+str(self.leng)+u' 附加说明：'+self.exExplain
            if self.gMainProgressBar:
                cmds.progressBar( self.gMainProgressBar, edit=True, pr=self.process ,status=self.proStatus )
                if cmds.progressBar(self.gMainProgressBar, query=True, isCancelled=True ) and timeDiff>4:
                    cmds.progressBar(self.gMainProgressBar, edit=True, endProgress=True)
                    cmds.error(u'结束进程')
                    sys.exit(1)
            else:
                # 当进度条不可用时，打印进度信息
                lprint("进度: {}/{}  ({:.1f}%) - {}".format(self._pro, self.leng, self.process, self.exExplain))
        except:
            traceback.print_exc()



    def end(self):
        try:
            if self.gMainProgressBar:
                cmds.progressBar(self.gMainProgressBar, edit=True, endProgress=True)
                self.minPro+=0.5
                cmds.progressBar( self.gMainProgressBar, edit=True ,status=self.proStatus ,pr=self.process+self.minPro)
                self.minPro-=0.5
            else:
                lprint("处理完成！")
            print( u'elapsed time--{} amount--{}'.format(time.time()-self.starttime,self.leng))
        except:
            traceback.print_exc()




def is_intermediate_shape(shape_node):
    # 检查节点是否存在
    if not cmds.objExists(shape_node):
        return False
    
    # 检查是否有 intermediateObject 属性
    if cmds.attributeQuery('intermediateObject', node=shape_node, exists=True):
        # 获取 intermediateObject 属性的值
        return cmds.getAttr("{}.intermediateObject".format(shape_node))
    
    return False

def getSGs(objList,):
    if isinstance(objList,str):
        objList=[objList]
    objList=converyToShNode(objList)
    shaderList=[]
    for obj in objList:
        shaders=cmds.ls(cmds.listSets(object=obj), type='shadingEngine')
        if shaders:
            shaderList.extend(shaders)

    return list(set(shaderList))
    #shader=listConnections(shader)
    #mat=list(set(ls(shader,mat=1)))

def getAllSGNodeList(*args):
    sgNodeList=cmds.ls(type='shadingEngine',long=1)
    return list(set(sgNodeList))
    #shader=listConnections(shader)
    #mat=list(set(ls(shader,mat=1)))

def getMats(obj):
    # 尝试获取对象的形状节点
    try:
        shNodeList = cmds.listRelatives(obj, s=True,fullPath=1) or []
    except:
        shNodeList = []
    materials=[]
    for shNode in shNodeList:
        if is_intermediate_shape(shNode):
            continue
        # 获取与对象关联的着色引擎
        shader_engines = getSGs(shNode) or []

        # 获取着色引擎连接的材质
        shaders = []
        for shader_engine in shader_engines:
            shader_connections = cmds.listConnections(shader_engine + '.surfaceShader') or []
            shaders.extend(shader_connections)

        # 去重并打印材质列表
        materials += list(set(cmds.ls(shaders, mat=True,long=1)))
    return materials
    

    
def getFilePathFromMat(mat):
    File=cmds.listConnections(mat,s=1,type='file')
    filePath=[]
    for f in File:
        f=cmds.getAttr( f.fileTextureName)
        filePath.append(f)
    return filePath



def converyToTrNode(nodeList=[]):
    result=[]
    nodeList=cmds.ls(nodeList,l=1)
    for x in nodeList:
        if cmds.nodeType(x)=='transform':
            result.append(x)
        else:
            result.append(cmds.listRelatives(x,p=1,fullPath=1)[0])
    return result

def converyToShNode(nodeList=[],no_intermediate_shape=True):
    # lprint (locals())
    result=[]
    nodeList=cmds.ls(nodeList,l=1)
    for x in nodeList:
        if cmds.nodeType(x)=='mesh':
            result.append(x)
        else:
            shNode=cmds.listRelatives(x,s=1,fullPath=1)
            if shNode:
                result+=shNode
    if result:
        result = [x for x in result if not is_intermediate_shape(x)]
    return result




def getSplecifyShapeNodeFaceSetNodeFromFaceSet(faceSetList=[],filterObj=[]):
    # geo:列表或者字符串
    # filterObj 变换节点或者形态节点都可以
    # 获取制定形态的面集

    resule=[]
    filterObj = converyToShNode(filterObj)
    #lprint(filterObj)
    if filterObj:
        for faceSet in faceSetList:
            shNode=cmds.ls(faceSet, o=True,l=1)[0]
            #lprint(shNode)
            if cmds.nodeType(shNode)=='transform':
                shNode=cmds.listRelatives(shNode,s=1)[0]
            if shNode in filterObj:
                resule.append(faceSet)
    return resule

def getShapeNodeFromFaceSet(shNode):
    return cmds.ls(shNode, o=True,l=1)

def copy2clip(txt):
    cmd='echo ' + txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def openMayaFileDirectory(*args):
    os.startfile(os.path.dirname(getMayaFilePath()))

def copyMayaFilePath(*args):
    copy2clip(getMayaFilePath())

def are_nodes_same_by_uuid(node1, node2):
    """
    通过节点的 UUID 判断两个节点是否为同一个。
    
    :param node1: 第一个节点名称
    :param node2: 第二个节点名称
    :return: 布尔值，表示是否为同一个节点
    """
    # 获取节点的 UUID
    uuid1 = cmds.ls(node1, uuid=True)[0]
    uuid2 = cmds.ls(node2, uuid=True)[0]
    
    return uuid1 == uuid2



def querySgisAssignToFace(sg,trNode,*args):
    trNodeList=cmds.listConnections(sg,type='mesh')
    lprint(trNodeList)
    faceSetList=cmds.sets(sg,q=1,)
    if not trNodeList: return False

    shNodeList=cmds.listRelatives(trNode,s=1,fullPath=1)
    for shNode in shNodeList:
        if is_intermediate_shape(shNode):
            continue
        if not faceSetList:
            return False
        FaceSetList=getSplecifyShapeNodeFaceSetNodeFromFaceSet(faceSetList=faceSetList,filterObj=[trNode])
        if FaceSetList:
            return True


def getMayaFileName(*args):
    import maya.OpenMaya as om
    return om.MFileIO.currentFile().split('/')[-1]

def getMayaFilePath(*args):
    import maya.OpenMaya as om
    return om.MFileIO.currentFile()





def __dir__():
    pass

def __dict__():
    pass
