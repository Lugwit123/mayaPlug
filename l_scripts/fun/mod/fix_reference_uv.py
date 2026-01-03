# -*- coding:utf-8 -*-
import maya.cmds as cm
import maya.mel as mel
import functools


def fix_reference_uv(type,*argvs):
    if type == 0:
        mesh_list = cm.listRelatives(cm.ls(sl = True),ad = True,pa = True,type = 'mesh')
    else:
        mesh_list = cm.ls(type = 'mesh')
    for mesh in mesh_list:
        #如果有一个为map1，且为空，就把另外的拷贝过去
        
        all_uv_set_list = cm.polyUVSet(mesh,auv = True,q = True)
        if all_uv_set_list:
            if 'map1' in all_uv_set_list:
                if len(all_uv_set_list) > 1:
                    if cm.polyEvaluate(mesh,uva = True,uvs = 'map1') == 0:
                        cm.polyCopyUV( mesh, uvi=all_uv_set_list[1], uvs='map1' )
                        print('fix{}'.format(mesh))
    mel.eval(u"print(\"执行完毕！\");")
            

def fix_reference_uv_window():
    winName = 'fix_reference_uv_win'
    if cm.window(winName,exists = True):
        cm.deleteUI(winName)
    cm.window(winName,title = u'修复uvset')
    cm.window(winName,e = True,w = 260,h = 100)
    cm.columnLayout(adj = True,rs = 5)
    cm.text(u'修复引用模型的uvset\n(如果map1为空，把第二个uvset复制到map1)',h = 70)
    btn1 = cm.button( label=u'修复所选',h = 30,c = functools.partial(fix_reference_uv,0))
    btn2 = cm.button( label=u'修复所有',h = 30,c = functools.partial(fix_reference_uv,1))
    cm.showWindow(winName)

    
if __name__ == '__main__':
    fix_reference_uv_window()