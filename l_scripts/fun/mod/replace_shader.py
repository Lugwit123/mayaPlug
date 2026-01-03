import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm


def is_polygon(polygon):
    if polygon.type() != "transform":
        return False
    shape = polygon.getShape()
    if not shape:
        return False
    if shape.type() != "mesh":
        return False
    return True


def name_polygon(group):
    data = {}
    polygons = group.listRelatives(ad=1, type="transform")
    polygons.insert(0, group)
    length = len(group.fullPath()) + 1
    for polygon in polygons:
        name = "|" + polygon.fullPath()[length:]
        if not is_polygon(polygon):
            continue
        data[name] = polygon
    return data


def map_polygon(src, dst):
    src_data = name_polygon(src)
    dst_data = name_polygon(dst)
    data = []
    for name, src_polygon in src_data.items():
        if name in dst_data:
            data.append([src_polygon, dst_data[name]])
    return data


def map_hair(src, dst):
    src_data = name_hair(src)
    dst_data = name_hair(dst)
    data = []
    for name, src_hair in src_data.items():
        if name in dst_data:
            data.append([src_hair, dst_data[name]])
    return data


def name_hair(group=None):
    if group is None:
        group = pm.selected(type="transform")[0]
    hairs = [hair.getParent() for hair in group.listRelatives(ad=1, type="hairSystem")]
    length = len(group.fullPath()) + 1
    data = {}
    for hair in hairs:
        name = "|" + hair.fullPath()[length:]
        data[name] = hair
    return data


def replace_hair_shader():
    selected = pm.selected(o=1)
    if not selected:
        return pm.warning("\n you should select tow group")
    if len(selected) != 2:
        return pm.warning("\n you should select tow group")
    src, dst = selected
    shader_types = pm.listNodeTypes("shader")
    for src_hair, dst_hair in map_hair(src, dst):
        for in_attr, out_attr in src_hair.getShape().inputs(p=1, c=1):
            if out_attr.node().type() not in shader_types:
                continue
            out_attr.connect(dst_hair.attr(in_attr.name().split(".")[-1]), f=1)
            dst_hair.aiOverrideHair.set(1)
            print out_attr, in_attr


def replace_shader():
    replace_hair_shader()
    selected = pm.selected(o=1)
    if not selected:
        return pm.warning("\n you should select tow group")
    if len(selected) != 2:
        return pm.warning("\n you should select tow group")
    src, dst = selected
    for origin, target in map_polygon(src, dst):
        data = {}
        for sg in origin.shadingGroups():
            ids = []
            for e in sg.elements():
                if not isinstance(e, pm.general.MeshFace):
                    continue
                if e.node() != origin.getShape():
                    continue
                for f in e:
                    ids.append(f.index())
            data[sg] = ids
        for sg, ids in data.items():
            if not ids:
                pm.sets(sg, e=1, forceElement=target)
            else:
                mesh = target.getShape()
                for i in ids:
                    pm.sets(sg, e=1, forceElement=mesh.f[i])

