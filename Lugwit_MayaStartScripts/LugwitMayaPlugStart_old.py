# coding:utf-8
import time
st=time.time()
from Lugwit_Module import *
lprint=LPrint
import inspect
__file__=inspect.getfile(inspect.currentframe())
print ('run module{}'.format(__file__))
print (u'系统变量-->{}'.format(sys.argv),)
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
    
#添加模块所在路径
fileDir = os.path.dirname(__file__)
sys.path.insert(0,fileDir)
from path import *

runTime.st=time.time()

#添加自己写的模块
sys.path.append(LugwitPath+r'\Python\PythonLib\Perforce')
import P4Lib



#导入Maya模块
# import maya.standalone
# maya.standalone.initialize(name='python')
import maya.mel as mm
mel = mm
mm.eval('renderThumbnailUpdate false;')
import maya.cmds as cmds
from functools import partial

#获取系统参数
userName = getpass.getuser()


unfold3dPath=r'Z:\Program Files\RizomUV 2022.0\rizomuv.exe'
sys.path.append(LugwitPath+r'\Python\PythonLib\generalLib')

#插件相关路径
iconDir = LugwitPath+'/mayaPlug/icon/'
# 模块目录
moduleFile = __file__
moduleFile = moduleFile.replace('\\', '/')
moduleDir = os.path.dirname(moduleFile)
#Maya插件目录
mayaPlugDir = re.search('.+/mayaPlug', moduleFile).group()
scriptsDir = mayaPlugDir+'/l_scripts'
print (u'导入模块花费时间{}'.format(time.time()-runTime.st))
#获取我的文档目录
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                      r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
docuDir = winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/')
print(u'我的文档目录是:{}'.format(docuDir))
print (u'获取我的文档目录花费时间{}'.format(time.time()-runTime.st))

#添加python库目录
sys.path.append(scriptsDir)  # 当前目录路径
sys.path.insert(0,LugwitPath+r'\mayaPlug')

#导入自定义模块

import L_pyGelLib as pgl

#加载第三方模块
sys.path.append(LugwitPath+r'\mayaPlug\l_scripts\ThridLib')
import pyperclip



print ('{} run to {} line,take time {}'.format(__file__[-40:],sys._getframe().f_lineno,time.time()-runTime.st))
#导入Maya材质插件模块
import materialPlug.scripts as mps
print ('{} run to {} line,take time {}'.format(__file__[-40:],sys._getframe().f_lineno,time.time()-runTime.st))

#导入Lugwit插件模块
import l_scripts
print ('{} run to {} line,take time {}'.format(__file__[-40:],sys._getframe().f_lineno,time.time()-runTime.st))
#导入Lugwit插件模块大库
IOLib=l_scripts.IOLib
print ('{} run to {} line,take time {}'.format(__file__[-40:],sys._getframe().f_lineno,time.time()-runTime.st))
RigLib=l_scripts.Rig
print ('{} run to {} line,take time {}'.format(__file__[-40:],sys._getframe().f_lineno,time.time()-runTime.st))
usualLib=l_scripts.usualLib
print ('{} run to {} line,take time {}'.format(__file__[-40:],sys._getframe().f_lineno,time.time()-runTime.st))
usual=usualLib.usual
print ('{} run to {} line,take time {}'.format(__file__[-40:],sys._getframe().f_lineno,time.time()-runTime.st))



txLib=l_scripts.Texture
print ('{} run to {} line,take time {}'.format(__file__[-40:],sys._getframe().f_lineno,time.time()-runTime.st))
mj=RigLib.MatchJoint
print ('{} run to {} line,take time {}'.format(__file__[-40:],sys._getframe().f_lineno,time.time()-runTime.st))
usRig=RigLib.usualRig

print (u'全局变量花费时间{},导入所有模块'.format(time.time()-st))

def uninstall(*args):
    if cmds.menu(u"芭阁动漫", ex=1):
        cmds.deleteUI(u"芭阁动漫")
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
    for moduleName,module in sys.modules.items():
        if module:
            try:
                if 'Lugwit_plug' in module.__file__:
                    if 'reload' not  in module.__file__:
                        print (u'卸载模块{}'.format(moduleName))
                        del sys.modules[moduleName]
            except:
                pass


def install(*args):
    statusLine = mel.eval('global string $gStatusLine;$temp = $gStatusLine;')
    cmds.rowLayout("HDR_rowLayout", p=statusLine,numberOfColumns=5,)
    cmds.checkBox('allOrSel', value=1, 
                  l=u'全部或者选择', ann=u'勾选应用于全部物体,不勾选应用于选择物体')
    cmds.text(u'HDR_Maya文件',bgc=[0.7,0.8,0])
    cmds.iconTextButton(label=u'白天', image1=r'S:\DataTrans\FQQ\ExchangeFolder\icon\day.jpg',
                        h=30,w=50,font='boldLabelFont',ann=u'白天HDR',
    c=lambda *args: cmds.file('S:/DataTrans/FQQ/ExchangeFolder/Light_LookDev.ma',
                              r=1,namespace='DayHDR'))
    cmds.popupMenu(b=3, mm=1)
    cmds.menuItem(rp="S",label=u'卸载',c=lambda *args:cmds.file('S:/DataTrans/FQQ/ExchangeFolder/Light_LookDev.ma',rr=1))
    
    cmds.iconTextButton(label=u'夜晚', image1=r'S:\DataTrans\FQQ\ExchangeFolder\icon\night_HDR.jpg',
                        h=30,w=50,font='boldLabelFont',ann=u'夜晚HDR',)
    
    cmds.menu(u"芭阁动漫", p=mm.eval(
        '$gMainWindow=$gMainWindow'), to=1, l=u"芭阁动漫")
    global items
    items = {group: cmds.menuItem(group, p=u"芭阁动漫", to=1, sm=1, l=label,)
             for group, label in zip(['usual', "usualDir", "Tex", "ani", 'IO', 'LugwitRig','CodeEncryption'],
                                     [u'通用', u"常用目录", u"材质", u"动画", 'IO', u'绑定',u'代码加密'])}
    print(items, '--------------------------------')
    # 通用工具
    usualMenu(parent=items['usual'])
    # 输入输出菜单
    IOMenu()
    # 常用目录菜单
    usualDirMenu()
    # 材质菜单
    texMenu()
    # 动画菜单
    aniMenu()
    # 工具盒
    ToolBoxMenu()
    # 绑定菜单
    rigMenu()
    
    #代码加密菜单
    CodeEncryptionMenu()

    # 视图菜单
    viewWS() 
    modelPaneMenu()
    # 交换文件菜单
    cmds.menuItem(divider=True, p=u"芭阁动漫", dividerLabel=u'文件交换')
    exchangeFileMenu()
    # 重载插件菜单
    cmds.menuItem(divider=True, p=u"芭阁动漫", dividerLabel=u'插件相关')
    cmds.menuItem(label=u'重载插件', p=u"芭阁动漫",
                  c="import reloadPlug;reload(reloadPlug);reloadPlug.UI()")
    path=os.path.expandvars("$HOME")+r'\maya\{}\prefs\pluginPrefs.mel'.format(cmds.about(version=1))
    cmds.menuItem(label=u'解锁启动插件列表', p=u"芭阁动漫",
                  c=lambda *args:lockLugwitPlug(0))
    cmds.menuItem(label=u'锁定启动插件列表', p=u"芭阁动漫",
                  c=lambda *args:lockLugwitPlug(1))
    cmds.menuItem(label=u'打开VsCodeD端口', p=u"芭阁动漫",
                c=lambda *args:cmds.commandPort(name="localhost:7001", sourceType= "python",echoOutput=1))
    print (u'加载插件耗费时间{}{}'.format(time.time()-st,__file__))
    
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
        cmd_onlyRead='attrib +r {}'.format(path)
        cmd_read='attrib -r {}'.format(path)
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
            fileAttr=subprocess.Popen('attrib {}'.format(path),stdout=subprocess.PIPE).stdout.read()
            if 'R' not in fileAttr:
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


def texMenu():
    cmds.menuItem(label=u'选择没有材质球的物体', p=items['Tex'], c=mps.uvSetTool.nonSG)
    cmds.menuItem(label=u'生成规范命名贴图', p=items['Tex'], c=combineMap)
    cmds.menuItem(label=u'贴图管理', p=items['Tex'], c=txLib.textureManager.main)
    cmds.menuItem(label=u'转换为分面材质球', p=items['Tex'], c=usual.cvtFaceSetSG)



def IOMenu():
    cmds.menuItem(label=u'导出ABC', p=items['IO'],)
    sys.path.append(r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\mayaPlug\l_scripts\usualLib')
    
    cmds.menuItem(label=u'工程打包', p=items['IO'], c=IOLib.pack.main)
    cmds.menuItem(label=u'导出材质Json文件', p=items['IO'], 
                  c=lambda *args:IOLib.export_mat_json(Key='Obj'))
    cmds.menuItem(label=u'导出所有的ShadingGroup网络', \
                p=items['IO'],c=lambda *args:IOLib.exSgNet(\
                exPath=''))


def aniMenu():
    cmds.menuItem(label=u'烘焙相机', p=items['ani'],
                  c=lambda *args: usualLib.bakeCameraUI(0))
    cmds.menuItem(optionBox=1, p=items['ani'],
                  c=lambda *args: usualLib.bakeCameraUI(1))


def exchangeFileMenu():
    cmds.menuItem(label=u'复制文件到交换目录', p=u"芭阁动漫",
                  c=lambda *args: exchangeFolder('copyFileToDir'))
    cmds.menuItem(label=u'导出选择到交换目录', p=u"芭阁动漫",
                  c=lambda *args: exchangeFolder('exSel'))
    cmds.menuItem(label=u'打开/导入/引用交换文件', p=u"芭阁动漫",
                  c=lambda *args: exchangeFolder('imSel'))


def usualMenu(parent=None):

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
    cmds.menuItem(label=u'解决模型没法赋予材质bug', p=parent, c=usual.unlockInitialShadingGroup)
    
    
    cmds.menuItem(divider=True, dividerLabel=u'清理引用文件材质修改-方式1,只需一步,不能还原用方式2', p=parent)
    cmds.menuItem(label=u'清理材质修改(一定要优先用这种方法)', p=parent, 
                  c=lambda *args:usualLib.cleanMatFromRef_MethodA())
    
    cmds.menuItem(divider=True, dividerLabel=u'清理引用文件材质修改-方式2,需两步,不能还原用方式2', p=parent)
    cmds.menuItem(label=u'导出引用修改', p=parent, 
                  c=lambda *args:usualLib.cleanMatFromRef_MethodB(ExMofify=1,importMofifyWithoutSG=0))
    cmds.menuItem(label=u'导入引用修改(不包含材质)', p=parent, 
                  c=lambda *args:usualLib.cleanMatFromRef_MethodB(ExMofify=0,importMofifyWithoutSG=1))


def refreshMenu():
    # 删除子菜单
    menuName=items['LugwitRig']
    mentItems = cmds.menu(menuName, q=1, ia=1)
    print('mentItems----:', mentItems)
    if mentItems:
        for mentItem in mentItems:
            cmds.deleteUI(mentItem)


def rigMenu(needReload=0):
    refreshMenu()
    if needReload:
        reload(usRig)
        reload(mj)
        
    #动补数据菜单开始    
    DongMuMenu = cmds.menuItem(label=u'动捕数据处理',
                                  p=items['LugwitRig'], subMenu=1, to=1)
    cmds.menuItem(label=u'匹配手指动捕动画', c=RigLib.DP.matchHandAni, p=DongMuMenu,
                  ann=u'先选择Tpose组,在选择动捕数据组')
    RigLibPath='import sys;sys.path.append(r"Z:\plug_in\Lugwit_plug\mayaPlug\l_scripts\Rig");'
    cmds.menuItem(label=u'导入并烘焙动捕数据', c=RigLibPath+'import HIK;reload(HIK),HIK.tranDoBuDataCall()',
                    p=DongMuMenu,)
    #动补数据菜单结束
    
    #小男孩菜单结束
    XNHMenu = cmds.menuItem(label=u'小男孩',
                            p=items['LugwitRig'], subMenu=1, to=1)
    cmds.menuItem(label=u'小男孩方案创建控制器节点', c=usRig.createCtlNode, p=XNHMenu)
    cmds.menuItem(label=u'小男孩方案命名规则', c=usRig.XNH_NameRule, p=XNHMenu)
    cmds.menuItem(label=u'小男孩方案创建包裹', c=usRig.autodeformModel_XNH, p=XNHMenu)
    bsMenu = cmds.menuItem(label=u'小男孩方案创建BS', c=usRig.createBS_XHN)
    cmds.menuItem(label=u'小男孩方案创建驱动关键帧动画',
                  c=lambda *args: usRig.setDrvKeyFra(), p=XNHMenu)
    cmds.menuItem(label=u'小男孩方案创建骨骼驱动',
                  c=lambda *args: usRig.setDrvKeyFra, p=XNHMenu)
    #小男孩菜单结束
    
    #metahuman菜单开始
    metahumanMenu = cmds.menuItem( label=u'metahuman',
                                  p=items['LugwitRig'], subMenu=1, to=1)

    # 绑定到新模型步骤
    cmds.menuItem(divider=True, p=metahumanMenu, dividerLabel=u'表情控制面板设置')

    cmds.menuItem(label=u'匹配骨骼到新模型', c=mj.matchJntPos, p=metahumanMenu,
                  ann=u'选择原始模型,再选择目标模型,再选择骨骼')
    cmds.menuItem(label=u'匹配骨骼到新模型(不包含子级)', c=lambda *args:mj.matchJntPos(recursionDepth=0), p=metahumanMenu,ann=u'选择原始模型,再选择目标模型,再选择骨骼')
    cmds.menuItem(label=u'绑定头部模型', c=mj.bindHead, p=metahumanMenu,
                  ann=u'根骨骼名称<DHIhead:spine_04>,metahuman原始头部模型名称<head_lod0_mesh>,新的头部模型名称<.head_mesh>')

    cmds.menuItem(divider=True, dividerLabel=u'locator控制器设置', p=metahumanMenu)
    cmds.menuItem(label=u'locator匹配骨骼颜色',
                  c=usRig.matchBSName, p=metahumanMenu)
    cmds.menuItem(label=u'更新locator位置',
                  c=mj.updateLocatorPos, p=metahumanMenu)
    cmds.menuItem(label=u'更新控制器位置到骨骼位置', c=mj.updateLocatorPos, p=metahumanMenu,
                  ann=u'如果你没有选择任何物体,将会更新所有控制,否则更新选中控制器')
    cmds.menuItem(label=u'重置控制器位置', c=mj.resetLoctorPos, p=metahumanMenu,
                  ann=u'如果你没有选择任何物体,将会更新所有控制,否则更新选中控制器')
    cmds.menuItem(label=u'镜像左边控制器位置到右边', c=mj.mirrorLocatorDate, p=metahumanMenu,
                  ann=u'如果你没有选择任何物体,将会更新所有控制,否则更新选中控制器')
    cmds.menuItem(divider=True, dividerLabel=u'数据备份与导出', p=metahumanMenu)
    cmds.menuItem(label=u'存储Locator控制器数据', c=mj.savelocatorDate, p=metahumanMenu,
                  ann=u'如果你没有选择任何物体,将会更新所有控制,否则更新选中控制器')
    cmds.menuItem(label=u'导入Locator控制器数据', c=mj.importCtlPreset, p=metahumanMenu,
                  ann=u'如果你没有选择任何物体,将会更新所有控制,否则更新选中控制器')
    cmds.menuItem(label=u'选中控制器',
                  c=usRig.seleyeCtl, p=metahumanMenu)
    
    cmds.menuItem(divider=True, dividerLabel=u'表情控制面板设置', p=metahumanMenu)
    cmds.menuItem(label=u'重置面部表情',
                  c=mj.resetPhiz, p=metahumanMenu)
    
    
    cmds.menuItem(label=u'给脸部面板控制器添加幅度控制参数',
                  c=usRig.addAmplitudeAttribute, p=metahumanMenu)
    cmds.menuItem(label=u'删除脸部面板控制器幅度控制参数',
                  c=usRig.removeAmplitudeAttribute, p=metahumanMenu)
    cmds.menuItem(label=u'存储控制器面板数据',
                  c=mj.savePhizAmpDate, p=metahumanMenu)
    cmds.menuItem(label=u'导入控制器面板数据',
                  c=mj.importPhizAmpDate, p=metahumanMenu)
    cmds.menuItem(label=u'镜像控制器面板数据',
                  c=mj.mirrorPhizAmpDate, p=metahumanMenu)

    # 眼球周边模型设置
    cmds.menuItem(divider=True, dividerLabel=u'眼球等模型设置', p=metahumanMenu)
    cmds.menuItem(label=u'移动Cartilage到新的模型',
                  c=mj.moveCartilageToTarMesh, p=metahumanMenu,ann=u'先选择要移动的物体,再选择原始依附物体,再选择目标依附物体')

    cmds.menuItem(divider=True, dividerLabel=u'绑定通用命令', p=metahumanMenu)
    
    #metahuman菜单结束
    
    cmds.menuItem(divider=True, p=items['LugwitRig'], dividerLabel=u'绑定清理相关命令')
    cmds.menuItem(
        label=u'删除包裹', c=lambda *args: usRig.delNodeByTp('wrap'), p=items['LugwitRig'])
    cmds.menuItem(label=u'删除输出历史', c=usRig.delOutput, p=items['LugwitRig'])
    cmds.menuItem(label=u'删除blendShapes',
                  c=lambda *args: usRig.delNodeByTp('blendShapes'), p=items['LugwitRig'])
    cmds.menuItem(label=u'删除关键帧', c=usRig.delKeyFra, p=items['LugwitRig'])
    
    cmds.menuItem(divider=True, p=items['LugwitRig'], dividerLabel=u'BlendShape相关命令')
    cmds.menuItem(label=u'匹配BlendShape名称',
                  c=usRig.matchBSName, p=items['LugwitRig'], ann=u'请先选择具有BS的模型')
    cmds.menuItem(label=u'设置BS权重为0', c=usRig.setBsWeightTo0, p=items['LugwitRig'])
    cmds.menuItem(label=u'烘焙blensShape目标',
                  c=usRig.exPhizFromBS, p=items['LugwitRig'], ann=u"锁定节点的bs目标不会被导出")
    cmds.menuItem(label=u'替换bs目标', c=usRig.replaceBSTarget, p=items['LugwitRig'],
                  ann=u'目标命名为Fix')

   
    
    cmds.menuItem(divider=True, p=items['LugwitRig'], dividerLabel=u'重绑定相关命令')
    cmds.menuItem(label=u'替换变形源', c=usRig.replaceDeformOri, p=items['LugwitRig'],
                  ann=u'请先选择已经绑好的物体,再选择要目标物体')
    cmds.menuItem(label=u'替换变形源并重新绑定', c=functools.partial(usRig.reBind,1), p=items['LugwitRig'],
                  ann=u'请先选择已经绑好的物体,再选择要目标物体')
    cmds.menuItem(label=u'当前模型和骨骼状态重绑定', c=functools.partial(usRig.reBind,0), p=items['LugwitRig'],
                  ann=u'移动骨骼前把蒙皮节点node节点节点行为设置为hasNoEffect,选中绑定好的模型,直接点击命令即可')
    
    cmds.menuItem(divider=True, p=items['LugwitRig'], dividerLabel=u'绑定Dubug工具')
    cmds.menuItem(label=u'选中模型相关骨骼', c=usRig.selectRelativeJnts, p=items['LugwitRig'],
                  ann=u'请先选择已经绑好的物体,再选择要目标物体')
    cmds.menuItem(label=u'通过顶点选择控制器', c=mj.selCtlVsVtx, p=items['LugwitRig'],
                  ann=u'请先选择已经绑好的物体,再选择要目标物体')
    cmds.menuItem(label=u'骨骼随机颜色', c=usRig.jntSetRanColor, p=items['LugwitRig'])
    
    cmds.menuItem(divider=True, p=items['LugwitRig'], dividerLabel=u'骨骼对称工具')
    cmds.menuItem(label=u'对称骨骼位置', c=usRig.symJntTransform, p=items['LugwitRig'],
                  ann=u'选择根骨骼')
    
    cmds.menuItem(divider=True, p=items['LugwitRig'], dividerLabel=u'模型包裹')
    cmds.menuItem(label=u'自动包裹', c=usRig.autodeformModel, p=items['LugwitRig'],
                  ann=u'先选在静态模型,在选在绑定模型')
    
    
    


viewMenuWidth=35   
def viewMenu(*args):
    
    if cmds.control('viewLeftMenu', ex=1):
        cmds.warning (u'视图菜单存在')
        cmds.deleteUI('viewLeftMenu')
    viewLeftMenu=cmds.columnLayout('viewLeftMenu',  w=viewMenuWidth,p="L_V",adj=1)
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
    
    cmds.iconTextButton(image1='textureEditor.png', c=cmds.TextureViewWindow)
    cmds.popupMenu(b=3, mm=1)
    cmds.menuItem(rp="N",label=u'贴图管理', c=txLib.textureManager.main)

    cmds.iconTextButton(image1='blendShapeEditor.png', c=cmds.ShapeEditor)
    cmds.popupMenu()
    cmds.menuItem(l=u'切换BlensShapeSS开关',c=usRig.switchBS)
    
    advDir = LugwitPath+r'/mayaPlug/ThridPlug/AdvancedSkeleton5/scripts/AdvancedSkeleton5Files'
    adv5MelPath=LugwitPath+r'/mayaPlug/ThridPlug/AdvancedSkeleton5/scripts/AdvancedSkeleton5.mel'
    cmds.iconTextButton(image1=iconDir+'AS5.png',
                        c="mel.eval('source \"{}\";AdvancedSkeleton5;')".format(adv5MelPath), iol='adv')
    
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
    
    cmds.iconTextButton(image1=r'Z:\plug_in\Lugwit_plug\mayaPlug\icon\U3D.png',w=15, 
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

    melFile="Z:/plug_in/Lugwit_plug/mayaPlug/l_scripts/Mel/PaiPin.mel"
    cmds.button(l=u'拍屏',w=15, h=25,c=lambda *args :mm.eval('source "{}";'.format(melFile)))
    cmds.button(l=u'截屏',w=15, h=25,c=usualLib.screenShot)
    
    cmds.button(l=u'路径',w=15, h=25,)
    cmds.popupMenu()
    cmds.menuItem(label=u'复制Maya文件路径',c=lambda *args:pyperclip.copy(cmds.file(q=1,sn=1)))
    cmds.menuItem(label=u'打开Maya文件路径',c=lambda *args:os.startfile(os.path.dirname(cmds.file(q=1,sn=1))))
    cmds.menuItem(label=u'打开临时目录',c=lambda *args:os.startfile(os.environ['TEMP']))
    
    cmds.iconTextButton(image1=LugwitPath+r'\icons\p4v.jpg',w=25,h=30)
    cmds.popupMenu(b=3, mm=1)
    cmds.menuItem(rp="N",label=u'添加/签出',c=lambda *args: P4Lib.checkOut(cmds.file(q=1,sn=1)))
    cmds.menuItem(rp="S",label=u'提交',)#c=lambda *args: P4Lib.checkOut
    
    

    
    


def WS(*args):
    cmds.workspaceControl("L_V", dtc=('MainPane','left'),retain=0,iw=viewMenuWidth,wp='free',fl=0,l='...')
    
def viewWS(*args):

    if cmds.control('L_V', ex=1):
        cmds.deleteUI('L_V')
        # cmds.workspaceControl("L_V", iw=width,wp='free',e=1,l='')  
        cmds.warning (u'视图菜单存在')
        WS()
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
            cmds.separator(height=80, style='none')  # style='none' 使其不可见
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
            pass
        
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
    cmds.menuItem(l=u'刷新绑定菜单', c=lambda *args: rigMenu(1))
    cmds.menuItem(l=u'刷新动画菜单')
    cmds.menuItem(l=u'刷新视图菜单', c=modelPaneMenu)
    cmds.button(label=u'更新Plug',ann='从P4获取最新代码' , bgc=[0, .8, 0])
    
    cmds.iconTextButton(image1=LugwitPath+r'\mayaPlug\materialPlug\prefs\icon\NiuMatIco.png',
                        w=14, h=38,c=loadMayaMatPlug,
                        ann=u'加载侧边栏插件')

def refreshViewMenu(*args):
    reload (sys.modules['LugwitMayaPlugStart'])
    viewWS()
    
    
def CodeEncryptionMenu(*args):
    cmds.menuItem(l=u'代码加密', c=CodeEncryptionUI,p=items[u'CodeEncryption'])

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
                    pass
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
            [1]
            # cmds.setAttr(FileNode+'.ftn', newcMap, type='string')
            if not os.path.exists(newcMap):
                # os.rename(newPath, newcMap)
                try:
                    cmds.rename(FileNode, mat+'_BaseColor')
                    cmds.select(mat)
                except:
                    pass

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
    with open (LugwitPath+r'\mayaPlug\l_scripts\Data\vscodePyhonEnv.txt','r') as f:
        env=f.read()
    env=eval(env)
    MayaCodeEncryptionUIFile=r'Z:/plug_in/Lugwit_plug/mayaPlug/l_scripts/CodeEncryption/MayaCodeEncryptionUI.py'
    subprocess.Popen('Z:/plug_in/Python/Python37/python.exe {}'.format(MayaCodeEncryptionUIFile)
                    ,cwd=r'Z:/plug_in/Lugwit_plug/mayaPlug/l_scripts/CodeEncryption',shell=True,env=env)

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


def loadMayaMatPlug(*args):
    cmds.select(cl=1)
    matPlugDir = LugwitPath+"/mayaPlug/materialPlug"
    sys.path.append(matPlugDir+'/scripts')
    if sys.version_info[0]==2:
        sys.path.append(matPlugDir+'/python_library')
    try:
        reload(UV_UI)
    except:
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
    exchangeDir = 'S:/DataTrans/FQQ/ExchangeFolder'
    exchangeFile = 'S:/DataTrans/FQQ/ExchangeFolder/exchangeFile.ma'
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
