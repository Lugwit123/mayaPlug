# -*- coding:utf-8 -*-
import maya.cmds as cm
import os
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import re
import functools
import time
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import *
    from PySide import __version__
    from shiboken import wrapInstance
except:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtUiTools import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance

import check_diference_models_tools as uitools
reload(uitools)
import check_difference_models as check_models
reload(check_models)


def paintEvent(self,event):
    opt = QStyleOption()
    opt.initFrom(self)
    p = QPainter(self)
    self.style().drawPrimitive(QStyle.PE_Widget,opt,p,self)

        
class TestWidget(QWidget):
    def __init__(self,parent = None):
        super(TitleWidget,self).__init__(parent)
        
TestWidget.paintEvent = paintEvent


class TreeViewItemDelegate(QStyledItemDelegate):

    def __init__(self,parent = None):
        super(TreeViewItemDelegate,self).__init__(parent)

    def paint(self,painter,option,index):
        viewOption = QStyleOptionViewItem(option)    
        # if(index.data(Qt.UserRole) == 1):
        if index.data(Qt.ForegroundRole):
            viewOption.palette.setColor(QPalette.HighlightedText,index.data(Qt.ForegroundRole).color())  
        super(TreeViewItemDelegate,self).paint(painter, viewOption, index)
        # QItemDelegate.paint(self,painter, viewOption, index)



class UIWin(QWidget):
    def __init__(self,parent = None):
        super(UIWin,self).__init__(parent)

        self.group1_item_dict = {}
        self.group2_item_dict = {}
        self.update_model_ing = False
        self.difference_polygons = []

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'模型层级对比')
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        loader = QUiLoader()
        # loader.registerCustomWidget(InteractiveListView)
        file = QFile(uitools.getUIPath('main.ui'))
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=uitools.getMayaWin())
        layout.addWidget(self.ui)
        file.close()


        self.group1_model = QStandardItemModel(self)
        self.group2_model = QStandardItemModel(self)

        tree_view_item_delegate = TreeViewItemDelegate(self)
        self.ui.group1_tree_view.setItemDelegate(tree_view_item_delegate)
        self.ui.group2_tree_view.setItemDelegate(tree_view_item_delegate)

        self.ui.group1_tree_view.setModel(self.group1_model)
        self.ui.group2_tree_view.setModel(self.group2_model)


        self.ui.doit_btn.clicked.connect(self.compare_groups)

        self.group1_tree_view_selection_model = self.ui.group1_tree_view.selectionModel()
        self.group2_tree_view_selection_model = self.ui.group2_tree_view.selectionModel()
        self.group1_tree_view_selection_model.selectionChanged.connect(self.select_obj)
        self.group2_tree_view_selection_model.selectionChanged.connect(self.select_obj)
        # a = QStandardItem('a')
        # a.appendRow(QStandardItem('b'))
        # a.appendRow(QStandardItem('c'))
        # group1_model.setItem(0,a)



        # self.ui.xxx
        self.setStyleSheet(uitools.getStyleSheet('main.qss'))


    def select_obj(self,selected,deselected):
        if self.update_model_ing:
            return
        try:
            indexes = selected.indexes()
            if not indexes:
                return
            index = indexes[0]
            if self.sender().model() == self.group1_model:
                if not self.ui.checkBox.isChecked():
                    self.group2_tree_view_selection_model.clear()
                
                obj = self.group1_model.data(index,101)
                if cm.objExists(obj):
                    cm.select(obj,r = True)
                    relative_path = self.group1_model.data(index,102)
                    if self.ui.checkBox.isChecked():
                        if relative_path in self.group2_item_dict.keys():
                            # print(self.group2_item_dict[relative_path].index())
                            self.group2_tree_view_selection_model.select(self.group2_item_dict[relative_path].index(),QItemSelectionModel.ClearAndSelect)
                            obj2 = self.group2_model.data(self.group2_item_dict[relative_path].index(),101)
                            if cm.objExists(obj2):
                                cm.select(obj2,add = True)
                        else:
                            self.group2_tree_view_selection_model.clear()
            else:
                if not self.ui.checkBox.isChecked():
                    self.group1_tree_view_selection_model.clear()
                obj = self.group2_model.data(index,101)
                if cm.objExists(obj):
                    cm.select(obj,r = True)
                    relative_path = self.group2_model.data(index,102)
                    if self.ui.checkBox.isChecked():
                        if relative_path in self.group1_item_dict.keys():
                            # print(self.group1_item_dict[relative_path].index())
                            self.group1_tree_view_selection_model.select(self.group1_item_dict[relative_path].index(),QItemSelectionModel.ClearAndSelect)
                            obj2 = self.group1_model.data(self.group1_item_dict[relative_path].index(),101)
                            if cm.objExists(obj2):
                                cm.select(obj2,add = True)
                        else:
                            self.group1_tree_view_selection_model.clear()
            # print('selected')
        except Exception as e:
            print(e)

    def clear_data(self):
        self.group1_model.clear()
        self.group2_model.clear()
        self.ui.group1_label.setText('')
        self.ui.group2_label.setText('')
        self.ui.group1_result_label.setText('')
        self.ui.group2_result_label.setText('')
        self.ui.info_label.setText('')
        self.group1_item_dict = {}
        self.group2_item_dict = {}
        self.difference_polygons = []

    def get_result(self,difference_list1,difference_polygons):
        error_message = u' %d 个错误'%len(difference_list1) if difference_list1 else ''
        warning_message = u' %d 个警告'%len(difference_polygons) if difference_polygons else ''
        if error_message and warning_message:
            return error_message + ',' + warning_message
        elif error_message or warning_message:
            return error_message + warning_message
        else:
            return u'没有错误'

    def compare_groups(self):
        self.update_model_ing = True
        self.clear_data()
        sel_objs = cm.ls(sl = True)
        if len(sel_objs) != 2:
            cm.warning(u'请选择两个组')
            self.update_model_ing = False
            return
        start_time = time.time()
        group1_children_dict = check_models.get_children_dict(sel_objs[0])
        group1_list = group1_children_dict.keys()
        group2_children_dict = check_models.get_children_dict(sel_objs[1])
        group2_list = group2_children_dict.keys()
        difference_list1,difference_list2 = check_models.get_difference_list(group1_list,group2_list)
        self.difference_polygons = check_models.get_difference_polygons(group1_children_dict,group2_children_dict)
        # print(group1_list)
        # print(group2_list)
        self.update_model(sel_objs[0],self.ui.group1_tree_view,group1_list,group1_children_dict,difference_list1,self.group1_item_dict)
        self.update_model(sel_objs[1],self.ui.group2_tree_view,group2_list,group2_children_dict,difference_list2,self.group2_item_dict)
        self.ui.group1_label.setText(sel_objs[0])
        self.ui.group2_label.setText(sel_objs[1])
        group1_result = self.get_result(difference_list1,self.difference_polygons)
        group2_result = self.get_result(difference_list2,self.difference_polygons)
        self.ui.group1_result_label.setText(group1_result)
        self.ui.group2_result_label.setText(group2_result)
        if difference_list1 or self.difference_polygons:
            self.ui.group1_result_label.setStyleSheet('color:rgb(255,0,0);')
        else:
            self.ui.group1_result_label.setStyleSheet('color:rgb(0,255,0);')
        if difference_list2 or self.difference_polygons:
            self.ui.group2_result_label.setStyleSheet('color:rgb(255,0,0);')
        else:
            self.ui.group2_result_label.setStyleSheet('color:rgb(0,255,0);')
        end_time = time.time()
        self.ui.info_label.setText(u'检查完毕！ time: %.8ss'%(end_time - start_time))
        self.ui.group1_tree_view.expandAll()
        self.ui.group2_tree_view.expandAll()
        self.update_model_ing = False
        

    def update_model(self,big_group,tree_view,group_list,children_dict,red_list,group_item_dict):
        model = tree_view.model()
        if not group_list:
            return
        group_dict = {}
        for group in group_list:
            group_dict.setdefault(len(group.split('|')),[]).append(group)
        layer_count_list = group_dict.keys()
        layer_count_list.sort()
        wrongColor = QColor(255,0,0)
        warningColor = QColor(255,255,0)
        transform_icon = QIcon(uitools.getImagePath('transform.png'))
        mesh_icon = QIcon(uitools.getImagePath('mesh.png'))
        for layer_count in layer_count_list:
            objs = group_dict[layer_count]
            for obj in objs:
                # obj_path = big_group + '|' + obj
                obj_path = children_dict[obj]
                item = QStandardItem(obj.split('|')[-1])
                group_item_dict[obj] = item
                item.setData(obj_path,101)
                item.setData(obj,102)
                if cm.listRelatives(obj_path,s = True,type = 'mesh'):
                    item.setIcon(mesh_icon)
                else:
                    item.setIcon(transform_icon)
                if obj in red_list:
                    item.setForeground(QBrush(wrongColor))
                else:
                    if obj in self.difference_polygons:
                        item.setForeground(QBrush(warningColor))
                if layer_count == 1:
                    model.appendRow(item)
                else:
                    parent = '|'.join(obj.split('|')[0:layer_count - 1])
                    group_item_dict[parent].appendRow(item)
                #print(group_dict[layer_count])


 #加入点线面识别，黄色警告
 #全部成功要弹窗
 #加入前面的显示线
 #顺序乱了调整一下

def mainUI():
    winName = 'check_diference_models_tools_win'
    if cm.window(winName,q = True,exists = True):
        cm.deleteUI(winName)

    win = UIWin(uitools.getMayaWin())
    win.setObjectName(winName)
    win.show()