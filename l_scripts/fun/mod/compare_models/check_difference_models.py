# coding:utf-8

import maya.cmds as cmds
import collections

def get_children_dict(group):
    u"""
    获取组下面的所有transform节点的相对路径
    """
    children_dict = collections.OrderedDict()
    group_long = cmds.ls(group,l = True)[0]
    long_transform_list = cmds.listRelatives(group,ad = True,type = 'transform',f = True)
    if long_transform_list:
        for long_transform in long_transform_list:
            # children_dict.append(long_transform[len(group_long) + 1:])
            relative_path_with_namespace = long_transform[len(group_long) + 1:]
            relative_path = '|'.join([name_part.split(':')[-1] for name_part in relative_path_with_namespace.split('|')])
            children_dict[relative_path] = long_transform
    return children_dict

def get_difference_polygons(children_dict1,children_dict2):
    u"""
    返回相对路径相同但模型点线面不同(点线面数量和点的位移)的列表
    children_dict是从get_children_dict返回的字典
    """
    difference_polygons = []
    for relative_path in children_dict1.keys():
        children_dict2_relative_paths = children_dict2.keys()
        if relative_path in children_dict2_relative_paths:
            obj1_is_poly = True if cmds.listRelatives(children_dict1[relative_path],s = True,type = 'mesh') else False
            obj2_is_poly = True if cmds.listRelatives(children_dict2[relative_path],s = True,type = 'mesh') else False
            if obj1_is_poly and obj2_is_poly:
                if cmds.polyCompare(children_dict1[relative_path],children_dict2[relative_path],v = True,e = True,fd = True):
                    difference_polygons.append(relative_path)
            elif obj1_is_poly or obj2_is_poly:
                difference_polygons.append(relative_path)
    return difference_polygons
    

def get_difference_list(list1,list2):
    # list1 = get_relative_paths(group1)
    # list2 = get_relative_paths(group2)
    difference_list1 = [obj for obj in list1 if obj not in list2]
    difference_list2 = [obj for obj in list2 if obj not in list1]
    return difference_list1,difference_list2

#创建treeListView的model时，按照相对层数分类，然后按照从少到多创建item
#创完遍历item，看它是否在difference_list里面，在就给红色
