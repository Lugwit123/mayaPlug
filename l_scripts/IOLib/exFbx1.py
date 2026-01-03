# coding:utf-8
from __future__ import print_function
from __future__ import absolute_import

import shutil
import copy,os,sys

# 添加模块所在路径
print (u'run into module {}'.format(__file__))
LugwitToolDir = os.getenv('LugwitToolDir')
sys.path.append(LugwitToolDir+'/Lib')
from Lugwit_Module import *

from Lugwit_Module.l_src.MayaToUe import ExHistoryFromMaya 
import inspect
from Lugwit_Module.l_src.MayaToUe import  *

import Lugwit_Module as LM
from Lugwit_Module import lprint
from Lugwit_Module.l_src.l_DataProcess import json_read
TempDir= LM.TempDir
LugwitPath=LM.LugwitPath
lprint.max_prints_per_line=10


sys_executable=sys.executable
lprint (u'sys.argv:{}'.format(sys.argv))
import os,re,sys

import msvcrt
import sys
import datetime
from imp import reload

def loadPluginFunc(plug):
    try:
        cmds.loadPlugin(plug)
    except:
        traceback.print_exc()
    
    
houtai = eval(os.environ.get('houtai','0'))
if houtai :
    import pymel.core as pm

import maya.cmds as cmds
import maya.mel as mm    

fileDir = os.path.dirname(__file__)
sys.path.insert(0,fileDir)

lprint ('run module{},sys.executable--{}'.format(__file__,sys.executable))
import re,json
import time,os,sys
import subprocess

st=time.time()
from imp import reload
import traceback
import codecs
from pprint import pprint

sys.path.append(LugwitPath+'/Python/Python27/Lib/site-packages')
sys.path.append(LugwitPath+'/Python/PythonLib')
sys.path.append(LugwitPath+'/Python/PythonLib\Perforce')

p4=0


#加载第三方模块
sys.path.append(LM.Lugwit_mayaPluginPath+r'\l_scripts\ThridLib')
sys.path.append(LM.Lugwit_mayaPluginPath+r'')
import  materialPlug.scripts as mps





tempFolder=Lugwit_publicPath+'/temp/mayaTemp'



# 由于pymel这个库导入比较慢,所以前台启动maya加载插件的时候不真正加载这个库
# 等用的时候再加载,后台启动Maya那导入Pymel库的那几秒时间就无所谓了
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
if not houtai:  
    pm=pm_class()
# 这是个大坑呀,后台一定要在打开文件之前加载pymel
# 不能用pm=pm_class()这种方式,否则会被坑死


import generalLib as gl



#添加库路径
sys.path.append(LM.Lugwit_mayaPluginPath+r'\l_scripts')
import usualLib 

cmds.dirmap(en=1)
cmds.dirmap(m=(r'H:\\', r'G:\\'))
import inspect
print ('__file__',inspect.getfile(inspect.currentframe()))
print (cmds.dirmap(gam=1))


def getjsonExCfg(mayaFile='',jsonExConfig=''): #getjsonExCfg(cmds.file(q=1,sn=1))
    mayaFile=mayaFile.replace('\\','/')
    try:
        ProjectDir=re.search('.+/BUG_Project/.+?/',mayaFile, re.I).group()
    except:
        ProjectDir=re.search('(.+/)Shot_work/.+?/',mayaFile, re.I).group(1)
    if not jsonExConfig:
        jsonExConfig=ProjectDir+u'/项目规范/Fbx导出规则.json'
    lprint (u'项目规范/Fbx导出规则.json:{}'.format(jsonExConfig))
    if os.path.exists(jsonExConfig):
        
        with open (jsonExConfig,'r') as open_jsonExConfig:
            jsonExConfig_content=open_jsonExConfig.read()
        jsonExConfig_content=eval(jsonExConfig_content)
        lprint (jsonExConfig_content,type(jsonExConfig_content))
        return jsonExConfig_content

def readInput(caption='', default='', timeout=5):
    start_time = time.time()
    inputStr = ''
    xianshi = u'提示:{} '.format(caption)
    lprint(xianshi)
    kbhit = 0
    while 1:
        shiqushijian = time.time()-start_time
        remainTime = int(timeout-shiqushijian)
        if not kbhit:
            lprint(u"\r{}s/{}s,默认值为{}:".format(remainTime, timeout, default)),
            if time.time() - start_time > timeout:
                inputStr = default
                break
        if msvcrt.kbhit():
            kbhit = 1
            chr = msvcrt.getwche()
            if ord(chr) == 13:  # enter_key
                if not inputStr:
                    inputStr = default
                break
            elif ord(chr) >= 32:  # space_char
                inputStr = inputStr+chr
            elif ord(chr) == 8:  # 退格键
                inputStr = inputStr[:-1]

    lprint(u'\n你选择的值为:{}\n'.format(str(inputStr)))
    return inputStr


@try_exp
def exTpose(moveSkeToRoot=0,openNewFile=1,mayaFile=''):
    # 获取描述文件
    lprint (locals())
    if openNewFile:
        try:
            cmds.file(mayaFile,open=True,ignoreVersion=True,force=True)
        except:
            lprint(u'打开文件失败！{}'.format(traceback.format_exc()))
    mayaFileName=os.path.basename(mayaFile)
    mayaFileNameDir=os.path.dirname(mayaFile)
    # 使用正则表达式移除 '_Rig' 及其后面的内容，直到文件扩展名前
    match = re.search(r'(.+?)_Rig.*\.ma$', mayaFileName,flags=re.IGNORECASE)
    if match:
        baseName = match.group(1)  # 捕获 '_Rig' 之前的部分
    else:
        baseName = mayaFileName.rsplit('.', 1)[0]  # 如果没有 '_Rig'，则直接去掉扩展名

    mayaFileDir=os.path.dirname(mayaFile)
    savePath = mayaFileDir+'/'+baseName + '.fbx'
    exFBX(JntGroup='DeformationSystem',geometryGroupList=['srfNUL','model_grp'],
          moveSkeToRoot=moveSkeToRoot,exSkelelonMesh=True,
          savePath=savePath,exSkelonAnim=0,sf=1, ef=1)



# 获取名称空间RN节点引用文件路径字典
def getNsKey_RfnAndFileDict():
    u'''
    {名称空间:{refNode:str,refNode_Exist:str,refFile:str}}
    '''
    Refs=cmds.ls(type='reference')
    lprint(Refs,pm)
    #lprint (Refs)
    nsRfnDict={}
    fileRef = []
    for ref in Refs:
        
        #if ref in 'sharedReferenceNode _UNKNOWN_REF_NODE_':
        if re.search('sharedReferenceNode|_UNKNOWN_REF_NODE_',ref):
            continue
        refNode=str(ref)
        #lprint (refNode)
        
        try:
            fileRef=pm.system.FileReference(refnode=refNode)
            nameSpace=str(fileRef.fullNamespace)
            if ':' in str(refNode):
                nameSpace=str(refNode).rsplit(':',1)[0]+':'+nameSpace
            nsRfnDict.setdefault(nameSpace,{}).setdefault('refNode',refNode)
            nsRfnDict.setdefault(nameSpace,{}).setdefault('refNode_Exist',cmds.objExists(refNode))
            try:
                refFile=cmds.referenceQuery(str(refNode),f=1)
                nsRfnDict.setdefault(nameSpace,{}).setdefault('refFile',refFile)
            except Exception as e:
                lprint (u'参考节点{}没得对应的文件'.format(str(refNode)))
                print (traceback.format_exc())
        except:
            lprint (fileRef)
            print (traceback.format_exc())

    return nsRfnDict

def replaceHigRigFile(nameSpace,NewFile):
    try:
        if os.path.exists(NewFile):
            lprint (u'替换高模文件{}开始'.format(NewFile))
            nsRfnDict=getNsKey_RfnAndFileDict()
            rfNode=nsRfnDict[nameSpace]['refNode']
            MayaType = os.path.splitext(NewFile)[1]
            typeDict = {'.ma': "mayaAscii", '.ma{1}': "mayaAscii", '.mb': "mayaBinary",
                            '.mb{1}': "mayaBinary", '.ma{2}': "mayaAscii", '.mb{2}': "mayaBinary"}
            MayaType = typeDict[MayaType]
            cmds.file(NewFile, loadReference=rfNode,
                                type=MayaType, options="v=0",f=1)
    except Exception as ex:
        lprint (traceback.format_exc())
        lprint (u'替换高模文件{}被中断'.format(NewFile))
     
     
def replaceRN():
    rfMayaFile = cmds.file(r=1, q=1)
    rfIsLoad = []
    for rf in rfMayaFile:
        rfNode = cmds.referenceQuery(rf, refNode=1)
        if not cmds.referenceQuery(rf, il=1):
            rfIsLoad.append(0)
            continue
        if rf.split('_')[-1].startswith('lay'):
            renFile = '_'.join(rf.split('_')[:-1])+'_ren.'+rf.split('.')[-1]
        elif rf.split('_')[-1].startswith('higRig'):
            renFile = '_'.join(rf.split('_')[:-1])+'_ren.'+rf.split('.')[-1]
        else:
            renFile = rf

        mayaFileDir, mayaFile = os.path.split(rf)[0], os.path.split(rf)[1]
        mayaFileBaseName, MayaType = os.path.splitext(os.path.basename(mayaFile))
        typeDict = {'.ma': "mayaAscii", '.ma{1}': "mayaAscii", '.mb': "mayaBinary",
                    '.mb{1}': "mayaBinary", '.ma{2}': "mayaAscii", '.mb{2}': "mayaBinary"}
        MayaType = typeDict[MayaType]
        if '{' in renFile:
            if os.path.exists(re.sub('{\d}', '', renFile)):
                lprint(u'为{}找寻高级别的最终文件为:{}'.format(rf, renFile))
                cmds.file(renFile, loadReference=rfNode,
                          type=MayaType, options="v=0;p=17;f=0")
                lprint(u'新的引用文件是:{}'.format(cmds.file(r=1, q=1)))
        elif os.path.exists(renFile):
            cmds.file(renFile, loadReference=rfNode,
                      type=MayaType, options="v=0;p=17;f=0")

def is_node_effectively_visible(node):
    """
    检查节点是否有效可见，包括检查所有父节点的可见性
    
    考虑以下因素：
    1. 节点自身的 visibility 属性
    2. 所有父节点的 visibility 属性  
    3. intermediateObject 属性（中间对象通常不可见）
    4. template 属性（模板对象通常不可见）
    5. 显示层的可见性
    
    Args:
        node: 要检查的节点名称
        
    Returns:
        bool: 如果节点有效可见则返回True，否则返回False
    """
    if not cmds.objExists(node):
        return False
        
    # 获取变换节点（如果当前是形状节点）
    original_node = node
    if cmds.nodeType(node) == 'mesh':
        transform_node = cmds.listRelatives(node, parent=True, fullPath=True)
        if transform_node:
            node = transform_node[0]
    
    # 检查intermediateObject属性（对形状节点）
    if cmds.nodeType(original_node) == 'mesh':
        try:
            if cmds.getAttr(original_node + '.intermediateObject'):
                return False
        except:
            pass
    
    # 检查template属性
    try:
        if cmds.getAttr(node + '.template'):
            return False
    except:
        pass
        
    # 检查显示层的可见性
    try:
        display_layers = cmds.listConnections(node + '.drawOverride', type='displayLayer')
        if display_layers:
            for layer in display_layers:
                if not cmds.getAttr(layer + '.visibility'):
                    return False
    except:
        pass

    # 递归检查当前节点及所有父节点的可见性
    current_node = node
    while current_node:
        try:
            # 检查当前节点的visibility属性
            if not cmds.getAttr(current_node + '.visibility'):
                return False
                
            # 获取父节点
            parents = cmds.listRelatives(current_node, parent=True, fullPath=True)
            current_node = parents[0] if parents else None
        except:
            # 如果无法获取可见性属性，认为该节点可见（避免因为属性不存在而误判）
            break
            
    return True

def list_all_children_mesh(nodes,getTrNode=1,includeInvisible=False):
    """Invalid because it will ignore a child if it's in 'nodes'
    whilst it was a child of another node in the list.
    
    Args:
        nodes: 要搜索的节点列表
        getTrNode: 是否返回变换节点而不是形状节点
        includeInvisible: 是否包含不可见节点（考虑父节点和祖节点的可见性）
    """
    lprint(locals())
    nodes = cmds.ls(nodes, long=True)
    
    lookup = set(nodes) # parent lookup   
    hierarchy = cmds.ls(nodes, dag=True, long=True, allPaths=True,type='mesh')
    children = []
    
    for node in hierarchy:   
        if node in lookup:
            # Ignore self
            continue
        if not any(node.startswith(x) for x in lookup):
            # Only include if it has a parent in the original nodes
            continue
            
        # 如果不包含不可见节点，检查可见性
        if not includeInvisible:
            if not is_node_effectively_visible(node):
                continue
                
        children.append(node)
        
    if getTrNode:
        parents=cmds.listRelatives(children,parent=True,fullPath=True)
        if parents:
            children=[x for x in parents if x]
            
        # 如果返回变换节点且不包含不可见节点，再次过滤
        if not includeInvisible:
            children = [child for child in children if is_node_effectively_visible(child)]
            
    return list(set(children))

# 获取与参考节点相关的参考
def getRelatedRefDictOld(refList='B003_S78_chars_wuji_layRN'):# 旧版
    if isinstance(refList,str):
        refList=[refList]
    relateDict={}
    for ref in refList:
        allRef=pm.listReferences()
        processRef=pm.system.FileReference(pathOrRefNode=ref) 
        allCon=pm.listConnections(ref,d=0)
        checkRef=set(allRef)-set([processRef])
        relatedRefs=[]
        for x in allCon:
            cons=x.connections(p=1,d=0)
            if '.sharedReference' not in str(cons) and '_UNKNOWN_REF_NODE_' not in str(x):
                for y in checkRef:
                    refNode=y.refNode
                    if y.namespace in str(cons):
                       relatedRefs.append(y)
        refNodeList=[]
        for x in list(set(relatedRefs)):
            refNodeList.append(str(x.refNode))
        relateDict[ref]=refNodeList
    all_refNodeList=[y for x in relateDict.values() for y in x if x]
    return relateDict,all_refNodeList

def getRelatedRefDict_Old(ref='P001_shoudiantong_RigRN'):
    all_constraint=pm.ls(type='constraint')
    RefNode=pm.ls(ref)[0]
    processRef=pm.system.FileReference(pathOrRefNode=RefNode) 
    nameSpace=processRef.namespace 
    targetNameSpaceList=[]
    relatedRefs=[]
    RefNode_PMList=[]
    for constraint in all_constraint:
        # if ':' in str(constraint):
        #     continue
        try:
            #targetList=constraint.target()
            targetList=pm.listConnections(str(constraint)+'.target')
            targetList=list(set(targetList))
            # lprint ('targetList',targetList)
        except:
            print (traceback.format_exc())
            targetList=[]
            continue
        for target in targetList:
            if ':' in str(target):
                nameSpace=str(target).rsplit(':',1)[0]
                lprint (RefNode)
                if nameSpace in targetNameSpaceList :
                    lprint (nameSpace in targetNameSpaceList)
                    continue
                referenceFile=pm.ls(nameSpace+':*')[0].referenceFile()
                refNode=referenceFile.refNode
                if str(refNode)==ref:
                    continue
                targetNameSpaceList.append(nameSpace)
                relatedRefs.append(referenceFile)
                RefNode_PMList.append('RefNode')
            elif  pm.nodeType(target)=='reference':
                refNode=target
                if str(refNode)==ref:
                    continue
                referenceFile=refNode.referenceFile()
                relatedRefs.append(referenceFile)
                RefNode_PMList.append(RefNode)
                targetNameSpaceList.append(referenceFile.namespace)
                
    targetNameSpaceList = list(set(targetNameSpaceList))
    relatedRefs=list(set(relatedRefs))
    refNodeList=[];relateDict={}
    for x in relatedRefs:
        refNodeList.append(str(x.refNode))
    relateDict[ref]=refNodeList
    all_refNodeList=[y for x in relateDict.values() for y in x if x]
    return relateDict,all_refNodeList,RefNode_PMList,targetNameSpaceList


def getRelatedRefNodes(refNode='luren4:a:C_YouLunLuRen01_RigRN'):
    fosterParents = cmds.listConnections(refNode + ".fosterParent")
    childNode_fosterParents = cmds.listRelatives(fosterParents, c=1) or []
    constraintNodeList = set()
    for childNode in childNode_fosterParents:
        constraintNodes = cmds.listConnections(childNode, s=1, d=0) or []  # 避免None，提供默认空列表
        for constraintNode in constraintNodes:
            if constraintNode != refNode and cmds.nodeType(constraintNode)=="reference":
                constraintNodeList.add(constraintNode)  
    return constraintNodeList

def exMultiAbcFromRefFile(forceStartFrame=None,geometryGroup=['geomrtry']):
    NsKey_RfnAndFileDict=getNsKey_RfnAndFileDict()
    for ns,[RefNode,refFile] in NsKey_RfnAndFileDict.items():
        MayaFileDir=os.path.dirname(cmds.file(q=1,sn=1),MayaFileDir)
        exPath=MayaFileDir+'/'+ns+'.abc'
        GeoExRangeSF=forceStartFrame if forceStartFrame else int(cmds.playbackOptions(q=1,min=1))
        GeoExRangeEF=int(cmds.playbackOptions(q=1,max=1))
        exABC(exPath=exPath, FrameRange=[GeoExRangeSF,GeoExRangeEF], root=[ns+':'+geometryGroup], writeVisibility=1)

@try_exp
def exABC(exPath='*.abc', 
        exAttrs=[], 
        FrameRange='1,2', 
        root=['|group|model_exToH'], 
        writeVisibility=1,
        mayaFile='',
        openNewFile=0,
        Triangulate=False,
        exGroup=True,
        is_nameSgFromMat=False,
        executeImmediately=True):
    '''
    函数参数介绍 :
    exPath            ：   abc导出路径
    exAttrs           ：   字符串列表参数 参数里面的属性会被导出到abc文件
    root              ：   选择要导出的组，可以选择多个组
    FrameRange        ：   导出帧范围
    writeVisibility   ：   是否写出可见性  

    函数功能介绍 ：
    如果属性名称以XYZ结尾，代表要导出三个属性，比如'exAttrs'参数的值为'translateXYZ',则会导出translateX,translateY,translateZ三个属性
    '''
    if openNewFile:
        try:
            print (u'打开文件')
            cmds.file(mayaFile,open=True,ignoreVersion=True,force=True)
        except:
            print (u'打开文件出错{}'.format(traceback.format_exc()))
    lprint (locals(),bool(openNewFile))
    lprint (u'当前打开文件{}'.format(cmds.file(q=1,sn=1)))
    try:
        root=eval(root)
    except:
        pass
    
    root = getGeometryGroupList(root,)
    from l_scripts.l_FX.main import nameSgFromMat
    
    # 包含低模:
    if ':' in root[0]:
        nameSpace= root[0].split(':')[0]
        LOD_GRP = cmds.ls(nameSpace+':*_LOD_GRP')
        if LOD_GRP:
            root += LOD_GRP
    lprint (root)
    FrameRange = FrameRange.replace(',', ' ')
    if not exPath:
        MayaFileBaseName=os.path.basename(cmds.file(q=1,sn=1)).split('.')[0]
        MayaFileDir=os.path.dirname(cmds.file(q=1,sn=1),MayaFileDir)
        exPath=MayaFileDir+'/'+MayaFileBaseName
    ExDir=os.path.dirname(exPath) if exPath.endswith('.abc') else exPath
    if not os.path.exists(ExDir):
        os.makedirs(ExDir)
    cmd_read='attrib -r {}'.format(exPath)
    os.system(cmd_read)
    loadPluginFunc('AbcExport.mll')
    _exAttrs = ''
    for att in exAttrs:
        if att.endswith('XYZ'):
            for i in 'XYZ':
                _exAttrs = _exAttrs+' -attr '+att.split('_')[0]+i+' '
        else:
            _exAttrs = ' -attr '+att+_exAttrs
    rootpath = ''

    if Triangulate:
        cmds.polyTriangulate(root, ch=1)
    
    for _root in root:
        if _root:
            # 选择组导出经常会出问题,因此每个模型都作为一个rootpath
            children_mesh=list_all_children_mesh(_root,getTrNode=1,includeInvisible=False)
            usualLib.cvtFaceSetSG(children_mesh)
            if is_nameSgFromMat:
                    cmds.select(root)
                    print(u"转分面材质")
                    nameSgFromMat(children_mesh,False)
            for child in children_mesh:
                if Triangulate:
                    try:
                        cmds.polyTriangulate(child, ch=1)
                    except Exception as e:
                        lprint (u'三角化节点{}错误,原因是{}'.format(child,e))
                if not exGroup:
                    rootpath = rootpath+' -root '+child
            if exGroup:
                rootpath = rootpath+' -root '+_root
    lprint(rootpath, 'rootpath')
    if writeVisibility:
        writeVisibilityCmd = '-writeVisibility'
    else:
        writeVisibilityCmd = ''
    lprint(FrameRange)
    sf,ef=FrameRange.split(" ")
    total_frame = int(ef) - int(sf)
    command = ('-frameRange {}  {} -stripNamespaces -writeVisibility -uvWrite -worldSpace {} -writeFaceSets {} '+\
    '-pythonPerFrameCallback \"from __future__ import print_function;print(str(cmds.currentTime(q=1))+{},end=\\\"\\\\r\\\")\" -file \"{}\"'\
        ).format(
        FrameRange, _exAttrs, writeVisibilityCmd, rootpath, repr("/{} {}".format(ef,exPath)), exPath)
    lprint(command, 'command',force_print=True)
    try:
        if executeImmediately:
            cmds.AbcExport(j=command)
    except:
        if not LM.isMayaPyEnv():
            from PySide2.QtWidgets import QApplication, QMessageBox
            if QApplication.instance() is None:
                app = QApplication([])
            # 显示警告对话框
            lprint (traceback.format_exc())
            QMessageBox.warning(None, u'警告', u"导出失败,文件{}被程序占用,".format(exPath)+
                                u"解除占用后再点OK可以继续,否则导出将会终止,报错是{}".
                                format(traceback.format_exc()))
            if executeImmediately:
                cmds.AbcExport(j=command)
        else:
            lprint(u"导出失败,文件{}被程序占用,".format(exPath)+
                                u"解除占用后再点OK可以继续,否则导出将会终止,报错是{}".
                                format(traceback.format_exc()),force_print=True)
    return command
    print ('\n export abc {} finished'.format(exPath))


@try_exp
def batch_exABCfromGroup(
        exPathList=[],  
        exAttrs=[], 
        FrameRange='1,2', 
        rootList=[['|group|model_exToH']], # 接受节点列表[[]]这样的形式
        writeVisibility=1,
        mayaFile='',
        openNewFile=0,
        Triangulate=False,
        exGroup=True,
        rootIsPerObjEx=True,
        is_nameSgFromMat=True,
        executeImmediately=True):
    '''
    函数参数介绍 :
    exPathList        ：   abc导出路径列表
    exAttrs           ：   字符串列表参数 参数里面的属性会被导出到abc文件
    rootList          ：   选择要导出的组列表，可以选择多个组 [[group1, group2], [group3]]
    FrameRange        ：   导出帧范围
    writeVisibility   ：   是否写出可见性
    mayaFile          ：   要打开的Maya文件路径
    openNewFile       ：   是否打开新文件
    Triangulate       ：   是否三角化模型
    exGroup           ：   是否按组导出
    rootIsPerObjEx    ：   是否按对象分别导出
    is_nameSgFromMat  ：   是否根据材质创建分面（默认True）

    函数功能介绍 ：
    如果属性名称以XYZ结尾，代表要导出三个属性，比如'exAttrs'参数的值为'translateXYZ',则会导出translateX,translateY,translateZ三个属性
    支持批量导出多个ABC文件，每个文件对应rootList中的一个根节点组合
    '''
    lprint(locals())
    if openNewFile:
        try:
            print (u'打开文件')
            cmds.file(mayaFile,open=True,ignoreVersion=True,force=True)
        except:
            print (u'打开文件出错{}'.format(traceback.format_exc()))
    lprint (locals(),bool(openNewFile))
    lprint (u'当前打开文件{}'.format(cmds.file(q=1,sn=1)))
    try:
        root=eval(root)
    except:
        pass

    # root = getGeometryGroupList(root,)

    # # 包含低模:
    # if ':' in root[0]:
    #     nameSpace= root[0].split(':')[0]
    #     LOD_GRP = cmds.ls(nameSpace+':*_LOD_GRP')
    #     if LOD_GRP:
    #         root += LOD_GRP
    # lprint (root)
    FrameRange = FrameRange.replace(',', ' ')

    for exPath in exPathList:
        ExDir=os.path.dirname(exPath)
        if not os.path.exists(ExDir):
            os.makedirs(ExDir)
        if os.path.exists(exPath):
            cmd_read='attrib -r {}'.format(exPath)
            os.system(cmd_read)
    loadPluginFunc('AbcExport.mll')
    _exAttrs = ''
    for att in exAttrs:
        if att.endswith('XYZ'):
            for i in 'XYZ':
                _exAttrs = _exAttrs+' -attr '+att.split('_')[0]+i+' '
        else:
            _exAttrs = ' -attr '+att+_exAttrs

    if writeVisibility:
        writeVisibilityCmd = '-writeVisibility'
    else:
        writeVisibilityCmd = ''

    commandList=[]
    root_list=[]
    for i,root_children in enumerate(rootList):
        # 选择组导出经常会出问题,因此每个模型都作为一个rootpath
        root_path=''
        for root in root_children:
            children_mesh=list_all_children_mesh(root,getTrNode=1,includeInvisible=False)
            usualLib.cvtFaceSetSG(children_mesh)
            
            # 材质分面处理
            if is_nameSgFromMat and children_mesh:
                from l_scripts.l_FX.main import nameSgFromMat
                cmds.select(children_mesh)
                lprint(u"执行材质分面转换")
                nameSgFromMat(children_mesh, False)
            
            if rootIsPerObjEx:
                for child in children_mesh:
                    child=cmds.ls(child,long=1)[0]
                    if child in root_list:
                        continue
                    root_list.append(child) 
                    if cmds.getAttr(child+'.visibility')==False:
                        continue
                    if Triangulate:
                        try:
                            cmds.polyTriangulate(child, ch=1)
                        except Exception as e:
                            lprint (u'三角化节点{}错误,原因是{}'.format(child,e))
                    root_path+="-root {} ".format(cmds.ls(child,l=1)[0])
            else:
                root_path+="-root {} ".format(cmds.ls(root,l=1)[0])
        command = '-frameRange {} {} -stripNamespaces -writeVisibility -uvWrite -writeColorSets -writeFaceSets -worldSpace  -writeUVSets  -dataFormat ogawa {} -file \"{}\"' .format(
            FrameRange, _exAttrs, root_path,exPathList[i].replace('\\', '/'))
        commandList.append(command)

    lprint('commandList', str(commandList)[:500],len(commandList))
    try:
        if executeImmediately:
            cmds.AbcExport(j=commandList)
    except Exception as e:
        if 'Conflicting root node names specified' in str(e):
            ref_file = cmds.referenceQuery(rootList[0][0], filename=True)
            cmds.file(ref_file, importReference=True)
            mps.usualSmallToolM.renameDuplicates()
            if executeImmediately:
                cmds.AbcExport(j=commandList)
        from PySide2.QtWidgets import QApplication, QMessageBox
        if QApplication.instance() is None:
            app = QApplication([])
        # 显示警告对话框
        lprint (traceback.format_exc())
        QMessageBox.warning(None, u'警告', u"导出失败,文件{}被程序占用,".format(exPath)+
                            u"解除占用后再点OK可以继续,否则导出将会终止,报错是{}".
                            format(traceback.format_exc()))
        if executeImmediately:
            cmds.AbcExport(j=command)
    return command
    lprint ('export finished')


@try_exp
def exABC_unified(
    exPath=None,               # 单文件路径（兼容旧exABC接口）
    exPathList=None,           # 批量路径列表
    root=None,                 # 单根节点列表（兼容旧exABC接口）
    rootList=None,             # 批量根节点列表 [[]]
    exAttrs=[],                # 导出属性列表
    FrameRange='1,2',          # 帧范围
    writeVisibility=1,         # 是否写出可见性
    mayaFile='',               # Maya文件路径
    openNewFile=0,             # 是否打开新文件
    Triangulate=False,         # 是否三角化
    exGroup=True,              # 是否按组导出
    is_nameSgFromMat=False,    # 是否根据材质分面
    rootIsPerObjEx=True,       # 是否按对象导出
    include_LOD=True,          # 是否包含LOD组
    show_progress=False,       # 是否显示进度
    batch_mode=None            # 批量模式（自动检测）
):
    """
    统一的ABC导出函数 - 合并了exABC和batch_exABCfromGroup的功能
    
    参数说明：
    exPath            : 单文件导出路径（与root配合使用）
    exPathList        : 批量导出路径列表
    root              : 单个根节点列表
    rootList          : 批量根节点列表 [[group1, group2], [group3]]
    exAttrs           : 要导出的属性列表
    FrameRange        : 导出帧范围 '1,100'
    writeVisibility   : 是否写出可见性
    mayaFile          : 要打开的Maya文件路径
    openNewFile       : 是否打开新文件
    Triangulate       : 是否三角化模型
    exGroup           : 是否按组导出（False则按对象导出）
    is_nameSgFromMat  : 是否根据材质创建分面
    rootIsPerObjEx    : 是否按对象分别导出
    include_LOD       : 是否自动包含LOD组
    show_progress     : 是否显示导出进度
    batch_mode        : 强制指定批量模式（None=自动检测）
    
    使用示例：
    # 单文件导出（兼容原exABC）
    exABC_unified(exPath='test.abc', root=['|group1'])
    
    # 批量导出（兼容原batch_exABCfromGroup）
    exABC_unified(exPathList=['a.abc', 'b.abc'], rootList=[['|grp1'], ['|grp2']])
    """
    lprint('=== exABC_unified 开始导出 ===')
    lprint(locals())
    
    # 自动检测批量模式
    if batch_mode is None:
        batch_mode = bool(exPathList and rootList)
    
    # 参数兼容性处理
    if not batch_mode:
        # 单文件模式 - 兼容原exABC接口
        if exPath and root:
            exPathList = [exPath]
            rootList = [root if isinstance(root, list) else [root]]
        else:
            raise ValueError("单文件模式需要提供exPath和root参数")
    else:
        # 批量模式验证
        if not exPathList or not rootList:
            raise ValueError("批量模式需要提供exPathList和rootList参数")
        if len(exPathList) != len(rootList):
            raise ValueError("exPathList和rootList长度必须相等")
    
    # 打开新文件
    if openNewFile and mayaFile:
        try:
            lprint(u'打开文件: {}'.format(mayaFile))
            cmds.file(mayaFile, open=True, ignoreVersion=True, force=True)
        except Exception as e:
            lprint(u'打开文件失败: {}'.format(str(e)))
    
    lprint(u'当前打开文件: {}'.format(cmds.file(q=1, sn=1)))
    
    # 处理帧范围
    FrameRange = FrameRange.replace(',', ' ')
    sf, ef = FrameRange.split()
    
    # 创建导出目录
    for exPath in exPathList:
        ExDir = os.path.dirname(exPath)
        if not os.path.exists(ExDir):
            os.makedirs(ExDir)
        if os.path.exists(exPath):
            cmd_read = 'attrib -r "{}"'.format(exPath)
            os.system(cmd_read)
    
    # 加载ABC导出插件
    loadPluginFunc('AbcExport.mll')
    
    # 处理导出属性
    _exAttrs = ''
    for att in exAttrs:
        if att.endswith('XYZ'):
            for i in 'XYZ':
                _exAttrs = _exAttrs + ' -attr ' + att.split('_')[0] + i + ' '
        else:
            _exAttrs = ' -attr ' + att + _exAttrs
    
    # 可见性参数
    writeVisibilityCmd = '-writeVisibility' if writeVisibility else ''
    
    # 构建导出命令列表
    commandList = []
    processed_roots = []  # 避免重复处理
    
    for i, (exPath, root_children) in enumerate(zip(exPathList, rootList)):
        lprint(u'处理第{}个导出任务: {} -> {}'.format(i+1, root_children, exPath))
        
        # 处理根节点
        try:
            if isinstance(root_children, str):
                root_children = eval(root_children)
        except:
            pass
        
        if not isinstance(root_children, list):
            root_children = [root_children]
        
        # 获取几何体组
        if not batch_mode or include_LOD:
            root_children = getGeometryGroupList(root_children)
            
            # 包含LOD组（仅单文件模式或明确启用时）
            if include_LOD and root_children and ':' in str(root_children[0]):
                nameSpace = str(root_children[0]).split(':')[0]
                LOD_GRP = cmds.ls(nameSpace + ':*_LOD_GRP')
                if LOD_GRP:
                    root_children += LOD_GRP
        
        lprint(u'最终根节点列表: {}'.format(root_children))
        
        # 构建根路径
        root_path = ''
        for root in root_children:
            if not root:
                continue
                
            # 获取子mesh
            children_mesh = list_all_children_mesh(root, getTrNode=1,includeInvisible=False)
            usualLib.cvtFaceSetSG(children_mesh)
            
            # 材质分面处理
            if is_nameSgFromMat and children_mesh:
                from l_scripts.l_FX.main import nameSgFromMat
                cmds.select(children_mesh)
                lprint(u"执行材质分面转换")
                nameSgFromMat(children_mesh, False)
            
            # 三角化处理
            if Triangulate:
                try:
                    cmds.polyTriangulate(root, ch=1)
                except Exception as e:
                    lprint(u'三角化根节点{}失败: {}'.format(root, str(e)))
            
            # 根据导出模式构建路径
            if rootIsPerObjEx and batch_mode:
                # 批量模式：按对象分别导出
                for child in children_mesh:
                    child = cmds.ls(child, long=1)[0]
                    
                    # 避免重复处理
                    if child in processed_roots:
                        continue
                    processed_roots.append(child)
                    
                    # 跳过不可见对象
                    if not cmds.getAttr(child + '.visibility'):
                        continue
                    
                    # 三角化子对象
                    if Triangulate:
                        try:
                            cmds.polyTriangulate(child, ch=1)
                        except Exception as e:
                            lprint(u'三角化子对象{}失败: {}'.format(child, str(e)))
                    
                    root_path += '-root {} '.format(cmds.ls(child, l=1)[0])
            else:
                # 单文件模式或按组导出
                if exGroup:
                    root_path += '-root {} '.format(cmds.ls(root, l=1)[0])
                else:
                    # 按子对象导出
                    for child in children_mesh:
                        if Triangulate:
                            try:
                                cmds.polyTriangulate(child, ch=1)
                            except Exception as e:
                                lprint(u'三角化子对象{}失败: {}'.format(child, str(e)))
                        root_path += '-root {} '.format(child)
        
        # 构建导出命令
        if show_progress and not batch_mode:
            # 单文件模式显示进度
            progress_callback = '-pythonPerFrameCallback "from __future__ import print_function;print(str(cmds.currentTime(q=1))+{},end=\\"\\\\r\\")"'.format(
                repr("/{} {}".format(ef, exPath)))
            command = '-frameRange {} {} -stripNamespaces {} -uvWrite -worldSpace -writeFaceSets {} {} -file "{}"'.format(
                FrameRange, _exAttrs, writeVisibilityCmd, progress_callback, root_path, exPath.replace('\\', '/'))
        else:
            # 批量模式或无进度显示
            command = '-frameRange {} {} -stripNamespaces {} -uvWrite -writeColorSets -writeFaceSets -worldSpace -writeUVSets -dataFormat ogawa {} -file "{}"'.format(
                FrameRange, _exAttrs, writeVisibilityCmd, root_path, exPath.replace('\\', '/'))
        
        commandList.append(command)
        lprint(u'导出命令 {}: {}'.format(i+1, command[:200] + '...' if len(command) > 200 else command))
    
    # 执行导出
    lprint(u'开始执行ABC导出，共{}个文件'.format(len(commandList)))
    try:
        if len(commandList) == 1:
            # 单文件导出
            cmds.AbcExport(j=commandList[0])
        else:
            # 批量导出
            cmds.AbcExport(j=commandList)
            
    except Exception as e:
        error_msg = str(e)
        lprint(u'ABC导出失败: {}'.format(error_msg))
        
        # 处理特定错误
        if 'Conflicting root node names specified' in error_msg and rootList:
            lprint(u'检测到根节点名称冲突，尝试导入引用并重命名')
            try:
                ref_file = cmds.referenceQuery(rootList[0][0], filename=True)
                cmds.file(ref_file, importReference=True)
                # 假设存在重命名重复项的函数
                # mps.usualSmallToolM.renameDuplicates()
                lprint(u'引用导入完成，重新尝试导出')
                cmds.AbcExport(j=commandList)
            except Exception as e2:
                lprint(u'引用导入失败: {}'.format(str(e2)))
                raise e
        else:
            # 其他错误处理
            if not LM.isMayaPyEnv():
                try:
                    from PySide2.QtWidgets import QApplication, QMessageBox
                    if QApplication.instance() is None:
                        app = QApplication([])
                    
                    QMessageBox.warning(None, u'ABC导出警告', 
                                      u"导出失败，可能是文件被占用。\n"
                                      u"请检查目标文件是否被其他程序使用。\n"
                                      u"错误信息：{}".format(error_msg))
                except:
                    pass
            
            # 重新抛出异常
            raise e
    
    # 导出完成
    for exPath in exPathList:
        lprint(u'ABC导出完成: {}'.format(exPath))
    
    lprint('=== exABC_unified 导出完成 ===')
    return exPathList


# 向后兼容的包装函数
def exABC_legacy(exPath='*.abc', 
        exAttrs=[], 
        FrameRange='1,2', 
        root=['|group|model_exToH'], 
        writeVisibility=1,
        mayaFile='',
        openNewFile=0,
        Triangulate=False,
        exGroup=True,
        is_nameSgFromMat=False):
    """
    原exABC函数的兼容包装 - 调用统一函数
    保持原有接口不变，内部使用新的统一函数
    """
    return exABC_unified(
        exPath=exPath,
        exAttrs=exAttrs,
        FrameRange=FrameRange,
        root=root,
        writeVisibility=writeVisibility,
        mayaFile=mayaFile,
        openNewFile=openNewFile,
        Triangulate=Triangulate,
        exGroup=exGroup,
        is_nameSgFromMat=is_nameSgFromMat,
        show_progress=True,  # 原函数默认显示进度
        batch_mode=False     # 强制单文件模式
    )


def batch_exABCfromGroup_legacy(
        exPathList=[],  
        exAttrs=[], 
        FrameRange='1,2', 
        rootList=[['|group|model_exToH']], 
        writeVisibility=1,
        mayaFile='',
        openNewFile=0,
        Triangulate=False,
        exGroup=True,
        rootIsPerObjEx=True,
        is_nameSgFromMat=True):
    """
    原batch_exABCfromGroup函数的兼容包装 - 调用统一函数
    保持原有接口不变，内部使用新的统一函数
    """
    return exABC_unified(
        exPathList=exPathList,
        rootList=rootList,
        exAttrs=exAttrs,
        FrameRange=FrameRange,
        writeVisibility=writeVisibility,
        mayaFile=mayaFile,
        openNewFile=openNewFile,
        Triangulate=Triangulate,
        exGroup=exGroup,
        rootIsPerObjEx=rootIsPerObjEx,
        is_nameSgFromMat=is_nameSgFromMat,  # 传递材质分面参数
        include_LOD=False,   # 原批量函数不包含LOD
        show_progress=False, # 原批量函数不显示进度
        batch_mode=True      # 强制批量模式
    )


@try_exp
def exAniClip_Simple(mayaFile='',moveSkeToRoot=False,openFile=True,JntGroup='UnrealRoot',GeometryGroup='geometry'):
    lprint (locals())
    cmds.dirmap(en=1)
    cmds.dirmap(m=(r'H:\\', r'G:\\'))
    try:
        moveSkeToRoot=eval(moveSkeToRoot)
    except:
        pass
    
    if not mayaFile: # 针对已经打开的Maya文件
        mayaFile=cmds.file(q=1,sn=1)
    
    if mayaFile and openFile:#针对没有打开Maya文件时
        lprint (u"打开文件{}".format(mayaFile))
        try:
            cmds.file(mayaFile, f=True, o=True)
        except:
            traceback.print_exc()

    lprint  (u'从{}导出动画资产--'.format(mayaFile))
    mayaFileBaseName=os.path.basename(mayaFile).split('.')[0]
    exDir=os.path.dirname(mayaFile)+'\\'+mayaFileBaseName
    exDir=exDir.replace('\\','/')
    lprint (exDir)
    os.system('cmd /c mkdir "{}"'.format(os.path.normpath(exDir)))
    cameraTrNodeList=findCamera()
    if  cameraTrNodeList:
        cameraTrNode=cameraTrNodeList[0]
    loadPluginFunc('mtoa.mll')
    loadPluginFunc('xgenToolkit.mll')
    loadPluginFunc('mayaHIK.mll')
    try:
        GeoExRangeSF = int(cameraTrNode.split('_')[-2])
        GeoExRangeEF = int(cameraTrNode.split('_')[-1])
    except:
        # GeoExRangeSF=int(cmds.playbackOptions(q=1,min=1))
        GeoExRangeSF = 50
        GeoExRangeEF=int(cmds.playbackOptions(q=1,max=1))
    if cameraTrNodeList:
        exCamera(mayaFile,exDir=exDir,sf=GeoExRangeSF,ef=GeoExRangeEF,cameraTrNode=cameraTrNode)
    NsRfnAndFileDict=getNsKey_RfnAndFileDict()
    lprint (NsRfnAndFileDict)
    bakeKeys=True;isStaticGeo=False
    for nameSpace,refInfo in NsRfnAndFileDict.items():
        try:
            refFile=refInfo["refFile"]
            RefNode=refInfo["refNode"]
            refNode_Exist=refInfo["refNode_Exist"]
            try:
                if not cmds.referenceQuery(RefNode,il=1):
                    lprint (u'引用节点{}未加载,跳过导出'.format(RefNode))
                    continue
                if not refNode_Exist:
                    lprint (u'引用节点{}不存在,跳过导出'.format(RefNode))
                    continue
            except:
                traceback.print_exc()
                continue
            lprint (nameSpace,RefNode,refFile)  
            savePath=os.path.join(exDir,nameSpace+'_AniGeo.fbx')
            skeAniExPath=os.path.join(exDir,nameSpace+'_ani.fbx')
            JntGroup_ins='{}:{}'.format(nameSpace,JntGroup)
            geometryGroupList=['{}:{}'.format(nameSpace,GeometryGroup)]
            lprint (JntGroup_ins)
            try:
                exFBX(JntGroup=JntGroup_ins,
                    geometryGroupList= geometryGroupList, 
                    skeAniExPath=skeAniExPath, 
                    moveSkeToRoot=moveSkeToRoot,
                    bakeKeys=bakeKeys, 
                    isStaticGeo=False,
                    refFile=refFile, 
                    sf=GeoExRangeSF,
                    ef=GeoExRangeEF,
                    exSkelonAnim=True)
                lprint (u'导出动画资产--{}\n--{}完成\n'.format(savePath,skeAniExPath))
            except Exception as e:
                lprint (u'导出名称空间{}--文件路径--{}失败,原因是:\n'.format(nameSpace,savePath))
                traceback.print_exc()
        except:
            traceback.print_exc()
    print ("导出完毕,请关闭窗口")       


def exAbc_Batch(mayaFile='',
                moveSkeToRoot=False,
                startFrame=80,
                geoGroup='nameSpace:*_geometry_Grp',
                openNewFile=False,
                isExCamera=False,
                rootIsPerObjEx=True,
                post_extra_frame=3,
                *args,
                **kwargs):
    lprint  (u'导出动画资产--')
    lprint(locals())

    if not mayaFile: # 针对已经打开的Maya文件
        mayaFile=cmds.file(q=1,sn=1)

    if mayaFile and openNewFile:#针对没有打开Maya文件时
        try:
            cmds.file(mayaFile, f=True, o=True,ignoreVersion=True)
        except:
            traceback.print_exc()

    mayaFileBaseName=os.path.basename(mayaFile).split('.')[0]
    exDir=os.path.dirname(mayaFile)+'/{}'.format(mayaFileBaseName)
    exDir=exDir.replace('\\','/')
    os.system('cmd /c mkdir "{}"'.format(os.path.normpath(exDir)))
    time_unit = cmds.currentUnit(query=True, time=True)
    frame_rate_mapping = {
        "game": 15,
        "film": 24,
        "pal": 25,
        "ntsc": 30,
        "show": 48,
        "palf": 50,
        "ntscf": 60
    }
    lprint(frame_rate_mapping.get(time_unit, None))
    GeoExRangeSF = startFrame
    GeoExRangeEF=int(cmds.playbackOptions(q=1,max=1))+post_extra_frame
    lprint(cmds.playbackOptions(q=1,max=1))
    lprint(GeoExRangeSF,GeoExRangeEF)
    import maya.mel as mel
    lprint(int(mel.eval('playbackOptions -q -maxTime')))
    import maya.api.OpenMayaAnim as oma2

    animationEndTime = oma2.MAnimControl.animationEndTime() # アニメーションの終了フレーム
    print("animationEndTime   = {} - {}".format(animationEndTime, animationEndTime.asUnits(animationEndTime.uiUnit())))

    if isExCamera:
        exCameraTrList,savePath_list=exCamera(mayaFile,exDir=exDir,sf=GeoExRangeSF,ef=GeoExRangeEF)
        lprint(exCameraTrList,savePath_list)
        for i,cameraTrNode in enumerate(exCameraTrList):
            exPath=savePath_list[i].replace('.fbx','.abc')
            exAbcCamera(frameRange=[GeoExRangeSF,GeoExRangeEF],root=cameraTrNode,exPath=exPath)
    NsRfnAndFileDict=getNsKey_RfnAndFileDict()
    lprint(NsRfnAndFileDict)
    bakeKeys=True;exDeformGeo=True;isStaticGeo=False
    exPathList=[];rootList=[]
    for nameSpace,RefInfo in NsRfnAndFileDict.items():
        RefNode=RefInfo.get("refNode")
        refFile=RefInfo.get("refFile")
        if not cmds.referenceQuery(RefNode,il=1):
            lprint (u'引用节点{}未加载,跳过导出'.format(RefNode))
            continue
        geometryGroupList=cmds.ls(geoGroup.replace('nameSpace',nameSpace),type='transform')
        lprint (u'找到{}个组'.format(len(geometryGroupList)),geometryGroupList)
        if geometryGroupList:
            rootList.append(geometryGroupList)
            lprint (nameSpace,RefNode,refFile)  
            savePath=os.path.join(exDir,nameSpace+'.abc').replace('\\','/')
            exPathList.append(savePath)
    try:
        batch_exABCfromGroup(  
                exPathList=exPathList,
                FrameRange="{},{}".format(GeoExRangeSF,GeoExRangeEF),
                rootList=rootList,
                openNewFile=True,
                rootIsPerObjEx=rootIsPerObjEx)
        # lprint (u'导出动画资产--{}--{}完成\n'.format(nameSpace,savePath,))
    except Exception as e:
        # lprint (u'导出名称空间--{}失败,原因是:\n'.format(nameSpace,savePath,))
        lprint (traceback.print_exc())

def exAbcCamera(frameRange=["0","100"],exPath="",root="" ):
    lprint(locals())
    frameRange=[str(x) for x in frameRange]
    root=cmds.ls(root,long=True)[0]
    if cmds.nodeType(root)=="camera":
        root=cmds.listRelatives(root,p=1)[0]
    exPath_dir=os.path.dirname(exPath)
    if not os.path.exists(exPath_dir):
        os.makedirs(exPath_dir)
    cmd="-frameRange {} -worldSpace -dataFormat ogawa ".format(' '.join(frameRange))+\
                    "-root {} -file \"{}\"".format(root,exPath)
    lprint (cmd)
    loadPluginFunc('AbcExport.mll')
    cmds.AbcExport(j=cmd)


@try_exp
def exAniClip_exTpose(mayaFile='',ExHistoryFile='',refFile='',AssetType_Zh='',
                    recordProcedureFile='',mayaPyExeFile='',JntGroup='',geometryGroupList='',moveSkeToRoot='',
                    exDeformGeo='',savePath='',openMayaFile=True,
                    isStaticGeo='',GeoExRangeSF='',upAxis='',batFile='',oriEnvVarDict='',logFile='',LowModName='',
                    **kwargs):
    
    # batFile=os.path.join(TempDir,nameSpace+'_exTpose.bat')

    exSkelonAnim = False
    exSkelelonMesh=True
    # lprint  (locals())
    locals_var=copy.deepcopy(locals())
    locals_var["mayaFile"]=refFile
    # 使用列表推导式找到所有值是字典的键
    keys_to_remove = [key for key, value in locals_var.items() if isinstance(value, dict)]
    # 删除找到的所有子字典
    for key in keys_to_remove:
        del locals_var[key]

    cmdStr=u''
    for x,y in locals_var.items():
        if ' ' in repr(y):
            y=u'"{}"'.format(y)
        lprint (y)
        cmdStr+=u' --{} {}'.format(x,y)
    run_exFbxFile=os.path.join(LugwitPath,'mayaPlug/l_scripts/Callpyd/run_exFbx.py')
    run_exFbxFile=run_exFbxFile.replace('\\','/')
    runList=['"'+mayaPyExeFile+'"',
        run_exFbxFile,'exFBX',
        re.sub(r' {2,}',' ',cmdStr)]
    
    
    with codecs.open(batFile,'w','utf-8') as f:
        cmdStr=' '.join(runList)
        cmdStr = 'set pythonpath=""\n'+cmdStr
        f.write(cmdStr)
    cmd=u'cmd/c {}'.format(os.path.normpath(batFile))
    lprint (cmd)
    
    isExByExHistory,ExHistoryDict,ori_ExHistoryDict=\
    ExHistoryFromMaya.isExFileAndRecordHistoryFunc(savePath,
            mayaFile=mayaFile,ExHistoryFile=ExHistoryFile,
            refFile=refFile,query=True)
    lprint (u'Tpose文件{}是否导出:{}'.format(savePath,isExByExHistory))
    
    deleteGroup=''
    if AssetType_Zh==repr(u'角色'):
        deleteGroup='Group'
    with codecs.open(recordProcedureFile, 'r', encoding='utf-8') as f:
        content=json.load(f)
        lprint (content)
        if savePath in content and os.path.exists(savePath):
            return
    with codecs.open(recordProcedureFile, 'w', encoding='utf-8') as f:
        content.append(savePath)
        lprint (content)
        json.dump(content, f, ensure_ascii=False, indent=4)

    jsonParmFile=os.environ.get('Temp')+'/'+os.path.basename(mayaFile).rsplit('.',1)[0]+'_exTpose_jsonParm.json'


    isExByExHistory,ExHistoryDict,ori_ExHistoryDict = \
        ExHistoryFromMaya.isExFileAndRecordHistoryFunc( savePath,
            mayaFile='',ExHistoryFile=ExHistoryFile,refFile=refFile,query=False )
    lprint (u'文件{}导出历史,返回Ture表示要重新导出',savePath,isExByExHistory)
    lprint (runList)
    
    
    logFileDir=os.path.dirname(logFile)
    if not os.path.exists(logFileDir):
        os.makedirs(logFileDir)
    with codecs.open(logFile,'w',encoding='utf-8') as f:
        json.dump(oriEnvVarDict,f,indent=2,ensure_ascii=False)
        process=subprocess.Popen(cmd,
                        shell=True,
                        stdout=f,
                        stderr=f,
                        env = oriEnvVarDict)
    return process

def get_rig_cameras():
    camCtl_index = cmds.getAttr("RigCam_rig:Cam_Con_G_con.SheXiangJiKongZhiQiXiangShi")
    tarCons = cmds.listConnections("RigCam_rig:Cam_Con_G_con.SheXiangJiKongZhiQiXiangShi", s=0)
    camVisNode = tarCons[camCtl_index]
    camTr_ParNode = cmds.listConnections(camVisNode + ".output", s=0)[0]
    
    cameras = [node for node in (cmds.listRelatives(camTr_ParNode, allDescendents=True, fullPath=True) or []) if cmds.nodeType(node) == 'camera']
    if cameras:
        return cameras[0]

# NOTE 导出动画片段
def exAniClip(mayaFile='',openNewFile=1,
              ExShotDir='',upToP4=0,description="备注信息",genMiddleFile=0,isP4File='',
              cameraTrNode='',**kwargs):
    '''
    ani/group/geometry
    cusCfg参数说明：为真时会给用让用户手动选择如何渲染文件
    '''
    if not os.path.exists(mayaFile):
        mayaFile=mayaFile.replace('D:/H','G:')
    lprint  (u'导出动画资产,exAniClip',)
    oriEnvVarFile = os.environ.get('oriEnvVarFile')
    lprint (oriEnvVarFile)
    with codecs.open(oriEnvVarFile, 'r', 'utf-8') as f:
        oriEnvVarDict = json.load(f)
        tempDict={}
        for key,val in oriEnvVarDict.items():
            tempDict[str(key)]=str(val)
        oriEnvVarDict = tempDict
    LugwitToolDir=os.environ.get('LugwitToolDir')
    env=copy.deepcopy(oriEnvVarDict)
    for key,val in os.environ.items():
        env[str(key)]=str(val)
    DingDing=LugwitToolDir+r'\Lib\Lugwit_Module\l_src\DingDing'

    env.update({'PYTHONHOME':r'D:\TD_Depot\plug_in\Python\Python39',
         'PYTHONPATH':r'D:\TD_Depot\plug_in\Python\Python39\Lib;{}'.format(DingDing)})
    #sys.exit(0)
    #如果没有提供maya文件则在系统变量中去寻找,一般在最后一项
    if not mayaFile:
        mayaFile = repr(sys.argv[-1]).replace('"','').replace("'",'')
    lprint (u'获取Maya文件{}'.format(mayaFile))
    
    if isP4File:
        P4Lib.getFile(mayaFile) 
    # get_rig_cameras()
    mayaFile=mayaFile.replace('\\\\','/');#里面可能有四个'\\\\'
    mayaFile=mayaFile.replace('\\','/')
    mayaFile=mayaFile.replace('//','/')
    lprint(u'\nyou process maya file is :{}'.format(mayaFile))
    mayaFileBaseName=os.path.basename(mayaFile).rsplit('.',1)[0]
    isReplaceHigRig= False


    lprint  (u'导出动画资产--')
    loadPluginFunc('mtoa.mll')
    loadPluginFunc('xgenToolkit.mll')
    loadPluginFunc('mayaHIK.mll')
    
    #导出的备注信息
    if description:
        if os.path.isfile(description):
            with codecs.open(description,'r','utf-8') as f:
                exInfoDict=json.load(f)
                infoConfig_oriDict=exInfoDict["ExSetingDict"]['infoFromExConfigJsonFile_oriDict']
            del exInfoDict["ExSetingDict"]['infoFromExConfigJsonFile_oriDict']
            exInfoDict_flat=json_read.flatDict(exInfoDict)
            lprint (exInfoDict_flat)
            descriptionText=exInfoDict_flat['comment']
            lprint (u'从文件 {} 读取导出信息'.format(description))

            ex_camera = exInfoDict["camera"][0]
            exNameSpace_desc= exInfoDict["nameSpace"]
            CameraFbxExPath=exInfoDict_flat["CameraFbxExPath"]
            exCameraList_desc=exInfoDict_flat["exCameraList"]
            exTimeRange_desc=exInfoDict_flat["exTimeRange"]
            extraExportTimeRange=exInfoDict_flat["extraExportTimeRange"]
            atDingTalk_desc=exInfoDict_flat["@dingTalk"]
            ExExplanation=exInfoDict_flat["ExExplanation"]

            exFileStartFrame = infoConfig_oriDict.get('exFileStartFrame')
            isExSkeAniFile = exInfoDict_flat["isExSkeAniFile"]
            moveSkeToRoot= exInfoDict_flat["moveSkeToRoot"]
            AniFbxExDir_Sim = infoConfig_oriDict.get('AniFbxExDir_Sim')
            
            isGenMayaCheckFile = exInfoDict_flat["isGenMayaCheckFile"]
            isGenMayaCheckVideoFile = exInfoDict_flat["isGenMayaCheckVideoFile"]
            is_useExistExFile = exInfoDict_flat["is_useExistTposeFbxFile"]
            onlyLoadNeededRef = exInfoDict_flat.get("onlyLoadNeededRef",True)
            recordProcedureFile = exInfoDict_flat['RecordProcedureFile']
            houdiniSim_SF = infoConfig_oriDict.get('houdiniSim_SF',0)
            department= exInfoDict_flat.get(u'部门',[])
            LowModName = exInfoDict_flat.get('LowModName','')

            
            
            
            ExHistoryFile=exInfoDict_flat['ExHistoryFile']
            if not os.path.exists(os.path.dirname(ExHistoryFile)):
                os.system('cmd /c mkdir "{}"'.format(os.path.dirname(ExHistoryFile)))

            JntGroup      = exInfoDict_flat['JntGroup']
            upAxis = exInfoDict_flat.get("upAxis") or infoConfig_oriDict["upAxis"]

            proName =infoConfig_oriDict['ProjectName']

            atDingDingTitle=u'自动导出文件'
            if ExExplanation:
                atDingDingTitle=ExExplanation
            waterMarkFile=exInfoDict_flat['waterMarkFile']
            Resolution=exInfoDict_flat['Resolution']
            
            sf = exTimeRange_desc[0]
            ef = exTimeRange_desc[1]
            lprint (sf,ef,openNewFile)
        else :
            if not  ExShotDir:
                ExShotDir=os.path.dirname(mayaFile)

    
    if openNewFile:
        openFileSt=time.time()
        try:
            lprint(u'打开文件{}'.format(mayaFile))
            loadReferenceDepth = 'none' if onlyLoadNeededRef else 'all'
            cmds.file(mayaFile, f=True, o=True,loadReferenceDepth = loadReferenceDepth)
        except:
            pass
        #cmds.file(mayaFile, f=True, o=True)
        lprint (u'打开新文件{}花费时间{}'.format(mayaFile,time.time()-openFileSt))
    else:
        lprint (u'使用已经打开的文件{}'.format(mayaFile)) 
        
    mayaPyExeFile=sys.executable.replace('maya.exe','mayapy.exe')
    
    loadPluginFunc('fbxmaya.mll')
    # 清理名称空间
    usualLib.cleanNameSpace()
    usualLib.cleanFile()
    #查询当前文件帧速率
    fps = cmds.currentUnit(q=1, t=1)

    #获取当前文件的所有名称空间
    nsRfnDict=getNsKey_RfnAndFileDict()
    lprint (u'名称空间引用字典为{}'.format(nsRfnDict))

    exDeformGeo=1
    bakeKeys=1
    exDeformGeo=1

    
    # GeoExRangeSF = sf+extraExportTimeRange[0]
    GeoExRangeSF = exFileStartFrame
    GeoExRangeEF = ef+extraExportTimeRange[1]
    # lprint (exNameSpace_desc)
    lprint (exNameSpace_desc.keys())
    lprint (GeoExRangeSF,GeoExRangeEF)
    processList = []
    abc_ex_job_list = []
    cameraTrNode=exCameraList_desc[0]
    for nameSpace in exNameSpace_desc:
        lprint(lprint (exNameSpace_desc.keys()))
        lprint (u'开始处理名称空间:{}'.format(nameSpace))
        refFile = exNameSpace_desc[nameSpace]['refFile']["filePath"]
        refFile=re.sub(r"\{\d+\}","",refFile)
        isExport=0;exFormat=''
        AssetType_Zh = exNameSpace_desc[nameSpace]['AssetType_Zh']
        if nameSpace==u"camera":
            if AssetType_Zh == u"绑定相机":
                maya_nameSpace = ex_camera
                cameraTrNode = 'RigCam_rig:Main_Cam'
            else:
                maya_nameSpace = ""
        else:
            maya_nameSpace = nameSpace

        isExport=exNameSpace_desc[nameSpace]['isEx']
        assetType=exNameSpace_desc[nameSpace]['AssetType']
        AssetType_Zh=exNameSpace_desc[nameSpace]['AssetType_Zh']
        HigRigFile=exNameSpace_desc[nameSpace]['HigRigFile']
        try:
            filePathList = exNameSpace_desc[nameSpace]["filePathList"]
        except:
            lprint(exNameSpace_desc[nameSpace])
            traceback.print_exc()
        
        #  新的方式,按照导出方式分组导出,
        """class exInfo_ex_method(Enum):
                fbx_cam = 0
                fbx_tpose = 1 
                fbx_skeAni = 2
                abc_cam = 3 
                abc_geo = 4
        """

        if exNameSpace_desc[nameSpace]['replaceHig'] and ':' in HigRigFile:
            isReplaceHigRig=True
        if AssetType_Zh == u'场景':
            GeoExRangeSF = 0
            GeoExRangeEF = 1
        else:
            GeoExRangeSF = exFileStartFrame
            GeoExRangeEF = ef+extraExportTimeRange[1]
        lprint (GeoExRangeSF,GeoExRangeEF)


        # 获取完整的名称空间
        for _ns,_rfn in nsRfnDict.items():
            if maya_nameSpace in _ns.split(':') and len(_ns.split(':'))>2:
                lprint (u'发现多重名称空间,{}使用完整名称空间:{}'.format(maya_nameSpace,_ns))
                maya_nameSpace=_ns
                break 

        rfn_Info=nsRfnDict.get(maya_nameSpace) 
        if not rfn_Info and (u"相机" not in AssetType_Zh):
            lprint (u'名称空间{}在{}没有找到引用信息,跳过'.format(maya_nameSpace,nsRfnDict))
            continue
        if rfn_Info:
            refNode = rfn_Info.get('refNode')
            refNode_Exist = rfn_Info.get('refNode_Exist')
            lprint ('isExport',isExport)  
            if not refFile:
                try:
                    RN=getNsKey_RfnAndFileDict()[nameSpace]['refNode']
                    refFile = cmds.referenceQuery(RN, f=True)
                    refFile=re.sub(r"\{\d+\}","",refFile)
                except:
                    lprint (traceback.format_exc())
        
        if not isExport:
            lprint (u'{}不需要导出'.format(maya_nameSpace))
            continue
            
        else :
            if refFile:
                # 这里一定要加载参考依赖的参考文件,再加载自身      
                lprint (u'导出名称空间:{}'.format(maya_nameSpace)) 
                RelatedRefList=[]
                try:
                    RelatedRefList= getRelatedRefNodes(nsRfnDict[maya_nameSpace]['refNode'])
                    lprint (RelatedRefList)
                except:
                    lprint (traceback.format_exc())
                if  RelatedRefList:
                    for relatedRef in RelatedRefList:
                        #referenceQuery =relatedRef.isLoaded() 参考查询可能会导致崩溃
                        #referenceQuery = cmds.referenceQuery()参考查询可能会导致崩溃
                        relatedRef = str(relatedRef)
                        referenceExist = bool(cmds.ls(relatedRef+':*'))
                        lprint (relatedRef,referenceExist)
                        if not referenceExist:
                            lprint (u'加载和{}相关的引用{}'.format(refNode,relatedRef))
                            try:
                                cmds.file(loadReference=str(relatedRef))
                            except:
                                lprint (u'加载和{}相关的引用{}失败,原因是{}'.format(refNode,relatedRef,traceback.format_exc()))
                            
                else:
                    lprint (u'no relative reference file with {}'.format(refNode))
                
                # bool(cmds.ls(nameSpace+':*')) 加上这句是因为文件已经加载的话再次加载会导致文件崩溃
                lprint (cmds.ls(maya_nameSpace+':*')[:10])
                if refNode_Exist and not cmds.referenceQuery(refNode, isLoaded=True) :
                    lprint(refFile,nameSpace,maya_nameSpace)
                    if os.path.exists(refFile):
                        try:
                            # 在打开Maya文件时如果没有加加载任何应用,
                            # 后面记载引用文件时第一个参数需要为引用文件,不然可能会导致Maya command error
                            # 默认第一个参数会是打开的文件,而不是应用的文件
                            refFile=refFile.replace('C_N_HanJiaPuCongA_Rig.ma','C_N_HanJiaPuCongA_Rig_New.ma')
                            print (u'需要导出的文件引用{}没有加载,加载引用'.format(refNode))
                            cmds.file(refFile,loadReference=refNode,force=True,loadReferenceDepth="all",ignoreVersion=True)
                            lprint (u'需要导出的文件引用{}没有加载,加载引用成功'.format(refNode))
                            
                                
                        except Exception as e:
                            lprint (u'尝试加载引用文件{}节点{}失败,原因为->'.format(refFile,refNode))
                            print (u'->{}-{}'.format(traceback.format_exc(),e))
                            
                        if not cmds.ls(maya_nameSpace+':*'):
                            lprint (u'加载引用文件没有成功,没找到以{}开头的节点'.format(maya_nameSpace))
                            continue
                    else:
                        lprint (u'需要导出的文件引用{}不存在'.format(refFile))
                        continue

            


        isStaticGeo=0

        #替换绑定文件为高模
        if genMiddleFile:
            cmds.file(rename=Lugwit_publicPath+'/RenderFarm/ExFbxMiddleFile/DiMo_{}_{}'.format(maya_nameSpace,mayaFileBaseName))
            cmds.file(force=True, type='mayaAscii', save=True)
        if isReplaceHigRig:
            replaceHigRigFile(nameSpace, HigRigFile)
            refFile=HigRigFile
            
        for exFilePathItem in filePathList:
            exFilePathDict = filePathList[exFilePathItem]
            ex_method = exFilePathDict.get("ex_method")
            
            lprint(exFilePathItem,exFilePathDict)
            filePath = exFilePathDict.get("filePath")
            geometryGroupList = exFilePathDict.get("ex_geo_grp",{})
            is_export = exFilePathDict.get("is_export")
            if nameSpace == "camera" :
                is_export = 1 # 相机不管怎么样都要导出,因为不需要多少时间
            if not is_export :
                print(u"{} no need export ,skip".format(filePath))
                continue
            if not ex_method :
                print(u"{} no ex_method no need export ,skip".format(filePath))
                continue
            
                        
             #geometryGroupList_withNameSpace = nameSpace+':'+exElement
            geometryGroupList_withNameSpace = [maya_nameSpace+':'+ x for x in geometryGroupList]
            lprint (u'geometryGroupList_withNameSpace',geometryGroupList_withNameSpace)
            skGroup_withNameSpace = maya_nameSpace+':'+JntGroup
            tempGroup = []
            for geometryGroup_withNameSpace in geometryGroupList_withNameSpace:
                lprint (cmds.objExists(geometryGroup_withNameSpace))
                if cmds.objExists(geometryGroup_withNameSpace):
                    polys=cmds.filterExpand(geometryGroup_withNameSpace, selectionMask=12, expand=True)
                    if polys:      
                        tempGroup.append(geometryGroup_withNameSpace)
            if tempGroup:
                geometryGroupList_withNameSpace = tempGroup
                lprint (u'geometryGroupList_withNameSpace from preset',tempGroup)
            else:
                geometryGroupList_withNameSpace_other=getRootNodeAndFilterPoly(nameSpace=maya_nameSpace,includeInvisible=False)
                # 可见性过滤已经在 getRootNodeAndFilterPoly 函数中处理
                if geometryGroupList_withNameSpace_other:
                    geometryGroupList_withNameSpace+=geometryGroupList_withNameSpace_other
                lprint (u'geometryGroupList_withNameSpace from other',geometryGroupList_withNameSpace_other)

            geometryGroupList= [x.split(':')[-1] for x in geometryGroupList_withNameSpace]

            lprint(filePath,geometryGroupList,exFilePathItem)

            lprint(u'geometryGroupList:{}'.format(geometryGroupList))

            
            if ex_method == 'fbx_tpose' :  #导出Tpose文件
                logFile='A:/TD/Temp/Log/MayaToUE/{}/{}/'.format(hostName,proName)+mayaFileBaseName+'/'+nameSpace+'_exTpose.log'
                batFile=os.path.join(TempDir,nameSpace+'_exTpose.bat')
                process = exAniClip_exTpose( mayaFile=mayaFile,
                                    savePath=filePath,
                                    ExHistoryFile=ExHistoryFile,
                                    refFile=refFile,
                                    AssetType_Zh=repr(AssetType_Zh),
                                    recordProcedureFile=recordProcedureFile,
                                    mayaPyExeFile=mayaPyExeFile,
                                    JntGroup=JntGroup,
                                    geometryGroupList = geometryGroupList,
                                    moveSkeToRoot=moveSkeToRoot,
                                    exDeformGeo=True,
                                    isStaticGeo=isStaticGeo,
                                    GeoExRangeSF=GeoExRangeSF,
                                    upAxis=upAxis,
                                    batFile=batFile,
                                    oriEnvVarDict=oriEnvVarDict,
                                    logFile=logFile,
                                    LowModName=LowModName,)
                if process:
                    processList.append(process)

            if ex_method == 'fbx_skeAni':  #导出Tpose文件
                exFBX(JntGroup=skGroup_withNameSpace, 
                        geometryGroupList=geometryGroupList_withNameSpace, 
                        skeAniExPath=filePath,moveSkeToRoot=moveSkeToRoot,bakeKeys=bakeKeys, 
                        exDeformGeo=exDeformGeo, 
                        isStaticGeo=isStaticGeo,refFile=refFile, sf=GeoExRangeSF,ef=GeoExRangeEF,
                        exSkelelonMesh=False,
                        deleteNameSpace=0,
                        exSkelonAnim=isExSkeAniFile,groupSkeAndGeo=1,upAxis=upAxis,
                        AssetType_Zh=AssetType_Zh)
                        # isExByExHistory,ExHistoryDict,ori_ExHistoryDict=\
                        # ExHistoryFromMaya.isExFileAndRecordHistoryFunc(SkeGeoAniFile,
                        #         mayaFile=mayaFile,ExHistoryFile=ExHistoryFile,
                        #         refFile=refFile,query=False)

            if ex_method == 'abc_cam':  #导出Tpose文件
                pass
                lprint (u'导出相机')
                ExShotDir=os.path.dirname(CameraFbxExPath)
                savevideoPath = '{}/{}_{}_{}.mov'.format(ExShotDir,proName,  sf, ef)
                saveCameraPath = CameraFbxExPath
                cmd_read='attrib -r {}'.format(saveCameraPath)
                os.system(cmd_read)
                if upToP4:
                    P4Lib.checkOut(saveCameraPath,)
                lprint (u'正在导出摄像机{}到{}'.format(cameraTrNode,filePath))
                try:
                    exAbcCamera(frameRange=[GeoExRangeSF,GeoExRangeEF],
                                root=cameraTrNode,
                                exPath=filePath)
                except:
                    traceback.print_exc()
            
            if ex_method == 'fbx_cam':  #导出Tpose文件
                lprint (u'导出相机')
                ExShotDir=os.path.dirname(CameraFbxExPath)
                savevideoPath = '{}/{}_{}_{}.mov'.format(ExShotDir,proName,  sf, ef)
                cmd_read='attrib -r {}'.format(filePath)
                os.system(cmd_read)
                if upToP4:
                    P4Lib.checkOut(filePath,)
                lprint (u'正在导出摄像机{}到{}'.format(cameraTrNode,filePath))
                exCamera(mayaFile,savePath=filePath,
                         sf=GeoExRangeSF,ef=GeoExRangeEF,
                         cameraTrNode=cameraTrNode) 
            

            if ex_method == 'abc_geo':  #导出Tpose文件
                if u"AniToSimAbcExPath" == exFilePathItem:
                    geometryGroupList_withNameSpace+=[maya_nameSpace+":simNUL"]
                    Triangulate=False
                else:
                    Triangulate=True
                abc_ex_job=exABC(exPath=filePath,
                    root=geometryGroupList_withNameSpace,
                    FrameRange='{},{}'.format(50,GeoExRangeEF),
                    is_nameSgFromMat=True,
                    Triangulate=Triangulate,
                    executeImmediately=False
                    )
                if abc_ex_job:
                    abc_ex_job_list.append(abc_ex_job)



    cmds.AbcExport(j=abc_ex_job_list)


    #sys.exit()
    #生成中间文件
    if genMiddleFile:
        lprint (Lugwit_publicPath+'/RenderFarm/ExFbxMiddleFile/EX_{}'.format(mayaFileBaseName))
        cmds.file(rename=Lugwit_publicPath+'/RenderFarm/ExFbxMiddleFile/EX_{}'.format(mayaFileBaseName))
        cmds.file(force=True, type='mayaAscii', save=True)
    if isP4File:
        DingDingExDirInfo=ExShotDir.replace('E:/BUG_Project','/')
        DingDing_descriptionText=descriptionText.replace('E:/BUG_Project','/')


    for process in processList:
        process.wait()
        
    # os.startfile(ExShotDir)
    
    if isGenMayaCheckFile:
        mergeFbxToMayaFile='{}/{}_{}_ExCheck.ma'.format(ExShotDir, proName)
        hasFbxFile=0
        cmds.file(force=True, new=True)
        exPathList =[]
        exPathList=list(set(exPathList))# 以防导出的路径列表里面有重复的
        for fbxFile in exPathList:
            if isP4File:
                getfiles=P4Lib.getFile(fbxFile)
                lprint ('getfiles:{}'.format(getfiles))
                if getfiles:
                    hasFbxFile=1
            else:
                hasFbxFile=os.path.exists(fbxFile)
            lprint (fbxFile.endswith('.fbx'))
            if fbxFile.endswith('.fbx'):
                lprint (u'导入引用文件{}'.format(fbxFile))
                # 如果P4里面有这个文件，则导入引用文件,参与拍屏
                try:
                    if isP4File:
                        lprint (u'从p4获取引用文件{},结果是{}'.format(fbxFile,getfiles))
                        P4Lib.p4.run_files(fbxFile)
                        cilentFileList=[x[0] for x in getfiles]
                    exFbxNs=os.path.basename(fbxFile).split('.')[0]
                    cmds.file(fbxFile,ns=exFbxNs,r=1,mergeNamespacesOnClash=1,type="FBX")
                except:
                    lprint (u'引用文件{}不在p4服务器'.format(fbxFile))
                    
            elif fbxFile.endswith('.abc'):
                lprint (u'导入引用文件{}'.format(fbxFile))
                # shd = cmds.shadingNode('blinn', name='blinn', asShader=True)
                # cmds.setAttr(shd+".color",0,0.3,0.2,type='double3',)
                # shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
                # cmds.connectAttr("%s.outColor" % shd, "%s.surfaceShader" % shdSG)
                ns=fbxFile.split('/')[-1].split('_Ani')[0]
                loadPluginFunc('AbcImport.mll')
                cmds.file(fbxFile, r=1,ns=ns,typ="Alembic")
                # cmds.sets(cmds.ls(ns+':*'), e=True, forceElement=shdSG)
        
        # 拍屏并保存Fbx审查文件
        mergeFbxToMayaFile=re.sub('_+','_',mergeFbxToMayaFile)
        savevideoPath=re.sub('_+','_',savevideoPath)
        lprint (u'生成Maya文件{}并开始拍屏'.format(mergeFbxToMayaFile))
        cmds.file(rename=mergeFbxToMayaFile)
        
        cmd_read='attrib -r {}'.format(mergeFbxToMayaFile)
        os.system(cmd_read)
        cmd_read='attrib -r {}'.format(savevideoPath)
        os.system(cmd_read)
        
        if upToP4:
            P4Lib.checkOut(mergeFbxToMayaFile,)
            
    if isGenMayaCheckFile and isGenMayaCheckVideoFile:
        if upToP4:
            P4Lib.checkOut(savevideoPath,)
        try:
            cmds.currentUnit(t='{}fps'.format(fps))
            lprint (u'设置帧速率为{}fps'.format(fps))
        except:
            cmds.currentUnit(t=fps)
            lprint (u'设置帧速率为{}'.format(fps))
        cmds.playbackOptions(min=sf, e=1)
        cmds.playbackOptions(max=ef, e=1)
            
        cmds.file(force=True, type='mayaAscii', save=True)
        lprint (u'保存拍屏路径:{}'.format(savevideoPath))
        renderOutputFile=renderOutputFBX(sf, ef, savePath=savevideoPath, waterMarkFile=waterMarkFile,
                                        fps=fps,cameraTrNode=exCameraTr,Resolution=Resolution,isP4File=isP4File)
        if isP4File:
            if renderOutputFile!=savevideoPath:
                P4Lib.checkOut(renderOutputFile,)
                P4Lib_Py2.submitChange(renderOutputFile, description=description)
        lprint (u'保存maya审查文件路径:{}'.format(savevideoPath))
        
        if upToP4:
            lprint (u'上传文件到P4:{}'.format(savevideoPath))
            #转换颜色空间
            P4Lib_Py2.submitChange(savevideoPath, description=description)
            P4Lib_Py2.submitChange(mergeFbxToMayaFile ,description=description)
            
    print(u"从 {} 导出完成".format(description))


'''单独调用
实例一：
import sys
sys.path.insert(0,os.environ.get('Lugwit_PluginPath')+r'\Lugwit_plug\mayaPlug\l_scripts\IOLib')
import exFbx;reload(exFbx)
exFbx.exAniClip(exFormat=0,mayaFile=cmds.file(q=1,sn=1),openNewFile=0,replaceExit=1,renderExportFbx=1,cusCfg=0,exDir='',upToP4=1,description="备注信息")
实例二：
import sys
sys.path.append(os.evplug_inPat+r'\Lugwit_plug\mayaPlug\l_scripts\IOLib')
import exFbx
reload(exFbx)
commentFile='//172.21.1.2/P4Triggers/Triggers/exAniClip_wlxx_sc006_ani_v001_UE_comment.txt'
mayaFile=cmds.file(q=1,sn=1)
exFbx.exAniClip(description=commentFile,
                upToP4=0,
                mayaFile=mayaFile,
                openNewFile=0)
'''

def batch_exAniClip(batchExFileList):
    lprint(batchExFileList)
    if isinstance(batchExFileList,str):
        batchExFileList=[batchExFileList]
    for batchExFile in batchExFileList:
        with codecs.open(batchExFile,'r','utf-8') as f:
            try:
                batchExFileDict=json.load(f)
                if batchExFileDict["ExFileFromMaya"]:
                    exAniClip(description=batchExFile,
                            mayaFile=batchExFileDict["mayaFilePath"])
            except:
                lprint(batchExFileDict)
                traceback.print_exc()


def getRootNodeAndFilterPoly(selected_objects='',nameSpace='',includeInvisible=False):
    """
    获取根节点并筛选多边形对象
    
    Args:
        selected_objects: 选择的对象列表
        nameSpace: 名称空间
        includeInvisible: 是否包含不可见节点
        
    Returns:
        list: 过滤后的根节点列表
    """
    lprint (locals())
    if not selected_objects:
        if nameSpace and nameSpace in cmds.namespaceInfo(lon=True):
            query_path = '|:*{}:*'.format(nameSpace)
            try:
                selected_objects=cmds.ls('{}:|*'.format(nameSpace),dag=0)
            except:
                selected_objects=cmds.ls('|*',dag=0)
        else:
            selected_objects=cmds.ls('|*',dag=0)
    lprint (selected_objects,nameSpace)
    # 使用cmds.filterExpand筛选多边形对象
    polygons = cmds.filterExpand(selected_objects, selectionMask=12, expand=True)
    if not polygons:
        return []
        
    # 如果不包含不可见节点，先过滤可见的多边形
    if not includeInvisible:
        visible_polygons = []
        for poly in polygons:
            if is_node_effectively_visible(poly):
                visible_polygons.append(poly)
        polygons = visible_polygons
        
    if not polygons:
        return []
        
    # 获取多边形对象的共同根层级节点列表
    root_nodes = []
    for poly in polygons:
        parents = cmds.listRelatives(poly, parent=True, fullPath=True)
        
        # 如果没有父节点，则添加多边形对象本身到根节点列表中
        if not parents:
            root_nodes.append(poly)
        else:
            root_node = parents[0]
            
            # 检查是否有更高级别的父节点
            while True:
                grandparent = cmds.listRelatives(root_node, parent=True, fullPath=True)
                if not grandparent:
                    break
                root_node = grandparent[0]
            
            if root_node not in root_nodes:
                root_nodes.append(root_node)

    # 打印共同根层级节点列表
    lprint("共同根层级节点:", root_nodes)
    return root_nodes

def getGeometryGroupList(geometryGroupList):
    lprint (locals())
    nameSpace = ''
    if isinstance(geometryGroupList,str):
        geometryGroupList=eval(geometryGroupList)
    tempGroup=[] 
    for geometryGroup in geometryGroupList:
        lprint (cmds.objExists(geometryGroup),geometryGroup)
        if cmds.objExists(geometryGroup) or cmds.objExists(geometryGroup.replace('Geometry','geometry')):
            tempGroup.append(geometryGroup)  # 判断几何体组是否存在
    if tempGroup:
        geometryGroupList = tempGroup
        lprint (u'geometryGroupList',geometryGroupList)
    else:
        if ':' in geometryGroupList[0]:
            nameSpace= geometryGroupList[0].split(':')[0]
        geometryGroupList=getRootNodeAndFilterPoly(nameSpace=nameSpace,includeInvisible=False)
        # 可见性过滤已经在 getRootNodeAndFilterPoly 函数中处理
        lprint (u'geometryGroupList',geometryGroupList)
    return geometryGroupList

def get_blend_shape_targets(blend_shape_node):
    """
    获取指定Blend Shape节点的所有目标模型。
    """
    # 获取blendShape节点的所有输入连接
    target_count = cmds.getAttr(blend_shape_node + ".weight", size=True)
    targets = []
    for i in range(target_count):
        # 构建连接名称
        connection_name = blend_shape_node + ".inputTarget[0].inputTargetGroup[{}].inputTargetItem[6000].inputGeomTarget".format(i)
        # 获取连接到该属性的对象
        connections = cmds.listConnections(connection_name)
        if connections:
            targets.append(connections[0])
    return targets


def filter_nodes(all_nodes):


    # 筛选出多边形网格节点
    mesh_nodes = cmds.ls(all_nodes, type='mesh')

    # 筛选出骨骼节点
    joint_nodes = cmds.ls(all_nodes, type='joint')

    # 筛选出变换节点
    transform_nodes = cmds.ls(all_nodes, type='transform')

    print("Mesh Nodes:", mesh_nodes)
    print("Joint Nodes:", joint_nodes)
    print("Transform Nodes:", transform_nodes)

    return mesh_nodes+joint_nodes+transform_nodes

def getBsTargetMeshList(bsNode):
    controlled_shapes = cmds.blendShape(bsNode, q=True, g=True)
    trNodeList=[]
    if controlled_shapes:
        for shape in controlled_shapes:
            if cmds.nodeType(shape)=='mesh':
                trNodeList.append(cmds.listRelatives(shape, p=True,f=1)[0] )
        return trNodeList
    return []

@try_exp
def exFBX(JntGroup='',geometryGroupList='',savePath='',moveSkeToRoot=False, 
       bakeKeys=False,isStaticGeo=False,refFile='',sf=1,ef=1,skeAniExPath='',
       deleteNameSpace=0,exSkelelonMesh=False,exSkelonAnim=False,mayaFile='',
       groupSkeAndGeo=False,deleteGroup='Group',upAxis='Y',AssetType_Zh=u'',LowModName='',
       jsonParmFile= None,openMayaFile=False,TposeExPath='',**kwargs):
    loadPluginFunc('fbxmaya.mll')
    lprint (locals())
    if not TposeExPath:# 兼容就得Api
        TposeExPath = savePath
    # 因为有的项目的道具的骨骼组明明比较乱,因此选择所有的骨骼的根骨骼组
    if openMayaFile:
        try:
            lprint (u'in function exFBX 中打开文件{}'.format(mayaFile))
            cmds.file(mayaFile, f=True, o=True,ignoreVersion=True)
        except Exception as e:
            print (u"打开文件出错,原因是{}".format(e))
    lprint (u"文件中根目录文件有\n",cmds.ls('|*'))
    nameSpace=JntGroup.rsplit(':',1)[0]
    lprint (AssetType_Zh,u'场景',repr(u'场景'),repr(AssetType_Zh),repr(AssetType_Zh)==repr(u'道具'))
    if AssetType_Zh==u"场景":
        JntGroup=""
        JntGroupExists = False
    else:
        JntGroupExists=cmds.objExists(JntGroup)
        if not JntGroupExists:
            if ':' in  JntGroup:
                JntGroupList=cmds.ls(nameSpace+':*',type='joint',l=1)
                lprint (JntGroupList)
            else:
                JntGroupList=cmds.ls(type='joint',l=1)
                lprint (JntGroupList)
            JntGroupList = sorted(JntGroupList,key=len)
            roorJnt=JntGroupList[0].split('|')[1]
            if cmds.nodeType(roorJnt)=='joint':
                JntGroup=roorJnt
                print ('roorJnt',roorJnt)
            else:
                if nameSpace:
                    JntGroup=re.search('\|{}:\w+\|{}:\w+\|'.format(nameSpace,nameSpace),JntGroupList[-1])
                else:
                    JntGroup=re.search('\|\w+\|\w+\|',JntGroupList[-1])
                try:
                    JntGroup=JntGroup.group()
                except:
                    JntGroup = JntGroupList[-1]
        lprint ('JntGroup',JntGroup)
    if not cmds.objExists(JntGroup):
        sf=0;ef=0;extraExportTimeRange=[0,0]
        

    
    moveSkeToRoot=eval(str(moveSkeToRoot))
    # todo 导出是定义fbx选项
    if 'cam_rig' in savePath:
        return
    if sf==ef:
        fbxExportOption(sf,ef,Animation='false',InputConnections='false',upAxis=upAxis)
    else:
        fbxExportOption(sf,ef,Animation='true',
                        InputConnections='false',
                        upAxis=upAxis,
                        Constraints='true')
     
    lprint ('fbxExportOption',sf,ef)
    mayaFileName=cmds.file(q=1,sn=1,shn=1) 
    if isinstance(geometryGroupList,str):
        geometryGroupList=eval(geometryGroupList)
    tempGroup=[] 
    
    geometryGroupList = getGeometryGroupList(geometryGroupList)
    if not geometryGroupList:
        return
    
    cmds.loadPlugin('fbxmaya.mll')
    savePathDir=os.path.dirname(savePath)
    if not os.path.exists(savePathDir):
        lprint (savePathDir)
        os.system('md {}'.format(os.path.normpath(savePathDir)))

    cmd_read='attrib -r {}'.format(savePath)
    os.system(cmd_read)
    cmds.select(cl=1)
    lprint (u'开始导出FBX文件--',savePath,geometryGroupList)

    try:
        namespace=JntGroup.split(':')[0]
        lprint (getNsKey_RfnAndFileDict())
        refFile=getNsKey_RfnAndFileDict()[namespace]['refFile']
        cmds.file(refFile, importReference=1,ignoreVersion=True)
        lprint (u'成功导入参考文件:{}'.format(refFile))
    except Exception as e:
        lprint (refFile)
        lprint (u'{}引用可能已经导入,原因是{}'.format(refFile,e))
        
    # 获取低模
    LowModList=cmds.ls(LowModName,type='transform')
        
    if moveSkeToRoot:
        try:
            cmds.select(JntGroup)
            cmds.parent(w=1)
        except Exception as e:
            lprint (traceback.format_exc())
            lprint (u'无法P出{},原因是{}'.format(JntGroup,e))
            
        try:
            cmds.select(geometryGroupList,add=1)
            lprint (u'几何体组{}下面的层级为{}'.format(geometryGroupList,cmds.listRelatives(geometryGroupList,c=1,fullPath=True)))
            cmds.parent(w=1)
        except:
            lprint (traceback.format_exc())
            lprint (u'无法P出{}'.format(geometryGroupList))

    bsNodeList = []              

    lprint (repr(JntGroup))
    if sf==ef:
        ef=ef+1
    if cmds.objExists(JntGroup):
        cmds.select(JntGroup)
        lprint('moveSkeToRoot,refFile:', moveSkeToRoot, refFile)
        if bakeKeys:
            rootNode=cmds.ls(JntGroup,l=1)[0].split('|')[1]
            lprint (rootNode)
            #rootNode='P_WuZheWuQi_Rig1:jnt_g'
            # cmds.file(rename='D:/aa/bake_before.ma')
            # cmds.file(save=True)
            cmds.select(rootNode)
            cmds.SelectHierarchy()
            cmds.bakeResults(rootNode, t=(sf, ef), sb=1, sm=1, oversamplingRate=1, at=[
                "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"], hi="below", shape=1)
            lprint (u'烘焙范围{}-{}'.format(sf,ef))
            # cmds.file(rename='D:/aa/bake.ma')
            # cmds.file(save=True)
            # sys.exit()
            # 烘焙Blender节点
            if ':' in JntGroup:
                bsNodeList=cmds.ls('{}:*'.format(JntGroup.split(':')[0]),type='blendShape')
                for blendShapeNode in bsNodeList:
                    bakeBlendShapeWeightAttr(blendShapeNode,sf,ef)


            
    # 如果遇到同名物体，选择所有同名物体
    try:
        cmds.select(geometryGroupList, add=1)
    except Exception as e:
        if 'More than one object matches name' in e.message:
            sl=cmds.ls(geometryGroupList)
            lprint (u'找到与{}同名的物体{}'.format(geometryGroupList,sl))
            cmds.select(sl, add=1)
            
    if isStaticGeo:
        lprint (u'导出场景,几何体组为{}'.format(geometryGroupList))
        cmds.select(geometryGroupList, add=1)
        for geometryGroup in geometryGroupList:
            if ':' in geometryGroup:
                cmds.select(geometryGroup.split(':')[0]+':*', add=1)
    try:
        cmds.select(JntGroup,add=1)
    except:
        pass
    
    #如果移动到跟骨骼删除命名空间
    if moveSkeToRoot:
        try:
            if deleteNameSpace:
                if ':' in geometryGroupList[0]:
                    nameSpace=geometryGroupList[0].rsplit(':',1)[0]
                    cmds.namespace( removeNamespace=nameSpace+':', mergeNamespaceWithRoot = True)
                    JntGroup=JntGroup.rsplit(':',1)[-1]
        except Exception as e:
            lprint (traceback.format_exc())
            lprint (u'删除命名空间失败,原因是{}'.format(e))
    
    

    lprint (exSkelelonMesh)
    if exSkelelonMesh:# 导出骨骼网格体
        cmd='FBXExport -f  "{}" -s'.format(TposeExPath.replace('\\','/'))
        if deleteGroup:
            if cmds.objExists(deleteGroup):
                cmds.select(deleteGroup,d=1)
        if LowModList:
            cmds.select(LowModList,add=1)
        bsNodeList_Tpose=cmds.ls(type='blendShape')
        if bsNodeList_Tpose:
            meshList=[]
            for bsNode in bsNodeList_Tpose:
                controlled_models = getBsTargetMeshList(bsNode)
                if controlled_models:
                    meshList+=controlled_models
                target_m=get_blend_shape_targets(bsNode)
                if target_m:
                    meshList+=target_m
            cmds.select(meshList,add=1)
        lprint (cmds.objExists("rigNode_grp"))
        if cmds.objExists("rigNode_grp"):
            cmds.select("rigNode_grp",add=1)

    if exSkelonAnim:
        cmd='FBXExport -f  "{}" -s'.format(skeAniExPath.replace('\\','/'))
        selectSke=False
        if moveSkeToRoot:
            try:
                cmds.select('|'+JntGroup)
                lprint (u'选择根层级的{}成功'.format(JntGroup))
                selectSke=True
            except Exception as e:
                # cmds.file(rename=r'A:\TD\RenderFarm\ExFbxMiddleFile\ExSkeAniError_{}'.format(mayaFileName))
                # cmds.file(force=True, type='mayaAscii', save=True)
                lprint (u'选择根层级的{}失败原因是{}'.format(JntGroup,e))
        else:
            try:
                cmds.select(JntGroup)
                lprint (u'选择骨骼层级的{}成功'.format(JntGroup))
                selectSke=True
            except:
                lprint (u'没有找到骨骼组{}'.format(JntGroup))
        if exSkelonAnim and selectSke:
            skeAniExPath = skeAniExPath.replace('_Rig','')
            skeExSavePathDir=os.path.dirname(skeAniExPath)
            lprint (os.path.exists(skeExSavePathDir),skeExSavePathDir)
            if not os.path.exists(skeExSavePathDir):
                os.system('md {}'.format(os.path.normpath(skeExSavePathDir)))
                if not os.path.exists(skeExSavePathDir):
                    os.makedirs(skeExSavePathDir, )
        lprint (u'导出内容,不包括BS节点对应的模型{}'.format(cmds.ls(sl=1)))
        lprint (bsNodeList)
        if bsNodeList:
            meshList=[]
            for bsNode in bsNodeList:
                controlled_models = getBsTargetMeshList(bsNode)
                if controlled_models:
                    meshList+=controlled_models
            if meshList:
                cmds.select(meshList,add=1)
        # fil_mesh=filter_nodes(cmds.ls(sl=1))
        # cmds.select(fil_mesh)

    lprint (u'导出内容{}'.format(cmds.ls(sl=1)))

    try:
        lprint ('cmd',cmd)
        mm.eval(cmd)
    except:
        traceback.print_exc()
        # cmds.file(rename='D:/aa/bake.ma')
        # cmds.file(save=True)
        # cmds.file(rename='D:/aa/aa.ma')
        # cmds.file(save=True)
        # cmds.file(skeAniExPath, 
        #         force=True, 
        #         options="v=0;", 
        #         typ="FBX export", 
        #         pr=True, 
        #         es=True)# 用这个导出可能会出现typ="FBX export",不存在的错误
    if os.path.exists(savePath):
        lprint (u'导出骨骼动画成功,路径为{}'.format(savePath))

        
    
    #如果祛除了命名空间,打个组
    if groupSkeAndGeo and deleteNameSpace:
        lprint (u'如果祛除了命名空间,打个组')
        try:
            cmds.select('|'+JntGroup.split(':')[-1])
            mm.eval('doGroup 0 1 1;')
            lprint (u'打组成功{}'.format('|'+JntGroup.split(':')[-1]))
        except:
            lprint (locals())
            lprint (traceback.format_exc())
        try:
            for geometryGroup in geometryGroupList:
                lprint (geometryGroup)
                cmds.select(geometryGroup.split(':')[-1],add=1)
                mm.eval('doGroup 0 1 1;')
                lprint (u'打组成功{}'.format('|'+geometryGroup.split(':')[-1]))
        except:
            traceback.print_exc()
        # lprint (u'保存临时文件')
        # cmds.file(rename='S:/DataTrans/FQQ/RenderFarm/ExFbxMiddleFile/aa.ma')
        # cmds.file(force=True, type='mayaAscii', save=True)


'''
exFBX(JntGroup='DeformationSystem', 
    geometryGroupList='Geometry',
     savePath='D:/aa/aa.fbx', 
     moveSkeToRoot=1, 
        bakeKeys=1, 
        exDeformGeo=1,
        isStaticGeo=0,
        refFile='E:/BUG_Project/B003_S78/Asset_work/chars/Rig/B003_S78_chars_wuji_Rig.ma', 
        sf=1001, 
        ef=1005,
        skeAniExPath=1,
        deleteNameSpace=1)
'''

def bakeBlendShapeWeightAttr(blendShapeNode,sf,ef):
    # 获取BlendShape节点的权重属性别名
    aliases = cmds.aliasAttr(blendShapeNode, query=True)
    if not aliases:
        return
    weightAliases = aliases[::2]  # 提取权重属性别名

    # 构造权重属性的完整名称列表
    weightAttributes = ['{}.{}'.format(blendShapeNode, alias) for alias in weightAliases]
    lprint (weightAttributes)
    # 使用cmds.bakeResults烘焙权重属性
    cmds.bakeResults(
        weightAttributes,
        simulation=True,
        time=(sf, ef),
        sampleBy=1,
        oversamplingRate=1,
        disableImplicitControl=True,
        preserveOutsideKeys=True,
        sparseAnimCurveBake=False,
        removeBakedAnimFromLayer=False,
        removeBakedAttributeFromLayer=False,
        bakeOnOverrideLayer=False,
        minimizeRotation=True,
        controlPoints=False,
        shape=True
    )


@try_exp
def fbxExportOption(sf=1, ef=1,exFormatIsAscii='false',Animation='true',
                    InputConnections='false',
                    Constraints='true',SkeletonDefinitions='true',Skins='true',Shapes='true',
                    upAxis='Y'):
    lprint (locals())
    if sf!=ef:
        mm.eval("FBXExportBakeComplexAnimation -v true")
    mm.eval("FBXExportSmoothingGroups -v true")
    mm.eval("FBXExportBakeComplexStart -v {}".format(sf))
    print ("FBXExportBakeComplexStart -v {}".format(sf))
    mm.eval("FBXExportBakeComplexEnd -v {}".format(ef))
    print ("FBXExportBakeComplexEnd -v {}".format(ef))
    mm.eval("FBXExportBakeComplexEnd -v {}".format(ef))
    print ("FBXExportBakeComplexEnd -v {}".format(ef))
    mm.eval("FBXExportConstraints -v {}".format(Constraints))
    print ("FBXExportConstraints -v {}".format(Constraints))
    mm.eval("FBXExportSkeletonDefinitions -v {}".format(SkeletonDefinitions))
    print ("FBXExportSkeletonDefinitions -v {}".format(SkeletonDefinitions))
    mm.eval('FBXProperty Export|IncludeGrp|Animation -v {}'.format(Animation))
    print ('FBXProperty Export|IncludeGrp|Animation -v {}'.format(Animation))
    mm.eval("FBXExportSkins -v true")
    mm.eval("FBXExportShapes -v true")
    mm.eval('FBXExportInputConnections -v {}'.format(InputConnections))
    print ('FBXExportInputConnections -v {}'.format(InputConnections))
    mm.eval(
        'FBXProperty Export|IncludeGrp|Animation|BakeComplexAnimation|ResampleAnimationCurves -v 0')
    print ('FBXProperty Export|AdvOptGrp|AxisConvGrp|UpAxis -v {}'.format(upAxis.upper()))
    # 有时候这个向上轴的大小写可能会出错
    mm.eval('FBXProperty Export|AdvOptGrp|AxisConvGrp|UpAxis -v {}'.format(upAxis.upper()))
    mm.eval('FBXProperty Export|AdvOptGrp|Fbx|ExportFileVersion -v FBX201800')
    #mm.eval('FBXProperty Export|IncludeGrp|Geometry|Triangulate -v 1')
    mm.eval("FBXExportCameras -v true")
    #mm.eval("FBXProperty Export|AdvOptGrp|Fbx|AsciiFbx -v \"{}\";".format(exFormatIsAscii))
    mm.eval("FBXExportInAscii -v {}".format(exFormatIsAscii))
    print ("FBXExportInAscii -v {}".format(exFormatIsAscii))

@try_exp
def exCamera(mayaFile='', sf=0, ef=1, savePath='',cameraTrNode='',openExdir=False,exDir='',
            reNameCameraNodeName=''):
    lprint (locals())
    mainFunc=None
    if not mayaFile:
        if len(sys.argv)>1:
            if sys.argv[1]=='exCamera':
                mainFunc='exCamera'
                cmds.file(mayaFile, f=True, o=True, lnr=1)
    if not sf :
        sf = int(cmds.playbackOptions(min=1, q=1))
        ef = int(cmds.playbackOptions(max=1, q=1))
                
    if savePath:
        cmd_read='attrib -r {}'.format(savePath)
        os.system(cmd_read)
        exDir = os.path.dirname(savePath)
    else:
        if not exDir:
            exDir = os.path.dirname(mayaFile)
    
    try:
        if not os.path.exists(exDir):
            os.makedirs(exDir)
    except:
        pass


    loadPluginFunc('fbxmaya.mll')
    cameraTrNode = cmds.ls(cameraTrNode)
    if cameraTrNode:
        cameraTrNode = cameraTrNode[0]
        if cmds.nodeType(cameraTrNode)=='camera':
            cameraTrNodeList=[cmds.listRelatives(cameraTrNode,p=1,f=1)[0]]
        else:
            cameraTrNodeList=[cameraTrNode]
    else :
        cameraTrNodeList = findCamera()
        
    lprint(u'场景中找到的摄像机有:{}'.format(cameraTrNodeList))
    NewCameraTrList=[]
    # 给摄像机的变换节点添加分辨率属性,这样在导出的Fbx中就能读取这个属性了 
    savePath_list=[]
    for i,cameraTrNode in enumerate(cameraTrNodeList):
        cmds.select(cmds.ls(cameraTrNode))    
        resW=cmds.getAttr("defaultResolution.width")
        resH=cmds.getAttr("defaultResolution.height")
        if not cmds.attributeQuery('RenderRes',n=cameraTrNode,ex=1):
            cmds.addAttr(longName='RenderRes',dt='string')
        cmds.setAttr(cameraTrNode+'.RenderRes','{}*{}'.format(resW,resH),type='string')
        cameraShNode = cmds.listRelatives(cameraTrNode,s=1)[0]
        try:
            # cmds.setAttr(u'{}.farClipPlane'.format(cameraShNode), lock=False)
            connections = cmds.listConnections(u'{}.farClipPlane'.format(cameraShNode), plugs=True, connections=True) or []
            for i in range(0, len(connections), 2):
                source = connections[i+1]  # 连接的源头
                target = connections[i]    # 连接的目标

                # 断开连接
                cmds.disconnectAttr(source, target)
                
            cmds.setAttr(u'{}.farClipPlane'.format(cameraShNode), 100000000)
            
        except Exception as e:
            lprint  (e)
            
        lprint(u'你选择的摄像机{}导出帧范围范围是:{}-{}\n'.format(cameraShNode,sf, ef))
        NewCameraTr=bakeCamera(cameraTrNode,sf, ef)
        if reNameCameraNodeName:
            cmds.rename(NewCameraTr,reNameCameraNodeName)
            NewCameraTr = reNameCameraNodeName
        fbxExportOption(sf, ef,exFormatIsAscii='true')
        if not savePath:
            saveName=NewCameraTr.rsplit('|',1)[-1]
            if ':' in saveName:
                saveName=saveName.replace(':','_')
            lprint (NewCameraTr,NewCameraTr.rsplit('|',1)[-1])
            savePath = '{}/{}camera_{}_{}.fbx'.format(exDir, saveName, sf, ef)
            savePath=savePath.replace('\\','/')
        lprint (u'导出路径是:{}'.format(savePath))
        savePath_list.append(savePath)
        cmds.select(NewCameraTr)
        #mm.eval('FBXExport -f -s "{}"'.format(savePath))
        loadPluginFunc('fbxmaya.mll')
        try:
            cmds.file(savePath, force=True, typ="FBX export", pr=True, es=True)
        except Exception as e:
            cmd='FBXExport -f  "{}" -s'.format(savePath.replace('\\','/'))
            lprint ('cmd',cmd)
            mm.eval(cmd)
        print (u'导出内容{}'.format(cmds.ls(sl=1)))
        
        lprint (u'保存路径是:{}'.format(savePath))

        
        # if openExdir:
        #     os.startfile(os.path.dirname(savePath))
        NewCameraTrList.append(NewCameraTr)
        savePath=''
        lprint (u'重置savePath')
    return NewCameraTrList,savePath_list


def bakeCamera(cameraTrNode,sf, ef):
    lprint(locals())
    if cmds.nodeType(cameraTrNode)=='camera':
        cameraTrNode=cmds.listRelatives(cameraTrNode,p=1)[0]
    NewCameraName=cameraTrNode+'_Ex'
    if not cmds.objExists(NewCameraName):
        NewCameraTr=cmds.duplicate(cameraTrNode,name=cameraTrNode+'_Ex',rc=1)[0]
    else:
        NewCameraTr=NewCameraName
    # cmds.parent(NewCameraTr,w=1) # 
    # NewCameraTr =cmds.camera(name=cameraTrNode+'_Ex')[0]
    attrList = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz',
                'sx', 'sy', 'sz', 'translate', 'scale', 'rotate']
    for attr in attrList:
        cmds.setAttr(NewCameraTr+'.'+attr, lock=0)
    cmds.select(NewCameraTr)
    try:
        cmds.parent(w=1)
    except:
        pass
    cameraShNode = cmds.listRelatives(cameraTrNode, s=1,fullPath=True)[0]
    focLen = cmds.getAttr(cameraShNode+'.fl')
    NewCameraShape = cmds.listRelatives(NewCameraTr, s=1,fullPath=True)[0]
    NewCameraTr = cmds.listRelatives(NewCameraShape, p=1,fullPath=True)[0]
    NewCameraShape = cmds.listRelatives(NewCameraTr, s=1,fullPath=True)[0]
    lprint(u"set {} node farClipPlane attribute".format(NewCameraShape))
    try:
        cmds.setAttr("{}.farClipPlane".format(NewCameraShape),10000000)
    except:
        lprint(u"set {} node farClipPlane attribute error,attribute is locked".format(NewCameraShape))
    for i in range(int(sf), int(ef+1)):
        cmds.currentTime(i)
        cameraRot = cmds.xform(cameraTrNode, q=1, ro=1, ws=1)
        cmds.select(cameraTrNode)
        bboxObj=cmds.geomToBBox(nameSuffix='_BBox',keepOriginal=1,single=1)
        cameraTr = cmds.xform(bboxObj, q=1, t=1, ws=1)
        print(cameraTr)
        cmds.delete(bboxObj)
        cmds.xform(NewCameraTr, ro=cameraRot)
        cmds.xform(NewCameraTr, t=cameraTr)
        focLen = cmds.getAttr(cameraShNode+'.fl')
        if isinstance(focLen, list):
            lprint (focLen)
            focLen = focLen[0]
        cmds.select(NewCameraTr)
        cmds.setKeyframe(at='tx', v=cameraTr[0])
        cmds.setKeyframe(at='ty', v=cameraTr[1])
        cmds.setKeyframe(at='tz', v=cameraTr[2])
        cmds.setKeyframe(at='rx', v=cameraRot[0])
        cmds.setKeyframe(at='ry', v=cameraRot[1])
        cmds.setKeyframe(at='rz', v=cameraRot[2])
        cmds.setKeyframe(NewCameraShape, at='fl', v=focLen)
    return NewCameraTr

def findCamera():
    cameraList = []
    cameraList = cmds.ls(type='camera')
    lprint (u'场景中所有的摄像机有{}'.format(cameraList))
    selfCameraList = ['sideShape', 'frontShape', 'topShape', 'perspShape','backShape','leftShape','bottomShape','ledtShape']
    cameraList=[x for x in cameraList 
                        if x.rsplit(':',1)[-1] not in selfCameraList ]
    cameraList = set(cameraList)-set(selfCameraList)
    cameraList=list(cameraList)
    cameraList=cmds.listRelatives(cameraList,p=1,f=1)
    return cameraList


def renderOutputFBX(sf=1001, ef=1058, savePath='D:/aa.mov', isP4File=False,
                    fps=30,cameraTrNode='',waterMarkFile='',Resolution=['1920','1080']):
    Resolution=[int(Resolution[0]),int(Resolution[1])]
    os.system('taskkill /f /t /im quicktimeShim.exe')
    cmd_read='attrib -r {}'.format(savePath)
    os.system(cmd_read)
    try:
        cmds.currentUnit(t='{}fps'.format(fps))
        lprint (u'设置帧速率为{}fps'.format(fps))
    except:
        cmds.currentUnit(t=fps)
        lprint (u'设置帧速率为{}'.format(fps))
    cmds.playbackOptions(min=sf, e=1)
    cmds.playbackOptions(max=ef, e=1)
    camaraInScene = findCamera()
    lprint (u'场景中的摄像机有{}'.format(camaraInScene))
    if not cameraTrNode:
        cameraTrNode = camaraInScene[0]
        cameraShNode = cmds.listRelatives(cameraTrNode, s=1)[0]
        lprint (u'自动找到的拍屏摄像机形态节点是>>>{}'.format(cameraShNode))
    else:
        for x in camaraInScene:
            if cameraTrNode[1:] in x:
                cameraShNode = cmds.listRelatives(x, s=1)[0]
                lprint (u'拍屏找到的摄像机形态节点是>>>{}'.format(cameraShNode))
                break
        
    cams = cmds.ls(type='camera')
    for cam in cams:
        if cam != cameraShNode:
            cmds.setAttr(cam + '.rnd', 0)#设置摄像机为不可渲染
    cmds.setAttr(cameraShNode + '.rnd', 1)#没有可以渲染的摄像机拍屏的时候maya会崩溃
    cmds.setAttr(u'{}.farClipPlane'.format(cameraShNode), 100000000)
    try:
        cmds.lookThru(cameraTrNode)
    except Exception as e:
        lprint (u'设置摄像机{}为当前视口摄像机失败,原因是{}'.format(cameraTrNode,e))
        
    cmds.setAttr('{}.displayFilmGate'.format(cameraShNode),1)
    cmds.setAttr('{}.displayGateMask'.format(cameraShNode),1)
    cmds.setAttr('{}.displayResolution'.format(cameraShNode),1)
    cmds.setAttr('{}.displayGateMaskColor'.format(cameraShNode),0,0,0)
    cmds.setAttr('{}.overscan'.format(cameraShNode),1.3)
    cmds.setAttr('{}.backgroundColor'.format(cameraShNode),0.282895 ,0.282895, 0.282895,type='double3')
    cmds.modelEditor( 'modelPanel4', e=True, displayTextures=1)
    try:
        cmds.headsUpDisplay('HUDObjedctPosition', section=1, block=1, blockSize='medium', label=u'芭阁动漫',labelFontSize='large',)
    except:
        pass
    cmds.colorManagementPrefs(e=True, cmEnabled=1)
    cmds.setAttr("defaultRenderGlobals.currentRenderer","mayaHardware2",type="string")
    cmds.setAttr("defaultRenderGlobals.imageFormat",22)
    cmds.setAttr("defaultRenderGlobals.ifp",savePath,type='string')
    try:
        cmds.setAttr("defaultRenderGlobals.encodingQuality",75)
    except:
        pass
    cmds.setAttr('defaultRenderGlobals.outFormatControl',1)
    cmds.setAttr('defaultRenderGlobals.startFrame',sf)
    cmds.setAttr('defaultRenderGlobals.endFrame',ef)
    cmds.setAttr('defaultRenderGlobals.animation',1)
    cmds.setAttr('defaultResolution.width',Resolution[0])
    cmds.setAttr('defaultResolution.height',Resolution[1])
    cmds.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 1)
    cmds.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 1)
    # try: ffmpeg 视乎无法处理mov文件
    #     lprint (u'开始拍屏mov')
    #     try:
    #         cmds.playblast(fmt="qt", f=savePath, p=100, orn=1, forceOverwrite=1,os=1,v=0,wh=Resolution,compression='H.264')
    #     except:
    #         cmds.playblast(fmt="qt", f=savePath, p=100, orn=1, forceOverwrite=1,os=0,v=0,wh=Resolution,compression='H.263')
    # except Exception as ex:
    #     lprint(traceback.format_exc())
    #     lprint (u'mov拍屏失败-开始拍屏avi')
    savePath=savePath.replace('.mov','.avi')
    if isP4File:
        P4Lib.checkOut(savePath)
    cmds.playblast(fmt="avi", f=savePath, p=100, orn=1, forceOverwrite=1,os=1,v=0,wh=Resolution)
    if houtai:
        savePath=savePath.replace('/','\\')
        fmt=savePath.split('.')[-1]
        ffmpegPath=Lugwit_PluginPath+r'\ffmpeg\bin\ffmpeg.exe'
        tempVideoA=os.environ['TEMP']+'\\testA.'+fmt
        tempVideoB=os.environ['TEMP']+'\\testB.'+fmt
        converrColorSpaceCmd='{} -i {} -vf eq=gamma=2.2 -y {}'.format(ffmpegPath,savePath,tempVideoA)
        os.system(converrColorSpaceCmd)
        #waterMarkCmd='{} -i {} -vf "movie=waterMark.png[watermark];[in][watermark]overlay=10:10:1[out]" -y {}'.\
        #                format(ffmpegPath,tempVideoA,tempVideoB)
        waterMarkCmd='{} -i {} -i {} -filter_complex "overlay=5:5" -y {}'.\
                format(ffmpegPath,tempVideoA,waterMarkFile,tempVideoB)
        lprint (waterMarkCmd)
        try:
            subprocess.call(waterMarkCmd,cwd=Lugwit_PluginPath+r'\ffmpeg\bin')
            os.system('echo f| Xcopy  {} {} /Y /F /R'.format(tempVideoB,savePath))   
        except:
            lprint (traceback.format_exc() )  
    return savePath




def C30assignNewMat(*args):
    '''
    C30项目新的材质赋予到旧的灯光文件实现原理
    比如灯光文件路径为:
    X:\Project\2018\C30\Shot_work\Lighting\1\Shot03_new\work\C30_shot003_Lgt_CH02_1442-1584.mb
    引用文件为 A : WBB  X:/Project/2018/C30/Shot_work/Animation/1/Shot03/approve/ABC/chars/WBB.abc
            B: WBBMat  X:/Project/2018/C30/Asset_work/chars/WBB/Texture/approve/C30_chars_WBB_higMat.ma
    现在要通过文件B找到新的材质文件
    新的路径为:
    C :  WBBMat_NewMat X:/Project/2018/C30/Asset_work/chars/WBB_new/Texture/work/C30_chars_WBB_new_Texture_v001.ma
    找到这个文件后引用这个文件到当前镜头灯光文件
    然后根据模型名称,拓扑去传递材质和贴图,如果同一个角色文件名称有变化,则使用拓扑去传递材质和uv,如果拓扑也发生了变化而UV没变,
    找到名称的对应关系去传递,比如同一个杯子原来叫'A_cup',现在叫'C_Bottle',只要把这个对应关系写到一个字典里面,能够自动去传递
    材质,当然UV肯定是没法传递的
    '''
    try:
        mayaFile = sys.argv[2]
        cmds.file(mayaFile, f=True, o=True)
        loadPluginFunc('AbcExport.mll')
    except:
        mayaFile=cmds.file(q=1,sn=1)
    rfList = sorted(cmds.ls(rf=1))
    newRFList = [x for x in rfList if 'camera' not in x and 'New' not in x]
    matRFList = [x for x in newRFList if 'Mat'  in x]
    allNameSpace = cmds.namespaceInfo(lon=1)
    for x in matRFList:
        lprint (x)

    #删除所有的灯光并创建天光
    delAllLight()    

    #创建层并隐藏新的材质引用文件
    if not cmds.objExists("HideNewMatReference"):
        NewMatLayer=cmds.createDisplayLayer(name="HideNewMatReference")
    cmds.setAttr('{}.visibility'.format("HideNewMatReference"),0)

    for i, rf in enumerate(matRFList):
        mayaMatFile = cmds.referenceQuery(rf, f=1)
        lprint  ('旧的Maya文件是:{}'.format(mayaMatFile))
        #查找新的maya材质文件开始
        newMayaFile = mayaMatFile.replace(
            '/Texture', '_new/Texture').replace('_higMat', '_new_Texture_v001').replace('/approve/','/work/')
        if  newMayaFile.endswith('}'):
            #i_QB_higMat.ma{6}
            newMayaFile=newMayaFile[:-3]
        if newMayaFile.endswith('.ma') and not os.path.exists(newMayaFile):
            newMayaFile=newMayaFile.replace('.ma','.mb')
        elif newMayaFile.endswith('.mb') and not os.path.exists(newMayaFile):
            newMayaFile=newMayaFile.replace('.mb','.ma')
        lprint  ('新的Maya文件是:{},文件存在:{}----'.format(newMayaFile,os.path.exists(newMayaFile)))

        #旧的Maya文件是否隐藏
        newNameSpace=rf.replace('RN','_NewMat')
        oldNameSpace=rf.replace('MatRN','')
        lprint ('旧的名称空间列表:{}'.format(oldNameSpace))
        oldRootList=cmds.ls('|'+oldNameSpace+':*')
        rootList=cmds.ls('|'+newNameSpace+':*')
        oldNameSpaceIsHided=0
        hideAtDisLayer=0
        for rl in oldRootList:
            lprint(rl,cmds.nodeType(rl))
            if cmds.nodeType(rl)=='transform':
                visDisplayLayers=cmds.listConnections('{}.drawOverride'.format(rl))
                lprint  ('visDisplayLayers:',visDisplayLayers)
                if visDisplayLayers:
                    for displayLayer in visDisplayLayers:
                        if not cmds.getAttr(displayLayer+'.visibility'):
                            hideAtDisLayer=1
                            break
                if not cmds.getAttr(rl+'.visibility') or hideAtDisLayer:
                    lprint  ('命名空间{}是隐藏的,被忽略'.format(oldNameSpace))
                    abcNameSpace=oldNameSpace
                    if cmds.namespace(nameSpaceIndex=abcNameSpace):
                        abcFile=cmds.referenceQuery(abcNameSpace+'RN',f=1)
                        #cmds.file(abcFile,ur=1) #不加载参考文件
                        cmds.file(abcFile,rr=1) #卸载不加载参考文件
                        oldNameSpaceIsHided=1
                        lprint ('卸载abc文件:{}'.format(abcFile))
        
        #创建层加入新的材质引用物体并隐藏层
        for a in rootList:
            cmds.editDisplayLayerMembers( 'HideNewMatReference', a)
            #break

        #卸载旧的maya材质文件
        cmds.file(mayaMatFile,rr=1) 
        
        #如果旧的名称空间是隐藏的,跳过这个循环
        if oldNameSpaceIsHided:
            continue

        if newNameSpace not in allNameSpace:  #不存在新的命名空间
            #导入引用文件
            lprint ('运行新的Mayapy.exe删除毛发')
            useExist=1
            delXgenMayaFile=deleteXgen(mayaFile=newMayaFile,useExist=1)
            curTime=time.time()
            lprint(u'删除xgen的Maya文件{}是否存在:{}'.format(delXgenMayaFile,os.path.exists(delXgenMayaFile)))

                
            
            while 1:
                if os.path.exists(delXgenMayaFile):
                    gentime = os.stat(delXgenMayaFile).st_mtime
                    if gentime-curTime>10 or  useExist:
                        lprint ('生成新的Maya材质文件成功')
                        break
                if time.time()-curTime>1000:
                    lprint ('删除xgen的Maya文件:{}超时'.format(delXgenMayaFile))
                    break
            newMayaFile=delXgenMayaFile
            lprint ('新的Maya文件是:{}'.format(newMayaFile))
            while 1:
                try:
                    cmds.file(newMayaFile, r=True,ignoreVersion = True,namespace = newNameSpace)
                    lprint ('newNameSpace+RN:{}'.format(newNameSpace+'RN'))
                    cmds.file(lr=newNameSpace+'RN')
                    lprint (cmds.ls(newNameSpace+':*')[0])
                    break
                except:
                    lprint ('try load reference')
            lprint ('导入引用文件{}成功'.format(newMayaFile))
        else:
            lprint ('命名空间"{}"已存在'.format(newNameSpace))

        

        newMatGeos=cmds.ls(newNameSpace+':*') # 导入的所有的新物体
        findSameObjIndex=0  # 找到了多个相同物体,如果没有找到相同的物体,尝试在相同的面和顶点数量之间传递材质和UV
        lprint ('处理的几何体数量:{}'.format(len(newMatGeos)))
        for newObj in newMatGeos:
            # 有的模型名称只做了部分改变,把这些物体单独放到一个字典中去
            matchDict={'ZLMat_NewMat:ZL_DnOrns_R_001_mo':'ZL:armor03','ZLMat_NewMat:ZL_DnOrns_L_001_mo':'ZL:armor17'}
            if matchDict.has_key(newObj):
                oldObj=matchDict[newObj]
            else:
                oldObj= newObj.replace(newNameSpace,rf.replace('MatRN',''))
            try:    
                if oldObj.split(':')[1]==newObj.split(':')[1] or sameObj :
                    if  cmds.nodeType(newObj)=='transform' and cmds.objExists(oldObj):
                        findSameObjIndex+=1
                        newShapeNode=cmds.listRelatives(newObj,s=1)[0]
                        oldShapeNode=cmds.listRelatives(oldObj,s=1)[0]
                        newMat=cmds.listConnections(newShapeNode,type='shadingEngine')
                        #cmds.polyTransfer( oldShapeNode,uv=1,ao=newShapeNode)
                        cmds.select(oldShapeNode)
                        lprint ('新的材质是:{}'.format(newMat))
                        cmds.sets(e=True, forceElement=newMat[0])
                        #cmds.hyperShade(a=newMat[0])
                        lprint ('同名物体{}传递材质给{}成功'.format(newObj,oldObj))
            except:
                s = sys.exc_info()
                lprint ('新物体:{},老物体{},传递材质失败'.format(newObj,oldObj))
                lprint ("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))
                pass
                #if newObj=='ZL_MMat_NewMat:head29':#Q'ZL_MMat_NewMat:head29':#
                    #break
        if findSameObjIndex<1:
            sys.path.append(r'S:\DataTrans\FQQ\plug_in\materialPlug\scripts')
            import autoTransferUV
            cmds.select(newNameSpace+':*')
            autoTransferUV.getSourceUV(dirConstraint=0,volumeConstraint=0,edgeSample=1)
            if cmds.objExists(rf[:-5]+':*'):
                cmds.select(rf[:-5]+':*')
                autoTransferUV.transferUV(dirConstraint=0,volumeConstraint=0,transferMat=1,transferMehtod=1,crackUV=1,edgeSample=1,transferUV=0)
        
    #sys.exit(0)  

    # 删除所有的显示层和渲染层和AOV
    cleanFile()

    genMayaFile=mayaFile[:-3]+'_AssignNewMat.ma'
    lprint ('genMayaFile:{}'.format(genMayaFile))
    # import mtoa.utils as mutils; 
    # light=mutils.createLocator("aiSkyDomeLight", asLight=True)
    # lprint (light,'create light ---------')
    # cmds.select(light[1])
    cmds.file(rename=genMayaFile)
    cmds.file(force=True, type='mayaAscii', save=True)  
    lprint ('----------------------------------------------------')
    filename = os.path.basename(mayaFile)[:-3]
    renderInfo=getRenderInfo()
    outFolder=os.path.dirname(mayaFile)+'/sequence'
    lprint ('输出文件夹:{},输出文件:{}'.format(outFolder,genMayaFile))
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    #renderOutput(renderInfo[0],renderInfo[1],outFolder,'exr',renderInfo[3],filename)  
    #'''
    ScriptFilename=r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\WinRightButton\deadLineRenderOut.py'
    import deadline_sumit
    deadline_sumit.ip =  "10.0.0.3"
    deadline_sumit.port = "8082"
    deadline_sumit.pool = 'fx'
    deadline_sumit.secondary_pool = 'cfx'
    deadline_sumit.priority = 100
    deadline_sumit.maya_version = "2018.5"
    deadline_sumit.frame = "{}-{}".format(renderInfo[0],renderInfo[1])
    #deadline_sumit.houdini_hython_path = settings['houdini_hython_path']
    deadline_sumit.submit_job(filename,genMayaFile,ScriptFilename,outFolder)
    lprint ('已提交任务{}到deadline'.format(filename))
    time.sleep(15)
    '''
import sys
sys.path.append(r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\WinRightButton')
import exFbx
reload(exFbx)
exFbx.C30assignNewMat()
    '''
#"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" S:\DataTrans\FQQ\plug_in\Lugwit_plug\WinRightButton\exFbx.py C30assignNewMat() "%1"         
#X:\Project\2018\C30\Shot_work\Lighting\1\Shot03_new\work\cs\C30_shot003_Lgt_CH01_1371-1441cs.ma                
# 渲染输出

# 导出Xgen As Ass

def exportXgenCode(sf='',ef=''):
    mayaFile = sys.argv[2]
    cmds.file(mayaFile, f=True, o=True)
    sys.path.append(r'S:\DataTrans\FQQ\plug_in\python2_lib')
    xgmPalettes=cmds.ls(type='xgmPalette')
    #mayaFile=cmds.file(q=True, sn=True)
    xgenSavePath=os.path.dirname(mayaFile)+'/XgenAssFile'
    lprint ('save path is:{}'.format(xgenSavePath))
    #maya.mel.eval('XgPreview')
    if not sf:
        sf = int(cmds.playbackOptions(min=1, q=1))
        ef = int(cmds.playbackOptions(max=1, q=1))
    if not os.path.exists(xgenSavePath):
        os.makedirs(xgenSavePath)
    xgenSavePathChildList=[]
    for xgm in xgmPalettes:
        xgmName=xgm.replace(':','_')
        xgenSavePathChild=xgenSavePath+'/'+xgmName
        if not os.path.exists(xgenSavePathChild):
            os.makedirs(xgenSavePathChild)
        cmds.select(xgm)
        path='"{}/{}_{}.ass"'.format(xgenSavePathChild,xgmName,ct)
        ass='arnoldExportAss -f {} -s -startFrame {} -endFrame {} -expandProcedurals  -fullPath -mask 6393 -shadowLinks 0 -lightLinks 0  -exportAllShadingGroups   -boundingBox -fullPath -asciiAss-cam perspShape;'.format(path,sf,ef)
        maya.mel.eval(ass)
        xgenSavePathChildList.append(xgenSavePathChild)




def exportXgenAsAss(sf='',ef='',xgmPalettes=[],ExDirSuffixParm='',deadLineParm={'pool':['vfx','cfx']}):
    import sys
    #list all xgmPalettes
    if not xgmPalettes:
        xgmPalettes=cmds.ls(type='xgmPalette')
    if not sf:
        sf = int(cmds.playbackOptions(min=1, q=1))-1
        ef = int(cmds.playbackOptions(max=1, q=1))+1
    mayaFile=cmds.file(q=True, sn=True)
    mayaFileName=os.path.basename(mayaFile)
    xgenSavePath=os.path.dirname(mayaFile)+'/XgenAssFile'
    import inspect
    ScriptFilename='S:/DataTrans/FQQ/plug_in/Lugwit_plug/Python/PythonLib/exportXgenASSDeadlineCode.py'
    import deadline_sumit
    deadline_sumit.ip =  "10.0.0.3"
    deadline_sumit.port = "8082"
    deadline_sumit.pool = deadLineParm['pool'][0]
    deadline_sumit.secondary_pool = deadLineParm['pool'][1]
    deadline_sumit.priority = 100
    deadline_sumit.maya_version = "2018.5"
    curTime=str(datetime.datetime.now()).split(' ')[1][:8].replace(':','_')
    deadline_sumit.BatchName = mayaFileName+'--'+curTime
    deadline_sumit.Blacklist = ['test']
    #deadline_sumit.frame = "{}-{}".format(sf-1,ef+1)
    #deadline_sumit.houdini_hython_path = settings['houdini_hython_path']
    for taskIndex in range(sf,ef+1):
        deadline_sumit.frame=str(taskIndex)
        with open(ScriptFilename,'r') as scriptContent:
            scriptContent=scriptContent.read().replace('setCurrentTime',str(taskIndex)).replace('ExDirSuffix',ExDirSuffixParm)
            NewPyFile=tempFolder+'/exXgenAss_'+str(taskIndex).zfill(4)+'_'+curTime+'.py'
            with open(NewPyFile,'w') as NewscriptFile:
                NewscriptFile.write(scriptContent)
        taskName=mayaFileName+'_'+str(taskIndex).zfill(4)
        deadline_sumit.submit_job( taskName,mayaFile,NewPyFile,xgenSavePath)
        lprint ('已提交任务{}到deadline'.format(taskName))
    time.sleep(2)

'''
import sys
sys.path.append(r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\Python\PythonLib')
import exFbx;reload(exFbx)
exFbx.exportXgenAsAss()
'''

def checkRefExist(ExDirSuffixParm='',deadLineParm={'pool':['vfx','cfx']},checkPath=r''):
    ScriptFilename=r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\Python\PythonLib\modifyPathCode.py'
    import deadline_sumit
    deadline_sumit.ip =  "10.0.0.3"
    deadline_sumit.port = "8082"
    deadline_sumit.pool = deadLineParm['pool'][0]
    deadline_sumit.secondary_pool = deadLineParm['pool'][1]
    deadline_sumit.priority = 100
    deadline_sumit.maya_version = "2018.5"
    curTime=str(datetime.datetime.now()).split(' ')[1][:8].replace(':','_')
    deadline_sumit.BatchName = 'checkRefExist'
    deadline_sumit.Blacklist = ['test']
    Path=checkPath.replace('\\','/')
    lprint ('Path:',Path)
    fileList=os.walk(Path)
    lprint ('fileList:',fileList)
    for root, dirs,files in fileList:
        lprint  (root)
        if root.endswith('towy') :
            for file in files:
                if 'test'  in file or 'deep' in file.lower() or '.mayaSwatche' in file or 'BG' in file:
                    continue
                absPath=os.path.join(root, file)
                absPath=absPath.replace('\\','/')
                if file.endswith('.mb') or file.endswith('.ma'):
                    with open(ScriptFilename,'r') as scriptContent:
                        scriptContent=scriptContent.read().replace('replaceMayaFilePath',absPath)
                        NewPyFile=tempFolder+'/'+file[:-3]+'.py'
                        with open(NewPyFile,'w') as NewscriptFile:
                            NewscriptFile.write(scriptContent)
                    deadline_sumit.submit_job( file,absPath,NewPyFile,'')
            lprint ('已提交任务{}到deadline'.format(deadline_sumit.BatchName))
    time.sleep(2)

'''
import sys
sys.path.append(r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\Python\PythonLib')
import exFbx;reload(exFbx)
exFbx.checkRefExist()
'''

#删除xgen文件
def deleteXgenNode(rightMenu=0):
    if rightMenu:
        mayaFile = sys.argv[2]
        cmds.file(mayaFile, f=True, o=True)
    else:
        mayaFile=cmds.file(q=1,sn=1)
    try:
        xgms=cmds.ls(type='xgmPalette')
        if xgms:
            for xgm in xgms:
                try:
                    cmds.select(cmds.listRelatives(xgm,p=1))
                    cmds.delete()
                except:
                    pass
            genMayaFile=mayaFile[:-3]+'_delXgen.ma'
            cmds.file(rename=genMayaFile)
            cmds.file(force=True, type='mayaAscii', save=True)  
            os.startfile(os.path.dirname(genMayaFile))
            lprint ('genMayaFile:{}'.format(genMayaFile))
        else:
            ('没有找到xgen节点')
    except:
        lprint ('没有找到"xgmPalette"类型物体')
    time.sleep(10)

#删除xgen文件  张辽赋予材质函数
def deleteXgen(mayaFile='',useExist=1,rightMenu=0):
    if rightMenu:
        mayaFile = sys.argv[2]
        cmds.file(mayaFile, f=True, o=True)
    with  open(os.path.dirname(__file__)+'/deleteXgenCode.txt','r') as xgenCode:
        deleteXgenCode=xgenCode.read()
    import os
    curTime=time.time()
    pyFileName=tempFolder+'/'+os.path.basename(mayaFile)+'.py'
    hasXgen=tempFolder+'/'+os.path.basename(mayaFile)+'.txt'
    with open(hasXgen,'w') as infoFile:
        infoFile.write('1')
    with open(pyFileName,'w') as pyFile:
        pyFile.write(deleteXgenCode.replace('mayaFile',repr(mayaFile)).replace('hasXgen',repr(hasXgen)))
    genMayaFile=mayaFile[:-3]+'_delXgen.ma'
    #genMayaFile=os.path.dirname(mayaFile)+'/New_delXgen.ma'
    batFileName=tempFolder+'/'+os.path.basename(mayaFile)+'.bat'
    batCode=r'"C:/Program Files/Autodesk/Maya2018/bin/mayapy.exe" {}'.format(pyFileName) 
    with open(batFileName,'w') as batFile:
        batFile.write(batCode)

    if useExist and os.path.exists(genMayaFile):
        return genMayaFile
    os.startfile(batFileName)
    #os.startfile(os.path.dirname(genMayaFile))
    while 1:
        with open(hasXgen,'r') as infoFile:
            info=infoFile.read()
            lprint  ('genMayaFile:{}有毛发,{}'.format(genMayaFile,info))
            if info=='0':
                return mayaFile
        if os.path.exists(genMayaFile) :
            gentime = os.stat(genMayaFile).st_mtime
            if gentime-curTime>10:
                lprint ('生成新的Maya材质文件成功')
                return genMayaFile
                break
        if time.time()-curTime>1000:
            lprint ('删除xgen的Maya文件:{}超时'.format(delXgenMayaFile))
            break

def cleanFile(delRen=1,delDis=1,delAOV=1):
    if delDis:
        displayLayers=cmds.ls(type='displayLayer')
        try:
            for displayLayer in displayLayers:
                cmds.select(displayLayer)
                cmds.delete()
        except:
            pass
    if delRen:
        renderLayers=cmds.ls(type='renderLayer')
        cmds.editRenderLayerGlobals( crl='defaultRenderLayer' )
        for renderLayer in renderLayers:
            cmds.select(renderLayer)
            try:
                cmds.delete()
            except:
                pass
                lprint (renderLayer)
    if delAOV:
        aiAOVs=cmds.ls(type='aiAOV')
        cmds.select(aiAOVs)
        cmds.delete()

    allLocatorNode=cmds.ls(type='locator')
    for  sh in  allLocatorNode:
        parNode=cmds.listRelatives(sh,p=1,f=1)
        if  parNode :
            if  cmds.nodeType(parNode[0])=='transform':
                cmds.select(parNode[0])
                cmds.delete() 

def delAllLight():
    allTrNode=cmds.ls(tr=1)
    allShapeNode=cmds.listRelatives(allTrNode,s=1,f=1)
    for  sh in  allShapeNode:
        if 'Light' in cmds.nodeType(sh):
            parNode=cmds.listRelatives(sh,p=1,f=1)
            if  parNode :
                if  cmds.nodeType(parNode)=='transform':
                    cmds.select(parNode[0])
                    cmds.delete()

def getRenderInfo():
    jsonExCfg=getjsonExCfg(cmds.file(q=1,sn=1))
    cameraShNode = findCamera()
    exCameraDict = dict()
    sf = int(cmds.playbackOptions(min=1, q=1))
    ef = int(cmds.playbackOptions(max=1, q=1))
    if len(cameraShNode)>1:
        exCameraDict = dict()
        for i, x in enumerate(cameraShNode):
            exCameraDict[i] = x
        lprint(u'场景中的摄像机列表:{}'.format(exCameraDict))
        if jsonExCfg:
            exYourCamera=cmds.listRelatives('|Cam',c=1)[0]
            sf = int(exYourCamera.split('_')[-2])
            ef = int(exYourCamera.split('_')[-1])
        else:
            exYourCamera = readInput(
                u'请选择你要导出的摄像机:', 0, 10)
        cameraShNode = exCameraDict[exYourCamera]
    else:
        cameraShNode = cameraShNode[0]
    cameraTrNode = cmds.listRelatives(cameraShNode, p=1)[0]
    return sf,ef,cameraShNode,cameraTrNode

def renderOutput(cameraStartFrame=1,cameraEndFrame=1,outFolder='D:/',renderFormat='exr',camera='',fileName = 'image'):
    '''
    函数参数介绍 :
    cameraStartFrame  ：  摄像机开始帧
    cameraEndFrame    ：  摄像机结束帧
    outFolder         ：  输出文件夹
    renderFormat      ：  渲染格式
    camera            ：  渲染的摄像机
    fileName          ：  生成图片的文件名称
    '''
    if not camera:
        camera=findCamera()[0]
    import maya.mel as mel    
    seq = ' '.join([str(i) for i in range(cameraStartFrame,cameraEndFrame+1)])
    mel.eval('setAttr -type "string" defaultRenderGlobals.imageFilePrefix "{}{}";'.format(outFolder,fileName))
    cmds.setAttr("defaultArnoldDriver.aiTranslator", renderFormat, type="string")
    cmds.arnoldRender(cam=camera,seq=seq)                   

