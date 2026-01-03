# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import Lugwit_Module.l_src.usualFunc as us
reload (us)
import re
import math

lprint = us.lprint
lprint.trace_depth=1

def get_edge_number_from_str(s): 
    number = re.search(r'\[\d+\]', s)
    return re.search(r'\d+', s).group() or False

def get_edges_by_vtx(vtx):
    return cmds.ls(cmds.polyListComponentConversion(vtx,te=1),fl=1)

def get_vtxs_by_edge(edge):
    return cmds.ls(cmds.polyListComponentConversion(edge,tv=1),fl=1)

def get_faces_by_vtx(vtx):
    return cmds.ls(cmds.polyListComponentConversion(vtx,tf=1),fl=1)
def get_bound_edges(obj):
    cmds.select(obj)
    cmds.polySelectConstraint(m=3, t=0x8000, w=1)
    # 获取选择的边界边
    borderEdges = cmds.ls(sl=True, fl=True)
    # 禁用选择约束
    cmds.polySelectConstraint(dis=True)
    return borderEdges

def get_connected_edges(obj,edge ,bound_edges,result_edges):
    vtxs = get_vtxs_by_edge(edge)
    lprint(vtxs)
    if is_pole_vertex(vtxs[0]) and is_pole_vertex(vtxs[1]) :
        lprint(u"{}关联的顶点都是角点".format(edge))
        return []
    lprint(u"不是尖点,处理{}\n{}".format(edge,vtxs))
    for vtx in vtxs:
        edges = get_edges_by_vtx(vtx)
        for _edge in edges:
            if _edge in result_edges:
                lprint(_edge,"已处理")
                continue
            if _edge not in bound_edges:
                lprint(u"{}不是边界边,跳过".format(_edge))
                continue
            if len(edges)>2:
                lprint(_edge,bound_edges)
                result_edges.append(_edge)
                get_connected_edges(obj,_edge ,bound_edges,result_edges)

def get_edge_loops():
    """
    获取选中网格的所有边循环，在尖点处断开
    返回边循环列表
    兼容 Python 2.7
    """
    # 获取选中的对象
    selection = cmds.ls(sl=True)
    
    if not selection:
        print(u"请选择一个网格对象")
        return []
    
    # 存储结果的列表
    all_edge_loops = [] # 嵌套列表
    
    
    # 对每个选中的对象
    len_obj=len(selection)
    print(len(selection))
    for i,obj in enumerate(selection):
        processed_edges = []
        lprint(u"正在处理第{0}/{1}个对象".format(i+1,len_obj))
        # 创建网格函数集
        selection_list = om.MSelectionList()
        selection_list.add(obj)
        dag_path = om.MDagPath()
        selection_list.getDagPath(0, dag_path)
        
        # 获取所有的边
        edges = cmds.ls(obj + ".e[*]", fl=True)
        bound_edges=get_bound_edges(obj)
        lprint(bound_edges)
        # 遍历所有边
        for i,edge in enumerate(edges):
            # if i!=1:
            #     continue
            lprint('>>>>>>>>>>>>>>>>>>>',edge)
            # 如果边已经处理过，跳过
            # 获取相邻的边
            if edge in processed_edges:
                continue
            if edge not in bound_edges:
                continue
            result_edges=[edge]
            get_connected_edges(obj,edge,bound_edges,result_edges)
            processed_edges.extend(result_edges)
            all_edge_loops.append(result_edges)
            if len(result_edges)>1:
                try:
                    lprint(u"{}边的循环边为{}".format(edge,result_edges),popui=True)
                    cmds.polyToCurve(result_edges)
                except:
                    pass
            

    lprint(u"找到 {0} 条边循环".format(len(all_edge_loops)))
    return all_edge_loops

def get_numeric_values(poly_info_result):
    """
    从polyInfo结果中提取数字值
    """
    if not poly_info_result or not isinstance(poly_info_result, list):
        return []
    result = []
    parts = poly_info_result[0].split(":")
    if len(parts) < 2:
        return []
    for part in parts[1].strip().split():
        try:
            num = int(part)
            result.append(num)
        except ValueError:
            continue
    return result

def get_angle_between_vectors(vec1, vec2):
  """计算两个向量的夹角（弧度）"""
  dot_product = sum(x * y for x, y in zip(vec1, vec2))
  magnitude1 = math.sqrt(sum(x ** 2 for x in vec1))
  magnitude2 = math.sqrt(sum(x ** 2 for x in vec2))
  cos_theta = dot_product / (magnitude1 * magnitude2)
  return math.degrees(math.acos(cos_theta))

def get_edge_vertices(edge):
  """获取边的两个顶点坐标"""
  obj = edge.split(".")[0]
  vertices = cmds.polyInfo(edge, ev=True)[0].split()
  v1 = cmds.xform(obj+".vtx["+str(vertices[2])+"]", q=True, ws=True, t=True)
  v2 = cmds.xform(obj+".vtx["+str(vertices[3])+"]", q=True, ws=True, t=True)
  return v1, v2

def get_edge_vector(v1, v2):
  """计算边的向量"""
  return (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
def get_angle_between_edges(edge1, edge2):
  """计算两条边的夹角（弧度）"""
  v1_1, v1_2 = get_edge_vertices(edge1)
  v2_1, v2_2 = get_edge_vertices(edge2)
  vec1 = get_edge_vector(v1_1, v1_2)
  vec2 = get_edge_vector(v2_1, v2_2)
  return get_angle_between_vectors(vec1, vec2)



    
    
def is_pole_vertex(vertex):
    connected_faces = get_faces_by_vtx(vertex)
    return len(connected_faces)==1


def edges_share_face(obj, edge1, edge2):
    """
    检查两条边是否共享一个面
    """
    # 获取边1的面
    edge1_faces = cmds.polyInfo(obj + ".e[" + str(edge1) + "]", ef=True)
    edge1_faces = get_numeric_values(edge1_faces)
    
    # 获取边2的面
    edge2_faces = cmds.polyInfo(obj + ".e[" + str(edge2) + "]", ef=True)
    edge2_faces = get_numeric_values(edge2_faces)
    
    # 检查是否有共享的面
    return bool(set(edge1_faces) & set(edge2_faces))

def select_all_edge_loops():
    """
    在Maya中选择所有边循环
    """
    edge_loops = get_edge_loops()
    lprint(u"一共{}对循环边".format(len(edge_loops)))
    if edge_loops:
        # 扁平化列表的列表
        all_edges = []
        for loop in edge_loops:
            all_edges.extend(loop)
        
        cmds.select(all_edges)
        print(u"已选择所有边循环，共 {0} 条边".format(len(all_edges)))
    else:
        print(u"未找到边循环")

def select_edge_loop_by_index(index=0):
    """
    根据索引选择特定的边循环
    """
    edge_loops = get_edge_loops()
    
    if not edge_loops:
        print(u"未找到边循环")
        return
    
    if index < 0 or index >= len(edge_loops):
        print(u"索引超出范围：0-{0}".format(len(edge_loops) - 1))
        return
    
    # cmds.select(edge_loops[index])
    print(u"已选择边循环 {0}，包含 {1} 条边".format(index, len(edge_loops[index])))

# 使用示例
if __name__ == "__main__":
    select_all_edge_loops()