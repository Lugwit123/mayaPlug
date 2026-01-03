import sys,os,re
import GV
reload (GV)
import maya.cmds as cmds
import Lugwit_Module as LM
reload (LM)
lprint = LM.lprint

@LM.try_exp
def check_material_assigned_to_object(obj):
    LM.lprint (obj)
    shapeNodeList=cmds.listRelatives(obj,s=1)
    lprint (shapeNodeList)
    for shapeNode in shapeNodeList:
        shading_engineList = cmds.listConnections(shapeNode, type='shadingEngine')
        shading_engineList=list(set(shading_engineList))
        if len(shading_engineList)>1:
            lprint (shading_engineList)
            for sgNode in shading_engineList:
                con = cmds.listConnections(sgNode+'.memberWireframeColor ',sh=1)
                lprint (con,sgNode)
                for i in range(10):
                    dagSetMembers=cmds.listConnections(sgNode+'.dagSetMembers{}'.format(i),sh=1,p=1)[0]
                    if dagSetMembers:
                        lprint (dagSetMembers)
                        if not con:
                            cmds.disconnectAttr(dagSetMembers,sgNode+'.dagSetMembers{}'.format(i))
                        elif  shapeNode not  in con[0]:
                            cmds.disconnectAttr(dagSetMembers,sgNode+'.dagSetMembers{}'.format(i))

                    

def process(*args):
    # 获取选定的物体
    gv_pro=GV.Process()
    gv_pro.proList=GV.allOrSel(tr=1)
    gv_pro.start()
    # 对每个选定的物体执行 check_material_assigned_to
    for selected_object  in gv_pro.proList:
        check_material_assigned_to_object(selected_object)
        gv_pro.pro()
    gv_pro.end()

if __name__=='__main__':    
    process()