# -*- coding: utf-8 -*-
from __future__ import print_function

import maya.cmds as cmds

if __name__ == "__main__":#如果是主程序
    all_mesh = cmds.ls(sl=True,type="mesh",dag=True)#获取所有选中的模型的mesh

    for _mesh in all_mesh:#循环
        try:
            cmds.setAttr("{}.{}".format(_mesh,"rsEnableSubdivision"),1)#设置属性1
            cmds.setAttr("{}.{}".format(_mesh,"rsMaxTessellationSubdivs"),2)#设置属性2

        except Exception as e:
            print(e)#如果报错，则打印报错原因
            continue