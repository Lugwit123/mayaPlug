# coding:utf-8

import maya.cmds as cmds

def rename_polygon_children(group):
    u"""
    把组下面的模型命名为 组名_xx(xx为数字，个位数前面会加0)
    """
    children = cmds.listRelatives(group,c = True,type = 'transform',pa = True)
    index = 1
    temp_list = []
    if children:
        #这个for循环改名是为了防止后面有物体跟现在要改的名字同名
        for child in children:
            if cmds.listRelatives(child,s = True,type = 'mesh',pa = True):
                temp_list.append(cmds.rename(child,'a'))                                    
        for child in temp_list:
            name = group + '_%02d'%index
            cmds.rename(child,name)
            index += 1
            
def rename_polygon_children_by_selection_groups():
    for group in cmds.ls(sl = True):
        rename_polygon_children(group)


