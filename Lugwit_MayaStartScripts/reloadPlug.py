# coding:utf-8
import maya.cmds as cmds
import sys,os
sys.path.append(os.environ.get('Lugwit_PluginPath')+r'\Lugwit_plug\mayaPlug\Lugwit_MayaStartScripts')
import LugwitMayaPlugStart
from imp import reload

LugwitToolDir=os.environ.get('LugwitToolDir')
sys.path.append(LugwitToolDir+'/Lib')

import Lugwit_Module as LM

def reloadPlugFunc(*args):
    cmds.unloadPlugin('LugwitStartPlug')
    import LugwitMayaPlugStart
    cmds.loadPlugin('LugwitStartPlug')
    loadMayaMatPlug()

def loadMayaMatPlug(*args):
    cmds.select(cl=1)
    matPlugDir = LM.LugwitPath+"/mayaPlug/materialPlug"
    sys.path.append(matPlugDir+'/scripts')
    if sys.version_info[0]==2:
        sys.path.append(matPlugDir+'/python_library')
    try:
        reload(UV_UI)
    except:
        print ('reald error,import UV_UI')
        import UV_UI
    UV_UI.UI()

def UI(*args):
    import maya.cmds as cmds
    if cmds.control('reloadUI',q=1,ex=1):
        cmds.showWindow('reloadUI')
    else:
        cmds.window('reloadUI',w=220,title=u'插件管理',h=40,s=0)
        cmds.rowColumnLayout(adj=1)
        cmds.button(u'重载插件',c=reloadPlugFunc,h=30)
        cmds.button(u'关闭插件',c="import maya.cmds as cmds;cmds.unloadPlugin('LugwitStartPlug')",h=30)
        cmds.button(u'打开插件',c="import maya.cmds as cmds;cmds.loadPlugin('LugwitStartPlug')",h=30)
        cmds.showWindow()
    
        


