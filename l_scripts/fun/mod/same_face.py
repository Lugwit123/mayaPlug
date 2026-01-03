from maya import cmds


def same_face():
    point_mesh = {}
    for mesh in cmds.ls(type="mesh", l=1):
        if cmds.getAttr(mesh + ".io"):
            continue
        point = tuple(int(p*10000) for p in cmds.xform(mesh+".vtx[*]", q=1, t=1, ws=1))
        point_mesh.setdefault(point, []).append(mesh)
    cmds.select(sum([mesh for mesh in point_mesh.values() if len(mesh) > 1], []))
    cmds.pickWalk(d="up")
