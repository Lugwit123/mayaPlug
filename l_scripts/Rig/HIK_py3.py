# coding:utf-8
# 添加模块所在路径
import os, re, sys
from typing import Optional, Dict, List, Tuple, Any, Union
from dataclasses import dataclass
import maya.cmds as cmds

fileDir = os.path.dirname(__file__)
sys.path.insert(0, fileDir)
os.environ["QT_API"] = "PySide2"
from functools import partial
import pysnooper

os.environ["Lugwit_Debug"] = "inspect"
sys.path.append(os.getenv("LugwitLibDir"))
from Lugwit_Module.l_src.UILib.QTLib import PySideLib
import Lugwit_Module as LM

lprint = LM.lprint
from importlib import reload

import os, sys
from pprint import pprint
import codecs

import os, sys

sys.path.append(r"D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug")
import load_pymel

pm = load_pymel.pm
nt = pm.nt  # Maya节点类型

if not pm.pluginInfo("mayaHIK", q=1, l=1):
    pm.loadPlugin("mayaHIK")
if not pm.pluginInfo("fbxmaya", q=1, l=1):
    pm.loadPlugin("fbxmaya")
pm.mel.source("hikGlobalUtils.mel")


from PySide2.QtWidgets import *
from PySide2 import QtCore
from PySide2.QtGui import QMovie
from PySide2.QtGui import *
from PySide2.QtCore import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


# 类型别名
MayaNode = Any  # pymel节点对象
JointList = List[MayaNode]
JointDict = Dict[str, MayaNode]
WidgetList = List[QWidget]


def get_maya_main_window():
    """获取Maya主窗口作为Qt对象"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    if main_window_ptr is not None:
        return wrapInstance(int(main_window_ptr), QWidget)
    return None


@dataclass
class JointMapping:
    """骨骼映射结构体"""

    adv_name: str
    hik_name: str


# 骨骼映射字典
Root_M_joints_dict: Dict[str, str] = {
    "Root_M": "Hips",
    "Spine_M": "Spine",
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
    "Toes_R": "RightToeBase",
}


def create_hik(
    reference: Optional[MayaNode] = None,
    name: str = "Character1",
    suffix: str = "suffix",
) -> Optional[MayaNode]:
    if reference is None:
        selected = pm.selected()
        if not len(selected) == 1:
            return
        reference = selected[0]
    lprint(reference, reference.name())
    if reference.name().endswith(suffix):
        joints = {
            joint.name().split(":")[-1].split("_")[-1]: joint
            for joint in reference.listRelatives(ad=1, type="joint")
        }
    else:
        # Root_M
        joints = {
            Root_M_joints_dict[joint.name().split(":")[-1].split("|")[-1]]: joint
            for joint in reference.listRelatives(ad=1, type="joint")
            if joint.name().split(":")[-1].split("|")[-1]
            in list(Root_M_joints_dict.keys())
        }
        joints["Hips"] = reference

    char = pm.mel.hikCreateCharacter(name)
    joint_orient_list = []
    for i in range(1, 212):
        node_name = pm.GetHIKNodeName(i)
        if node_name not in joints:
            continue

        pm.mel.setCharacterObject(joints[node_name], char, i, 0)
    return char


@dataclass
class LimbMapping:
    """肢体骨骼映射结构体"""

    adv_names: List[str]
    hik_names: List[str]


# 肢体骨骼映射
arms_mapping = LimbMapping(
    adv_names=["Scapula", "Shoulder", "Elbow", "Wrist"],
    hik_names=["Shoulder", "Arm", "ForeArm", "Hand"],
)
legs_mapping = LimbMapping(
    adv_names=["Hip", "Knee", "Ankle", "Toes"],
    hik_names=["UpLeg", "Leg", "Foot", "ToeBase"],
)


@dataclass
class FingerMapping:
    """手指骨骼映射结构体"""

    adv_names: List[str]
    hik_names: List[str]


# 手指骨骼映射
finger_mappings: List[FingerMapping] = [
    FingerMapping(
        adv_names=["ThumbFinger" + str(i) for i in range(1, 5)],
        hik_names=["HandThumb" + str(i) for i in range(1, 4)],
    ),
    FingerMapping(
        adv_names=["IndexFinger" + str(i) for i in range(1, 4)],
        hik_names=["HandIndex" + str(i) for i in range(1, 4)],
    ),
    FingerMapping(
        adv_names=["MiddleFinger" + str(i) for i in range(1, 4)],
        hik_names=["HandMiddle" + str(i) for i in range(1, 4)],
    ),
    FingerMapping(
        adv_names=["RingFinger" + str(i) for i in range(1, 4)],
        hik_names=["HandRing" + str(i) for i in range(1, 5)],
    ),
    FingerMapping(
        adv_names=["PinkyFinger" + str(i) for i in range(1, 4)],
        hik_names=["HandPinky" + str(i) for i in range(1, 5)],
    ),
]


@pysnooper.snoop("D:/file.log")
def get_control(con_name: str) -> Optional[nt.Transform]:
    """
    查找指定名称的Maya控制器节点

    Args:
        con_name: 控制器节点名称，如 'C_A001_HanYang_Rig:FKRoot_M'

    Returns:
        Optional[nt.Transform]: 如果控制器节点存在且唯一则返回Transform节点，否则返回None

    Note:
        - 检查节点是否存在：pm.objExists(con_name)
        - 获取节点列表：pm.ls(con_name)
        - 确保节点唯一性：len(cons) == 1
    """
    if not pm.objExists(con_name):
        return
    cons = pm.ls(con_name)
    if len(cons) != 1:
        return
    return cons[0]


@pysnooper.snoop("D:/file.log")
def get_controls(
    prefix: str = "", suffix: str = "", names: Optional[List[str]] = None
) -> List[nt.Transform]:
    """
    批量查找符合命名规则的Maya控制器节点

    Args:
        prefix: 名称前缀，如 'C_A001_HanYang_Rig:FK'
        suffix: 名称后缀，如 '_L' 或 '_R'
        names: 节点名称列表，如 ['Hip', 'Knee', 'Ankle', 'Toes']

    Returns:
        List[nt.Transform]: 找到的控制器节点列表

    Example:
        # 查找左腿骨骼：C_A001_HanYang_Rig:FKHip_L, C_A001_HanYang_Rig:FKKnee_L...
        get_controls('C_A001_HanYang_Rig:FK', '_L', ['Hip', 'Knee', 'Ankle', 'Toes'])
    """
    if names is None:
        return []
    cons = []
    for name in names:
        con = get_control(prefix + name + suffix)
        if con:
            cons.append(con)
    return cons


@pysnooper.snoop("D:/file.log")
def get_splines() -> List[nt.Transform]:
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


@pysnooper.snoop("D:/file.log")
def create_joint(
    prefix: str,
    name: str,
    source_joint: MayaNode,
    parent: MayaNode,
    reference: MayaNode,
    ConstraintType: Any = pm.parentConstraint,
) -> MayaNode:
    """
    创建新的骨骼节点并建立约束关系

    Args:
        prefix: 新骨骼名称前缀，如 'Rig'
        name: 新骨骼名称，如 'LeftUpLeg'
        source_joint: 源骨骼节点（用于复制位置和约束目标）
        parent: 新骨骼的父节点
        reference: 参考节点（约束的父节点）
        ConstraintType: 约束类型，默认为父子约束

    Returns:
        MayaNode: 创建的新骨骼节点

    Process:
        1. 基于源骨骼创建新骨骼：pm.joint(source_joint, n=prefix+"_"+name)
        2. 设置新骨骼的父级：joint.setParent(parent)
        3. 创建约束：新骨骼约束源骨骼
        4. 将约束节点归到参考节点下：pm.parent(create_parentConstraint, reference)
    """
    joint = pm.joint(source_joint, n=prefix + "_" + name)
    joint.setParent(parent)
    create_parentConstraint = ConstraintType(joint, source_joint)
    pm.parent(create_parentConstraint, reference)
    return joint


@pysnooper.snoop("D:/file.log")
def create_joints(
    prefix: str,
    names: List[str],
    cons: List[MayaNode],
    parent: MayaNode,
    reference: MayaNode,
    ConstraintType: Any = pm.parentConstraint,
) -> JointList:
    """
    批量创建骨骼链

    Args:
        prefix: 骨骼名称前缀
        names: 骨骼名称列表，按父子顺序排列
        cons: 源骨骼节点列表，与names一一对应
        parent: 第一个骨骼的父节点
        reference: 参考节点
        ConstraintType: 约束类型

    Returns:
        JointList: 创建的骨骼链列表

    Process:
        - 依次创建每个骨骼
        - 每个新骨骼成为前一个骨骼的子节点
        - 形成骨骼链结构
    """
    joints = []
    for name, source_joint in zip(names, cons):
        joints.append(
            create_joint(prefix, name, source_joint, parent, reference, ConstraintType)
        )
        parent = joints[-1]  # 下一个骨骼的父级是当前骨骼
    return joints


@dataclass
class SkeletonComponents:
    """Tpose FK控制器组件结构体

    注意：存储的是Tpose中的FK控制器节点（nt.Transform），
    不是骨骼节点（nt.Joint）。这些节点用于动画控制和位置参考。
    """

    root: Optional[nt.Transform]  # FK根控制器
    l_leg: List[nt.Transform]  # 左腿FK控制器链
    r_leg: List[nt.Transform]  # 右腿FK控制器链
    spline: List[nt.Transform]  # 脊柱FK控制器链
    l_arm: List[nt.Transform]  # 左臂FK控制器链
    r_arm: List[nt.Transform]  # 右臂FK控制器链
    neck: List[nt.Transform]  # 颈部FK控制器链
    l_fingers: List[List[nt.Transform]]  # 左手FK控制器
    r_fingers: List[List[nt.Transform]]  # 右手FK控制器


@pysnooper.snoop("D:/file.log")
def find_cons(prefix: str = "") -> SkeletonComponents:
    """
    查找并组装完整的角色骨骼系统

    Args:
        prefix: 命名空间前缀，如 'C_A001_HanYang_Rig:'

    Returns:
        SkeletonComponents: 包含所有身体部位的骨骼组件

    Components:
        - root: 根骨骼 (FKRoot_M)
        - l_leg/r_leg: 左右腿骨骼链 (Hip->Knee->Ankle->Toes)
        - spline: 脊柱骨骼链 (Spine1->Spine2->...->Spine9+Chest)
        - l_arm/r_arm: 左右臂骨骼链 (Scapula->Shoulder->Elbow->Wrist)
        - neck: 颈部骨骼链 (Chest->Neck->Head)
        - l_fingers/r_fingers: 左右手指骨骼 (5个手指 x 3-4个关节)

    Note:
        从日志可以看到，查找过程会遍历所有命名节点，
        只返回存在且唯一的节点，不存在的节点会被跳过。
    """
    # 查找根骨骼
    root = get_control(prefix + "FKRoot_M")

    # 查找腿部骨骼（左右各4个关节）
    l_leg = get_controls(prefix + "FK", "_L", legs_mapping.adv_names)
    r_leg = get_controls(prefix + "FK", "_R", legs_mapping.adv_names)

    # 查找脊柱骨骼（9个脊柱节点 + Chest）
    spline = get_controls(prefix + "FKSpine", "_M", [str(i) for i in range(1, 10, 1)])

    # 查找手臂骨骼（左右各4个关节）
    l_arm = get_controls(prefix + "FK", "_L", arms_mapping.adv_names)
    r_arm = get_controls(prefix + "FK", "_R", arms_mapping.adv_names)

    # 查找手指骨骼（5个手指，每个3-4个关节）
    l_fingers = []
    r_fingers = []
    for finger_mapping in finger_mappings:
        lprint(("adv_finger", finger_mapping.adv_names))
        l_fingers += [get_controls(prefix + "FK", "_L", finger_mapping.adv_names)]
        r_fingers += [get_controls(prefix + "FK", "_R", finger_mapping.adv_names)]

    # 查找颈部骨骼（从脊柱中分离Chest，保留Neck和Head）
    neck = get_controls(prefix + "FK", "_M", ["Chest", "Neck", "Head"])
    spline.append(neck.pop(0))  # 将Chest移到脊柱末尾

    return SkeletonComponents(
        root=root,
        l_leg=l_leg,
        r_leg=r_leg,
        spline=spline,
        l_arm=l_arm,
        r_arm=r_arm,
        neck=neck,
        l_fingers=l_fingers,
        r_fingers=r_fingers,
    )


@pysnooper.snoop("D:/file.log")
def connect_pole(joint: MayaNode, offset: float, con: str, reference: MayaNode) -> None:
    pole = pm.group(em=1, p=joint, n=joint.name() + "_Pole")
    pole.ty.set(offset)
    pm.parent(pm.parentConstraint(joint, pole, mo=1), reference)
    pm.parent(pm.pointConstraint(pole, con), reference)
    pm.parent(pole, reference)


@pysnooper.snoop("D:/file.log")
def rotate_joints(joints: JointList, rotate: List[float]) -> None:
    temp = pm.group(em=1)
    temp.r.set(rotate)
    for joint in joints:
        pm.delete(pm.orientConstraint(temp, joint))
    pm.delete(temp)


@pysnooper.snoop("D:/file.log")
def create_hik_joints(
    prefix: str, Suffix: str, skeleton_components: SkeletonComponents
) -> MayaNode:
    """
    基于源骨骼创建HIK标准命名的新骨骼系统

    Args:
        prefix: 新骨骼名称前缀，如 'Rig'
        Suffix: 新骨骼名称后缀，如 'Group'
        skeleton_components: 源骨骼组件集合

    Returns:
        MayaNode: 参考定位器节点

    Process:
        1. 创建参考定位器作为所有约束的父节点
        2. 创建HIK标准命名的骨骼系统
        3. 建立新骨骼与源骨骼的约束关系
        4. 创建极坐标约束
        5. 旋转骨骼到标准方向

    HIK命名规则:
        - 腿部: UpLeg->Leg->Foot->ToeBase
        - 手臂: Shoulder->Arm->ForeArm->Hand
        - 脊柱: Spine->Spine1->Spine2->...
        - 手指: HandThumb1/2/3, HandIndex1/2/3, etc.
    """
    # 创建参考定位器（所有约束的父节点）
    reference = pm.spaceLocator(n=prefix + "_" + Suffix)

    # 创建髋关节（根骨骼的子节点）
    hips = create_joint(prefix, "Hips", skeleton_components.root, reference, reference)

    # 创建腿部骨骼链（左右各4个HIK标准关节）
    l_leg = create_joints(
        prefix,
        ["Left" + name for name in legs_mapping.hik_names],
        skeleton_components.l_leg,
        hips,
        reference,
    )
    pprint(("new legs joints", l_leg))
    cmds.select(l_leg)

    r_leg = create_joints(
        prefix,
        ["Right" + name for name in legs_mapping.hik_names],
        skeleton_components.r_leg,
        hips,
        reference,
    )

    # 创建脊柱骨骼链（Spine + Spine1-9）
    hik_spines = ["Spine"] + [
        "Spine" + str(i) for i in range(1, len(skeleton_components.spline), 1)
    ]
    spline = create_joints(
        prefix, hik_spines, skeleton_components.spline, hips, reference
    )
    chest = spline[-1]  # 胸部是脊柱的最后一个节点

    # 创建手臂骨骼链（左右各4个HIK标准关节）
    l_arm = create_joints(
        prefix,
        ["Left" + name for name in arms_mapping.hik_names],
        skeleton_components.l_arm,
        chest,
        reference,
    )
    r_arm = create_joints(
        prefix,
        ["Right" + name for name in arms_mapping.hik_names],
        skeleton_components.r_arm,
        chest,
        reference,
    )

    # 创建颈部骨骼链
    neck = create_joints(
        prefix, ["Neck", "Head"], skeleton_components.neck, chest, reference
    )

    # 创建手指骨骼（5个手指，每个3-4个关节）
    pprint(
        (
            "cons",
            [
                (i, getattr(skeleton_components, field))
                for i, field in enumerate(
                    [
                        "root",
                        "l_leg",
                        "r_leg",
                        "spline",
                        "l_arm",
                        "r_arm",
                        "neck",
                        "l_fingers",
                        "r_fingers",
                    ]
                )
            ],
        )
    )
    for i, finger_mapping in enumerate(finger_mappings):
        l_finger = create_joints(
            prefix,
            ["Left" + name for name in finger_mapping.hik_names],
            skeleton_components.l_fingers[i],
            l_arm[-1],
            reference,
        )
        r_finger = create_joints(
            prefix,
            ["Right" + name for name in finger_mapping.hik_names],
            skeleton_components.r_fingers[i],
            r_arm[-1],
            reference,
        )

    lprint(("l_finger", l_finger))

    # 创建约束 在
    # lprint((u'使用{}节点父子约束{}'.format(
    #     l_leg[-2], cons[1][-2].name().replace("FKAnkle", "IKLeg"))))
    create_parentConstraint = pm.parentConstraint(
        l_leg[-2],
        skeleton_components.l_leg[-2].name().replace("FKAnkle", "IKLeg"),
        mo=1,
    )
    # lprint((u'设置约束{}的父节点为{}'.format(create_parentConstraint, reference)))
    pm.parent(create_parentConstraint, reference)
    pm.parent(
        pm.parentConstraint(
            r_leg[-2],
            skeleton_components.r_leg[-2].name().replace("FKAnkle", "IKLeg"),
            mo=1,
        ),
        reference,
    )
    pm.parent(
        pm.parentConstraint(
            l_arm[-1],
            skeleton_components.l_arm[-1].name().replace("FKWrist", "IKArm"),
            mo=1,
        ),
        reference,
    )
    pm.parent(
        pm.parentConstraint(
            r_arm[-1],
            skeleton_components.r_arm[-1].name().replace("FKWrist", "IKArm"),
            mo=1,
        ),
        reference,
    )

    # 极坐标约束
    connect_pole(
        l_leg[-3],
        -1,
        skeleton_components.l_leg[-3].name().replace("FKKnee", "PoleLeg"),
        reference,
    )
    connect_pole(
        r_leg[-3],
        1,
        skeleton_components.r_leg[-3].name().replace("FKKnee", "PoleLeg"),
        reference,
    )
    connect_pole(
        l_arm[-2],
        1,
        skeleton_components.l_arm[-2].name().replace("FKElbow", "PoleArm"),
        reference,
    )
    connect_pole(
        r_arm[-2],
        -1,
        skeleton_components.r_arm[-2].name().replace("FKElbow", "PoleArm"),
        reference,
    )

    # 旋转骨骼
    rotate_joints([hips] + spline + neck, [90, 0, 90])
    rotate_joints(l_leg[:-1], [-90, 0, 90])
    rotate_joints(r_leg[:-1], [90, 0, -90])
    rotate_joints(l_arm, [90, 180, 0])
    rotate_joints(r_arm, [90, 0, 180])
    lprint(locals())
    pm.parent(
        pm.parentConstraint(hips, get_control(prefix + ":RootX_M"), mo=1), reference
    )
    pm.parent(pm.pointConstraint(hips, get_control(prefix + ":Main"), mo=1), reference)
    return reference


@pysnooper.snoop("D:/file.log")
def rig_hik() -> None:
    skeleton_components = find_cons()
    reference = create_hik_joints("Rig", skeleton_components)
    create_hik(reference=reference, name="Character1")


@dataclass
class FBXReferenceData:
    """FBX引用数据结构体"""

    tpose_node: MayaNode
    fbx_path: str
    namespace: str
    reference_nodes: List[MayaNode]
    locator_node: MayaNode
    ref_node_namespace: str
    ref_node_root: str
    suffix: str

def reference_fbx_before_snooper(sender: QPushButton) -> None:  # 传递动捕数据
    # 移除日志文件，确保每次运行都是全新的日志
    with open("D:/file.log", "w") as f:
        f.write("")
    reference_fbx(sender)

# NOTE: 核心函数 - 动捕数据传递主流程
@pysnooper.snoop("D:/file.log")
def reference_fbx(sender: QPushButton) -> None:  # 传递动捕数据
    """
    动捕数据传递的核心函数

    实现原理:
    1. 根据T-pose的FK骨骼位置创建HIK标准命名的新骨骼系统
       - 新骨骼与源骨骼建立父子约束关系
       - 新骨骼作为HIK系统的输入

    2. 引入FBX动捕文件并建立HIK驱动关系
       - FBX文件包含动捕数据
       - 通过HIK系统将动捕数据传递到新骨骼
       - 最终驱动原始角色骨骼

    Args:
        sender: UI按钮对象，用于存储临时数据

    Process:
        1. 获取T-pose节点和FBX文件路径
        2. 查找T-pose中的所有骨骼组件
        3. 创建HIK标准命名的新骨骼系统
        4. 引入FBX动捕文件
        5. 建立HIK角色定义和驱动关系
        6. 设置T-pose姿势（如果需要）
    """
    # 获取UI中的Tpose节点和FBX文件路径
    tpose_node_name: str = tranDoBuDataUI_Instance.SetSelTpose_widgets[
        0
    ].text()  # Tpose节点名称
    tpose_node: nt.Transform = pm.ls(tpose_node_name)[0]  # 转换为Maya节点对象

    # 验证Tpose节点必须是引用文件
    if not tpose_node.isReferenced():
        QMessageBox.information(
            None, "消息提示!", "小哥哥,你选择的文件需要是引用的形式额"
        )
        return

    fbx_file_path: str = tranDoBuDataUI_Instance.fbxSelWidgets[
        0
    ].currentText()  # FBX文件路径

    # 获取Tpose命名空间并查找所有骨骼组件
    namespace_prefix: str = tpose_node.namespace()  # 如 'C_A001_HanYang_Rig:'
    skeleton_components: SkeletonComponents = find_cons(
        namespace_prefix
    )  # 查找Tpose中所有骨骼组件
    lprint(skeleton_components)

    # 引入FBX动捕文件
    # 创建FBX引用，命名空间为原命名空间+FBX后缀
    fbx_reference_nodes: List[MayaNode] = pm.createReference(
        fbx_file_path,
        type="FBX",
        namespace=namespace_prefix[:-1] + "FBX",
        referenceNode=namespace_prefix[:-1] + "FbxRN",
        returnNewNodes=True,
    )
    lprint(fbx_reference_nodes)

    # 从FBX文件中提取关键信息
    fbx_locator_nodes: List[nt.Locator] = [
        node for node in fbx_reference_nodes if node.type() == "locator"
    ]
    lprint(fbx_locator_nodes)
    main_locator_node: nt.Locator = fbx_locator_nodes[0]  # 主要定位器节点
    fbx_namespace: str = main_locator_node.namespace()[:-1]  # FBX命名空间
    fbx_root_node: nt.Transform = main_locator_node.getParent(-1)  # FBX根节点
    print("fbx_root_node", main_locator_node, type(main_locator_node))
    suffix: str = fbx_root_node.split(":")[-1]  # 如 'MAN02'

    # 第一步：基于Tpose创建HIK标准命名的新骨骼系统
    # 新骨骼将作为Tpose和FBX动捕数据之间的桥梁
    # 从日志可以看到：创建C_A001_HanYang_Rig_MAN02定位器作为参考节点
    reference: nt.Transform = create_hik_joints(
        namespace_prefix[:-1], suffix, skeleton_components
    )
    return
    # 创建HIK角色定义，用于管理骨骼映射
    # 日志显示：rig = 'C_A001_HanYang_RigRig'
    rig: str = create_hik(
        reference=reference, name=namespace_prefix[:-1] + "Rig", suffix=suffix
    )

    # 第二步：建立FBX动捕数据到HIK系统的驱动关系
    # 根据FBX文件结构选择不同的处理方式
    # 从日志可以看到：实际执行了方式2（Root_M结构）

    if pm.objExists("|" + fbx_root_node):
        # 方式1：FBX有明确的根节点（如MAN02）
        # 直接创建动画角色并建立驱动关系
        ani: str = create_hik(
            pm.PyNode("|" + fbx_root_node), fbx_namespace + ":Ani", suffix=suffix
        )
        pm.mel.hikCharacterLock(rig, 1, 0)  # 锁定角色定义
        lprint(ani)
        pm.mel.hikSetCharacterInput(rig, ani)  # 设置动画输入

    elif pm.objExists("|" + fbx_namespace + ":Root_M"):
        # 方式2：FBX使用标准Root_M结构（实际执行的路径）
        # 需要先调整到T-pose姿势，然后建立驱动关系
        lprint("Root_M")

        # 调整FBX骨骼到标准T-pose姿势
        # 从日志可以看到：依次调整了各个关节的旋转角度
        pm.joint("|" + fbx_namespace + ":Root_M", e=True, apa=True, ch=True)
        # 右臂姿势
        pm.PyNode(fbx_namespace + ":Shoulder_R").ry.set(-58.279)
        pm.PyNode(fbx_namespace + ":Elbow_R").rz.set(-30.764)
        pm.PyNode(fbx_namespace + ":Wrist_R").rz.set(10.857)
        pm.PyNode(fbx_namespace + ":Knee_R").rz.set(9.143)
        # 左臂姿势
        pm.PyNode(fbx_namespace + ":Shoulder_L").ry.set(-58.279)
        pm.PyNode(fbx_namespace + ":Elbow_L").rz.set(-30.764)
        pm.PyNode(fbx_namespace + ":Wrist_L").rz.set(10.857)
        pm.PyNode(fbx_namespace + ":Knee_L").rz.set(9.143)
        pm.PyNode(fbx_namespace + ":Chest_M").rz.set(19.571)
        # 注释掉的颈部和头部调整（根据需要启用）
        # pm.PyNode(fbx_namespace+":Neck_M").rz.set(-51.562)
        # pm.PyNode(fbx_namespace+":Head_M").rz.set(32.963)

        # 创建动画角色并建立驱动关系
        # 从日志可以看到：ani = 'C_A001_HanYang_RigFBX:Ani'
        ani: str = create_hik(
            pm.PyNode("|" + fbx_namespace + ":Root_M"), fbx_namespace + "Ani"
        )
        pm.mel.hikCharacterLock(rig, 1, 0)
        pm.mel.hikSetCharacterInput(rig, ani)

    # 保存FBX根节点信息，供后续操作使用
    # 从日志可以看到：sender.refNodeRootNode=fbx_root_node 被执行
    sender.refNodeRootNode = fbx_root_node


@dataclass
class UIWidgets:
    """UI控件结构体"""

    setFps_widget: Any
    setFps_widgets: WidgetList
    SetSelTpose_widget: Any
    SetSelTpose_widgets: WidgetList
    fbxSelWidget: Any
    fbxSelWidgets: WidgetList
    transferDateBtn: QPushButton
    SetCtlPar_widget: Any
    SetCtlPar_widgets: WidgetList
    ctlToHide_widget: Any
    SetCtlHide_widgets: WidgetList
    bakeRange_widget: Any
    bakeCtl_widget: Any
    RemoveData: Any


class tranDoBuDataUI(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        if parent is None:
            parent = get_maya_main_window()
        super(tranDoBuDataUI, self).__init__(parent)
        self.setObjectName("Lugwit_HIK_tranDoBuDataUI")
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowTitle("导入并烘焙动捕数据")
        self.resize(400, 200)
        self.topLay = QVBoxLayout()
        helpButtonLay = QHBoxLayout()
        helpButton = QPushButton("?")

        helpButtonLay.addWidget(helpButton)
        helpButton.setToolTip("这里录制了一个好看的小视频✺◟(∗❛ัᴗ❛ั∗)◞✺")
        helpButtonLay.setAlignment(Qt.AlignLeft)
        self.topLay.addLayout(helpButtonLay)
        helpButton.clicked.connect(
            lambda *args: os.startfile(
                LM.Lugwit_mayaPluginPath + r"\mov_help\bakeDongDu.mp4"
            )
        )

        widgetList = [
            (QRadioButton, "", {"setText": "24"}),
            (QRadioButton, "", {"setText": "25"}),
            (QRadioButton, "", {"setText": "30"}),
            (QRadioButton, "", {"setText": "60"}),
        ]
        self.setFps_widget = PySideLib.LQHVGrp(
            btnGrp=1,
            par=self.topLay,
            widgetList=widgetList,
            groupBox="请先设置好帧速率",
        )
        self.setFps_widgets = self.setFps_widget.get_widgetList()
        btnGrp = self.setFps_widget.get_btnGrp()
        self.setFps_widget.get_groupBox().setStyleSheet("color:red")

        def setFps_widget_clicked():
            checkedBtn = btnGrp.checkedButton()
            checkedBtnText = checkedBtn.text()
            cmds.currentUnit(t=checkedBtnText + "fps")
            self.setFps_widget.get_groupBox().setStyleSheet("")
            self.transferDateBtn.setEnabled(1)

        btnGrp.buttonClicked.connect(setFps_widget_clicked)

        widgetList = [
            (
                QLineEdit,
                "",
                {"setText": "C_A001_HanYang_Rig:Group", "setReadOnly": 1},
                (0, 1, 1, 3),
            ),
            (QPushButton, "", {"setText": "设置选择"}),
        ]
        self.SetSelTpose_widget = PySideLib.LQHVGrp(
            widgetList=widgetList,
            par=self.topLay,
            groupBox="1,请在大纲视图中选择Tpose任意一节点,点击设置选择",
        )
        self.SetSelTpose_widgets = self.SetSelTpose_widget.get_widgetList()
        self.SetSelTpose_widgets[1].clicked.connect(self.SetTposeNodeFunc)

        self.fbxSelWidget = PySideLib.LPathSel(
            par=self.topLay,
            l_lab="",
            buttonName="选择动捕文件",
            DialogCommit="choose fbx",
            fileType="*.fbx",
            chooseFunc="getOpenFileName",
            defaultPath=".fbx",
            groupBox="2,选择动捕文件",
        )
        self.fbxSelWidgets = self.fbxSelWidget.get_widgetList()
        self.fbxSelWidget.setText(
            r"D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\Rig\JZXCJ_DBSJ\SC001_001_SHOT1-20_001\SC001_001_SHOT1-20_001_30f_hanyang.fbx"
        )

        StepThreeGB = QGroupBox("3.传递动捕数据(设置好帧速率命令才可用)")
        StepThreeLay = QVBoxLayout()

        StepThreeGB.setLayout(StepThreeLay)
        self.transferDateBtn = QPushButton("传递动捕数据")
        self.transferDateBtn.clicked.connect(
            partial(reference_fbx_before_snooper, self.transferDateBtn)
        )
        StepThreeLay.addWidget(self.transferDateBtn)

        self.transferDateBtn.setEnabled(0)

        # self.topLay.addWidget(StepOneGB)

        self.topLay.addWidget(StepThreeGB)

        self.postProcess()
        self.setLayout(self.topLay)

        self.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.WindowMinimizeButtonHint
            | QtCore.Qt.WindowCloseButtonHint
        )

        self.setStyleSheet(
            """
                           QGroupBox{font-size:15px;}
                           QCheckBox{font-size:17px;height:20px;}
                           QPushButton{font-size:15px;height:15px;}
                           QLabel{font-size:20px;color:red;height:20px;}
                           QComboBox{height:25px;}
                           """
        )
        helpButton.setStyleSheet("height:5px;background-color:#888a42;")

    def postProcess(self) -> None:

        selfSetCtlPar = ["FKShoulder_R", "FKShoulder_L", "FKHead_M"]
        widgetList = [
            (QListWidget, "", {"addItems": selfSetCtlPar}, (0, 1, 1, 5)),
            (QPushButton, "", {"setText": "设置参数"}),
        ]
        self.SetCtlPar_widget = PySideLib.LQHVGrp(
            widgetList=widgetList,
            par=self.topLay,
            groupBox="4.设置大臂和头部的控制器global参数为10",
        )
        self.SetCtlPar_widgets = self.SetCtlPar_widget.get_widgetList()
        self.SetCtlPar_widgets[0].setFixedHeight(60)
        self.SetCtlPar_widgets[1].clicked.connect(self.setGlobalToTen)
        self.SetCtlPar_widgets[0].setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.SetCtlPar_widgets[0].itemClicked.connect(self.selectCtl)

        self.ctlToHideList = [
            "Fingers_R",
            "HipSwinger_M",
            "FKIKLeg_R",
            "FKIKLeg_L",
            "FKIKSpine_M",
            "Fingers_L",
            "controller",
            "FKIKArm_R",
            "FKIKArm_L",
        ]
        widgetList = [
            (QListWidget, "", {"addItems": self.ctlToHideList}, (0, 0, 1, 5)),
            (QPushButton, "", {"setText": "隐藏控制器"}),
        ]
        self.ctlToHide_widget = PySideLib.LQHVGrp(
            widgetList=widgetList,
            par=self.topLay,
            groupBox="5.下列控制器添加到显示层并隐藏",
        )
        self.SetCtlHide_widgets = self.ctlToHide_widget.get_widgetList()
        self.SetCtlHide_widgets[0].setMinimumHeight(65)
        self.SetCtlHide_widgets[1].clicked.connect(self.hideCtl)

        # frameRangeLay=QHBoxLayout()
        # StepThreeLay.addLayout(frameRangeLay)

        # frameRangeLay.addWidget(QLabel(u'帧范围:'))
        # StepThreeLay.addWidget(QLineEdit('0'))
        # StepThreeLay.addWidget(QLineEdit('0'))
        widgetList = [
            (QLineEdit, "", {"setText": "0"}),
            (QLineEdit, "", {"setText": "200"}),
        ]
        self.bakeRange_widget = PySideLib.LQHVGrp(
            widgetList=widgetList, par=self.topLay, groupBox="6.设置烘焙范围"
        )

        widgetList = [(QPushButton, "", {"setText": "烘焙动补数据到控制器"})]
        self.bakeCtl_widget = PySideLib.LQHVGrp(
            widgetList=widgetList, par=self.topLay, groupBox="7.烘焙动补数据到控制器"
        )
        self.bakeCtl_widget.get_widgetList()[0].clicked.connect(self.bakeCtlFunc)

        widgetList = [(QPushButton, "", {"setText": "移除动捕Fbx文件及临时数据"})]
        self.RemoveData = PySideLib.LQHVGrp(
            widgetList=widgetList,
            par=self.topLay,
            groupBox="8.移除动捕Fbx文件及临时数据",
        )
        self.RemoveData.get_widgetList()[0].clicked.connect(self.removeData)
        self.topLay.setSpacing(5)

    def selectCtl(self) -> None:
        cmds.select(cl=1)
        items = self.SetCtlPar_widgets[0].selectedItems()
        for item in items:
            cmds.select(item.text(), add=1)

    def bakeCtlFunc(self) -> None:
        TposeNameSpace = self.SetSelTpose_widgets[0].text().split(":")[0]
        ctls = cmds.ls(TposeNameSpace + ":*", type="nurbsCurve", l=1)
        bakeList = []
        for ctl in ctls:
            vis = cmds.getAttr(ctl + ".visibility")
            ctlShortName = cmds.listRelatives(ctl, p=1)[0]
            if vis:
                if (
                    "Face" not in ctl
                    and "MainExtra2" not in ctlShortName
                    and "MainExtra1" not in ctlShortName
                ):
                    bakeList.append(ctlShortName)
        ikList = ["IKArm_L", "PoleArm_L", "IKArm_R", "PoleArm_R"]
        ikList = [TposeNameSpace + ":" + x for x in ikList]
        bakeList += ikList

        hideCtlList = []
        for i in range(self.SetCtlHide_widgets[0].count()):
            itemText = self.SetCtlHide_widgets[0].item(i).text()
            hideCtlList.append(itemText)
        bakeList = [each for each in bakeList if each not in hideCtlList]

        sf = self.bakeRange_widget.get_widgetList()[0].text()
        ef = self.bakeRange_widget.get_widgetList()[1].text()
        cmds.bakeResults(
            bakeList,
            t=(int(sf), int(ef)),
            sb=1,
            sm=1,
            oversamplingRate=1,
            at=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
            hi="below",
            shape=1,
        )

    def removeData(self) -> None:
        TposeNode = self.SetSelTpose_widgets[0].text()
        DongbuFbxName = self.fbxSelWidgets[0].currentText()
        suffix = self.transferDateBtn.refNodeRootNode.split(":")[-1]
        if cmds.objExists(TposeNode.split(":")[0] + "FBX:" + suffix):
            cmds.file(DongbuFbxName, rr=1)
        cmds.delete(TposeNode.split(":")[0] + "_" + suffix)

    def SetTposeNodeFunc(self) -> None:

        TposeNameSpace = cmds.ls(sl=1)[0].split(":")[0]
        # TposeNameSpace = 'C_A001_HanYang_Rig:Group'
        self.SetSelTpose_widgets[0].setText(cmds.ls(sl=1)[0])
        for i in range(self.SetCtlHide_widgets[0].count()):
            itemText = self.SetCtlHide_widgets[0].item(i).text()
            self.SetCtlHide_widgets[0].item(i).setText(TposeNameSpace + ":" + itemText)
        for i in range(self.SetCtlPar_widgets[0].count()):
            itemText = self.SetCtlPar_widgets[0].item(i).text()
            self.SetCtlPar_widgets[0].item(i).setText(TposeNameSpace + ":" + itemText)
        filename = cmds.referenceQuery(TposeNameSpace + "RN", filename=1)
        DongBuDir = re.search("e:/BUG_Project/[0-9a-z_]+/?", filename, flags=re.I)
        lprint(DongBuDir.group())
        if DongBuDir:
            DongBuDir = DongBuDir.group() + "/Shot_work/DongBu/"
            lprint("DongBuDir", DongBuDir)
            lprint(os.path.exists(DongBuDir))
            if os.path.exists(DongBuDir):
                for file in os.listdir(DongBuDir):
                    if file.endswith(".fbx"):
                        self.fbxSelWidgets[0].addItem(DongBuDir + file)
            self.fbxSelWidgets[0].removeItem(0)

    def setGlobalToTen(self) -> None:
        cmds.select(cl=1)
        for i in range(self.SetCtlPar_widgets[0].count()):
            itemText = self.SetCtlPar_widgets[0].item(i).text()
            cmds.setAttr(itemText + ".Global", 10)
            cmds.select(itemText, add=1)

    def hideCtl(self) -> None:
        if cmds.objExists("Hide_Ctl"):
            cmds.delete("Hide_Ctl")
        cmds.createDisplayLayer(noRecurse=True, name="Hide_Ctl", empty=1)
        cmds.setAttr("Hide_Ctl.visibility", 0)
        for i in range(self.SetCtlHide_widgets[0].count()):
            itemText = self.SetCtlHide_widgets[0].item(i).text()
            cmds.editDisplayLayerMembers("Hide_Ctl", itemText)


global tranDoBuDataUI_Instance
tranDoBuDataUI_Instance = None


def tranDoBuDataCall(*args) -> None:
    global tranDoBuDataUI_Instance
    if sys.executable.endswith("maya.exe"):
        app = QApplication.instance()
    else:
        app = QApplication.instance() or QApplication(sys.argv)
    existing = None
    for widget in QApplication.topLevelWidgets():
        if widget.objectName() == "Lugwit_HIK_tranDoBuDataUI":
            existing = widget
            break
    if existing is not None:
        try:
            existing.close()
        except Exception:
            pass
        try:
            existing.deleteLater()
        except Exception:
            pass
        tranDoBuDataUI_Instance = None
    tranDoBuDataUI_Instance = tranDoBuDataUI()
    tranDoBuDataUI_Instance.show()
    # senondUI=setRigFileUI()
    # senondUI.show()
    if not sys.executable.endswith("maya.exe"):
        sys.exit(app.exec_())


if __name__ == "__main__":
    tranDoBuDataCall()

""" 
import sys
print(sys.executable)
from imp import reload
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\Rig')
try:
    reload(HIK_py3)
except NameError:
    import HIK_py3
HIK_py3.tranDoBuDataCall()
"""
