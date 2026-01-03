import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm

data = dict(
    specularRoughness=dict(alphaIsLuminance=1, colorSpace="Raw"),
    baseColor=dict(alphaIsLuminance=0, colorSpace="sRGB"),
    metalness=dict(alphaIsLuminance=1, colorSpace="Raw"),
    bumpValue=dict(alphaIsLuminance=1, colorSpace="Raw"),
    opacity=dict(alphaIsLuminance=1, colorSpace="Raw"),
    displacementShader=dict(alphaIsLuminance=1, colorSpace="Raw"),

)


def output_attr_name(node):
    for n in ["outColor", "outAlpha"]:
        for attr in node.attr(n).outputs(p=1):
            return attr.name().split(".")[-1]


def tex_file():
    for node in pm.ls(type="file"):
        name = output_attr_name(node)
        if name is None:
            continue
        if name not in data:
            continue
        for attr, value in data[name].items():
            if not node.hasAttr(attr):
                continue
            node.attr(attr).set(value)
