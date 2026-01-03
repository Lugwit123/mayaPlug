# coding:utf-8
import time,os,sys,json,traceback,inspect
#导出基础模块
import subprocess
import shutil
from imp import reload
import functools
import sys
import glob
import re
import os
import codecs
import getpass
from shutil import copyfile
try:
    import _winreg as winreg
except:
    import winreg

os.environ['QT_API'] = 'PySide2'
st=time.time()
LugwitToolDir=os.environ.get('LugwitToolDir')
sys.path.append(LugwitToolDir+'/Lib')

if r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp" in sys.path:
    sys.path.remove(r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp")
    
from Lugwit_Module import *
import Lugwit_Module as LM
sys.path.append(LM.Lugwit_mayaPluginPath)
lprint=LM.lprint
print("LugwitToolDir",LugwitToolDir)

LugwitPath=os.environ.get('LugwitPath')
Lugwit_PluginPath=os.environ.get('Lugwit_PluginPath')
Lugwit_publicPath=os.environ.get('Lugwit_publicPath')
__file__=inspect.getfile(inspect.currentframe())
print ('run module{}'.format(__file__))
print (u'系统变量-->{}'.format(sys.argv),)


    
#添加模块所在路径
fileDir = os.path.dirname(__file__)
sys.path.insert(0,fileDir)


#添加自己写的模块
sys.path.append(LugwitPath+r'\Python\PythonLib\Perforce')
sys.path.append(LM.Lugwit_mayaPluginPath+ r'\ThridPlug')
sys.path.insert(0,LM.Lugwit_mayaPluginPath+r'\l_scripts\fun')
# import mod.hierarchy.ui as hierarchy_modui

#导入Maya模块
# import maya.standalone
# maya.standalone.initialize(name='python')
import maya.mel as mm
mel = mm
mm.eval('renderThumbnailUpdate false;')
import maya.cmds as cmds
from functools import partial
from maya.utils import executeInMainThreadWithResult
from l_scripts import L_GV
cmds.loadPlugin('Dll1_'+cmds.about(v=1))
#获取系统参数
userName = getpass.getuser()
try:
    cmds.loadPlugin("MayaScanner")
    cmds.loadPlugin("MayaScannerCB")
except:
    pass

unfold3dPath=Lugwit_P4CLIENTDIR+r'\Software\ProgramFiles\RizomUV2022\rizomuv.exe_lugwit.lnk'
sys.path.append(LugwitPath+r'\Python\PythonLib\generalLib')

#插件相关路径
iconDir = LM.Lugwit_mayaPluginPath+'/icon/'
# 模块目录
moduleFile = __file__
moduleFile = moduleFile.replace('\\', '/')
moduleDir = os.path.dirname(moduleFile)
#Maya插件目录
mayaPlugDir = LM.Lugwit_mayaPluginPath
scriptsDir = mayaPlugDir+'/l_scripts'

#获取我的文档目录
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                      r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
docuDir = winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/')
print(u'我的文档目录是---:{}'.format(docuDir))


#添加python库目录
sys.path.append(scriptsDir)  # 当前目录路径
sys.path.insert(0,LM.Lugwit_mayaPluginPath)

#导入自定义模块


import M_ViewLib
print ('import M_ViewLib')
#加载第三方模块
sys.path.append(LM.Lugwit_mayaPluginPath+r'\l_scripts\ThridLib')
import pyperclip
print ('import pyperclip')


#导入Maya材质插件模块
import materialPlug.scripts as mps
print ('import mps')
#导入Lugwit插件模块

import l_scripts

print ('import l_scripts')

#导入Lugwit插件模块大库
IOLib=l_scripts.IOLib
print ('IOLib')
RigLib=l_scripts.Rig
print ('RigLib')
usualLib=l_scripts.usualLib
print ('usualLib')
usual=usualLib.usual
print ('124usual')
from l_scripts.usualLib import ui_code,attr_connect

ui_code.modify_font()

from l_scripts.l_FX import main as l_FX





txLib=l_scripts.Texture
mj=RigLib.MatchJoint
usRig=RigLib.usualRig

print (u'全局变量花费时间{},导入所有模块'.format(time.time()-st))

def uninstall(*args):
    if cmds.control("HDR_rowLayout", ex=1):
        cmds.deleteUI("HDR_rowLayout")
    if cmds.rowColumnLayout("LugwitToolBox", ex=1):
        cmds.deleteUI("LugwitToolBox")
    if cmds.control('L_V', ex=1):
        cmds.deleteUI('L_V')
    allPane=cmds.getPanel(type='modelPanel')
    for pane in allPane:
        if cmds.control('LugwitViewMenuA_'+pane,q=1,ex=1):
            cmds.deleteUI('LugwitViewMenuA_'+pane)
    mayaLocation=os.getenv("MAYA_LOCATION")
    for moduleName,module in sys.modules.items():
        if module:
            try:
                module_file=getattr(module,'__file__',"")
                if 'Lugwit' in module_file :
                    if 'reload' not  in module_file:
                        if 'import' not in str(module):
                            if not module_file.startswith(mayaLocation):
                                print (u'卸载模块{}'.format(moduleName))
                                del sys.modules[moduleName]
            except:
                traceback.print_exc()   
    

def install(*args):
    import debug_ui
    debug_ui.SwitchButtonFunc()
    
    sys.path.append(Lugwit_mayaPluginPath)
    from MayaMenu import createMenu
    createMenu.CreateMainMenu(sso_menu="PipeLine_Menu")
    
    statusLine = mel.eval('global string $gStatusLine;$temp = $gStatusLine;')
    if cmds.rowLayout("HDR_rowLayout", ex=1,q=1):
        cmds.deleteUI("HDR_rowLayout")
    cmds.rowLayout("HDR_rowLayout", p=statusLine,numberOfColumns=6,)
    cmds.checkBox('allOrSel', value=0, 
                  l=u'全部或\n者选择', 
                  ann=u'勾选应用于全部物体,不勾选应用于选择物体')
    cmds.text(u'HDR\nMaya文件',bgc=[0.7,0.8,0])
    cmds.iconTextButton(label=u'白天', image1=Lugwit_publicPath+r'\MayaLightEnv\icon\day.jpg',
                        h=20,w=30,font='boldLabelFont',ann=u'白天HDR',
    c=lambda *args: cmds.file(Lugwit_publicPath+r'/MayaLightEnv/Light_LookDev.ma',
                              r=1,namespace='DayHDR'))
    cmds.popupMenu(b=3, mm=1)
    cmds.menuItem(rp="S",label=u'卸载',
                  c=lambda *args:cmds.file(Lugwit_publicPath+r'/MayaLightEnv/Light_LookDev.ma',rr=1))
    
    cmds.iconTextButton(label=u'夜晚', image1=Lugwit_publicPath+r'\MayaLightEnv\icon\night_HDR.jpg',
                        h=20,w=40,font='boldLabelFont',ann=u'夜晚HDR',)
    
    @try_exp
    def openFileCheckWin(*args):
        RELATIVE = 0
        SUFFIX = None
        ICON = 'publish.png'
        TOOLTIP = u'模型发布工具'
        sys.path.append(LM.Lugwit_mayaPluginPath+r'\LfileCheck\file_check_kit\maya\scripts')
        from publish import publishMain as PM
        reload ( PM )
        PM.Publish(abbr='mod', tooltip=TOOLTIP).showWin()
        
    cmds.button(label=u'模型检查', h=30,w=50,c=openFileCheckWin)
    cmds.button(label=u'贴图尺寸切换', h=30,c=txLib.mapSizeSwitch.show_ui)
    

    ToolBoxMenu()

    # 视图菜单
    viewWS() 

    modelPaneMenu()

    
def lockLugwitPlug(lock=1):
    import os
    path_enUS=docuDir+r'\maya\{}\prefs\pluginPrefs.mel'.format(cmds.about(version=1))
    print ('path_enUS->',path_enUS)
    path_zhCN=os.path.expandvars("$HOME")+r'\maya\{}\zh_CN\prefs\pluginPrefs.mel'.format(cmds.about(version=1))
    pathList=[path_enUS,path_zhCN]
    plugStr=r'evalDeferred("autoLoadPlugin(\"\", \"LugwitStartPlug.py\", \"LugwitStartPlug\")");'
    for path in pathList:
        if not os.path.exists(path):
            continue
        cmd_onlyRead=u'attrib +r {}'.format(path)
        cmd_read=u'attrib -r {}'.format(path)
        if lock==1:
            # if 'R' in fileAttr_onlyRead:
            #     subprocess.Popen(cmd_read)
            noLugwitPlugInStarrtList=False
            with open(path,'r') as open_path:
                read_path=open_path.read()
                if plugStr not in read_path:
                    noLugwitPlugInStarrtList=True
            if noLugwitPlugInStarrtList==True:
                subprocess.Popen(cmd_read)
                with open(path,'a+') as open_path:
                    read_path=read_path.replace('\n'+plugStr,'')
                    read_path+=plugStr
                    print (read_path)
                    open_path.seek(0, 0)
                    open_path.truncate()
                    open_path.write(read_path)
            fileAttr=subprocess.Popen(u'attrib {}'.format(path),stdout=subprocess.PIPE).stdout.read()
            if 'R' not in str(fileAttr):
                subprocess.Popen(cmd_onlyRead)
        elif lock==0:
            subprocess.Popen(cmd_read)
lockLugwitPlug()
        
    


def usualDirMenu():
    cmds.menuItem(label=u'Maya文件目录', p=items['usualDir'], c=lambda *args: os.startfile(
        os.path.dirname(cmds.file(q=1, sn=1))))
    tempDir_menuItem=cmds.menuItem('tempDir', label=u'Temp目录(新到旧)',
                  p=items['usualDir'], subMenu=1)
    for mayaFile in mayaFileInTempDir():
        mayaFile = mayaFile.replace('\\', '/')
        c = "cmds.file('{}',o=1,f=1)".format(mayaFile)
        cmds.menuItem(label=mayaFile, p=tempDir_menuItem, c=c)

def execute_code(code, *_):
    

    try:
        executeInMainThreadWithResult(code)
    except Exception as e:
        lprint (u'执行代码失败,原因是{}'.format(e))
        mm.eval(code)
    except Exception as e:
        print(u"code\n{}\n{}\n".format(code,e))
        
def execute_CodeFile(codeFile, *_):
    try:
        execfile(codeFile)
    except Exception as e:
        print ('try run python code file {} failed,reason is {}'.format(codeFile,e))
        try:
            with codecs.open(codeFile, 'r', 'utf-8') as f:
                code = f.read()
                mm.eval(code)
        except Exception as e:
            print ('try run open code file {}  failed,reason is {}'.format(codeFile,e))
            mm.eval('source {}'.format(codeFile))

            
def smallToolMenu(TempToolDir,parentMenu=None,menuLabel=u'临时小工具'):   
    #temToolMenu=cmds.menuItem(label=menuLabel, subMenu=1, to=1,p=parentMenu)
    cmds.menuItem(label=u'∨∨∨∨∨∨∨∨∨∨∨∨小工具∨∨∨∨∨∨∨∨∨∨∨∨', 
                p=parentMenu,image=LugwitPath+'/icons/tool.png')
    #cmds.separator(p=parentMenu)
    cmds.menuItem(label=u'打开小工具目录,可以自己添加小插件', c=lambda *args : os.startfile(TempToolDir),p=parentMenu,image=LugwitPath+'/icons/openfolder.ico')
    fileInDir=glob.glob(TempToolDir + "/*.[py,mel,txt]*")
    print (u'临时工具目录{}里面的文件{}'.format(TempToolDir,fileInDir))
    for pyFile in fileInDir:
        label=os.path.basename(pyFile)
        if pyFile.endswith('.pyc'):
            continue
        cmds.menuItem(label=label, c=partial(execute_CodeFile,pyFile),p=parentMenu)
            
def ModMenu():
    
    sys.path.append(mayaPlugDir+r'/l_scripts')
    print (os.path.exists(mayaPlugDir+r'/l_scripts'))
    import fun
    # 临时工具菜单
    TempToolDir=mayaPlugDir+r'/l_scripts/Mod/modTempTool'
    smallToolMenu(TempToolDir=TempToolDir,parentMenu=items['Mod'],menuLabel=u'临时小工具')
    
    # cmds.menuItem(label=u'选择没有材质球的物体', p=items['Tex'], c=mps.uvSetTool.nonSG)

def texMenu():
    sys.path.append(mayaPlugDir+r'/l_scripts')
    print (os.path.exists(mayaPlugDir+r'/l_scripts'))
    import fun
    cmds.menuItem(label=u'选择没有材质球的物体', p=items['Tex'], c=mps.uvSetTool.nonSG)
    cmds.menuItem(label=u'生成规范命名贴图', p=items['Tex'], c=combineMap)
    cmds.menuItem(label=u'贴图管理', p=items['Tex'], c=txLib.textureManager.main)
    cmds.menuItem(label=u'转换为分面材质球', p=items['Tex'], c=usual.cvtFaceSetSG)
    cmds.menuItem(label=u'转换颜色空间', p=items['Tex'], c=txLib.SetColorSpace.main)
    cmds.menuItem(label=u'AOV渲染分层', p=items['Tex'], c=fun.Tex.RenderDividelayer.ui_Main_ins.show_Main)
    cmds.menuItem(label=u'A解决分面材质球', p=items['Tex'], c=fun.Tex.RenderDividelayer.ui_Main_ins.show_Main)
    # 临时工具菜单
    texTempToolDir=mayaPlugDir+r'/l_scripts/Texture/TempTool'
    smallToolMenu(TempToolDir=texTempToolDir,parentMenu=items['Tex'],menuLabel=u'临时小工具')



def IOMenu():
    cmds.menuItem(label=u'导出ABC', p=items['IO'],)
    sys.path.append(Lugwit_publicPath+r'\plug_in\Lugwit_plug\mayaPlug\l_scripts\usualLib')
    
    cmds.menuItem(label=u'工程打包', p=items['IO'], c=IOLib.pack.main)
    cmds.menuItem(label=u'导出选择物体材质Json文件', p=items['IO'], 
                  c=lambda *args:IOLib.export_mat_json(Key='Obj'))
    cmds.menuItem(label=u'导出选择物体材质Json文件(临时目录)', p=items['IO'], 
                  c=lambda *args:IOLib.export_mat_json(Key='Obj',path=os.environ['TEMP']+'\\matJson.json'))
    
    cmds.menuItem(label=u'导出所有的ShadingGroup网络', \
                p=items['IO'],c=lambda *args:IOLib.exSgNet(\
                exPath=''))
    
    cmds.menuItem(label=u'导出所有的ShadingGroup网络(临时目录)', \
                p=items['IO'],c=lambda *args:IOLib.exSgNet(\
                exPath=os.environ['TEMP']+'\\SgNet.ma'))


def aniMenu():
    cmds.menuItem(label=u'烘焙相机', p=items['ani'],
                  c=lambda *args: usualLib.bakeCameraUI(0))
    cmds.menuItem(optionBox=1, p=items['ani'],
                  c=lambda *args: usualLib.bakeCameraUI(1))
    # 临时工具菜单
    TempToolDir=mayaPlugDir+r'\l_scripts\Ani\ThridTool'
    smallToolMenu(TempToolDir=TempToolDir,parentMenu=items['ani'],menuLabel=u'临时小工具')


def FixBugMenu(parent=None):

    cmds.menuItem(label=u'修复渲染设置UI界面', p=parent, c="maya.mel.eval('deleteUI unifiedRenderGlobalsWindow;buildNewSceneUI;')")
    cmds.menuItem(label=u'修复渲染层切换Bug', p=parent, c="maya.mel.eval('fixRenderLayerOutAdjustmentErrors')")
    cmds.menuItem(label=u'创建file时没有创建坐标节点或者file节点没有连接到材质球', p=parent, c=lambda *args :cmds.lockNode('defaultTextureList1',l=0,lu=0))
    cmds.menuItem(label=u'解决模型没法赋予材质及无法创建模型的问题', p=parent, c=usual.unlockInitialShadingGroup)

def usualMenu(parent=None):
    cmds.menuItem(divider=True, dividerLabel=u'项目规范', p=parent)
    cmds.menuItem(label=u'大纲视图命名', p=parent, c=hierarchy_modui.show_Main)
    
    cmds.menuItem(divider=True, dividerLabel=u'导入导出', p=parent)
    cmds.menuItem(label=u'导出obj序列以节点名', p=parent, c=usual.exObjNamedByNodeName)
    cmds.menuItem(label=u'根据输入输出命名',
                  p=parent, c=usRig.modifyNameRecursion)
    cmds.menuItem(divider=True, dividerLabel=u'文件清理', p=parent)
    cmds.menuItem(label=u'删除多余的shape节点',
                  p=parent, c=usual.cleanShapeNode)
    cmds.menuItem(label=u'清除未知节点',
                  p=parent, c=usual.delete_unknowNodes)
    cmds.menuItem(label=u'清除未知插件',
                  p=parent, c=usual.delete_unknowPlugins)
    cmds.menuItem(divider=True, dividerLabel=u'侧边栏插件', p=parent)
    cmds.menuItem(label=u'加载侧边栏插件', p=parent, c=loadMayaMatPlug)
    cmds.menuItem(label=u'对称传递位置', p=parent, c=usual.mirrorTransferPosition)

    
    cmds.menuItem(divider=True, dividerLabel=u'清理引用文件材质修改-方式1,只需一步,不能还原用方式2', p=parent)
    cmds.menuItem(label=u'清理材质修改(一定要优先用这种方法)', p=parent, 
                  c=lambda *args:usualLib.cleanMatFromRef_MethodA())
    
    cmds.menuItem(divider=True, dividerLabel=u'清理引用文件材质修改-方式2,需两步,不能还原用方式2', p=parent)
    cmds.menuItem(label=u'导出引用修改', p=parent, 
                  c=lambda *args:usualLib.cleanMatFromRef_MethodB(ExMofify=1,importMofifyWithoutSG=0))
    cmds.menuItem(label=u'导入引用修改(不包含材质)', p=parent, 
                  c=lambda *args:usualLib.cleanMatFromRef_MethodB(ExMofify=0,importMofifyWithoutSG=1))
    
    cmds.menuItem(divider=True, dividerLabel=u'模型替换', p=parent)
    cmds.menuItem(label=u'替换高低模', p=parent, 
                  c=lambda *args:usualLib.replaceHigModel.main())


def refreshMenu():
    # 删除子菜单
    menuName=items['LugwitRig']
    mentItems = cmds.menu(menuName, q=1, ia=1)
    print('mentItems----:', mentItems)
    if mentItems:
        for mentItem in mentItems:
            cmds.deleteUI(mentItem)



viewMenuWidth=35   
def viewMenu(*args):
    if cmds.control('viewLeftMenu', ex=1):
        cmds.warning (u'视图菜单存在,删除重建')
        cmds.deleteUI('viewLeftMenu')
    viewLeftMenu=cmds.columnLayout('viewLeftMenu',  w=viewMenuWidth,p="L_V",adj=1,rs=1)
    cmds.iconTextButton(image1='menuIconModify.png', overlayLabelBackColor=(.1, .1, .1, .9),
                        iol='cp', c=cmds.CenterPivot)
    cmds.iconTextButton(image1='Freeze.png', overlayLabelBackColor=(.1, .1, .1, .9),
                        iol='ft', c=cmds.FreezeTransformations,ann=u'冻结变换')

    cmds.iconTextButton(image1=iconDir+'unlock.png',dcc=lambda *args:unlockTransform(1),
                        overlayLabelBackColor=(.1, .1, .1, .9), h=20, w=20,
                        c=lambda *args:unlockTransform(0),ann=u'单击解锁,双击锁定')
    # cmds.popupMenu(b=3, mm=1)
    # cmds.menuItem( l=u"解锁移动缩放旋转", c=cmds.DeleteAllHistory)

    cmds.iconTextButton(c=cmds.DeleteHistory, overlayLabelBackColor=(
        .1, .1, .1, .9), image1='menuIconEdit.png', ann=u'清理',iol=u'清理')
    cmds.popupMenu(b=3, mm=1)
    cmds.menuItem( l=u"清理全部历史", c=cmds.DeleteAllHistory)
    cmds.menuItem( l=u"清理点数值并删除历史", c=usual.cleanVtxDateAndDelHis)
    
    cmds.menuItem(divider=True,  dividerLabel=u'层清理')
    cmds.menuItem(l=u"清除多余的shape节点", c=usual.cleanShapeNode)
    cmds.menuItem(l=u"清理选择物体的非变形节点", c=cmds.BakeNonDefHistory)
    
    cmds.menuItem(divider=True,  dividerLabel=u'层清理')
    cmds.menuItem( l=u"清除外来物体", c=usual.cleanImportObj,ann=u'清理多余的形态节点\
                                                        ,解锁法线,软化边,删除历史')
    cmds.menuItem(label=u'清除文件(未知节点和插件)',
                c=usual.cleanFile)
    
    cmds.menuItem(divider=True,  dividerLabel=u'层清理')
    cmds.menuItem(label=u'清理显示层',
                c='aa=cmds.ls(type="displayLayer");cmds.lockNode(aa,lock=0);cmds.delete(aa)')
    cmds.menuItem(label=u'清理动画层',
                c='aa=cmds.ls(type="animLayer");cmds.lockNode(aa,lock=0);cmds.delete(aa)')
    
    cmds.menuItem(divider=True,  dividerLabel=u'表情控制面板设置')
    cmds.menuItem(label=u'清理多重名称空间', c=usualLib.cleanNameSpace)
    cmds.menuItem(label=u'清理重命名', c=mps.usualSmallToolM.renameDuplicates)
    cmds.menuItem(label=u'清理所有通道', c=cmds.DeleteAllChannels)
    cmds.menuItem(label=u'形态节点和变换节点同名时重命名形态节点', c=usualLib.shapeNodeMatchTransfromNode)
    
    cmds.iconTextButton(image1='textureEditor.png', c=cmds.TextureViewWindow)
    cmds.popupMenu(b=3, mm=1)
    cmds.menuItem(rp="N",label=u'贴图管理', c=txLib.textureManager.main)
    cmds.menuItem(rp="S",label=u'清理没有实际赋予到物体的lambert1', c=attr_connect.disSg_NonAssignFace)
    cmds.iconTextButton(image1='blendShapeEditor.png', c=cmds.ShapeEditor)
    cmds.popupMenu()
    cmds.menuItem(l=u'切换BlensShapeSS开关',c=usRig.switchBS)
    cmds.menuItem(l=u'自动传递bs',c=RigLib.autoBs.main)
    
    advDir = LM.Lugwit_mayaPluginPath+r'/ThridPlug/AdvancedSkeleton5/scripts/AdvancedSkeleton5Files'
    adv5MelPath=LM.Lugwit_mayaPluginPath+r'/ThridPlug/AdvancedSkeleton5/scripts/AdvancedSkeleton5.mel'
    cmds.iconTextButton(image1=iconDir+'AS5.png',
                        c="import maya.mel as mel;mel.eval('source \"{}\";AdvancedSkeleton5;')".format(adv5MelPath), iol='adv')
    
    cmds.popupMenu()
    
    cmds.menuItem(l=u'Selector:biped', image=iconDir+'asBiped.png',
                c=lambda *args: mm.eval('source "{}/Selector/biped.mel"'.format(advDir)))
    cmds.menuItem(l=u'Selector:face', image=iconDir+'asFace.png',
                c=lambda *args: mm.eval('source "{}/Selector/face.mel"'.format(advDir)))
    cmds.menuItem(l=u'picker', image=iconDir+'picker.png',
                c=lambda *args: mm.eval('source "{}/picker/picker.mel"'.format(advDir)))
    
    cmds.button(label='uodo', c=undoTimes)
    cmds.button(l=u"默值",c=lambda *args:usual.restoreDefaultTransformAttribute(t=1),)
    cmds.popupMenu()
    cmds.menuItem(l=u'重置旋转', c=lambda *args:usual.restoreDefaultTransformAttribute(r=1))
    cmds.menuItem(l=u'重置缩放',c=lambda *args:usual.restoreDefaultTransformAttribute(s=1))
    cmds.menuItem(l=u'重置位移旋转',c=lambda *args:usual.restoreDefaultTransformAttribute(r=1,t=1))
    cmds.menuItem(l=u'重置位移缩放旋转', 
                  c=lambda *args:usual.restoreDefaultTransformAttribute(r=1,t=1,s=1))

    cmds.iconTextButton(c=cmds.DeleteHistory, overlayLabelBackColor=(
        .1, .1, .1, .9), image1=iconDir+'setting.png',h=30 )
    
    cmds.popupMenu(b=3, mm=1)
    cmds.menuItem(rp="NW", l=u"<  设置maya为英文",
                c="import os;os.popen('setx MAYA_UI_LANGUAGE en_US')")
    cmds.menuItem(rp="NE", l=u">  设置maya为中文",
                c="import os;os.popen('setx MAYA_UI_LANGUAGE zh_CH')")
    
    cmds.iconTextButton(image1=LM.Lugwit_mayaPluginPath+r'\icon\U3D.png',w=15, 
                        h=25,c=lambda *args:mps.maya2unfold3DFinish.export(uv=1),
                        dcc=lambda *args:mps.maya2unfold3DFinish.export(uv=0))
    cmds.popupMenu(b=3, mm=1)
    cmds.menuItem(rp="W",label=u'导出UV',c=lambda *args:mps.maya2unfold3DFinish.export(uv=1))
    cmds.menuItem(rp="E",label=u'导出',c=lambda *args:mps.maya2unfold3DFinish.export(uv=0))
    cmds.menuItem(rp="S",label=u'导入',c=mps.maya2unfold3DFinish.importObjDeleteHistory)
    cmds.menuItem(rp="SE",label=u'带ShadingGroup',checkBox=True)
    cmds.menuItem(rp="N",label=u'清理',checkBox=True)
    cmds.menuItem(rp="SW",label=u'打开Unfold3D',c=lambda *args:os.startfile(unfold3dPath))

    
    cmds.button(l=u'选择',w=15, h=25)
    cmds.popupMenu(b=3, mm=1)
    def selgroup(geo=0,deformation=0):
        sels=cmds.ls(sl=1);
        selNodeList=[]
        for sel in sels:
            if geo:
                if ":" in sel:
                    geoNode=sel.split(":")[0]+":Geometry"
                else:
                    geoNode="Geometry"
                if cmds.objExists(geoNode):
                    selNodeList.append(geoNode)
            if deformation:
                if ":" in sel:
                    deformationNode=sel.split(":")[0]+":DeformationSystem"
                else:
                    deformationNode="DeformationSystem"
                if cmds.objExists(deformationNode):
                    selNodeList.append(deformationNode)
        cmds.select(selNodeList)
        
    cmds.menuItem(rp="E",label=u'选择DeformationSystem组',c=lambda *args:selgroup(deformation=1))
    cmds.menuItem(rp="S",label=u'选择Geometry组和DeformationSystem组',c=lambda *args:selgroup(1,1))
    cmds.menuItem(rp="W",label=u'选择Geometry组',c=lambda *args:selgroup(geo=1))
    cmds.menuItem(rp="N",label=u'选择与解算物体同材质物体',c=getattr(l_FX,'selSameMatObjForZFS',))


    paipinFile=u"D:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/MayaMenu/menuDir/E_Animation/paipin.py"
    cmds.button(l=u'拍屏',w=15, h=25,c=lambda *args :execfile(paipinFile))
    cmds.button(l=u'截屏',w=15, h=25,c=usualLib.screenShot)
    cmds.button(l=u'Udim\n预览',w=15, h=35,c=M_ViewLib.genUdimPreview)
    
    cmds.button(l=u'路径',w=15, h=25,)
    cmds.popupMenu()
    def copyMayaFilePath(*args):
        cmd=u'echo {} | clip'.format(os.path.normpath(cmds.file(q=1,sn=1)))
        lprint (cmd)
        os.system(cmd)
    cmds.menuItem(label=u'复制Maya文件路径',c=L_GV.copyMayaFilePath )
    # system() takes exactly 1 argument (2 given) # 
    cmds.menuItem(label=u'打开Maya文件路径',c=L_GV.openMayaFileDirectory)
    cmds.menuItem(label=u'打开临时目录',c=lambda *args:os.startfile(os.environ['TEMP']))
    
    cmds.iconTextButton(image1=LugwitPath+r'\icons\p4v.jpg',w=25,h=30)
    cmds.popupMenu(b=3, mm=1)
    cmds.menuItem(rp="N",label=u'添加/签出',c=lambda *args: P4Lib.checkOut(cmds.file(q=1,sn=1)))
    cmds.menuItem(rp="S",label=u'提交',)#c=lambda *args: P4Lib.checkOut

    cmds.button(l=u'解算',w=15, h=25,)
    cmds.popupMenu()
    del_unused_node_Ckb=cmds.menuItem(label=u'将模型材质名称添加到着色组前先删除无用的材质节点', checkBox=False)
    del_unused_node_Ckb_dynValue=lambda:cmds.menuItem(del_unused_node_Ckb,q=1,checkBox=True)
    cmds.menuItem(rp="N",label=u'将模型材质名称添加到着色组',\
                  command=lambda *args: l_FX.nameSgFromMat([], del_unused_node_Ckb_dynValue()))
    cmds.menuItem(rp="N",label=u'还原所有着色组',c=l_FX.retoremSgAndMat,)
    cmds.menuItem(label=u'给导入的Abc创建材质',c=l_FX.createMatForAbc,)
    cmds.menuItem(label=u'转为分面材质',c=lambda checked=False: usual.cvtFaceSetSG(),)
    cmds.menuItem(label=u'选择srfNUL组中可见的多边形',c=usual.selsrfNUL_VisPloy,)
    cmds.menuItem(label=u'导出Abc',c=IOLib.call_batch_ex_abc.main,image="alembic.png")
    def shoulong(*args):
        cmds.workspaceControl("L_V", edit = 1 ,collapse=True)
    cmds.button(l=u'收拢',w=15, h=25,c=shoulong)
    
    

    
    

@LM.try_exp
def WS(*args):
    cmds.workspaceControl("L_V", dtc=('MainPane','left'),
                        retain=1,iw=viewMenuWidth,
                        wp='free',fl=0,l='<<<',mw=35,
        uiScript=lambda *args:getattr(sys.modules['UV_UI'],'switch_realTime')(),w=viewMenuWidth)

    
def viewWS(*args):
    
    if cmds.control('L_V', ex=1):
        cmds.deleteUI('L_V')
        # cmds.workspaceControl("L_V", iw=width,wp='free',e=1,l='')  
        cmds.warning (u'视图菜单存在')
        WS()
        print (1111)
    else:
        WS()

    viewMenu()

    modelPaneMenu()

       
def modelPaneMenu(*args):
    def toggleVis(layoutA='',layoutB='',visBtn='',*args):
        if cmds.control(layoutB, q=1, ex=1):
            vis = cmds.control(layoutB, q=1, vis=1)
            if vis:
                print (u'可见')
                cmds.layout(layoutA, e=1, w=15)
                cmds.control(layoutB,e=1,vis=0)
                cmds.button(visBtn, e=1, l='>>', h=21,al='left')
            else:
                print (u'不可见')
                cmds.layout(layoutA, e=1, w=35)
                cmds.control(layoutB,e=1,vis=1)
                cmds.button(visBtn, e=1, l='<<<',w=35,h=15)
    allPane=cmds.getPanel(type='modelPanel')
    for pane in allPane:
        if cmds.layout('LugwitViewMenuA_'+pane,q=1,ex=1):
            cmds.deleteUI('LugwitViewMenuA_'+pane)
        try:
            cmds.columnLayout('LugwitViewMenuA_'+pane,  w=viewMenuWidth,p=pane+'|'+pane)
            cmds.iconTextButton(image1='Camera.png', c=selCamera, h=17,w=35)
            
            def updateCameraMenu(cameraPopupMenu,*args):
                # 清除现有菜单项
                
                menuItems = cmds.popupMenu(cameraPopupMenu, q=True, itemArray=True)
                if menuItems:
                    for item in menuItems:
                        cmds.deleteUI(item)
                print("menuItems",menuItems,"cameraPopupMenu",cameraPopupMenu)
                # 动态添加场景中的所有摄像机到右键菜单
                allCameras = cmds.ls(type='camera')
                for cam in allCameras:
                    # 获取摄像机的变换节点
                    camTransform = cmds.listRelatives(cam, parent=True)
                    print("camTransform",camTransform)
                    if camTransform:
                        camName = camTransform[0]
                        cmds.menuItem(label=camName, c=partial(cmds.select, camName), parent=cameraPopupMenu)
                
                # 添加分割线和创建摄像机菜单项
                cmds.menuItem(divider=True, parent=cameraPopupMenu)
                cmds.menuItem(label=u'创建摄像机', c=lambda *args: cmds.camera(), parent=cameraPopupMenu)
            
            cameraPopupMenu = cmds.popupMenu(b=3, mm=1, )
            cmds.popupMenu(cameraPopupMenu,e=1, postMenuCommand=partial(updateCameraMenu, cameraPopupMenu))
            cmds.button('visBn_'+pane, c=partial(toggleVis,'LugwitViewMenuA_'+pane, 'LugwitViewMenuB_'+pane,'visBn_'+pane),p='LugwitViewMenuA_'+pane,h=15, l='<<<', bgc=[0.12, 0.15, 0.2])
            cmds.rowColumnLayout('LugwitViewMenuB_'+pane, w=35)
            cmds.button(label=u'独多', c=usual.View().onlyDisPolygon,ann=u'仅显示多边形')
            cmds.popupMenu()
            cmds.menuItem(label=u'骨骼显示切换',c=lambda *args:usual.View().disByType('joints'))
            cmds.menuItem(label=u'locator显示切换',c=lambda *args:usual.View().disByType('locators'))
            cmds.menuItem(label=u'显示Nurbs,Polygons,Locators',c=lambda *args:usual.View().disByType(['locators','polymeshes','nurbsCurves']))
            cmds.menuItem(label=u'显示全部',c=usual.View().disAll)
            cmds.menuItem(label=u'设置所有骨骼的drawStyle为bone',c=dispalyAllBone)
            cmds.button(label=u'高亮', c=usual.View().higShowMesh)
        except:
            traceback.print_exc()
        
def dispalyAllBone(*args):
    allJnt=cmds.ls(type='joint')
    for jnt in allJnt:
        cmds.setAttr(jnt+'.drawStyle',0)


def ToolBoxMenu():
    ToolBox = mel.eval('global string $gToolBox;$temp = $gToolBox;')
    print('ToolBox:', ToolBox)
    if cmds.control('LugwitToolBox', q=1, ex=1):
        cmds.deleteUI('LugwitToolBox')
    cmds.rowColumnLayout('LugwitToolBox', p=ToolBox,
                         adj=1, bgc=[0.2, 0.2, 0.2], w=40)
    cmds.button(label=u'刷新', c=refreshViewMenu, bgc=[0, .8, 0],ann=u'重载入口插件LugwitMayaPlugStart,刷新视图菜单')
    cmds.popupMenu()

    cmds.menuItem(l=u'刷新垂直工具架',c=viewMenu)
    cmds.menuItem(l=u'刷新视图菜单', c=modelPaneMenu)
    
    cmds.button(label=u'更新\n插件',
                ann='从P4获取最新代码' , 
                bgc=[0, .8, 0],
                c=lambda *args:updatePlug(isUpdatePlug=True))
    cmds.popupMenu()
    cmds.menuItem(l=u'重载', c=lambda *args:updatePlug(isUpdatePlug=False))
    
    cmds.iconTextButton(image1=LM.Lugwit_mayaPluginPath+r'\materialPlug\prefs\icon\NiuMatIco.png',
                        w=14, h=38,c=loadMayaMatPlug,
                        ann=u'加载侧边栏插件')
    
def updatePlug(isUpdatePlug=True):
    print (u'更新{}并重载插件'.format(isUpdatePlug))
    import threading,time
    st=time.time()
    #environDict=dict(os.environ)
    with codecs.open (os.getenv('oriEnvVarFile'),'r',encoding='utf8') as f:
        env=json.load(f)
        tempDict = {}
        for key,val in env.items():
            try:
                tempDict[str(key)]  = str(val)
            except:
                traceback.print_exc()
    env = tempDict

    # env['USERNAME']=getpass.getuser()
    # env['USERPROFILE']=os.environ['USERPROFILE']
    updatePlugFromMaya_File='{}/updateLugwitPlug.txt'.format(os.environ["Temp"])
    env['updatePlugFromMaya_File']=updatePlugFromMaya_File

    def updatePlugA(*args):
        updatePlugFromMaya_File='{}/updateLugwitPlug.txt'.format(os.environ["Temp"])
        if os.path.exists(updatePlugFromMaya_File):
            os.remove(updatePlugFromMaya_File)
            if not os.path.exists(updatePlugFromMaya_File):
                print (u'移除更新记录文件{}成功'.format(updatePlugFromMaya_File))

        syncPlugFile=Lugwit_publicPath+u'/Python/PyFile/syncPlugLib/syncPlug_nojieshiqi.bat'
        #os.startfile(syncPlugFile)
        subprocess.Popen('start '+syncPlugFile,shell=True,env=env)
        
    def Reload(*args):
        print (u'重载插件')
        updatePlugFromMaya_File='{}/updateLugwitPlug.txt'.format(os.environ["Temp"])
        while 1:
            time.sleep(0.5)
            if os.path.exists(updatePlugFromMaya_File) or isUpdatePlug==False: 
                reloadPlugPath="import sys\nsys.path.append(r'{}\Lugwit_MayaStartScripts')\n".format(LM.Lugwit_mayaPluginPath)
                reloadPlugStr="import reloadPlug\nreload(reloadPlug);\nreloadPlug.reloadPlugFunc()"
                print (reloadPlugPath+reloadPlugStr)
                executeInMainThreadWithResult(reloadPlugPath+reloadPlugStr)
                print (u'更新插件成功')
                break
            if time.time()-st>60:
                print (u'更新超时')
                break
    
    
    Pro_A=threading.Thread(target=updatePlugA)
    Pro_B=threading.Thread(target=Reload)
    Pro_B.start()
    if isUpdatePlug:
        print (u'更新插件')
        Pro_A.start()
    loadMayaMatPlug()

def refreshViewMenu(*args):
    reload (sys.modules['LugwitMayaPlugStart'])
    viewWS()
    
    
# def CodeEncryptionMenu(*args):
#     cmds.menuItem(l=u'代码加密', c=CodeEncryptionUI,p=items[u'CodeEncryption'])

def submitFileToFarmUI(*args):
    sys.path.append(r'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\Lib')
    from Lugwit_Module.l_src import l_subprocess
    MayaCodeEncryptionUIFile=LugwitToolDir+r'\Lib\L_DeadLine\MayaDeadline\UI.py'
    l_subprocess.startPyFile(
        MayaCodeEncryptionUIFile,
        sys_argv='',
        usePythonw=True)

    
def mayaFileInTempDir(*args):
    tempDir = os.environ['temp']
    files = [f for f in glob.glob(tempDir + "/*.ma")] + \
        [f for f in glob.glob(tempDir + "/*.mb")]
    files = sorted(files, key=lambda x: os.stat(x).st_mtime)
    files = reversed(files)
    return files


def combineMap():
    fileNodes = cmds.ls(type='file')
    # fileNodes=['ONEMT_set_zhanchang_MOD:pasted__MapFBXASC032FBXASC035321499311']
    for fileNode in fileNodes:
        fileNodeOut = cmds.listConnections(fileNode+'.outColor')
        if fileNodeOut:
            if len(fileNodeOut) > 1:
                try:
                    mats = fileNodeOut
                    sgs = [cmds.listConnections(mat, type='shadingEngine')[
                        0] for mat in mats]
                    cmds.select(sgs)
                    cmds.sets(cmds.ls(sl=True), e=True, forceElement=sgs[0])
                except:
                    traceback.print_exc()
    sgs = cmds.ls(type='shadingEngine')
    mats = [cmds.listConnections(x+'.surfaceShader')[0] for x in sgs]
    for mat in mats:
        try:
            FileNode = cmds.listConnections(mat+'.color')
        except:
            try:
                FileNode = cmds.listConnections(mat+'.baseColor')
            except:
                continue
        print('FileNode', FileNode)
        if FileNode:
            FileNode = FileNode[0]
            if not cmds.attributeQuery('ftn', node=FileNode, ex=1):
                continue
            cMap = cmds.getAttr(FileNode+'.ftn')
            convertDir = os.path.dirname(cMap)+'/Convert'
            if not os.path.exists(convertDir):
                os.makedirs(convertDir)
            newcMap = convertDir+'/T_'+mat+'_BC.'+cMap.split('.')[1]
            # newPath = convertDir+'/'+os.path.basename(cMap)
            print('mat,cMap,\n newPath', mat, cMap, newcMap)
            copyfile(cMap, newcMap)
            # cmds.setAttr(FileNode+'.ftn', newcMap, type='string')
            if not os.path.exists(newcMap):
                # os.rename(newPath, newcMap)
                try:
                    cmds.rename(FileNode, mat+'_BaseColor')
                    cmds.select(mat)
                except:
                    traceback.print_exc()

            # 处理其他贴图
            checkMapDict = {'Roughness': 'Roughness',
                            'Normal': 'N', 'Metallic': 'Metallic'}
            keyList = checkMapDict.keys()
            for texture in keyList:
                # checkMap = cMap.replace('BaseColor', texture)
                pattern = cMap.split('_')[-1]
                checkMap = re.sub(pattern, texture+'.' +
                                  cMap.split('.')[-1], cMap, flags=re.IGNORECASE)
                print('checkmap,', checkMap)
                newPath = newcMap.replace('BC', checkMapDict[texture])
                if os.path.exists(checkMap):
                    copyfile(checkMap, newPath)


def togSelH(*args):
    now = cmds.modelEditor('modelPanel4', q=True, selectionHiliteDisplay=1)
    now = cmds.modelEditor('modelPanel4', e=True, selectionHiliteDisplay=1-now)

def CodeEncryptionUI(*args):
    #environDict=dict(os.environ)
    with open (LM.Lugwit_mayaPluginPath+r'\l_scripts\Data\vscodePyhonEnv.txt','r') as f:
        env=f.read()
    env=eval(env)
    MayaCodeEncryptionUIFile=LM.Lugwit_mayaPluginPath+r'\l_scripts\CodeEncryption\MayaCodeEncryptionUI.py'
    print (Lugwit_PluginPath+ r'\Python\Python37\python.exe {}'.format(MayaCodeEncryptionUIFile))
    subprocess.Popen(Lugwit_PluginPath+ r'\Python\Python37\python.exe -i {}'.format(MayaCodeEncryptionUIFile)
                    ,cwd=LM.Lugwit_mayaPluginPath+r'\l_scripts\CodeEncryption',shell=True,env=env)

def undoTimes(*args):
    result = cmds.promptDialog(
        title='redo times',
        message='times:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel',
        text=1000)
    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)
        for i in range(int(text)):
            cmds.undo()

@LM.try_exp
def loadMayaMatPlug(*args):
    cmds.select(cl=1)
    matPlugDir = LM.Lugwit_mayaPluginPath+"/materialPlug"
    sys.path.append(matPlugDir+'/scripts')
    if sys.version_info[0]==2:
        sys.path.append(matPlugDir+'/python_library')
    try:
        reload(UV_UI)
    except:
        print ('reald error,import UV_UI')
        import UV_UI
    UV_UI.UI()


def exSelWin(exchangeDir):
    cmds.window(title=u'导出文件到交换文件夹')
    cmds.columnLayout(adj=1)
    if cmds.ls(sl=1):
        text = cmds.ls(sl=1)[0]
    else:
        text = 'exchangeFile'
    text = text.replace(':', '_')
    text = text.replace('|', '_')
    if text.startswith('_'):
        text=text[1:]
    cmds.textFieldGrp('exFileName', label=u'文件名称', text=text)

    cmds.radioButtonGrp('TempFileTypeList', label=u'文件类型', labelArray3=[
                        'ma', 'obj', 'fbx', ], numberOfRadioButtons=3, sl=1)
    cmds.textFieldGrp('exFileRemark', label=u'备注', text='')
    cmds.checkBoxGrp('Lugwit_tempFile', numberOfCheckBoxes=1, label=u'临时存储', v1=1,)
    cmds.button(l=u'导出', c=lambda *args: exFile(exchangeDir))
    cmds.showWindow()


def exFile(exchangeDir, *args):
    typeDict = {'ma': "mayaAscii", 'obj': 'OBJexport', 'fbx': 'FBX export'}
    tempFileCtl = cmds.checkBoxGrp('Lugwit_tempFile', q=1, l=1)
    typeList = cmds.radioButtonGrp('TempFileTypeList', q=1, la3=1)
    typ = typeList[cmds.radioButtonGrp('TempFileTypeList', q=1, sl=1)-1]
    exFileName = cmds.textFieldGrp('exFileName', q=1, text=1)
    exFile = exchangeDir+'/'+exFileName+'.'+typ
    print(u'导出路径为{}'.format(exFile))
    cmds.file(exFile, es=1, typ=typeDict[typ], f=1,
              options="groups=1;ptgroups=0;materials=0;smoothing=0;normals=1")
    remarkFile = exchangeDir+'/remarkFile/'+exFileName+'.txt'
    with codecs.open(remarkFile, 'w', encoding='utf-8') as open_remarkFile:
        open_remarkFile.write(u'{}:{}'.format(
            userName, cmds.textFieldGrp('exFileRemark', q=1, text=1)))
    #pyperclip.copy(exFile)


def imFile(exchangeDir, method='import', *args):
    def removeSelf(absPath,rowLayoutUI,*args):
        os.remove(absPath)
        cmds.deleteUI(rowLayoutUI)
    def modifyRemark(ui,curTime,remarkFile,remark,*args):
        result = cmds.promptDialog(
		title=u'请输入备注信息',
		message=u'备注信息:',
		button=['OK', 'Cancel'],
		defaultButton='OK',
		cancelButton='Cancel',
		dismissString='Cancel',text=remark)
        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)
            cmds.text(ui,e=1,l=curTime+userName+':'+text)
            print  ('remarkFile:',remarkFile)
            with codecs.open(remarkFile, 'w', encoding='utf-8') as open_remarkFile:
                open_remarkFile.write(u'{}:{}'.format(userName, text))
            
    cmds.window(title=u'打开/导入/引用交换文件'.format(method))
    importUI=cmds.rowColumnLayout(adj=1)
    width=(200,350,50,50,50,50)
    cmds.rowLayout( numberOfColumns=6,columnWidth6=width,adj=2,columnAlign=(2, 'left'))
    cmds.text(l=u'文件名');cmds.text(l=u'修改日期及备注');
    cmds.text(l=u'打开');cmds.text(l=u'导入');cmds.text(l=u'引用');cmds.text(l=u'删除')
    cmds.separator(p=importUI)
    files = os.listdir(exchangeDir)
    files = sorted(files, key=lambda x: os.stat(exchangeDir+'/'+x).st_mtime)
    files = reversed(files)
    for file in files:
        if file.endswith('.obj') or file.endswith('.ma') or file.endswith('.fbx'):
            rowLayoutUI=cmds.rowLayout( numberOfColumns=6,p=importUI,columnWidth6=width,adj=2,columnAlign=(2, 'left'))
            absPath = exchangeDir+'/'+file
            times = os.stat(absPath).st_mtime
            curTime = time.strftime(
                "%Y-%m-%d %H:%M:%S   ", time.localtime(times))
            if method == 'import':
                method = 'i'
            exFileName = file.split('.')[0]
            remarkFile = exchangeDir+'/remarkFile/'+exFileName+'.txt'
            read_remarkFile = ''
            if os.path.exists(remarkFile):
                with codecs.open(remarkFile, 'r', encoding='utf-8') as open_remarkFile:
                    read_remarkFile = open_remarkFile.read()
            cmds.text(l=file )
            textUI=cmds.text(l=curTime+read_remarkFile);
            cmds.popupMenu()
            remark=read_remarkFile.replace(userName+':','')
            cmds.menuItem(l=u'修改备注',c=functools.partial(modifyRemark,textUI,curTime,remarkFile,remark))
            cmds.button(l=u'打开', c="cmds.file('{}',o=1,f=1)".format(absPath))
            cmds.button(l=u'导入', c="cmds.file('{}',i=1,f=1)".format(absPath))
            cmds.button(l=u'引用', c="cmds.file('{}',r=1,f=1)".format(absPath))
            cmds.button(l=u'删除', c=functools.partial(removeSelf,absPath,rowLayoutUI))
            sep=cmds.separator(p=importUI)
            # cmds.button(
            #     l=file, c="cmds.file('{}',{}=1,f=1)".format(absPath, method))
    cmds.showWindow()
   


def exchangeFolder(func='copyFileToDir'):
    # func='copyFileToDir','exSel','imSel','openExFile'
    exchangeDir = Lugwit_publicPath+r'/ExchangeFolder'
    exchangeFile = Lugwit_publicPath+r'/ExchangeFolder/exchangeFile.ma'
    MayaFile = cmds.file(q=1, sn=1)
    # newPath = exchangeFolder+'/'+os.path.basename(MayaFile)
    # print ('newPath:',newPath)
    if func == 'copyFileToDir':
        shutil.copy(MayaFile, exchangeDir)
    elif func == 'exSel':
        exSelWin(exchangeDir)
    elif func == 'imSel':
        imFile(exchangeDir, method='import')
    elif func == 'openExFile':
        imFile(exchangeDir, method='open')


def unlockTransform(lockState=0):
    attrList = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz',
                'sx', 'sy', 'sz', 'translate', 'scale', 'rotate']
    sel = cmds.ls(sl=1)
    for s in sel:
        for attr in attrList:
            cmds.setAttr(s+'.'+attr, lock=lockState)



def selCamera(*args):
    panel = cmds.getPanel(withFocus=True)
    print (u'当前面板是{}'.format(panel))
    cam = cmds.modelPanel(panel, query=True, camera=True)
    lprint (cam)
    camShapeNode=cmds.listRelatives(cam,s=1)[0]
    cmds.select(cam)
    print (cmds.ls(sl=1))
