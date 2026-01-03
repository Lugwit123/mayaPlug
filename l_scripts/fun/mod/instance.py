import re
import os
import sys

import json

try:
    import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm
except ImportError:
    pm = None


def mel_to_json(path=r"E:/work/scene/description34.mel"):
    with open(path, "r") as ft:
        data = [[float(s) for s in match[0][1:].split(" ")]
                for match in re.findall("(( [.0123456789+-e]+){16})", ft.read())]
    with open(path[:-3]+"json", "w") as ft:
        json.dump(data, ft, indent=4)


def load_json_to_transform(path=r"E:/work/scene/description34.json"):
    with open(path, "r") as ft:
        data = json.load(ft)
    group = pm.group(em=1, n="glassGroup")
    for m in data:
        glass = pm.group(em=1, p=group, n="glass")
        pm.parent("|glass|glassShape", glass, s=1, add=1)
        pm.xform(glass, m=m)


def asset_path_matrix(json_path=r"E:/work/scene/tree.json"):
    path_matrix = {}
    for ass in pm.ls(type="aiStandIn"):
        path = ass.dso.get().replace("\\", "/")
        matrix = pm.xform(ass.getParent(), q=1, m=1, ws=1)
        print matrix
        path_matrix.setdefault(path, []).append(matrix)
    dir_name = os.path.dirname(json_path)

    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    with open(json_path, "w") as fp:
        json.dump(path_matrix, fp, indent=4)


def import_ass(ass_path):
    name = os.path.basename(ass_path).replace(".", "_")
    ass = pm.group(em=1, n=name)
    shape = pm.createNode('aiStandIn', p=ass, n=name + "AssShape")
    shape.dso.set(ass_path)
    if not pm.objExists('ArnoldStandInDefaultLightSet'):
        pm.createNode("objectSet", name=":ArnoldStandInDefaultLightSet", shared=True)
        pm.lightlink(object='ArnoldStandInDefaultLightSet', light='defaultLightSet')
    pm.mel.sets(ass, add='ArnoldStandInDefaultLightSet')
    return ass


def ass_to_abc(ass_path="E:/work/scene/tree_008_root.ass"):
    ass = import_ass(ass_path)
    pm.select(ass)
    base_path = os.path.splitext(ass_path)[0]
    pm.arnoldBakeGeo(f=base_path+".obj")


def all_ass_to_abc(dir_path="X:/Project/2018/C14/Asset_work/sets/YSXA/Texture/work/ass"):
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            _, ext = os.path.splitext(file_name)
            if not ext == ".ass":
                continue
            ass_path = os.path.join(root, file_name).replace("\\", "/")
            ass_to_abc(ass_path)


def load_roots(dir_path="X:/Project/2018/C14/Asset_work/sets/YSXA/Texture/work/ass"):
    data_json = dir_path + "/data.json"
    with open(data_json, "r") as fp:
        data = json.load(fp)

    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            base_name, ext = os.path.splitext(file_name)
            if not ext == ".ass":
                continue
            if not any(["root" in file_name, "stick" in file_name]):
                continue
            ass_path = os.path.join(root, file_name).replace("\\", "/")
            if ass_path not in data:
                continue
            obj_path = ass_path[:-3]+"obj"
            pm.mel.file(obj_path, type="OBJ", ignoreVersion=True, i=True)
            mesh = pm.PyNode("Mesh")
            mesh.rename(base_name)
            for m in data[ass_path]:
                instance = pm.instance(mesh)[0]
                pm.xform(instance, ws=1, m=m)
            pm.delete(mesh)
if __name__ == '__main__':
    load_roots()
