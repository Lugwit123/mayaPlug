# coding:utf-8


import os,sys
from pprint import pprint

try:
    import maya.cmds as cmds
    if 'pymel' not in str(sys.modules.keys()):
        cmds.confirmDialog(
            title=u'提示', message=u'第一次使用需要加载Pymel模块,需要10s左右', button=[u'好的'])
    import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm

    if not pm.pluginInfo("mayaHIK", q=1, l=1):
        pm.loadPlugin("mayaHIK")
    if not pm.pluginInfo("fbxmaya", q=1, l=1):
        pm.loadPlugin("fbxmaya")
    pm.mel.source("hikGlobalUtils.mel")
except:
    pass

try:
    from PySide2.QtWidgets import *
except ImportError:
    from PySide.QtGui import *


Root_M_joints_dict = {
    "Root_M": "Hips",
    "Spine1_M": "Spine",
    "Spine2_M": "Spine1",
    "Chest_M": "Spine3",
    "Neck_M": "Neck",
    "Head_M": "Head",
    "Scapula_L": "LeftShoulder",
    "Shoulder_L": "LeftArm",
    "Elbow_L": "LeftForeArm",
    "Wrist_L": "LeftHand",
    "Scapula_R": "RightShoulder",
    "Shoulder_R": "RightArm",
    "Elbow_R": "RightForeArm",
    "Wrist_R": "RightHand",
    "Hip_L": "LeftUpLeg",
    "Knee_L": "LeftLeg",
    "Ankle_L": "LeftFoot",
    "Toes_L": "LeftToeBase",
    "Hip_R": "RightUpLeg",
    "Knee_R": "RightLeg",
    "Ankle_R": "RightFoot",
    "Toes_R": "RightToeBase"
}


def create_hik(reference=None, name="Character1"):
    if reference is None:
        selected = pm.selected()
        if not len(selected) == 1:
            return
        reference = selected[0]
    if reference.name().endswith('Reference'):
        joints = {joint.name().split(
            ":")[-1].split("_")[-1]: joint for joint in reference.listRelatives(ad=1, type="joint")}
    else:
        # Root_M
        joints = {Root_M_joints_dict[joint.name().split(":")[-1].split("|")[-1]]: joint for joint in reference.listRelatives(ad=1, type="joint")
                  if joint.name().split(":")[-1].split("|")[-1] in Root_M_joints_dict.keys()}
        joints['Hips'] = reference

    char = pm.mel.hikCreateCharacter(name)
    joint_orient_list = []
    for i in range(1, 212):
        node_name = pm.GetHIKNodeName(i)
        if node_name not in joints:
            continue

        pm.mel.setCharacterObject(joints[node_name], char, i, 0)
    return char


adv_arms = ["Scapula", "Shoulder", "Elbow", "Wrist"]
hik_arms = ["Shoulder", "Arm", "ForeArm", "Hand"]
adv_legs = ["Hip", "Knee", "Ankle", "Toes"]
hik_legs = ["UpLeg", "Leg", "Foot", "ToeBase"]

adv_fingersA = ["ThumbFinger"+str(i) for i in range(1, 5)]
adv_fingersB = ["IndexFinger"+str(i) for i in range(1, 4)]
adv_fingersC = ["MiddleFinger"+str(i) for i in range(1, 4)]
adv_fingersD = ["RingFinger"+str(i) for i in range(1, 4)]
adv_fingersE = ["PinkyFinger"+str(i) for i in range(1, 4)]
# adv_fingersF= ["WristEnd"]
adv_fingers = [adv_fingersA,adv_fingersB,adv_fingersC,adv_fingersD,adv_fingersE]

hik_fingersA = ["HandThumb"+str(i) for i in range(1, 4)]
hik_fingersB = ["HandIndex"+str(i) for i in range(1, 4)]
hik_fingersC = ["HandMiddle"+str(i) for i in range(1, 4)]
hik_fingersD = ["HandRing"+str(i) for i in range(1, 5)]
hik_fingersE = ["HandPinky"+str(i) for i in range(1, 5)]
# hik_fingerF= ["WristEnd"]
hik_fingers = [hik_fingersA,hik_fingersB,hik_fingersC,hik_fingersD,hik_fingersE]


def get_con(con_name):
    u"""
    查找有没有名称为con_name的节点,不存在返回None
    con_name名字是唯一就返回这个物体，否则返回空
    """
    if not pm.objExists(con_name):
        return
    cons = pm.ls(con_name)
    if len(cons) != 1:
        return
    return cons[0]


def get_cons(prefix="", suffix="", names=None):
    u"""
    names里面的名字name，如果prefix + name + suffix名字唯一，
    就添加物体进数组，返回这个数组
    """
    if names is None:
        return []
    cons = []
    for name in names:
        con = get_con(prefix+name+suffix)
        if con:
            cons.append(con)
    return cons


def get_splines():
    cons = []
    for i in range(1, 10, 1):
        con_name = "FKSpine%i_M" % i
        if not pm.objExists("FKSpine%i_M" % i):
            continue
        _cons = pm.ls(con_name)
        if len(_cons) != 1:
            continue
        cons.append(_cons[0])
    return cons


def create_joint(prefix, name, con, parent, reference,ConstraintType=pm.parentConstraint):
    # 前缀,名称,复制于哪个节点,父节点,顶级Locator
    print(u'创建骨骼名称为{},复制于来自{}'.format(prefix+"_"+name, con))
    joint = pm.joint(con, n=prefix+"_"+name)
    print(u'设置骨骼{}父级为{}'.format(joint, parent))
    joint.setParent(parent)
    print(u'对新生成的的骨骼{}和她的母亲{}创建父子约束'.format(joint, con))
    print(u'用生成的骨骼来驱动她的母亲')
    create_parentConstraint = ConstraintType(joint, con)
    print(u'把{}的父级为{}'.format(create_parentConstraint, reference))
    pm.parent(create_parentConstraint, reference)
    return joint


def create_joints(prefix, names, cons, parent, reference,ConstraintType=pm.parentConstraint):
    print(prefix, names, cons, parent, reference)
    joints = []
    for name, con in zip(names, cons):
        joints.append(create_joint(prefix, name, con, parent, reference,ConstraintType))
        parent = joints[-1]
    return joints


def find_cons(prefix=""):
    # 寻找跟骨骼,腿部,脊柱,手臂和脖子的骨骼,和手指骨骼
    root = get_con(prefix+"FKRoot_M")
    l_leg = get_cons(prefix+"FK", "_L", adv_legs)
    r_leg = get_cons(prefix+"FK", "_R", adv_legs)
    spline = get_cons(prefix+"FKSpine", "_M",
                      [str(i) for i in range(1, 10, 1)])
    l_arm = get_cons(prefix+"FK", "_L", adv_arms)
    r_arm = get_cons(prefix+"FK", "_R", adv_arms)

    l_fingers=[];r_fingers=[]
    for adv_finger in adv_fingers:
        print ('adv_finger', adv_finger)
        l_fingers += [get_cons(prefix+"FK", "_L", adv_finger)]
        r_fingers += [get_cons(prefix+"FK", "_R", adv_finger)]

        

    neck = get_cons(prefix+"FK", "_M", ["Chest", "Neck", "Head"])
    spline.append(neck.pop(0))
    return root, l_leg, r_leg, spline, l_arm, r_arm, neck, l_fingers,r_fingers


def connect_pole(joint, offset, con, reference):
    pole = pm.group(em=1, p=joint, n=joint.name()+"_Pole")
    pole.ty.set(offset)
    pm.parent(pm.parentConstraint(joint, pole, mo=1), reference)
    pm.parent(pm.pointConstraint(pole, con), reference)
    pm.parent(pole, reference)


def rotate_joints(joints, rotate):
    temp = pm.group(em=1)
    temp.r.set(rotate)
    for joint in joints:
        pm.delete(pm.orientConstraint(temp, joint))
    pm.delete(temp)


def create_hik_joints(prefix, cons):
    # 创建HIK骨骼
    # 创建一个Locator
    reference = pm.spaceLocator(n=prefix + "_" + "Reference")
    # 创建Hips骨骼,命名为prefix_Hips,Hip的父节点为新创建的Locator
    # create_joint的参数为前缀,名称,复制于哪个节点,父节点
    # Hip因为意思为髋关节
    hips = create_joint(prefix, "Hips", cons[0], reference, reference)
    # 创建腿部节点,腿部节点不止一个,所以用列表来存储
    # create_joints的参数为:
    #                       前缀,名称,复制于哪个节点,父节点,顶级Locator
    l_leg = create_joints(
        prefix, ["Left"+name for name in hik_legs], cons[1], hips, reference)
    pprint((u'new legs joints', l_leg))
    cmds.select(l_leg)

    r_leg = create_joints(
        prefix, ["Right"+name for name in hik_legs], cons[2], hips, reference)
    hik_spines = ["Spine"] + ["Spine" +
                              str(i) for i in range(1, len(cons[3]), 1)]
    spline = create_joints(prefix, hik_spines, cons[3], hips, reference)
    chest = spline[-1]
    l_arm = create_joints(
        prefix, ["Left"+name for name in hik_arms], cons[4], chest, reference)
    r_arm = create_joints(
        prefix, ["Right"+name for name in hik_arms], cons[5], chest, reference)
    neck = create_joints(prefix, ["Neck", "Head"], cons[6], chest, reference)
    pprint (('cons', list(enumerate(cons))))
    for i,hik_finger in enumerate(hik_fingers):
        l_finger = create_joints(prefix, ["Left"+name for name in hik_finger], cons[7][i], l_arm[-1],reference)
        r_finger = create_joints(prefix, ["Right"+name for name in hik_finger], cons[8][i], r_arm[-1],reference)

        
    print('l_finger', l_finger)
    
    # 创建约束 在
    print(u'使用{}节点父子约束{}'.format(
        l_leg[-2], cons[1][-2].name().replace("FKAnkle", "IKLeg")))
    create_parentConstraint = pm.parentConstraint(
        l_leg[-2], cons[1][-2].name().replace("FKAnkle", "IKLeg"), mo=1)
    print(u'设置约束{}的父节点为{}'.format(create_parentConstraint, reference))
    pm.parent(create_parentConstraint, reference)
    pm.parent(pm.parentConstraint(
        r_leg[-2], cons[2][-2].name().replace("FKAnkle", "IKLeg"), mo=1), reference)
    pm.parent(pm.parentConstraint(
        l_arm[-1], cons[4][-1].name().replace("FKWrist", "IKArm"), mo=1), reference)
    pm.parent(pm.parentConstraint(
        r_arm[-1], cons[5][-1].name().replace("FKWrist", "IKArm"), mo=1), reference)

    #极坐标约束
    connect_pole(l_leg[-3], -1, cons[1]
                 [-3].name().replace("FKKnee", "PoleLeg"), reference)
    connect_pole(r_leg[-3], 1, cons[2]
                 [-3].name().replace("FKKnee", "PoleLeg"), reference)
    connect_pole(l_arm[-2], 1, cons[4]
                 [-2].name().replace("FKElbow", "PoleArm"), reference)
    connect_pole(r_arm[-2], -1, cons[5]
                 [-2].name().replace("FKElbow", "PoleArm"), reference)

    #旋转骨骼
    rotate_joints([hips]+spline+neck, [90, 0, 90])
    rotate_joints(l_leg[:-1], [-90, 0, 90])
    rotate_joints(r_leg[:-1], [90, 0, -90])
    rotate_joints(l_arm, [90, 180, 0])
    rotate_joints(r_arm, [90, 0, 180])
    pm.parent(pm.parentConstraint(hips, get_con(
        prefix + ":RootX_M"), mo=1), reference)
    pm.parent(pm.pointConstraint(hips, get_con(
        prefix + ":Main"), mo=1), reference)
    return reference


def rig_hik():
    cons = find_cons()
    reference = create_hik_joints("Rig", cons)
    create_hik(reference=reference, name="Character1")


def reference_fbx():
    '''实现原理:
    1,根据在Adv_Tpose的Fk骨骼的位置创建一套新的骨骼,骨骼命名为HIK命名规则
    每根骨骼父子约束Fk的每根骨骼
    1.创建一套骨骼定义,骨骼的位置来自于Adv_Tpose的骨骼
    
    2,使用动捕的骨骼数据通过HIK驱动第一步创建的骨骼定义
    
    '''
    selected = pm.selected()
    # if not len(selected):
    #     QMessageBox.information(None, u'消息提示!',
    #                             u"小哥哥,你需要选择最外层的大环哟")
    #     return
    con = selected[0]
    if not con.isReferenced():
        QMessageBox.information(None, u'消息提示!',
                                u"小哥哥,你选择的文件需要是引用的形式额")
        return
    path, _ = QFileDialog.getOpenFileName(QApplication.activeWindow(), "fbx", "", "fbx(*.fbx)")

    prefix = con.namespace()
    cons = find_cons(prefix)  # 寻找Tpose中根骨骼,腿部,脊柱,手臂和脖子和手指的骨骼
    # prefix[:-1] 名称空间去掉最后一个字符':'
    pprint(('find_cons(prefix)', find_cons(prefix)))
    pprint (('cons', list(enumerate(cons))))

    reference = create_hik_joints(prefix[:-1], cons)  # 传入Tpose的名称空间和新的骨骼名称

    # 创建HIK骨骼,参数1为创建的Locator节点,参数2为HIK角色定义名称
    rig = create_hik(reference=reference, name=prefix[:-1]+"Rig")
    
    
    pm.createReference(
        path, type="FBX", namespace=prefix[:-1]+"FBX", referenceNode=prefix[:-1]+"FbxRN")
    if pm.objExists("|"+prefix[:-1]+"FBX:Reference"):
        print('Reference')
        ani = create_hik(
            pm.PyNode("|"+prefix[:-1]+"FBX:Reference"), prefix[:-1]+"Ani")
        pm.mel.hikCharacterLock(rig, 1, 0)
        pm.mel.hikSetCharacterInput(rig, ani)
    elif pm.objExists("|"+prefix[:-1]+"FBX:Root_M"):
        # 摆tpose
        print('Root_M')
        pm.joint("|"+prefix[:-1]+"FBX:Root_M", e=True, apa=True, ch=True)
        pm.PyNode(prefix[:-1]+"FBX:Shoulder_R").ry.set(-58.279)
        pm.PyNode(prefix[:-1]+"FBX:Elbow_R").rz.set(-30.764)
        pm.PyNode(prefix[:-1]+"FBX:Wrist_R").rz.set(10.857)
        pm.PyNode(prefix[:-1]+"FBX:Knee_R").rz.set(9.143)
        pm.PyNode(prefix[:-1]+"FBX:Shoulder_L").ry.set(-58.279)
        pm.PyNode(prefix[:-1]+"FBX:Elbow_L").rz.set(-30.764)
        pm.PyNode(prefix[:-1]+"FBX:Wrist_L").rz.set(10.857)
        pm.PyNode(prefix[:-1]+"FBX:Knee_L").rz.set(9.143)
        pm.PyNode(prefix[:-1]+"FBX:Chest_M").rz.set(19.571)
        # pm.PyNode(prefix[:-1]+"FBX:Neck_M").rz.set(-51.562)
        # pm.PyNode(prefix[:-1]+"FBX:Head_M").rz.set(32.963)

        #
        ani = create_hik(
            pm.PyNode("|"+prefix[:-1]+"FBX:Root_M"), prefix[:-1]+"Ani")
        pm.mel.hikCharacterLock(rig, 1, 0)
        pm.mel.hikSetCharacterInput(rig, ani)


def play_fbx(path):
    pm.openFile("E:/C14_HC_chars_low.mb", f=1)
    cons = find_cons("")
    reference = create_hik_joints("body", cons)
    rig = create_hik(reference=reference, name="bodyRig")
    prefix = "body"
    pm.createReference(
        path, type="FBX", namespace=prefix[:-1]+"FBX", referenceNode=prefix[:-1]+"FbxRN")
    if pm.objExists("|"+prefix[:-1]+"FBX:Reference"):
        ani = create_hik(
            pm.PyNode("|"+prefix[:-1]+"FBX:Reference"), prefix[:-1]+"Ani")
        pm.mel.hikCharacterLock(rig, 1, 0)
        pm.mel.hikSetCharacterInput(rig, ani)
    st = int(round(pm.playbackOptions(q=1, min=-1)))
    et = int(round(pm.playbackOptions(q=1, max=1)))
    wh = (1920, 1080)
    pm.playblast(f=os.path.splitext(path)[
                 0], fmt="qt", c="H.264", st=st, et=et, orn=1, os=True, qlt=100, p=100, wh=wh, v=0)


def play_all_fbx(path=r"E:\fbxs"):
    for name in os.listdir(path):
        fbx_path = os.path.join(path, name)
        print fbx_path
        ext = os.path.splitext(fbx_path)[-1]
        print ext
        if ext != ".fbx":
            continue
        play_fbx(fbx_path)
