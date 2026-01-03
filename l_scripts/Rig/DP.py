# coding:utf-8
import maya.mel as mm,re
import maya.cmds as cmds
def matchHandAni(*args):
    TposeNameSpace = cmds.ls(sl=1)[0].split(':')[0]  #控制器名称空间
    DongBuNameSpace = cmds.ls(sl=1)[1].split(':')[0] #动补骨骼器名称空间
    '''
    #jnt='B003_S78_chars_wuji_lowRig1FBX:LeftHandMiddle3' 中指骨骼
    #ctl=B003_S78_chars_wuji_lowRig1:FKMiddleFinger3_L  中指控制器
    B003_S78_chars_wuji_lowRig1:FKIndexFinger3_L  时值控制器
    B003_S78_chars_wuji_lowRig1FBX:LeftHandIndex3  时值骨骼
    B003_S78_chars_wuji_lowRig1:FKThumbFinger3_L   拇指控制器
    B003_S78_chars_wuji_lowRig1FBX:LeftHandThumb3 拇指骨骼
    '''
    jnts_left=cmds.ls(DongBuNameSpace+':LeftHand*',type='joint')[1:]
    jnts_right=cmds.ls(DongBuNameSpace+':RightHand*',type='joint')[1:]
    jnts_Hand=jnts_left+jnts_right
    print (len(jnts_Hand))
    #ctl=TposeNameSpace+'FK'+ThumbFinger3_L'
    ctlList=[]
    for jnt in jnts_Hand:
        cmds.select(jnt) #B003_S78_chars_wuji_lowRig1:FKIndexFinger1_L
        print ('jnt',jnt)
        ctl=jnt.replace('LeftHand','').replace('RightHand','').replace(DongBuNameSpace+':','')
        ctl=TposeNameSpace+':'+'FK'+ctl
        leftRight=re.search('Left|Right',jnt,re.I).group()[0]
        ctl=ctl[:-1]+'Finger'+ctl[-1]+'_'+leftRight
        print ('ctl',ctl)
        cmds.select(ctl,add=1)
        mm.eval('doCreateOrientConstraintArgList 1 { "1","0","0","0","0","0","0","1","","1" };')  
        ctlList.append(ctl)
    cmds.select(ctlList)
    print (len(ctlList))

