# coding:utf-8

import maya.api.OpenMaya as om
import os
import os,sys
import L_GV
import maya.cmds as cmds


LugwitToolDir = os.getenv('LugwitToolDir')
sys.path.append(LugwitToolDir+'/Lib')
import Lugwit_Module as LM
lprint=LM.lprint

# 日志文件路径
LOG_FILE_PATH = "D:/bb.log"

# 删除日志文件（如果存在）
if os.path.exists(LOG_FILE_PATH):
    os.remove(LOG_FILE_PATH)


# 限制递归深度
RECURSION_DEPTH_LIMIT = 1000

# 打印 instObjGroups 属性的连接信息并断开
def disconnect_instObjGroups_attributes(source_node_name, target_node, current_depth):
    # lprint(locals())
    # 创建选择列表并添加节点
    sel_list = om.MSelectionList()
    try:
        sel_list.add(source_node_name)
    except Exception as e:
        lprint(u"节点 {} 不存在，错误: {}".format(source_node_name, e))
        return

    # 获取节点的 MObject
    node = sel_list.getDependNode(0)
    
    # 创建 MFnDependencyNode 函数集
    fn_node = om.MFnDependencyNode(node)
    
    # 获取 instObjGroups 属性的 MPlug
    try:
        instObjGroups_plug = fn_node.findPlug('instObjGroups', False)
    except Exception as e:
        lprint("无法找到属性 'instObjGroups'，错误: {}".format(e))
        return

    # 跳过 compInstObjGroups 及其子属性
    if 'compInstObjGroups' in instObjGroups_plug.name():
        lprint(u"跳过 compInstObjGroups 属性，plug: {}".format(instObjGroups_plug.name()))
        return
    
    try:
        num_instObjGroups_elements = instObjGroups_plug.numElements()
        lprint(u"instObjGroups 属性的元素数量: {}".format(num_instObjGroups_elements))
    except Exception as e:
        lprint(u"获取 instObjGroups.numElements 时发生错误: {}".format(e))
        return

    for i in range(num_instObjGroups_elements):
        instObjGroup_element = instObjGroups_plug.elementByPhysicalIndex(i)
        index_i = instObjGroup_element.logicalIndex()

        # 获取 objectGroups 属性
        objectGroups_plug = instObjGroup_element.child(0)  # 假设 objectGroups 是第一个子属性
        
        # 跳过导致崩溃的属性
        if 'compObjectGroups' in objectGroups_plug.name():
            lprint(u"跳过 compObjectGroups 属性，plug: {}".format(objectGroups_plug.name()))
            continue
        
        try:
            num_objectGroups_elements = objectGroups_plug.numElements()
            #lprint(u"objectGroups[{}] 属性的元素数量: {}".format(index_i, num_objectGroups_elements))
        except Exception as e:
            lprint(u"获取 objectGroups.numElements 时发生错误: {}".format(e))
            continue

        for j in range(num_objectGroups_elements):
            objectGroup_element = objectGroups_plug.elementByPhysicalIndex(j)
            index_j = objectGroup_element.logicalIndex()

            # 打印并断开 instObjGroups[i].objectGroups[j] 的连接
            disconnect_plug_between_nodes(objectGroup_element, target_node, current_depth + 1)

            # 处理 objectGroups 的子属性
            num_children = objectGroup_element.numChildren()
            for k in range(num_children):
                child_plug = objectGroup_element.child(k)
                disconnect_plug_between_nodes(child_plug, target_node, current_depth + 1)

def are_nodes_same_by_uuid(source_node, target_node):

    # 使用 MFnDependencyNode 来获取名称
    source_node_fn = om.MFnDependencyNode(source_node)
    target_node_fn = om.MFnDependencyNode(target_node)

    # 对比 UUID
    return L_GV.are_nodes_same_by_uuid(source_node_fn.name(), target_node_fn.name())



def get_plug_full_name(plug):
    lprint(locals())
    node_obj = plug.node()
    full_plug_name=""
    if node_obj.hasFn(om.MFn.kDagNode):
        try:
            dag_path = om.MDagPath.getAPathTo(node_obj)
            lprint(dag_path)
            full_path_name = dag_path.fullPathName()
            full_plug_name = "{}.{}".format(full_path_name, plug.partialName())
        except Exception as e:
            lprint(e)
    else:
        try:
            full_plug_name = plug.name()
            lprint(type(full_plug_name))
        except Exception as e:
            lprint(e)
    
    lprint(full_plug_name)
    return full_plug_name






# 打印并断开连接信息
def disconnect_plug_between_nodes(plug, target_node, current_depth=0):
    if current_depth > RECURSION_DEPTH_LIMIT:
        lprint(u"递归深度超过限制，终止操作")
        return
    # 检查插槽是否已连接
    if plug.isConnected:
        # 打印目标连接
        dest_plugs = plug.destinations()
        if dest_plugs:
            for dest_plug in dest_plugs:
                if dest_plug.node() == target_node:
                    s=get_plug_full_name(plug)
                    t=get_plug_full_name(dest_plug)
                    lprint(u"断开链接{} -> {} ->{}".format(s, t,dest_plug))
                    try:
                        cmds.disconnectAttr(s,t)
                    except Exception as e:
                        lprint(e)


        # 打印源连接
        source_plug = plug.source()
        if not source_plug.isNull and source_plug.node() == target_node :
            # 断开连接
            try:
                s=get_plug_full_name(source_plug)
                t=get_plug_full_name(plug)
                lprint(u"断开链接{} -> {}".format(s, t))
                lprint(type(s))
                cmds.disconnectAttr(s,t)
            except Exception as e:
                lprint(e)
    # 递归处理数组元素
    if plug.isArray:
        try:
            num_elements = plug.evaluateNumElements()  # 使用 evaluateNumElements 代替 numElements()
            lprint(u"数组属性 {} 的元素数量: {}".format(plug.name(), num_elements))
        except Exception as e:
            lprint(u"获取 {}.numElements 时发生错误: {}".format(plug.name(), e))
        for i in range(num_elements):
            element_plug = plug.elementByLogicalIndex(i)  # 使用 elementByLogicalIndex() 代替 elementByPhysicalIndex()
            disconnect_plug_between_nodes(element_plug, target_node, current_depth + 1)

    # 递归处理复合子属性
    if plug.isCompound:
        
        num_children = plug.numChildren()
        # lprint(u"复合属性 {} 的子属性数量: {}".format(plug.name(), num_children))
        for i in range(num_children):
            child_plug = plug.child(i)
            disconnect_plug_between_nodes(child_plug, target_node, current_depth + 1)

# 主函数，区分处理 instObjGroups 和其他属性
def disconnect_attributes_between_nodes(source_node_name, target_node_name, current_depth=0):
    # 创建选择列表并添加目标节点
    sel_list = om.MSelectionList()
    try:
        sel_list.add(target_node_name)
    except Exception as e:
        lprint(u"目标节点 {} 不存在，错误: {}".format(target_node_name, e))
        return

    # 获取目标节点的 MObject
    target_node = sel_list.getDependNode(0)

    # 首先处理 instObjGroups 属性
    disconnect_instObjGroups_attributes(source_node_name, target_node, current_depth)


def disSg_NonAssignFace(trNodeList,*args):
    shNodeList=L_GV.converyToShNode(trNodeList)
    sgNodeList=cmds.listConnections(shNodeList,type='shadingEngine')
    process=L_GV.Process(proList=sgNodeList)
    if not sgNodeList: 
        lprint(shNodeList,u"这几个物体没有材质")
        return
    for sg in sgNodeList:
        process.pro()
        _trNodeList=cmds.listConnections(sg,type='mesh')
        # lprint(_trNodeList)
        faceSetList=cmds.sets(sg,q=1,)
        if not _trNodeList: continue
        for trNode in _trNodeList:
            shNodeList=cmds.listRelatives(trNode,s=1,fullPath=1)
            for shNode in shNodeList:
                if L_GV.is_intermediate_shape(shNode):
                    continue
                if not faceSetList:
                    # lprint(shNode,sg)
                    disconnect_attributes_between_nodes(shNode,sg)
                    continue
                FaceSetList=L_GV.getSplecifyShapeNodeFaceSetNodeFromFaceSet(faceSetList=faceSetList,filterObj=[trNode])
                # lprint(FaceSetList)
                if not FaceSetList:
                    disconnect_attributes_between_nodes(shNode,sg)
    process.end()
    
if __name__ == "__main__":
    source_node_name = 'C_XiaoChan_Mod_Cloth03_GeoShape'
    target_node_name = 'C_XiaoChan_Cloth03_1_Inst'
    disconnect_attributes_between_nodes(source_node_name, target_node_name)
