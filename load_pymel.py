# -*- coding: utf-8 -*-
import maya.mel

class PmLoader:
    def __init__(self):
        # 初始情况下不加载 pymel.core
        global cc
        

    def __getattr__(self, name):
        import pymel.core as pm
        return getattr(pm, name)

# 创建 PmLoader 实例
pm = PmLoader()