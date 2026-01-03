# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel
from materialPlug.scripts import autoTransferUV
from l_scripts.usualLib import usual
from l_scripts import L_GV
from usualLib import attr_connect
reload (L_GV)
reload (autoTransferUV)
import  Lugwit_Module as LM
lprint = LM.lprint
import time
from PySide2.QtWidgets import QMessageBox,QLabel
abc_namespace = "abc_sg"
import random
import colorsys


def selSameMatObjForZFS(getdefalut='btn',):
    print (u"选择相同材质球的物体")
    cmds.SelectHierarchy()
    
    selectObjList=cmds.ls(sl=1,l=1)
    selectObjList=cmds.ls(cmds.filterExpand(selectObjList,sm=12),l=1)
    selectObjList = list(set(selectObjList))
    if cmds.currentTime(q=1)!=50.0:
        cmds.currentTime(50)
    finallyObjList=[]
    if not selectObjList:
        result = cmds.confirmDialog(
                            title=u'确认操作',
                            message=u'请选择解算之后的物体在执行此操作？',
                            button=[u'好的'],
                        )
        return
    lprint (selectObjList)
    len_obj=len(selectObjList)
    sametopoList=[]
    if len_obj>15:
        result = cmds.confirmDialog(
                            title=u'确认操作',
                            message=u'你选择的物体大于15,请确认你选择的解算物体是对的,一共有{}个？'.format(len_obj),
                            button=[u'请继续',u'取消'],
                            defaultButton=u'请继续',
                        )
        if result==u'取消':
            return
    
    process=L_GV.Process(proList=selectObjList)
    for obj in selectObjList:
        process.pro()
        sameMatObjList=convertyToOriginalSgAndGetSameMatObjList(obj)
        sameMatObjList = cmds.ls(sameMatObjList, objectsOnly=True)
        sameMatObjList=cmds.ls(cmds.filterExpand(sameMatObjList,sm=12),l=1)
        lprint ('sameMatObjList',sameMatObjList)
        sameMatObjList_stripNameSpace=[x.split(':')[-1] for x in sameMatObjList if ':Geometry' in x]
        sameMatObjList_stripNameSpace=list(set(sameMatObjList_stripNameSpace))
        lprint("sameMatObjList_stripNameSpace->",sameMatObjList_stripNameSpace)
        if not sameMatObjList:
            continue
        for sameMatObj in sameMatObjList:
            # if obj.split(':')[-1] in sameMatObjList_stripNameSpace:
            #     continue
            if 'simNUL' in sameMatObj:
                continue
            if 'cfx|' in sameMatObj.lower():
                continue
            if obj.split('|')[-1] == sameMatObj.split('|')[-1]:#高模中对应的物体不要包括进来
                continue
            lprint("check sameMatObj->",obj,sameMatObj)
            sourceFaceNum=cmds.polyEvaluate(obj,f=1)
            sourceVtxNum=cmds.polyEvaluate(obj,v=1)
            targetFaceNum=cmds.polyEvaluate(obj,f=1)
            targetVtxNum=cmds.polyEvaluate(obj,v=1)
            st=time.time()
            isSameObj=autoTransferUV.sameObj(sourceObj=obj,
                                targetObj=sameMatObj,
                                dirConstraint=False,
                                volumeConstraint=False,
                                sameObjSampleNum=1,
                                dirThreshold=0.002,
                                volumeThreshold=0.01,
                                useJsonFile=False,
                                preferUseNameMatch=True,
                                targetFaceNum=targetFaceNum,
                                targetVtxNum=targetVtxNum,
                                sourceFaceNum=sourceFaceNum,
                                sourceVtxNum=sourceVtxNum,)
            if not isSameObj:
                lprint (sameMatObj,obj)
                finallyObjList.append(sameMatObj)
            else :
                sametopoList.append(sameMatObj)
    lprint(sametopoList)
    finallyObjList=set(finallyObjList)-set(sametopoList)
    process.end()
    result_obj = list(finallyObjList)+selectObjList
    ok = cmds.confirmDialog(
                            title=u'确认操作',
                            message=u'是否要转换为分面材质球？'.format(len_obj),
                            button=[u'好的',u'不用了,谢谢'],
                            defaultButton=u'好的',
                        )
    if ok == u'好的':
        usual.cvtFaceSetSG(result_obj)
    cmds.select(result_obj)
    return result_obj

def convertyToOriginalSgAndGetSameMatObjList(obj,*args):
    shNode=cmds.listRelatives(obj,s=1,f=1)
    sgNode=cmds.listConnections(shNode,type='shadingEngine')[0]
    connected_objs=[]
    SameMatObj=L_GV.getSameMatObj(obj)
    if sgNode.startswith(abc_namespace):
        mat = cmds.listConnections(sgNode + ".surfaceShader")[0]
        orginalMat=mat.replace('_dup_mat','')
        orginalSg=cmds.listConnections(orginalMat,type='shadingEngine')[0]
        connected_objs = cmds.listConnections(orginalSg+ ".dagSetMembers", source=True)+SameMatObj
        lprint(orginalSg,connected_objs)
    else:
        connected_objs=SameMatObj
    return connected_objs


def nameSgFromMat(selList,del_unused_node,*args):
    # 获取选择的对象列表
    lprint(locals())
    if not selList:
        selList = cmds.ls(sl=True,l=1)
    # 检查并创建命名空间
    if not cmds.namespace(exists=abc_namespace):
        cmds.namespace(add=abc_namespace)
    if del_unused_node:
        mel.eval('MLdeleteUnused;')
    convertList=[]
    process=L_GV.Process(proList=selList)
    newMat='newMat'
    attr_connect.disSg_NonAssignFace(selList)
    for sel in selList:
        # 获取选定对象的材质列表
        matList = L_GV.getMats(sel)
        sgNodes = []
        for mat in matList:
            process.pro()
            # 获取连接到材质的shadingEngine节点
            sgNodes = cmds.listConnections(mat, type='shadingEngine')
            if not sgNodes:
                continue
            for sgNode in sgNodes:

                FaceSetList=cmds.sets(sgNode, q = 1)
                # lprint(sgNode,FaceSetList)
                if not FaceSetList:
                    continue
                FaceSetList=L_GV.getSplecifyShapeNodeFaceSetNodeFromFaceSet\
                        (FaceSetList,filterObj=[sel])
                newSgName = "{}:{}".format(abc_namespace, mat.split(':')[-1]).replace("_dup_mat","")
                if newSgName==sgNode:
                    cmds.sets(FaceSetList, edit=True, forceElement=newSgName)
                    continue

                # 检查并删除已经存在的节点
                newMat_dup_name = mat + "_dup_mat"
                # if cmds.objExists(newMat_dup_name):
                #     cmds.delete(newMat_dup_name)

                #print("newSgName",newSgName)# cmds.select(newSg)
                # 复制shadingEngine节点和上游节点
                if mat=='lambert1':
                    continue
                duplicated_nodes = cmds.duplicate(mat, upstreamNodes=True)
                #print("duplicated sg {} to {}".format(sg,duplicated_nodes))
                # 获取新复制的shadingEngine节点
                newMat = cmds.ls(duplicated_nodes,type=cmds.nodeType(mat))[0]
                shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="myShadingGroup")
                if not cmds.objExists(newMat_dup_name):
                    cmds.rename(newMat, newMat_dup_name)

                # 如果新的shadingEngine节点名字需要改变，进行重命名
                if shading_group != newSgName:
                    if not cmds.objExists(newSgName):
                        cmds.rename(shading_group, newSgName)
                else:
                    print(u"节点 {} 已经存在，跳过重命名。".format(newSgName))
                try:
                    cmds.connectAttr(newMat_dup_name+".outColor", newSgName+".surfaceShader",f=1)
                except Exception as e:
                    cmds.select(newMat_dup_name)
                    raise Exception(u"Failed to connect {}.outColor to {}.surfaceShader. Error: {}".format(newMat_dup_name,newSgName,e))

                cmds.sets(FaceSetList, edit=True, forceElement=newSgName)
        shiji_mat=L_GV.getSGs(sel)
        convertList.append((str(sgNodes),str(shiji_mat)))
    process.end()
    if convertList:
        convertList_str ='\n'.join([x+'  ->  '+y for x,y in convertList[:30]])
        convertList_str=convertList_str+"\nconvertList length {}...".format(len(convertList))
        if LM.isMayaPyEnv():
            lprint(convertList_str)
        else:
            msg_box = QMessageBox()
            msg_box.setText(convertList_str)
            msg_box.setWindowTitle("转换材质")
            # 通过查找QMessageBox的QLabel来设置其最小宽度
            label = msg_box.findChild(QLabel, "qt_msgbox_label")
            if label:
                label.setMinimumWidth(1200)  # 设置最小宽度
                #label.setMax h(1200)  # 设置最小宽度
            msg_box.exec_()

    usual.cvtFaceSetSG(selList) 

    attr_connect.disSg_NonAssignFace(selList)
    result_info_str=''
    for x in selList:
        result_info_str+='{}  -->>  {}\n'.format(x.split('|')[-1],L_GV.getSGs(x))
    if LM.isMayaPyEnv():
        lprint(result_info_str)  
    else:
        msg_box = QMessageBox()
        msg_box.setText(result_info_str)
        msg_box.setWindowTitle("转换材质")
        # 通过查找QMessageBox的QLabel来设置其最小宽度
        label = msg_box.findChild(QLabel, "qt_msgbox_label")
        if label:
            label.setMinimumWidth(1900)  # 设置最小宽度
        msg_box.exec_()  
        result = cmds.confirmDialog(
                                title=u'材质绿色错误显示',
                                message=u'场景中是否出现了绿色的无材质物体的状态',
                                button=[u'是的,刷新状态(耗时1-5s)',u'没有绿色,跳过刷新'],
                                defaultButton=u'没有绿色,跳过刷新',)
        print(result)
        if result==u'是的,刷新状态(耗时1-5s)':
            print(u"刷新状态")
            cmds.ogs( pause=True)
            cmds.ogs( pause=True)

def exAbc(*args):
    selSameMatObjForZFS()
    nameSgFromMat([])

def retoremSgAndMat(SGNodeList=[],*args):
    if not SGNodeList:
        SGNodeList = L_GV.getAllSGNodeList()
    process=L_GV.Process(proList=SGNodeList)
    for sg in SGNodeList:
        process.pro()
        connected_objs = cmds.listConnections(sg + ".dagSetMembers", source=True)
        sg_surfaceShader=cmds.listConnections(sg + ".surfaceShader")
        if not sg_surfaceShader:
            continue
        mat = sg_surfaceShader[0]
        orginalMat=mat.replace('_dup_mat','')
        orginalSg=cmds.listConnections(orginalMat,type='shadingEngine')[0]
        if connected_objs:
            for obj in connected_objs:
                try:
                    cmds.sets(obj, edit=True, forceElement=orginalSg)
                    print(u"成功将 {} 分配到 {}".format(obj,orginalSg))
                except Exception as e:
                    print(u"分配 {} 到 {} 时出现错误: {}".format(obj,orginalSg,e))
    process.end()

def renameSgNoe(*args):
    # 检查并创建命名空间
    if not cmds.namespace(exists=abc_namespace):
        cmds.namespace(add=abc_namespace)

    allSg=cmds.ls(type='shadingEngine')
    for sg in allSg:
        mats=cmds.listConnections(sg+'.surfaceShader')
        if not mats:
            continue
        mat = mats[0]
        newSgName = "{}:{}".format(abc_namespace, mat.split(':')[-1])
        if sg != newSgName:
            cmds.rename(sg, newSgName)
            print (u"重命名{}为{}".format(sg,newSgName))
        else:
            print(u"节点 {} 已经存在，跳过重命名。".format(newSgName))               


def createMatForAbc(*args):
    if not cmds.namespace(exists=abc_namespace):
        cmds.namespace(add=abc_namespace)

    # 获取当前选中的变换节点
    selected_objects = cmds.ls(selection=True, type='transform',l=1)

    # 将变换节点转换为形态节点
    shape_nodes = cmds.listRelatives(selected_objects, shapes=True, fullPath=True) if selected_objects else []
    shape_nodes_set =set(shape_nodes)

    shading_groups = cmds.ls(type='shadingEngine')
    findSgList=[]
    mel.eval('MLdeleteUnused;')
    for sg in shading_groups:
        if sg=="initialShadingGroup":
            continue
        # 获取shadingGroup绑定的几何体
        if not cmds.objExists(sg):
            continue
        geometries = cmds.sets(sg, q=True)
        geometries=cmds.ls(geometries,l=1)
        findSgList+=L_GV.getShapeNodeFromFaceSet(geometries)
        if geometries:
            # 过滤仅对选中形态节点生效
            print("geometriesA",geometries)
            geometries = [geo for geo in geometries if set(L_GV.getShapeNodeFromFaceSet(geo))&shape_nodes_set]
            print("geometriesB",geometries)
            # 创建新材质
            material_name = sg + "_new_material"
            if not cmds.objExists(material_name):
                material = cmds.shadingNode('lambert', asShader=True, name=material_name)
                
                # 随机生成HSV颜色，饱和度范围在100-360之间
                h = random.uniform(0, 1)  # 随机生成0到1的色调
                s = random.uniform(200/360, 1)  # 将饱和度限制在100-360度之间
                v = random.uniform(0.8, 1)  # 保证亮度较高以显示彩色

                # 将HSV转换为RGB
                r, g, b = colorsys.hsv_to_rgb(h, s, v)

                # 设置材质的颜色
                cmds.setAttr(material + ".color", r, g, b, type="double3")
                
                # 创建新的着色组 (shadingGroup)
                new_sg_name = abc_namespace + ":" + sg.split(':')[-1] + "_newSG"
                if not cmds.objExists(new_sg_name):
                    new_shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=new_sg_name)
                    
                    # 将新材质连接到新的着色组
                    cmds.connectAttr(material + ".outColor", new_shading_group + ".surfaceShader", force=True)
                
                # 将几何体添加到新的材质组
                for geo in geometries:
                        cmds.sets(geo, e=True, forceElement=new_sg_name)

    usual.cvtFaceSetSG(selected_objects)
    difference = shape_nodes_set - set(findSgList)
    if difference:
        difference_str='\n\n'.join(difference)
        msg_box = QMessageBox()
        msg_box.setText(difference_str)
        msg_box.setWindowTitle("没有材质的物体")
        # 通过查找QMessageBox的QLabel来设置其最小宽度
        label = msg_box.findChild(QLabel, "qt_msgbox_label")
        if label:
            label.setMinimumWidth(1200)  # 设置最小宽度
        msg_box.exec_()
    cmds.select(difference)

