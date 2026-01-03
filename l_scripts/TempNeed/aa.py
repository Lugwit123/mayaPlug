def getSGs(obj):
    try:
        obj=cmds.listRelatives(obj,s=1,f=1)
    except:
        pass
    shader=cmds.listConnections(obj,type='shadingEngine')
    return list(set(shader))
  #shader=listConnections(shader)
  #mat=list(set(ls(shader,mat=1)))
faceObjList=[]
for sel in cmds.ls(sl=1,l=1):
    sgs=getSGs(sel)
    print sel
    if len(sgs)>1:
        faceObjList.append(sel)
cmds.select(faceObjList)