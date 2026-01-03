import os
import re
maya.mel.eval('python("import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm")')


Type, Node, Children = "Type", "Node", "Children"
Material, Textures, ShadingEngine, Utility = "Material", "Textures", "ShadingEngine", "Utility"


def inputs(node, nodes, data, shader=None):
    if node not in nodes:
        return
    doc = dict(
        Node=node,
        Children=[],
    )
    _data = data
    if node.type() == "shadingEngine":
        doc[Type] = ShadingEngine
        shader = doc[Children]
        _data = doc[Children]
    elif node.type()in pm.listNodeTypes("shader"):
        doc[Type] = Material
        _data = doc[Children]
    elif node.type() in ["file", "RedshiftNormalMap"]:
        doc[Type] = Textures
    else:
        doc[Type] = Utility
    for i in node.inputs():
        inputs(i, nodes, _data, shader)
    if doc[Type] == Material:
        shader.append(doc)
    else:
        data.append(doc)
    nodes.remove(node)


def get_data():
    shader_types = [typ for node_type in ["texture", "utility", "imageplane", "shader"]
                    for typ in pm.listNodeTypes(node_type)]
    shader_types.extend(["shadingEngine", "groupId"])
    nodes = set(pm.ls(type=shader_types, l=1))
    nodes.update(set(pm.lsThroughFilter("DefaultMrNodesFilter")))
    sgs = list(set(sg for mesh in pm.ls(type="mesh") for sg in mesh.shadingGroups()
                   if sg.name().split(":")[-1] not in ["initialParticleSE", "initialShadingGroup"]))
    data = []
    for sg in sgs:
        inputs(sg, nodes, data)
    return data


def get_tex_path(node):
    path = ""
    if node.type() == "file":
        if node.fileTextureName.get():
            path = node.fileTextureName.get().replace("\\", "/")
    elif node.type() == "RedshiftNormalMap":
        if node.tex0.get():
            path = node.tex0.get().replace("\\", "/")
    if path[0] == "$":
        env = path.split("/")[0]
        if env[1:] in os.environ:
            path = path.replace(env, os.environ[env[1:]]).replace("\\", "/")
    return path


def set_tex_path(node, path):
    if node.type() == "file":
        return node.fileTextureName.set(path)
    elif node.type() == "RedshiftNormalMap":
        return node.tex0.set(path)


def get_tex_name(node):
    path = get_tex_path(node)
    name = path.split("/")[-1].split(".")[0]
    if name:
        return name
    return node.name()


def exit_tex(node):
    path = get_tex_path(node)
    if os.path.isfile(path):
        return True
    dir_name, basename = os.path.split(path)
    if not os.path.isdir(dir_name):
        return False
    ud = re.sub(ur"([0-9]{4}|<UDIM>|<udim>)", "<UDIM>", basename)
    for name in os.listdir(dir_name):
        if re.sub(ur"([0-9]{4}|<UDIM>|<udim>)", "<UDIM>", name) == ud:
            return True
    return False


def rename_tex(node, name):
    path = get_tex_path(node)
    dir_name, basename = os.path.split(path)
    ext = os.path.splitext(basename)[-1][1:]
    ud = re.sub(ur"([0-9]{4}|<UDIM>|<udim>)", "<UDIM>", basename)
    if "<UDIM>" in ud:
        nodes = [n for n in pm.ls(type=["file"]) + pm.ls("RedshiftNormalMap")
                 if ud == re.sub(ur"([0-9]{4}|<UDIM>|<udim>)", "<UDIM>", os.path.basename(get_tex_path(n)))]
        for _name in os.listdir(dir_name):
            if re.sub(ur"([0-9]{4}|<UDIM>|<udim>)", "<UDIM>", _name) == ud:
                src = os.path.join(dir_name, _name)
                f = re.findall(ur"([0-9]{4}|<UDIM>|<udim>)",  _name)[0]
                dst = "{dir_name}/{basename}.{f}.{ext}".format(dir_name=dir_name, basename=name, ext=ext, f=f)
                if os.path.isfile(src) and not os.path.isfile(dst):
                    os.rename(src, dst)
        for n in nodes:
            path = get_tex_path(n)
            _dir, _basename = os.path.split(path)
            print _basename
            f = re.findall(ur"([0-9]{4}|<UDIM>|<udim>)",  _basename)[0]
            dst = "{dir_name}/{basename}.{f}.{ext}".format(dir_name=_dir, basename=name, ext=ext, f=f)
            set_tex_path(n, dst)
    else:
        nodes = [n for n in pm.ls(type=["file"])+pm.ls("RedshiftNormalMap") if get_tex_path(n) == path]
        src = path
        dst = "{dir_name}/{basename}.{ext}".format(dir_name=dir_name, basename=name, ext=ext)
        if os.path.isfile(src) and not os.path.isfile(dst):
            os.rename(src, dst)
            for n in nodes:
                set_tex_path(n, dst)


def pack(pack_dir=r"E:\work\TD\textu\tex"):
    pack_dir = pack_dir.replace("\\", "/")
    for node in pm.ls(type=["file"])+pm.ls("RedshiftNormalMap"):
        if not exit_tex(node):
            continue
        path = get_tex_path(node)
        dir_name, expression = os.path.split(path)
        if expression.count(".") == 1:
            basename, ext = expression.split(".")
            mat = basename.split("_")[-2:][0]
            if os.path.isfile(path):
                src = "{dir_name}/{basename}.{ext}".format(dir_name=dir_name, basename=basename, ext=ext)
                dst = "{dir_name}/{mat}/{basename}.{ext}".format(dir_name=pack_dir, basename=basename, ext=ext, mat=mat)
                dst_dir = os.path.dirname(dst)
                if not os.path.isdir(dst_dir):
                    os.makedirs(dst_dir)
                if os.path.isfile(src) and not os.path.isfile(dst):
                    os.rename(src, dst)
                    set_tex_path(node, dst)
        elif expression.count(".") == 2:
            basename, sequence, ext = expression.split(".")
            mat = basename.split("_")[-2:][0]
            for n in os.listdir(dir_name):
                math = re.match("{basename}\.([\d]+)\.{ext}".format(basename=basename, ext=ext), n)
                if math:
                    i = math.group(1)
                    src = "{dir_name}/{basename}.{i}.{ext}".format(dir_name=dir_name, i=i, basename=basename, ext=ext)
                    dst = "{dir_name}/{mat}/{basename}.{i}.{ext}".format(
                        dir_name=pack_dir, i=i, basename=basename, ext=ext, mat=mat)
                    dst_dir = os.path.dirname(dst)
                    if not os.path.isdir(dst_dir):
                        os.makedirs(dst_dir)
                    if os.path.isfile(src) and not os.path.isfile(dst):
                        os.rename(src, dst)
            set_tex_path(node, "{dir_name}/{mat}/{basename}.{sequence}.{ext}".format(
                dir_name=dir_name, sequence=sequence, basename=basename, ext=ext, mat=mat))