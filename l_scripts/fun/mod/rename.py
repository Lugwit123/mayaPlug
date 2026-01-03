# coding:utf-8
maya.mel.eval('python("import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm")')


def rename(name="prefix{2}suffix"):
    u"""
    :param name: 需要在{}内填入序列位数，如填入{3}，则重命名为001，002， 003
    :return:
    """
    name = name.replace("{", "{:0>")
    for i, obj in enumerate(pm.selected()):
        obj.rename(name.format(i+1))
        if obj.getShape():
            obj.getShape().rename(name.format(i+1)+"Shape")

