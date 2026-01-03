# coding:utf-8
from __future__ import print_function
#添加模块所在路径
import os,re,sys,time,sys,os
import traceback
curDir = os.path.dirname(__file__)
sys.path.insert(0,curDir)

from Lugwit_Module import *
lprint (__file__)



import shutil

from imp import reload
import os,sys

try:
    import maya.cmds as cmds
    import maya.mel as mm
    sf = int(cmds.playbackOptions(ast=1, q=1))
    ef = int(cmds.playbackOptions(aet=1, q=1))
    MayaFileDir=os.path.dirname(cmds.file(q=1,sn=1))
except:
    pass
import time
import getpass
userName=getpass.getuser()


#添加模块所在路径
import os,re,sys
curDir = os.path.dirname(__file__)
sys.path.insert(0,curDir)

sys.path.append(LugwitPath+r'\mayaPlug')
sys.path.insert(0,LugwitPath+r'\mayaPlug\l_scripts')


tempDir=os.environ['TEMP']
# 删除多余的shape节点
def cleanShapeNode(*args):
    sel=cmds.ls(sl=1)
    for s in sel:
        s_shapes=cmds.listRelatives(s,s=1)
        if len(s_shapes)>1:
            cmds.delete(s_shapes[1:])
        




#删除未知节点
def delete_unknowNodes(*args):
    ls_unknownNodes = cmds.ls(type='unknown')+cmds.ls(type='unknownDag')+cmds.ls(type='unknownTransfrom')
    lprint (u'清理未知节点:'.format(ls_unknownNodes))
    for unknownNode in ls_unknownNodes:
        if cmds.objExists(unknownNode):
            cmds.lockNode(unknownNode,lock=False)
            cmds.delete(unknownNode)
        else:
            lprint(u'\n\n\n\t你的场景已经清理未知节点')
    return ls_unknownNodes
#删除未知插件
def delete_unknowPlugins(*args):
    plugin_list = cmds.unknownPlugin(q=True,l=True) or []
    lprint (u'清理未知插件:{}...'.format(plugin_list[:10]))
    if plugin_list:
        for plugin in plugin_list:
            try:
                cmds.unknownPlugin(plugin,r=True)
            except:
                pass
    return plugin_list

def cleanFile(*args):  
    unknowNodes=delete_unknowNodes()
    unknowPlugin=delete_unknowPlugins()
    if unknowNodes:
        cmds.confirmDialog( title=u'清理文件', message=u'清理掉{}个未知节点'.format(len(unknowNodes)))
    if unknowPlugin:
        cmds.confirmDialog( title=u'清理文件', message=u'清理掉{}个未知插件'.format(len(unknowPlugin)))
    return unknowPlugin,unknowNodes

def exObjNamedByNodeName(*args):
    mayaFile=cmds.file(q=1,sn=1)
    mayaFileDir=os.path.dirname(mayaFile)
    exFileDir=mayaFileDir+'/exObj'
    if not os.path.exists(exFileDir):
        os.makedirs(exFileDir)
    sels=cmds.ls(sl=1)
    sels=cmds.listRelatives(sels,c=1)
    for sel in sels:
        if cmds.listRelatives(sel,s=1):
            cmds.select(sel)
            exFilePath=exFileDir+'/'+sel+'.obj'
            cmds.file(exFilePath,es=1,f=1,type='OBJexport',options='groups=0;ptgroups=0;materials=0;smoothing=1;normals=1')
    os.startfile(exFileDir)
    # #关闭窗口
    # def delete_UI(*args):
    #     cmds.deleteUI(window,window=True)

    # #打开窗口
    # window = cmds.window( title='点击清理相关项',widthHeight=(200,100) )
    # cmds.columnLayout( adjustableColumn=True,columnOffset=('both',20),rowSpacing=10,columnWidth=50 )
    # cmds.button( label='清理未知节点', command=delete_unknowNodes )
    # cmds.button( label='清理未知插件',command=delete_unknowPlugins )
    # cmds.button( label='关闭',command=delete_UI )
    # cmds.showWindow()
    
def listHisNodeByType(nodeName='',nodeList='',nodeType='blendShape'):
    cleNode=[]
    if nodeName:
        nodes=[nodeName]
    else:
        nodes=nodeList
    for node in nodes:
        con = sorted(cmds.listHistory(node))
        for con_a in con:
            if cmds.nodeType(con_a) == nodeType:
                cleNode.append(con_a)
    return cleNode

def cleanVtxDateAndDelHis(*args):
    for s in cmds.ls(sl=1):
        cmds.polyNormalPerVertex(s,ufn =1)
        cmds.ConformPolygonNormals()
        cmds.DeleteHistory()
        
def cleanImportObj(*args):
    cleanShapeNode()
    sl=cmds.ls(sl=1)
    for s in cmds.ls(sl=1):
        cmds.polyNormalPerVertex(s,ufn =1)
        mm.eval('SoftPolyEdgeElements 1')
        cmds.DeleteHistory()
    cmds.select(cl=1)
    cmds.select(sl)
        
def restoreDefaultTransformAttribute(t=0,r=0,s=0):
    sels=cmds.ls(sl=1)
    for sel in sels:
        #trValueList=cmds.attributeQuery('translate',node=s,listDefault=1)
        #trValueList=cmds.attributeQuery('tx',node=s,listDefault=1)
        for i in range(3):
            try:
                if t:
                    cmds.setAttr(sel+'.t'+'xyz'[i],0)
                if r:
                    cmds.setAttr(sel+'.r'+'xyz'[i],0)
                if s:
                    cmds.setAttr(sel+'.s'+'xyz'[i],1)
            except Exception as e:
                lprint (e)
                
class View():
    def __init__(self): 
        self.curPanel=cmds.getPanel(up=True)
        lprint (u'当前面板是{}'.format(self.curPanel))
    def onlyDisPolygon(self,*args):
        curPane=cmds.getPanel(up=True)
        lprint (curPane)
        lprint (tempDir+'/'+curPane+'.txt')
        with open(tempDir+'/'+curPane+'.txt','a+') as open_curPane:
            read_curPane=open_curPane.read()
            try:
                vis=int(bool(eval(read_curPane)))
            except:
                vis=0
            open_curPane.seek(0, 0)
            open_curPane.truncate()
            open_curPane.write(str(1-vis))
        cmds.modelEditor(curPane,e=1,allObjects=vis)
        cmds.modelEditor(curPane,e=1,pm=1)
    def disAll(self,*args):
        curPane=cmds.getPanel(up=True)
        cmds.modelEditor(curPane,e=1,allObjects=1)
    def disByType(self,comTypes='',*args):
        curPane=cmds.getPanel(up=True)
        if isinstance(comTypes,str):
            comTypes=[comTypes]

        disStr=''
        for comType in comTypes:
            curValue='cmds.modelEditor("{}",q=1,{}=1)'.format(curPane,comType)
            curValue=eval(curValue)
            if cmds.modelEditor(curPane,q=1,planes=1):
                lprint (u'当前显示类型{}显示状态为{}'.format(comType,curValue))
                disStr+='{}=1,'.format(comType)
            else:
                cmds.modelEditor(curPane,e=1,allObjects=1)
                return
        cmds.modelEditor(curPane,e=1,allObjects=0)
        ss='cmds.modelEditor("{}",e=1,{})'.format(cmds.getPanel(up=True),disStr)
        lprint ('ss-----',ss)
        exec (ss)
    
    @staticmethod
    def higShowMesh(*args):    
        curPane=cmds.getPanel(up=True)
        now = cmds.modelEditor(curPane, q=True, selectionHiliteDisplay=1)
        now = cmds.modelEditor(curPane, e=True, selectionHiliteDisplay=1-now)

def mirrorTransferPosition(*args):
    '''
    把第一个物体的所有顶点的x的坐标传递给第二个物体
    '''      
    sl=pm.ls(sl=1)
    oriMesh=sl[0]
    tarMesh=sl[1]
    tarMeshVtx=tarMesh.vtx
    for index,vtx in enumerate(oriMesh.vtx):
        tr=vtx.getPosition('world')
        tarMeshVtx[index].setPosition([-tr[0],tr[1],tr[2]])

def unlockInitialShadingGroup(*args) :  
    cmds.lockNode('initialShadingGroup',l=0,lu=0) ;
    cmds.lockNode('defaultTextureList1',l=0,lu=0) ;
    cmds.lockNode('defaultShaderList1',l=0,lu=0) ;


class getProjectInfo():
    def __init__(self):
        pass
    def getActiveCamera(self):
        activeCamera = om.MDagPath()
        omui.M3dView().active3dView().getCamera(activeCamera)
        return activeCamera.fullPathName()
    def isLoadUI(self,infoFile):
        self.setCamera()
        lookCamera=cmds.lookThru( q=True )
        lprint ('lookCamera-----{}\n'.format(lookCamera))
        findCamera=cmds.listRelatives(self.findCamera()[0],p=1)[0]
        lprint ('findCamera-----{}\n'.format(findCamera))
        lprint (lookCamera == findCamera)
        lprint ('infoFile:{}'.format(infoFile))
        lprint (type(lookCamera))
        lprint (  type(findCamera))
        if lookCamera == findCamera:
            with open(infoFile,'r+') as openInfoFile:
                txt=openInfoFile.readlines()
                txt[2]=self.findCamera()[0]+'\n'
                openInfoFile.seek(2)
                openInfoFile.truncate()
                openInfoFile.writelines(txt)
                lprint ('set camera sucess')

    def findCamera(self):
        cameraList = []
        cameraList = cmds.ls(type='camera')
        selfCameraList = ['sideShape', 'frontShape', 'topShape', 'perspShape']
        cameraList = set(cameraList)-set(selfCameraList)
        return list(cameraList)

    def setCamera(self,camera='',infoFile=''):
        if not camera:
            cmds.lookThru(self.findCamera()[0])
            lprint ('set camera {}'.format(self.findCamera()[0]))
            
class fileIO():
    def __init__(self):
        self.sf = int(cmds.playbackOptions(min=1, q=1))
        self.ef = int(cmds.playbackOptions(max=1, q=1))
        self.mayaFilePath=cmds.file(q=1,sn=1)
        self.mayaFileName=os.path.basename(self.mayaFilePath)
        self.MayaFileFolder=os.path.dirname(self.mayaFilePath)
    def exportXgenASS(self,assNodeList=[],frameRange=[-1,-1],replaceExist=0,outFolder=''):
        if frameRange[0]<0:
            frameRange=range(self.sf-1,self.ef+1)
        else:
            frameRange=range(frameRange[0],frameRange[1]+1)
        if not outFolder:
            outFolder=self.MayaFileFolder
        if not assNodeList:
            assNodeList=cmds.ls(type='xgmPalette')
        lprint ('assNodeList:{}'.format(assNodeList))
        lprint ('frameRange:{}'.format(frameRange))
        for frame in frameRange:
            cmds.currentTime(frame)
            for xgm in assNodeList:
                cmds.select(xgm)
                lprint ('xgmNode:{}'.format(xgm))
                if ':' in xgm:
                    xgm=xgm.split(':')[1]
                xgmSavePath=outFolder+'/XgenAssFile_'+xgm
                if not os.path.exists(xgmSavePath):
                    os.makedirs(xgmSavePath)
                currentFrame=str(frame).zfill(4)
                path='"'+xgmSavePath+'/'+xgm+'_'+currentFrame+'.ass'+'"'
                lprint ('ass file "{}" already exist,is replaceExist ({})-----'.format(path,replaceExist))
                with open('D:/aa.txt','w') as aa:
                    aa.write('ass file "{}" already exist {} ,is replaceExist ({})-----'.format(path,os.path.exists(path),replaceExist))
                if os.path.exists(path) and not replaceExist:
                    lprint ('ass file "{}" already exist,is replaceExist ({})+++++'.format(path,replaceExist))
                    continue
                
                assArnold='arnoldExportAss -f {} -s -expandProcedurals  -mask 6393 -shadowLinks 0  -lightLinks 0  -exportAllShadingGroups   -boundingBox -fullPath -asciiAss-cam {};'.format(path,getProjectInfo().findCamera()[0])
                lprint (assArnold)
                #assFile='file -force -options "-expandProcedurals;-shadowLinks 0;-mask 6393;-lightLinks 0;-exportAllShadingGroups;-boundingBox;-fullPath;-asciiAss" -typ "ASS Export" -pr -es "{}"'.format(path)
                maya.mel.eval(assArnold)
    def setPort(self,port):
        cmds.commandPort(n = ":{}".format(port),stp="python");   
        '''
        import sys
        sys.path.append(r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\Python\PythonLib')
        import mayaLib
        mayaLib.fileIO().sotPort()
        '''  
    def splitXgenTodiffMayaFile(self,xgmPalettes=[]):
        '''
        import sys
        sys.path.append(r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\Python\PythonLib')
        import mayaLib
        mayaLib.fileIO().splitXgenTodiffMayaFile(cmds.ls(type='xgmPalette')[2:3])
        '''
        if not xgmPalettes:
            xgmPalettes=cmds.ls(type='xgmPalette')
        GenNewMayaFileCodeFile=r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\Python\PythonLib\exportXgenASSDeadlineCode_A.py'
        tempFolder='S:/DataTrans/FQQ/temp/mayaTemp'
        mayaFilePath=cmds.file(q=1,sn=1)
        mayaFileName=os.path.basename(mayaFilePath)
        for i,xgm in enumerate(xgmPalettes):
            with open(GenNewMayaFileCodeFile,'r') as codeA:
                codeA=codeA.read()
                codeA=codeA.replace('xgmNode',xgm).replace('openMayaFile',mayaFilePath)
            if ':' in xgm:
                xgmNodeName=xgm.split(':')[1]
            else:
                xgmNodeName=xgm
            pyExAssFile= tempFolder+'/exXgenAss_'+xgmNodeName+'.py'
            with open(pyExAssFile,'w') as codeB:
                codeB.write(codeA)
            
            batFileName=tempFolder+'/exXgenAss_'+xgmNodeName+'.bat'
            batCode=r'"C:/Program Files/Autodesk/Maya2018/bin/mayapy.exe" {}'.format(pyExAssFile) 
            with open(batFileName,'w') as codeC:
                codeC.write(batCode)
            taskName=xgmNodeName
            time.sleep(i*0.1)
            os.startfile(batFileName)



def bakeCameraUI(exCameraOption=1):
    import IOLib.exFbx as exFbx
    if not cmds.ls(sl=1):
        cmds.confirmDialog( title='Warning', message='Please select a camera' )
    mayaFile=cmds.file(q=1,sn=1)
    mayaFileDir=os.path.dirname(mayaFile)
    defaultExCameraPath=mayaFileDir+'/camara.fbx'
    lprint (defaultExCameraPath)
    sf = int(cmds.playbackOptions(ast=1, q=1))
    ef = int(cmds.playbackOptions(aet=1, q=1))
    if exCameraOption:
        window=cmds.window(s=0,title=u"导出摄像机,请选中一个摄像机再进行导出或者烘焙操作", widthHeight=(450, 100))
        cmds.columnLayout( adjustableColumn=True )
        cmds.intFieldGrp( 'bakeCameraRange',numberOfFields=2, label=u'帧范围', value1=sf, value2=ef)
        cmds.textFieldButtonGrp( 'exCamPath',label=u'导出位置', text=defaultExCameraPath, buttonLabel=u'浏览',bc=getPath)
        bakeSf=cmds.intFieldGrp('bakeCameraRange' ,q=1, value1=1)
        bakeEf=cmds.intFieldGrp('bakeCameraRange' ,q=1, value2=1)
        cmds.button(label=u'烘焙摄像机',c= lambda *args :exFbx.bakeCamera(cmds.ls(sl=1)[0],bakeSf,bakeEf))
        getExFileDir=cmds.textFieldButtonGrp('exCamPath',q=1,text=1)#.replace('\\','/')
        cmds.button(label=u'烘焙并导出摄像机',c= lambda *args :exFbx.exCamera(mayaFile='', sf=bakeSf, ef=bakeEf, savePath=getExFileDir,cameraTrNode=cmds.ls(sl=1)[0]) )
        
        cmds.showWindow( window )
    else:
        sf = int(cmds.playbackOptions(ast=1, q=1))
        ef = int(cmds.playbackOptions(aet=1, q=1))
        exFbx.bakeCamera(cmds.ls(sl=1)[0],sf,ef)


def getPath():
	multipleFilters = 'fbx Files(*.fbx)'
	pathName=cmds.fileDialog2(fileMode=1, caption="select fbxFile",ff=multipleFilters,fm=0,dir=MayaFileDir)[0]
	cmds.textFieldButtonGrp('exCamPath',e=1,tx=pathName)
	# maya.mel.eval("updateFileNodeSwatch("+'"'+FileNode+'")')

def cvtFaceSetSG(cvtObj='',*args,**kwargs): #转换为分面材质球
    print(locals())
    cmds.lockNode('initialShadingGroup',l=0,lu=0)
    convertList=[]
    processedSGList=[]
    if not cvtObj:
        cmds.SelectHierarchy()
    else:
        cmds.select(cvtObj)
        cmds.SelectHierarchy()
    sel_list = cmds.ls(sl=1,dag=1,type="mesh",l=1)
    lprint("XKX_ChA_LiBai_rig1:XKX_ChA_LiBai_Bao_GeoShape" in str(sel_list))
    if not sel_list:
        cmds.headsUpMessage("请选择模型再次执行脚本")
    else:
        for shapeNode in sel_list:
            SGNodeList = cmds.listConnections(shapeNode,type="shadingEngine")
            if SGNodeList:
                SGNodeList = list(set(SGNodeList))
                if u'initialShadingGroup' in SGNodeList:
                    SGNodeList.remove(u'initialShadingGroup')
                if len(SGNodeList)==1:
                    for SGNode in SGNodeList:
                        # if SGNode in processedSGList:
                        #     print()
                        #     continue
                        cmds.select(SGNode)
                        selectlist=cmds.ls(sl=1)
                        faceSetList=[]
                        for select in selectlist:
                            if cmds.nodeType(select)!="mesh":
                                continue
                            if '.' not in select:
                                faceAmount=cmds.polyEvaluate(select, f=1)
                                try:
                                    faceSetList.append(select+'.f[0:{}]'.format(faceAmount-1))
                                except Exception as e:
                                    lprint(faceAmount,cmds.nodeType(select))
                                    print(traceback.format_exc())
                                    lprint(u"当前选择是,{}".format(select))
                                    raise (e)
                                    
                                    
                        cmds.select(select,cl=1)
                        for select in selectlist:     
                            try: 
                                cmds.select(select,add=1)
                            except:
                                print(traceback.format_exc())
                                print(u"当前选择面集列表是-{},着色节点是-{}".format(select,SGNode))
                        lprint("XKX_ChA_LiBai_rig1:XKX_ChA_LiBai_Bao_GeoShape" in str(cmds.ls(sl=1)))
                        cmds.ConvertSelectionToFaces()
                        cmds.sets(fe="initialShadingGroup", e=1)
                        cmds.sets(forceElement=SGNode, e=1)
                        convertList.append(shapeNode)
            if SGNodeList:
                processedSGList+=SGNodeList

    cmds.select(cl=True)
    cmds.headsUpMessage( u'转换成功{}个mesh,前三个是'.format(len(convertList)))
    # lprint(sel_list)
    print (u"转换列表{}".format(convertList))
            
def cleanNameSpace(*args):
    import re
    print (cmds)
    refs=cmds.ls(type='reference')
    for ref in refs:
        try:
            nameSpace=cmds.referenceQuery(ref,ns=11)
            colon=re.findall(':',nameSpace)
            lprint (colon)
            if len(colon)>1:
                lprint (u'清理名称空间{}'.format(nameSpace))
                nameSpace=nameSpace[1:]
                nameSpace=nameSpace.rsplit(':',1)[0]
                lprint (u'清理名称空间{}'.format(u'清理后的名称空间为{}'.format(nameSpace)))
                lprint (cmds.namespace( removeNamespace=nameSpace+':', mergeNamespaceWithRoot = True))
        except:
            pass
        
def list_all_children_mesh(nodes,getTrNode=1):
    """Invalid because it will ignore a child if it's in 'nodes'
    whilst it was a child of another node in the list."""
    
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
        children.append(node)
    if getTrNode:
        children=[x for x in cmds.listRelatives(children, parent=True, fullPath=True) if x]
    return children 

def cleanKeyFrame(*args):
    sel=cmds.ls(sl=1)
    all_children_mesh=list_all_children_mesh(sel,getTrNode=1)
    for mesh in all_children_mesh:
        cmds.disconnectAttr(mesh+'.tx');

def screenShot(*args):
    import maya.OpenMaya as OpenMaya
    import maya.OpenMayaUI as OpenMayaUI
    view = OpenMayaUI.M3dView.active3dView()
    camDag = OpenMaya.MDagPath()
    view.getCamera(camDag)
    camera = camDag.fullPathName()
    cameraName= cmds.listRelatives(camera, parent = True)[0]
    curRender=cmds.getAttr("defaultRenderGlobals.ren",);
    cmds.setAttr("defaultRenderGlobals.ren",'mayaHardware2',type='string');
    defaultResolutionW=cmds.getAttr("defaultResolution.width")
    defaultResolutionH=cmds.getAttr("defaultResolution.height")
    cmds.setAttr("defaultRenderGlobals.imageFormat",8)
    cmds.setAttr("defaultRenderGlobals.animation",0)
    cmds.colorManagementPrefs(e=True, ote=1)
    outImagePath=cmds.ogsRender(w=defaultResolutionW,h=defaultResolutionH)
    newPath=cmds.fileDialog2(fileFilter='*.jpg', dialogStyle=2)[0]
    shutil.copyfile(outImagePath,newPath)
    cmds.setAttr("defaultRenderGlobals.ren",curRender,type='string');
    
def getSGs(obj):
    try:
        obj=cmds.listRelatives(obj,s=1)
    except:
        pass
    if obj:
        shader=cmds.listConnections(obj,type='shadingEngine')
        return list(set(shader))
        #shader=listConnections(shader)
        #mat=list(set(ls(shader,mat=1)))

def getMat(obj):
    try:
        obj=cmds.listRelatives(obj,s=1)
    except:
        pass
    try:
        shader=cmds.listConnections(obj,type='shadingEngine')
        shader=[cmds.listConnections(s+'.surfaceShader') for s in shader]
        mat=list(set(cmds.ls(shader,mat=1)))
        return mat
    except:
        return []
    
def shapeNodeMatchTransfromNode(*args):
    transformNodeList=cmds.ls(type='transform')
    for transfromNode in transformNodeList:
        shapeNodeList=cmds.listRelatives(transfromNode,s=1,f=1)
        if shapeNodeList:
            for shapeNode in shapeNodeList:
                if shapeNode.split('|')[-1]==transfromNode.split('|')[-1]:
                    cmds.rename(shapeNode,shapeNode.split('|')[-1]+'shape')

def selsrfNUL_VisPloy(*args):
    if ':' in cmds.ls(sl=1)[0]:
        nameSpace=cmds.ls(sl=1)[0].split(':')[0]
    else:
        nameSpace=''
    cmds.select(nameSpace+":srfNUL")
    cmds.SelectHierarchy()
    all_objects=cmds.ls(sl=1,l=1)
    # 过滤出所有可见的多边形物体
    visible_polygons = []
    for obj in all_objects:
        # 检查物体是否是多边形物体
        if cmds.polyEvaluate(obj, vertex=True):
            # 检查物体的可见性和 lodVisibility
            if cmds.getAttr(obj + ".visibility") and cmds.getAttr(obj + ".lodVisibility"):
                shNode=cmds.listRelatives(obj,s=1)
                if shNode:
                    visible_polygons.append(obj)

    # 打印或选择所有可见的多边形
    cmds.select(visible_polygons)
    cmds.warning(u"你选择了{}个物体".format(len(visible_polygons)) )
