#!/usr/bin/python
# -*- coding: utf-8 -*-

import maya.cmds as mc
import maya.OpenMaya as om
import re,sys
"""
#python command
import aiToonWidth;reload(aiToonWidth)
aiToonWidth.doIt()
"""
def doIt():
    allAiToon = mc.ls(type="aiToon")
    #Add every aiToon attributes
    infos = {"Width":["edgeWidthScale",0,1,10,"R","X"],
            "Angle":["angleThreshold",0,180,500,"G","Y"]}
    #break old connect in
    for sder in allAiToon:
        for key in infos:
            dvnAtr,min,max,dval,rgb,xyz = infos[key]
            atrname = "%s.%s"%( sder,dvnAtr )
            plug = mc.listConnections(atrname,s=True,d=False,p=True)
            if plug!=None:
                mc.disconnectAttr(plug[0],atrname)
    #get exists ctrl for parent
    p2Ctrls = ["Visibility_ctrl","FKHead_M"]
    if not mc.objExists(p2Ctrls[0]) and not mc.objExists(p2Ctrls[1]):
        om.MGlobal.displayError( "Can not find ctrl <%s> or <%s>"%(p2Ctrls[0],p2Ctrls[1]) )
        return None
    pTo =  p2Ctrls[0] if mc.objExists(p2Ctrls[0]) else p2Ctrls[1]
    xmin, ymin, zmin, xmax, ymax, zmax = mc.exactWorldBoundingBox(pTo)
    #crete aitoon ctrl
    postion = [ [-1.11, 0.01, 0.0], [0.0, 1.11, 0.0], [-0.01, -1.11, 0.0], [-1.11, 0.0, 0.0], 
                [1.11, -0.01, 0.0], [-0.0, -1.11, 0.0], [0.01, 1.11, 0.0], [1.11, -0.0, 0.0] ]
    #ctrl size
    s_ = (xmax-xmin)/30.0*2
    for idx,als in enumerate( postion ):
        postion[idx][0] *= s_
        postion[idx][1] *= s_
    ctrl = "aiToon_ctrl"
    if mc.objExists(ctrl):
        mc.delete(ctrl)
    cv = mc.curve(d=3,p=postion)
    ctrl = mc.rename(cv,ctrl)
    mc.xform(ctrl,ws=True,t=[xmax+2*s_,ymax,zmin] )
    mc.color(ud=8)
    for atr in mc.listAttr(ctrl,k=True):
        mc.setAttr( "%s.%s"%(ctrl,atr),k=False )
    #Add global ctrl attbibutes
    mc.addAttr(ctrl,ln="_",at="enum",en="--Global--",k=True)
    mc.setAttr("%s._"%ctrl,lock=True)
    mc.addAttr(ctrl,ln="globalWidthX",at="double",k=True,min=0,max=10,dv=1)
    mc.addAttr(ctrl,ln="globalAngleX",at="double",k=True,min=0,max=10,dv=1)
    mc.addAttr(ctrl,ln="__",at="enum",en="--------------",k=True)
    mc.setAttr("%s.__"%ctrl,lock=True)
    mc.parent(ctrl,pTo)    
    
    for sder in allAiToon:
        norlName = sder
        if ":" in sder:
            namSplit = re.split(":",sder)
            norlName = namSplit[-1]
        clmp = mc.createNode( "clamp",name="%s_clmp"%norlName )
        xmd = mc.createNode( "multiplyDivide",name="%s_md"%norlName )
        mc.connectAttr( ".outputX","%s.inputR"%clmp )
        mc.connectAttr( ".outputY","%s.inputG"%clmp )
        for key in infos:
            dvnAtr,min,max,dval,rgb,xyz = infos[key]
            mc.setAttr("%s.min%s"%(clmp,rgb),min )
            mc.setAttr("%s.max%s"%(clmp,rgb),max )
            #print dvnAtr,min,max,dval
            atrname = "%s.%s"%( sder,dvnAtr )
            ctVal = mc.getAttr( atrname )      
            mc.addAttr(ctrl,ln=norlName+key,at="double",k=True,dv=ctVal,min=min,max=max)
            driver = "%s.%s%s"%(ctrl,norlName,key)
            #Drive by global 
            mc.connectAttr("%s.global%sX"%(ctrl,key),"%s.input1%s"%(xmd,xyz) ,f=True)
            #Drive by component
            mc.setDrivenKeyframe("%s.input2%s"%(xmd,xyz) ,cd=driver,dv=-1*dval,v=-1*dval,ott="linear",itt="linear")
            mc.setDrivenKeyframe("%s.input2%s"%(xmd,xyz) ,cd=driver,dv=+1*dval,v=+1*dval,ott="linear",itt="linear")
            #clamp --> edgeWidthScale / angleThreshold
            mc.connectAttr("%s.output%s"%(clmp,rgb),atrname,f=True)
    mc.select(ctrl)
            