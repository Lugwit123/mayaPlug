# coding:utf-8
#添加模块所在路径
import os,re,sys
import maya.cmds as cmds
fileDir = os.path.dirname(__file__)
sys.path.insert(0,fileDir)
os.environ['QT_API']='PySide2'
from functools import partial


sys.path.append(os.getenv('LugwitLibDir'))
from Lugwit_Module.l_src.UILib.QTLib import PySideLib
import Lugwit_Module as LM
lprint = LM.lprint 
from imp import reload

import os,sys
from pprint import pprint
import codecs 

import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm

if not pm.pluginInfo("mayaHIK", q=1, l=1):
    pm.loadPlugin("mayaHIK")
if not pm.pluginInfo("fbxmaya", q=1, l=1):
    pm.loadPlugin("fbxmaya")
pm.mel.source("hikGlobalUtils.mel")


try:
    
    from PySide2.QtWidgets import *
    from PySide2 import QtCore
    from PySide2.QtGui import QMovie
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide import QtCore 
    import PySide.QtGui
    lprint (PySide.QtGui)

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

Root_M_joints_dict = {
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
    "Toes_R": "RightToeBase"
}


def create_hik(reference=None, name="Character1",suffix='suffix'):
    if reference is None:
        selected = pm.selected()
        if not len(selected) == 1:
            return
        reference = selected[0]
    lprint (reference,reference.name())
    if reference.name().endswith(suffix):
        joints = {joint.name().split(
            ":")[-1].split("_")[-1]: joint for joint in reference.listRelatives(ad=1, type="joint")}
    else:
        # Root_M
        joints = {Root_M_joints_dict[joint.name().split(":")[-1].split("|")[-1]]: joint for joint in reference.listRelatives(ad=1, type="joint")
                  if joint.name().split(":")[-1].split("|")[-1] in list(Root_M_joints_dict.keys())}
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
    """
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
    """
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
    #lprint((u'创建骨骼名称为{},复制于来自{}'.format(prefix+"_"+name, con)))
    joint = pm.joint(con, n=prefix+"_"+name)
    #lprint((u'设置骨骼{}父级为{}'.format(joint, parent)))
    joint.setParent(parent)
    #lprint((u'对新生成的的骨骼{}和她的母亲{}创建父子约束'.format(joint, con)))
    #lprint(u'用生成的骨骼来驱动她的母亲')
    create_parentConstraint = ConstraintType(joint, con)
    #lprint((u'把{}的父级为{}'.format(create_parentConstraint, reference)))
    pm.parent(create_parentConstraint, reference)
    return joint


def create_joints(prefix, names, cons, parent, reference,ConstraintType=pm.parentConstraint):
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
        lprint(('adv_finger', adv_finger))
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


def create_hik_joints(prefix,Suffix,cons):
    # 创建HIK骨骼
    # 创建一个Locator
    
    reference = pm.spaceLocator(n=prefix+'_'+Suffix)
    # 创建Hips骨骼,命名为prefix_Hips,Hip的父节点为新创建的Locator
    # create_joint的参数为前缀,名称,复制于哪个节点,父节点
    # Hip因为意思为髋关节
    hips = create_joint(prefix, "Hips", cons[0], reference, reference)
    # 创建腿部节点,腿部节点不止一个,所以用列表来存储
    # create_joints的参数为:
    #                       前缀,名称,复制于哪个节点,父节点,顶级Locator
    l_leg = create_joints(
        prefix, ["Left"+name for name in hik_legs], cons[1], hips, reference)
    pprint(('new legs joints', l_leg))
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

        
    lprint(('l_finger', l_finger))
    
    # 创建约束 在
    # lprint((u'使用{}节点父子约束{}'.format(
    #     l_leg[-2], cons[1][-2].name().replace("FKAnkle", "IKLeg"))))
    create_parentConstraint = pm.parentConstraint(
        l_leg[-2], cons[1][-2].name().replace("FKAnkle", "IKLeg"), mo=1)
    #lprint((u'设置约束{}的父节点为{}'.format(create_parentConstraint, reference)))
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
    lprint (locals())
    pm.parent(pm.parentConstraint(hips, get_con(
        prefix + ":RootX_M"), mo=1), reference)
    pm.parent(pm.pointConstraint(hips, get_con(
        prefix + ":Main"), mo=1), reference)
    return reference


def rig_hik():
    cons = find_cons()
    reference = create_hik_joints("Rig", cons)
    create_hik(reference=reference, name="Character1")


def reference_fbx(sender):# 传递动捕数据
    '''实现原理:
    1,根据在Adv_Tpose的Fk骨骼的位置创建一套新的骨骼,骨骼命名为HIK命名规则
    每根骨骼父子约束Fk的每根骨骼
    1.创建一套骨骼定义,骨骼的位置来自于Adv_Tpose的骨骼
    
    2,使用动捕的骨骼数据通过HIK驱动第一步创建的骨骼定义
    
    '''

    con = tranDoBuDataUI_Instance.SetSelTpose_widgets[0].text()#Tpose节点名称
    con=pm.ls(con)[0]#Tpose节点名称
    if not con.isReferenced():
        QMessageBox.information(None, '消息提示!',
                                "小哥哥,你选择的文件需要是引用的形式额")
        return
    path= tranDoBuDataUI_Instance.fbxSelWidgets[0].currentText()

    prefix = con.namespace() # 获取Tpose节点的名称控件
    cons = find_cons(prefix)  # 寻找Tpose中根骨骼,腿部,脊柱,手臂和脖子和手指的骨骼
    lprint(u'从Tpose中寻找根骨骼,腿部,脊柱,手臂和脖子和手指的骨骼',
           prefix, find_cons(prefix))
    lprint (('cons', list(enumerate(cons))))
    
    
    
    
    returnNewNodes=pm.createReference(
        path, type="FBX", namespace=prefix[:-1]+"FBX", referenceNode=prefix[:-1]+"FbxRN"
        ,returnNewNodes=True)

    locator_nodes = [node for node in returnNewNodes if node.type() == "locator"]
    lprint(locator_nodes)
    locator_node = locator_nodes[0]
    refNodeNameSpace=locator_node.namespace()[:-1]
    refNodeRootNode=locator_node.getParent(-1)
    print("refNodeRootNode",locator_node,type(locator_node))
    suffix = refNodeRootNode.split(':')[-1]
    # 传入Tpose的名称空间和新的骨骼名称
    reference = create_hik_joints(prefix[:-1], 
                                suffix,
                                cons)  
    
    # 创建HIK骨骼,参数1为创建的Locator节点,参数2为HIK角色定义名称
    rig = create_hik(reference=reference, name=prefix[:-1]+"Rig",suffix=suffix)

    
    
    if pm.objExists("|"+refNodeRootNode):
        ani = create_hik(
            pm.PyNode("|"+refNodeRootNode), refNodeNameSpace+":Ani",suffix=suffix)
        pm.mel.hikCharacterLock(rig, 1, 0)
        lprint (ani)
        pm.mel.hikSetCharacterInput(rig, ani)
    elif pm.objExists("|"+refNodeNameSpace+":Root_M"):
        # 摆tpose
        lprint('Root_M')
        pm.joint("|"+refNodeNameSpace+":Root_M", e=True, apa=True, ch=True)
        pm.PyNode(refNodeNameSpace+":Shoulder_R").ry.set(-58.279)
        pm.PyNode(refNodeNameSpace+":Elbow_R").rz.set(-30.764)
        pm.PyNode(refNodeNameSpace+":Wrist_R").rz.set(10.857)
        pm.PyNode(refNodeNameSpace+":Knee_R").rz.set(9.143)
        pm.PyNode(refNodeNameSpace+":Shoulder_L").ry.set(-58.279)
        pm.PyNode(refNodeNameSpace+":Elbow_L").rz.set(-30.764)
        pm.PyNode(refNodeNameSpace+":Wrist_L").rz.set(10.857)
        pm.PyNode(refNodeNameSpace+":Knee_L").rz.set(9.143)
        pm.PyNode(refNodeNameSpace+":Chest_M").rz.set(19.571)
        # pm.PyNode(refNodeNameSpace+":Neck_M").rz.set(-51.562)
        # pm.PyNode(refNodeNameSpace+":Head_M").rz.set(32.963)

        #
        ani = create_hik(
            pm.PyNode("|"+refNodeNameSpace+":Root_M"), refNodeNameSpace+"Ani")
        pm.mel.hikCharacterLock(rig, 1, 0)
        pm.mel.hikSetCharacterInput(rig, ani)
    sender.refNodeRootNode=refNodeRootNode


class tranDoBuDataUI(QWidget):
    def __init__(self, parent = None):
        super(tranDoBuDataUI, self).__init__(parent)
        self.setObjectName('Lugwit_HIK_tranDoBuDataUI')
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowTitle(u'导入并烘焙动捕数据')
        self.resize(400, 200)
        self.topLay = QVBoxLayout()
        helpButtonLay=QHBoxLayout()
        helpButton=QPushButton('?')
        
        helpButtonLay.addWidget(helpButton)
        helpButton.setToolTip(u'这里录制了一个好看的小视频✺◟(∗❛ัᴗ❛ั∗)◞✺')
        helpButtonLay.setAlignment(Qt.AlignLeft)
        self.topLay.addLayout(helpButtonLay)
        helpButton.clicked.connect(lambda *args:os.startfile(
            LM.Lugwit_mayaPluginPath+r'\mov_help\bakeDongDu.mp4'))
        
        widgetList=[(QRadioButton,'',{'setText':'24'}),(QRadioButton,'',{'setText':'25'}),
                    (QRadioButton,'',{'setText':'30'}),(QRadioButton,'',{'setText':'60'})]
        self.setFps_widget=PySideLib.LQHVGrp(btnGrp=1,par=self.topLay,widgetList=widgetList,
                                            groupBox=u'请先设置好帧速率')
        self.setFps_widgets=self.setFps_widget.get_widgetList()
        btnGrp=self.setFps_widget.get_btnGrp()
        self.setFps_widget.get_groupBox().setStyleSheet('color:red')
        def setFps_widget_clicked():
            checkedBtn=btnGrp.checkedButton()
            checkedBtnText=checkedBtn.text()
            cmds.currentUnit(t=checkedBtnText+'fps')
            self.setFps_widget.get_groupBox().setStyleSheet('')
            self.transferDateBtn.setEnabled(1)
        btnGrp.buttonClicked.connect(setFps_widget_clicked)
        
        widgetList=[(QLineEdit,'',{u'setText':u'C_A001_HanYang_Rig:Group','setReadOnly':1},(0,1,1,3)),
                    (QPushButton,'',{u'setText':u'设置选择'})]
        self.SetSelTpose_widget=PySideLib.LQHVGrp(widgetList=widgetList,par=self.topLay,groupBox=u'1,请在大纲视图中选择Tpose任意一节点,点击设置选择')
        self.SetSelTpose_widgets=self.SetSelTpose_widget.get_widgetList()
        self.SetSelTpose_widgets[1].clicked.connect(self.SetTposeNodeFunc)

        self.fbxSelWidget=PySideLib.LPathSel(par=self.topLay,l_lab='',buttonName=u'选择动捕文件',DialogCommit='choose fbx',fileType='*.fbx',chooseFunc='getOpenFileName',defaultPath='.fbx',groupBox=u'2,选择动捕文件')
        self.fbxSelWidgets=self.fbxSelWidget.get_widgetList()
        self.fbxSelWidget.setText(r"D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\Rig\JZXCJ_DBSJ\SC001_001_SHOT1-20_001\SC001_001_SHOT1-20_001_30f_hanyang.fbx")
        
        StepThreeGB=QGroupBox(u'3.传递动捕数据(设置好帧速率命令才可用)')
        StepThreeLay=QVBoxLayout()


        StepThreeGB.setLayout(StepThreeLay)
        self.transferDateBtn=QPushButton(u'传递动捕数据')
        self.transferDateBtn.clicked.connect(partial(reference_fbx,self.transferDateBtn))
        StepThreeLay.addWidget(self.transferDateBtn)

        

        self.transferDateBtn.setEnabled(0)
        

        #self.topLay.addWidget(StepOneGB)

        self.topLay.addWidget(StepThreeGB)
        
        
        self.postProcess()
        self.setLayout(self.topLay)
        
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |   # 使能最小化按钮
                            QtCore.Qt.WindowType.WindowCloseButtonHint |      # 使能关闭按钮
                            QtCore.Qt.WindowStaysOnTopHint) 
        
        self.setStyleSheet('''
                           QGroupBox{font-size:15px;}
                           QCheckBox{font-size:17px;height:20px;}
                           QPushButton{font-size:15px;height:15px;}
                           QLabel{font-size:20px;color:red;height:20px;}
                           QComboBox{height:25px;}
                           '''
                           )
        helpButton.setStyleSheet('height:5px;background-color:#888a42;')
    def postProcess(self):

        selfSetCtlPar=['FKShoulder_R',
                    'FKShoulder_L',
                    'FKHead_M']
        widgetList=[(QListWidget,'',{'addItems':selfSetCtlPar},(0,1,1,5)),(QPushButton,'',{'setText':u'设置参数'})]
        self.SetCtlPar_widget=PySideLib.LQHVGrp(widgetList=widgetList,par=self.topLay,groupBox=u'4.设置大臂和头部的控制器global参数为10')
        self.SetCtlPar_widgets=self.SetCtlPar_widget.get_widgetList()
        self.SetCtlPar_widgets[0].setFixedHeight(60)
        self.SetCtlPar_widgets[1].clicked.connect(self.setGlobalToTen)    
        self.SetCtlPar_widgets[0].setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.SetCtlPar_widgets[0].itemClicked.connect(self.selectCtl)


        self.ctlToHideList=['Fingers_R',
                            'HipSwinger_M',
                            'FKIKLeg_R',
                            'FKIKLeg_L',
                            'FKIKSpine_M',
                            'Fingers_L',
                            'controller',
                            'FKIKArm_R',
                            'FKIKArm_L']
        widgetList=[(QListWidget,'',{'addItems':self.ctlToHideList},(0,0,1,5)),
                    (QPushButton,'',{'setText':u"隐藏控制器"})]
        self.ctlToHide_widget=PySideLib.LQHVGrp(widgetList=widgetList,par=self.topLay,groupBox=u'5.下列控制器添加到显示层并隐藏')
        self.SetCtlHide_widgets=self.ctlToHide_widget.get_widgetList()
        self.SetCtlHide_widgets[0].setMinimumHeight(65)
        self.SetCtlHide_widgets[1].clicked.connect(self.hideCtl)

        # frameRangeLay=QHBoxLayout()
        # StepThreeLay.addLayout(frameRangeLay)
        
        # frameRangeLay.addWidget(QLabel(u'帧范围:'))
        # StepThreeLay.addWidget(QLineEdit('0'))
        # StepThreeLay.addWidget(QLineEdit('0'))
        widgetList=[(QLineEdit,'',{'setText':u'0'}),
                    (QLineEdit,'',{'setText':u'200'})]
        self.bakeRange_widget=PySideLib.LQHVGrp(widgetList=widgetList,par=self.topLay,
                                              groupBox=u'6.设置烘焙范围')

        widgetList=[(QPushButton,'',{'setText':u'烘焙动补数据到控制器'})]
        self.bakeCtl_widget=PySideLib.LQHVGrp(widgetList=widgetList,par=self.topLay,groupBox=u'7.烘焙动补数据到控制器')
        self.bakeCtl_widget.get_widgetList()[0].clicked.connect(self.bakeCtlFunc)




        widgetList=[(QPushButton,'',{'setText':u"移除动捕Fbx文件及临时数据"})]
        self.RemoveData=PySideLib.LQHVGrp(widgetList=widgetList,par=self.topLay,groupBox=u'8.移除动捕Fbx文件及临时数据')
        self.RemoveData.get_widgetList()[0].clicked.connect(self.removeData)
        self.topLay.setSpacing(5);
    
    def selectCtl(self):
        cmds.select(cl=1)
        items = self.SetCtlPar_widgets[0].selectedItems()
        for item in items:
            cmds.select(item.text(),add=1)

        
    def bakeCtlFunc(self):
        TposeNameSpace=self.SetSelTpose_widgets[0].text().split(':')[0]
        ctls=cmds.ls(TposeNameSpace+':*',type='nurbsCurve',l=1)
        bakeList=[]
        for ctl in ctls:
            vis=cmds.getAttr(ctl+'.visibility')
            ctlShortName=cmds.listRelatives(ctl,p=1)[0]
            if vis:
                if 'Face' not in ctl and 'MainExtra2' not in ctlShortName and 'MainExtra1' not in ctlShortName:
                    bakeList.append(ctlShortName)
        ikList=['IKArm_L','PoleArm_L','IKArm_R','PoleArm_R']
        ikList=[TposeNameSpace+':'+x for x in ikList]
        bakeList+=ikList
        
        hideCtlList=[]
        for i in range(self.SetCtlHide_widgets[0].count()):
            itemText=self.SetCtlHide_widgets[0].item(i).text()
            hideCtlList.append(itemText)
        bakeList=[each for each in bakeList if each not in hideCtlList]
            
        sf = self.bakeRange_widget.get_widgetList()[0].text()
        ef = self.bakeRange_widget.get_widgetList()[1].text()
        cmds.bakeResults(bakeList, t=(int(sf), int(ef)), sb=1, sm=1, 
                         oversamplingRate=1, at=[
                        "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"], 
                        hi="below", shape=1)
            
    def removeData(self):
        TposeNode=self.SetSelTpose_widgets[0].text()
        DongbuFbxName=self.fbxSelWidgets[0].currentText()
        suffix=self.transferDateBtn.refNodeRootNode.split(':')[-1]
        if cmds.objExists(TposeNode.split(':')[0]+'FBX:'+suffix):
            cmds.file(DongbuFbxName,rr=1)
        cmds.delete(TposeNode.split(':')[0]+'_'+suffix)
    
    def SetTposeNodeFunc(self):
        
        TposeNameSpace=cmds.ls(sl=1)[0].split(':')[0]
        # TposeNameSpace = 'C_A001_HanYang_Rig:Group'
        self.SetSelTpose_widgets[0].setText(cmds.ls(sl=1)[0])   
        for i in range(self.SetCtlHide_widgets[0].count()):
            itemText=self.SetCtlHide_widgets[0].item(i).text()
            self.SetCtlHide_widgets[0].item(i).setText(TposeNameSpace+':'+itemText)
        for i in range(self.SetCtlPar_widgets[0].count()):
            itemText=self.SetCtlPar_widgets[0].item(i).text()
            self.SetCtlPar_widgets[0].item(i).setText(TposeNameSpace+':'+itemText)
        filename=cmds.referenceQuery(TposeNameSpace+'RN',filename=1)
        DongBuDir=re.search('e:/BUG_Project/[0-9a-z_]+/?',filename,flags=re.I)
        lprint (DongBuDir.group())
        if DongBuDir:
            DongBuDir=DongBuDir.group()+'/Shot_work/DongBu/'
            lprint ('DongBuDir',DongBuDir)
            lprint (os.path.exists(DongBuDir))
            if os.path.exists(DongBuDir):
                for file in os.listdir(DongBuDir):
                    if file.endswith('.fbx'):
                        self.fbxSelWidgets[0].addItem(DongBuDir+file)
            self.fbxSelWidgets[0].removeItem(0)

    
    def setGlobalToTen(self):
        cmds.select(cl=1)
        for i in range(self.SetCtlPar_widgets[0].count()):
            itemText=self.SetCtlPar_widgets[0].item(i).text()
            cmds.setAttr(itemText+'.Global',10)
            cmds.select(itemText,add=1)
            
            
    def hideCtl(self):
        if cmds.objExists('Hide_Ctl' ):
            cmds.delete('Hide_Ctl')
        cmds.createDisplayLayer( noRecurse=True, name='Hide_Ctl' ,empty=1)
        cmds.setAttr('Hide_Ctl.visibility',0)
        for i in range(self.SetCtlHide_widgets[0].count()):
            itemText=self.SetCtlHide_widgets[0].item(i).text()
            cmds.editDisplayLayerMembers( 'Hide_Ctl', itemText )


''' 
import sys
sys.path.append(r'Z:\plug_in\Lugwit_plug\mayaPlug\l_scripts\Rig')
try:
    reload( HIK)
except NameError:
    import HIK
HIK.main()
'''    


global tranDoBuDataUI_Instance 
tranDoBuDataUI_Instance = None

def tranDoBuDataCall(*args):
    global tranDoBuDataUI_Instance
    if sys.executable.endswith('maya.exe'):
        app = QApplication.instance()
    else:
        app = QApplication.instance() or QApplication(sys.argv)
    existing = None
    for widget in QApplication.topLevelWidgets():
        if widget.objectName() == 'Lugwit_HIK_tranDoBuDataUI':
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
    if not sys.executable.endswith('maya.exe'):
        sys.exit(app.exec_())

if __name__=='__main__':
    tranDoBuDataCall()
