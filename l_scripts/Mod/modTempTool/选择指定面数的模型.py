# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om
import maya.cmds as cmds

class MyTools():

    def __init__(self):
        self.window_name = "AnyTools"
        self.window_title = "Any Tools"
        self.layoutMain = "layoutMain"

    def showUI(self):
        if cmds.window(self.window_name, ex = 1):
            cmds.deleteUI(self.window_name, window = 1)
        if cmds.windowPref(self.window_name, ex = 1):
            cmds.windowPref(self.window_name, r = 1)

        current_window = cmds.window(self.window_name, t = self.window_title, w = 350, bgc = [0.2,0.2,0.2])

        cmds.columnLayout(self.layoutMain, adj = 1, cal = "center", cat = ["both", 0], p = current_window)
        cmds.separator(p=self.layoutMain)
        cmds.separator(p=self.layoutMain)

        # Replace low model with instance
        cmds.rowLayout(nc=2, ad2 = 1, p = self.layoutMain)
        cmds.intField('_ployint')
        cmds.button(l=u'获取所选模型面数', w=100, c=lambda x:self.get_faceNum())
        cmds.button(l=u"选择指定面数模型", c=lambda x:self._select_poly(), p = self.layoutMain)
        cmds.separator(p=self.layoutMain)

        # Bottom of window
        cmds.showWindow(self.window_name)

    def get_faceNum(self):
        _selected = cmds.ls(sl = True)
        if len(_selected) == 1:
            _faces = cmds.polyEvaluate(_selected[0], f=1)
            print(_faces)
            cmds.intField('_ployint', e=1, v=_faces)
            cmds.select(cl=1)
            # return _faces
        else:
            cmds.warning(u'请选择一个单独模型')
    
    def _select_poly(self):
        _num = cmds.intField('_ployint', q=1, v=1)
        _select_grp = cmds.ls(sl = True)
        if _select_grp:
            _all_transform = cmds.listRelatives(_select_grp, ad = True, type = "transform")
        else:
            _all_transform = cmds.ls(type = "transform")
        _need_transform = []
        for _transform in _all_transform:
            try:
                _transform_shape = cmds.listRelatives(_transform, c = True, s = True)[0]
            except:
                continue
            if cmds.nodeType(_transform_shape) == "mesh":
                _need_transform.append(_transform)
        
        _final_poly = []
        for _trans in _need_transform:
            _mesh = cmds.listRelatives(_trans, s = True, ni = True, type = "mesh")[0]
            selectionList = om.MSelectionList()
            selectionList.add(_mesh)
            _node = selectionList.getDependNode(0)
            _fnMesh = om.MFnMesh(_node)
            _polynum = _fnMesh.numPolygons
            
            if _polynum == _num:
                _final_poly.append(_trans)
                
        cmds.select(_final_poly)

win = MyTools()
win.showUI()