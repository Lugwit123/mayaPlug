import pymel.core as py
 
sl = py.ls(selection=1)
cv = sl[0]
bone = py.listRelatives(sl[1],allDescendents=True)
bone.append(sl[1])
bone.reverse()
 
py.rebuildCurve(cv,constructionHistory=True,replaceOriginal=True,
                rebuildType=0,endKnots=1,keepRange=0,keepControlPoints=True,
                keepEndPoints=True,keepTangents=False,spans=0,
                degree=3,tolerance=0)
for i in range(0,len(bone)):
    pos = py.pointOnCurve(cv,parameter=(i*(1.0/len(bone)*(len(bone)/(len(bone)-1.0)))),position=1)
    py.move(pos[0],pos[1],pos[2],bone[i])
py.joint(bone[0],edit=True,orientJoint='xyz',secondaryAxisOrient='yup',
            children=True,zeroScaleOrient=True)
py.setAttr(bone[len(bone)-1]+'.jointOrient',0,0,0,type='double3')