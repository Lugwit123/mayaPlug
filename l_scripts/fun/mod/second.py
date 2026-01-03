import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm


class SelectError(Exception):
    pass


def set_controller_reverse(i=0):
    for select in pm.selected(type="transform"):
        for mul in select.getParent().t.inputs():
            mul.input2.set(i, i, i)


def make_follicle(geometry=None, name="follicle", u=0, v=0):
    if geometry is None:
        geometry = pm.selected()[0]
    follicle = pm.createNode("transform", n=name)
    pm.createNode("follicle", n=name+"Shape", p=follicle)
    follicle.parameterU.set(u)
    follicle.parameterV.set(v)
    follicle.inheritsTransform.set(False)
    if geometry.getShape().type() == "mesh":
        geometry.outMesh.connect(follicle.inputMesh)
    else:
        geometry.local.connect(follicle.inputSurface)
    geometry.worldMatrix.connect(follicle.inputWorldMatrix)
    follicle.outRotate.connect(follicle.rotate)
    follicle.outTranslate.connect(follicle.translate)
    follicle.getShape().v.set(0)
    return follicle


def get_polygon_transforms():
    selected = pm.selected()
    if len(selected) > 1:
        if selected[0].getShape() and selected[0].getShape().type() == "mesh":
            return selected[0], selected[1:]
    raise SelectError("You must select transforms and polygon")


def polygon_point_connect():
    polygon, transforms = get_polygon_transforms()
    mesh = polygon.getShape()
    for transform in transforms:
        point = transform.getTranslation(space="world")
        _, face_id = mesh.getClosestPoint(point, space="world")
        face = mesh.f[face_id]
        length_map = {(mesh.vtx[vId].getPosition(space="world") - point).length(): mesh.vtx[vId] for vId in
                      face.getVertices()}
        vtx = length_map[min(length_map.keys())]
        id_uv = {i:(u, v) for u, v, i in zip(*vtx.getUVs())}
        u, v = id_uv.get(face_id, id_uv.values()[0])
        follicle = make_follicle(polygon, transform.name()+"PNC", u, v)
        pnc = pm.pointConstraint(follicle, transform, n=transform.name()+"PFC", mo=True)
        follicle.getShape().setParent(pnc, s=1, add=1)
        for attr in follicle.connections(p=1):
            attr.disconnect()
        pm.delete(follicle)
        pnc.outTranslate.connect(pnc.target[0].targetTranslate, f=1)