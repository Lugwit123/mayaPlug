# coding:utf-8
import maya.cmds as cmds,os,sys

hezi=r"Q:\SoftwareA\SoftwareB\MayaPlugins\ShanShui\ShanShui_L\MayaIcons\hezi.png"
jinlin=r"Q:\SoftwareA\SoftwareB\MayaPlugins\ShanShui\ShanShui_L\MayaIcons\jinlin.png"
os.environ['New']='False'
os.environ['Lugwit_Debug']='noprint'

LugwitToolDir=os.environ.get('LugwitToolDir')
sys.path.append(LugwitToolDir+'/Lib')


import Lugwit_Module as LM


def jinlinhezi_switch(*args):
    image=cmds.iconTextCheckBox('jinlinhezi_switch',q=1,image=1)
    if image==hezi:
        cmds.iconTextCheckBox('jinlinhezi_switch',e=1,image=jinlin)
        import os
        os.environ['New']='True'
        print  ("os.environ['New']:",os.environ['New'])
    else :
        cmds.iconTextCheckBox('jinlinhezi_switch',e=1,image=hezi)
        import os
        os.environ['New']='False'
        print  ("os.environ['New']:",os.environ['New'])

@LM.try_exp
def lockDockingButton_command(*args):
    value=cmds.optionVar(query="workspacesLockDocking")
    print ('workspacesLockDocking',value)
    cmds.optionVar(intValue=("workspacesLockDocking", 1-value))


def debug_option_changeFunc(item) :
    os.environ['Lugwit_Debug']=item
    print (os.environ['Lugwit_Debug'])
    
def cgtw_cache_switch_func(*args):
    state = cmds.symbolCheckBox('cgtw_cache_switch', q=True, value=True)
    os.environ['LUGWIT_CGTW_CACHE'] = 'on' if state else 'off'
    print(u'LUGWIT_CGTW_CACHE:', os.environ['LUGWIT_CGTW_CACHE'])

def SwitchButtonFunc(*args):
    if cmds.control('lockDockingButton',q=1,ex=1):
        cmds.deleteUI('lockDockingButton')
    if cmds.control('lugwit_workspaceSwitchFormLayout',q=1,ex=1):
        cmds.deleteUI("lugwit_workspaceSwitchFormLayout")
    cmds.frameLayout('lugwit_workspaceSwitchFormLayout',
                    parent='MayaWindow|workspaceSelectorLayout', 
                    width=108, height=25, borderVisible=False,labelVisible=False)
    cmds.rowColumnLayout('lugwit_workspaceSwitchLayout',
                         p='lugwit_workspaceSwitchFormLayout',
                         numberOfColumns=4)
    cmds.symbolCheckBox('lockDockingButton',
                cc=lockDockingButton_command,p='lugwit_workspaceSwitchLayout',
                image='lock.png',hlc=[0.5,0.1,0])
    # cmds.symbolCheckBox('cgtw_cache_switch',
    #             cc=cgtw_cache_switch_func, p='lugwit_workspaceSwitchLayout',
    #             image='commandButton.png', value=os.environ.get('LUGWIT_CGTW_CACHE', '0') == '1',
    #             ann=u'切换CGTW缓存（勾选=关闭缓存）')
    cmds.optionMenu('debug_option',w=120,cc=debug_option_changeFunc,label='Debug:')
    cmds.menuItem( label='noprint' )
    cmds.menuItem( label='pureprint' )
    cmds.menuItem( label='inspect' )
    # cmds.iconTextCheckBox('jinlinhezi_switch',style='iconOnly',
    #                         p='lugwit_workspaceSwitchLayout',
    #                         image=hezi,cc=jinlinhezi_switch,mh=0,w=60,
    #                         backgroundColor=[0, 0, 0],ebg=0,ekf=0,olb=[0,0,0,0],ua=0)

cmds.symbolCheckBox('lockDockingButton',e=1,v=1)
if __name__ == "__main__":
    SwitchButtonFunc()
