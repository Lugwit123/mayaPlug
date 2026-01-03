# -*- coding: utf-8 -*- 
import maya.mel as mel
import maya.cmds as cm
import re
import os
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import __version__
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance

version = 1.2

def has_invalid_vert(obj):
    u'''
    检查物体是否有无面的点
    :param obj: 'body'
    :return: bool
    '''
    m_list = om.MSelectionList()
    m_list.add(obj)
    
    dag_path = m_list.getDagPath(0)
    #print(dag_path.fullPathName())
    try:
        itVertex = om.MItMeshVertex(dag_path)
    except:
        #模型可能没有点
        return False
    else:
        while not itVertex.isDone():
            itVertex.next()
            
            if not itVertex.getConnectedFaces():
                return True
                break
        return False

def clean_model(model):
    u'''清除多余的模型点'''
    cm.select(model,r = True)
    vtx_count_old = cm.polyEvaluate(model,v = True)
    poly_clean_node = cm.polyClean(ch = True)
    vtx_count_new = cm.polyEvaluate(model,v = True)
    if vtx_count_old == vtx_count_new:
        cm.delete(poly_clean_node)
    else:
        mel.eval('''doBakeNonDefHistory( 1, {"prePost" });''')
    
def get_all_models():
    model_set = {cm.listRelatives(mesh,p = True,pa = True)[0] \
    for mesh in cm.ls(type = 'mesh') if not cm.getAttr(mesh + '.io')}
    model_list = list(model_set)
    model_list.sort()
    return model_list

def get_all_invalid_vert_models():
    model_list = get_all_models()
    invalid_vert_model_list = list()
    for model in model_list:
        if has_invalid_vert(model):
            invalid_vert_model_list.append(model)
    return invalid_vert_model_list

def clean_all_models():
    u'''
    清除场景内所有模型的非法点
    '''
    model_list = get_all_invalid_vert_models()
    if model_list:
        for model in model_list:
            clean_model(model)


def get_wrong_shader_name_list():
    u'''检查材质节点命名(不检查引用的节点)'''
    all_shader_node_set = set()
    surface_list = cm.listNodeTypes( 'shader')
    surface_list.extend(cm.listNodeTypes( 'texture'))
    surface_list.extend(cm.listNodeTypes( 'utility'))
    for index in range(len(surface_list)):
        node_list = cm.ls(type = surface_list[index])
        all_shader_node_set.update(set(node_list))
    sg_list = cm.ls(type = 'shadingEngine')
    all_shader_node_set.update(set(sg_list))
    all_shader_node_list = list(all_shader_node_set)
    #只对非引用节点作修改
    all_shader_node_list = [node for node in all_shader_node_list if \
        not cm.referenceQuery(node,isNodeReferenced = True)]
    all_shader_node_list.sort()
    wrong_node_list = list()
    for node in all_shader_node_list:
        if node.startswith('_') or node.endswith('_') or ':' in node or re.search('_{2,}',node):
            wrong_node_list.append(node)
    return wrong_node_list

def get_right_shader_name(node):
    node = node.strip('_')
    node = node.replace(':','_')
    return(re.sub('_{2,}','_',node))

def fix_shader_name_list(node_list):
    for node in node_list:
        new_name = get_right_shader_name(node)
        try:
            cm.rename(node,new_name)
        except:
            pass

def fix_all_shader_names_from_scene():
    u'''
    修复场景内所有材质类型的节点的名字
    '''
    wrong_node_list = get_wrong_shader_name_list()
    if wrong_node_list:
        fix_shader_name_list(wrong_node_list)

# clean_all_models()
# fix_all_shader_names_from_scene()


#检查模型transform是否归零，不归零会影响aiTriplanar节点的效果
#因为aiTriplanar有world和object这些模式，制作人员使用的一般都是object模式
#
#

#查找层级结构是否正确(主要能否因此得到角色和其他物体)


#查看摄像机camera aperture 是否36 x 36

#检查aiSkyDomeLight缩放值是否三个轴相同

#shader和sg名字是否匹配?


#检查要导出的模型的sg，是不是连的非arnold材质球，是的话报错
def get_sg(obj):
    u'''物体的sg列表'''
    sg_list = list()
    t_sg_list = cm.listConnections(obj,s = False,type = 'shadingEngine')
    shape_list = cm.listRelatives(obj,s = True,pa = True,ni = True)
    if t_sg_list:
        sg_list.extend(t_sg_list)
    if shape_list:
        for shape in shape_list:
            shape_sg_list = cm.listConnections(shape,s = False,type = 'shadingEngine')
            sg_list.extend(shape_sg_list)
    return list(set(sg_list))

def is_shader_arnold(sg):
    u'''sg节点的surface shader是否arnold shader'''
    #如果aiSurfaceShader有连接就把它当作surface shader
    shader_list = cm.listConnections(sg + '.aiSurfaceShader',d = False)
    shader = shader_list[0] if shader_list else ''
    #否则就找surfaceShader的连接
    if not shader_list:
        shader_list = cm.listConnections(sg + '.surfaceShader',d = False) 
        shader = shader_list[0] if shader_list else ''
    mtoa_node_type_list = cm.pluginInfo('mtoa',dependNode = True,q = True)
    if shader:
        if cm.nodeType(shader) in mtoa_node_type_list:
            return True
    return False

def is_obj_shader_arnold(obj):
    u'''物体的材质是否arnold'''
    obj_sg_list = get_sg(obj)
    if obj_sg_list:
        for sg in obj_sg_list:
            if not is_shader_arnold(sg):
                return False
        return True
    return False

def get_wrong_shader_obj_list(obj):
    u'''obj里面所有的模型有哪些不是arnold材质球的'''
    #这里面的ni好像是废的
    mesh_list = cm.listRelatives(obj,ad = True,type = 'mesh',ni = True,pa = True)
    wrong_obj_list = list()
    if mesh_list:
        sub_obj_set = {cm.listRelatives(mesh,p = True,
                                        pa = True)[0] for mesh in mesh_list if not cm.getAttr('%s.io'%mesh)}
        wrong_obj_list = [sub_obj for sub_obj in sub_obj_set if not is_obj_shader_arnold(sub_obj)]
    return wrong_obj_list

def get_all_wrong_shader_obj_list():
    obj_list = cm.ls(assemblies=True)
    wrong_list = []
    for obj in obj_list:
        wrong_list.extend(get_wrong_shader_obj_list(obj))
    return wrong_list

def get_wrong_value_cam_list():
    u'''
    返回参数值错误的摄像机
    camera aperture(inch):1.417 1.417
    camera aperture(mm):36.000 36.000
    如果摄像机参数值不是上面所示，导进houdini会显示错误
    :return:list
    '''
    camera_list = cm.ls(type = 'camera')
    wrong_cam_list = list()
    for cam in camera_list:
        cam_transform = cm.listRelatives(cam,p = True,pa = True)[0]
        if cam_transform in ['persp','top','front','side']:
            continue
        if cm.getAttr('%s.orthographic'%cam):
            continue
        if round(cm.getAttr('%s.horizontalFilmAperture'%cam),3) != 1.417:
            wrong_cam_list.append(cam_transform)
            continue
        if round(cm.getAttr('%s.verticalFilmAperture'%cam),3) != 1.417:
            wrong_cam_list.append(cam_transform)
    return wrong_cam_list

def fix_all_wrong_value_cam_list():
    cam_list = get_wrong_value_cam_list()
    if cam_list:
        for cam in cam_list:
            try:
                cm.setAttr('%s.horizontalFilmAperture'%cam,1.4173228346456694)
                cm.setAttr('%s.verticalFilmAperture'%cam,1.4173228346456694)
            except:
                pass

def get_wrong_value_aiSkyDomeLights():
    wrong_aiSkyDomeLight_list = []
    skyDomeLight_list = cm.ls(type = 'aiSkyDomeLight')
    for light in skyDomeLight_list:
        light_transform = cm.listRelatives(light,p = True,pa = True)[0]
        scale = cm.getAttr('%s.s'%light_transform)
        if round(scale[0][0],3) != round(scale[0][1],3) or round(scale[0][0],3) != round(scale[0][2],3):
            wrong_aiSkyDomeLight_list.append(light_transform)
    return wrong_aiSkyDomeLight_list

def fix_all_wrong_value_aiSkyDomeLights():
    light_list = get_wrong_value_aiSkyDomeLights()
    if light_list:
        for light in light_list:
            try:
                sx = cm.getAttr('%s.sx'%light)
                cm.setAttr('%s.sy' % light, sx)
                cm.setAttr('%s.sz' % light, sz)
            except:
                pass


def get_all_namespace_node_list():
    cm.namespace(setNamespace=':')
    namespaces = cm.namespaceInfo(listOnlyNamespaces=True)
    all_nodes = []
    for ns in namespaces:
        nodes = cm.namespaceInfo(ns, listOnlyDependencyNodes=True, recurse=True, dagPath=True)
        if nodes:
            all_nodes.extend(nodes)
    # all_nodes = list(set(all_nodes))
    all_nodes.sort()
    return all_nodes


def deleteNamespace(ns):
    sub_ns_list = cm.namespaceInfo(ns, listOnlyNamespaces=True)
    if sub_ns_list:
        for sub_ns in sub_ns_list:
            deleteNamespace(sub_ns)
    cm.namespace(removeNamespace=ns, mergeNamespaceWithParent=True)


def deleteAllNamespaces():
    cm.namespace(setNamespace=':')
    namespaces = cm.namespaceInfo(listOnlyNamespaces=True)
    for ns in namespaces:
        if ns not in ['UI', 'shared']:
            deleteNamespace(ns)

#arnold 灯光属性值检查
def is_light_value_right(light_shape):
    u'''
    arnold灯光的值是否正确，主要检查visibility下面的值，
    因为maya中这些值可以>1，houdini中不可以，
    所以这些参数>1将被认为是错误
    '''
    attr_list = ['aiCamera', 'aiTransmission', 'aiDiffuse',
                 'aiSpecular', 'aiSss', 'aiIndirect', 'aiVolume']
    for attr in attr_list:
        if cm.attributeQuery(attr, n=light_shape, ex=True):
            if cm.getAttr(light_shape + '.' + attr) > 1:
                return False
    return True


def fix_light_value(light):
    attr_list = ['aiCamera', 'aiTransmission', 'aiDiffuse',
                 'aiSpecular', 'aiSss', 'aiIndirect', 'aiVolume']
    light_shape = cm.listRelatives(light, s=True, pa=True)[0]
    for attr in attr_list:
        if cm.attributeQuery(attr, n=light_shape, ex=True):
            if cm.getAttr(light_shape + '.' + attr) > 1:
                cm.setAttr(light_shape + '.' + attr, 1)


def get_all_wrong_value_lights():
    light_list = cm.ls(cm.ls("*.lightData", o=True), dag=True)
    wrong_light_list = []
    for light in light_list:
        if not is_light_value_right(light):
            wrong_light_list.append(cm.listRelatives(light, p=True, pa=True)[0])
    return wrong_light_list


def fix_all_wrong_value_lights():
    wrong_light_list = get_all_wrong_value_lights()
    for light in wrong_light_list:
        fix_light_value(light)


def get_non_zero_transform_from_prop():
    root_obj_list = cm.ls(assemblies=True)
    has_prop = False
    non_zero_transform_list = []

    for obj in root_obj_list:
        if obj.lower() == 'prop':
            has_prop = True
            transform_list = cm.listRelatives(obj, ad=True, type='transform', pa=True)
            for transform in transform_list:
                if cm.getAttr('%s.t' % transform) != [(0, 0, 0)]:
                    non_zero_transform_list.append(transform)
                    continue
                if cm.getAttr('%s.r' % transform) != [(0, 0, 0)]:
                    non_zero_transform_list.append(transform)
                    continue
                if cm.getAttr('%s.s' % transform) != [(1, 1, 1)]:
                    non_zero_transform_list.append(transform)
                    continue
    return has_prop, non_zero_transform_list


#渲染前设置
def setting_before_render():
    u'''
    maya文件渲染前的设置，需要做这些设置，才能让maya > Houdini转换成功
    '''
    #忽略置换
    cm.setAttr('defaultArnoldRenderOptions.ignoreDisplacement',1)

    mesh_list = [mesh for mesh in cm.ls(type = 'mesh') if not cm.getAttr(mesh + '.io')]
    for mesh in mesh_list:
        #模型的细分关闭?
        cm.setAttr(mesh + '.aiSubdivType',0)
        #模型不显示smooth
        if cm.getAttr(mesh + '.displaySmoothMesh'):
            cm.setAttr(mesh + '.displaySmoothMesh',0)
    #关闭aces设置
    #把file贴图都改成sRgb模式

#houdini端渲染前需要做的设置:
#1.忽略置换


def getMayaWin():
    ptr = omui.MQtUtil.mainWindow()
    mayaWin = wrapInstance(long(ptr), QWidget)
    return mayaWin

class CheckAssetWindow(QWidget):
    def __init__(self,parent = None):
        super(CheckAssetWindow,self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose,True)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'CHECK MTOA ASSET TOOL    v%.1f'%version)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__),'check_asset.ui')
        file = QFile(ui_path)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file,self)
        self.ui.layout().setContentsMargins(5,5,5,5)
        self.ui.layout().setSpacing(5)
        layout.addWidget(self.ui)
        file.close()

        check_model = QStandardItemModel()
        self.ui.checklistView.setModel(check_model)

        self.ui.select_all_btn.clicked.connect(self.select_all_check)
        self.ui.select_none_btn.clicked.connect(self.select_none_check)
        self.ui.checkBtn.clicked.connect(self.check_asset)
        self.ui.fixBtn.clicked.connect(self.fix_asset)
        self.ui.check_result_textBrowser.selectionChanged.connect(self.select)

        check_item_list = [u'无效的模型点',u'带空间名的节点',u'材质节点命名',u'摄像机参数',
                           u'aiSkyDomeLight缩放值',u'非arnold材质物体',u'prop物体变换归零',u'arnold灯光参数值']
        for check_item in check_item_list:
            item = QStandardItem(check_item)
            item.setCheckable(True)
            item.setCheckState(Qt.Checked)
            check_model.appendRow(item)

    def select(self):
        text = self.ui.check_result_textBrowser.textCursor().selectedText()
        names = re.findall("[\w.:\|\[\]]+", text)
        if not names:
            return
        names = [name for name in names if cm.objExists(name)]
        if not names:
            return
        selected = cm.ls(names)
        if not selected:
            return
        cm.select(selected,ne = True)

    def select_check(self,all = True):
        check_model = self.ui.checklistView.model()
        check_model_count = check_model.rowCount()
        if check_model_count:
            for row in range(check_model_count):
                item = check_model.item(row)
                if all:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)

    def select_all_check(self):
        self.select_check()

    def select_none_check(self):
        self.select_check(False)

    def check_asset(self):
        result_text = u''

        check_model = self.ui.checklistView.model()

        item0 = check_model.item(0)
        if item0.checkState() == Qt.Checked:
            invalid_vert_model_list = get_all_invalid_vert_models()
            result_text += u'含有无效点的模型:\n'
            if invalid_vert_model_list:
                result_text += '\n'.join(invalid_vert_model_list)
                result_text += '\n'
            else:
                result_text += u'无\n'
            result_text += '\n'

        item1 = check_model.item(1)
        if item1.checkState() == Qt.Checked:
            namespace_node_list = get_all_namespace_node_list()
            result_text += u'带空间名的节点:\n'
            if namespace_node_list:
                result_text += '\n'.join(namespace_node_list)
                result_text += '\n'
            else:
                result_text += u'无\n'
            result_text += '\n'

        item2 = check_model.item(2)
        if item2.checkState() == Qt.Checked:
            wrong_shader_name_list = get_wrong_shader_name_list()
            result_text += u'错误的材质节点命名:\n'
            if wrong_shader_name_list:
                result_text += '\n'.join(wrong_shader_name_list)
                result_text += '\n'
            else:
                result_text += u'无\n'
            result_text += '\n'

        item3 = check_model.item(3)
        if item3.checkState() == Qt.Checked:
            wrong_cam_list = get_wrong_value_cam_list()
            result_text += u'参数错误的摄像机:\n'
            if wrong_cam_list:
                result_text += '\n'.join(wrong_cam_list)
                result_text += '\n'
            else:
                result_text += u'无\n'
            result_text += '\n'

        item4 = check_model.item(4)
        if item4.checkState() == Qt.Checked:
            wrong_aiSkyDomeLight_list = get_wrong_value_aiSkyDomeLights()
            result_text += u'参数错误的aiSkyDomeLight:\n'
            if wrong_aiSkyDomeLight_list:
                result_text += '\n'.join(wrong_aiSkyDomeLight_list)
                result_text += '\n'
            else:
                result_text += u'无\n'
            result_text += '\n'

        item5 = check_model.item(5)
        if item5.checkState() == Qt.Checked:
            wrong_shader_obj_list = get_all_wrong_shader_obj_list()
            result_text += u'非arnold材质物体:\n'
            if wrong_shader_obj_list:
                result_text += '\n'.join(wrong_shader_obj_list)
                result_text += '\n'
            else:
                result_text += u'无\n'
            result_text += '\n'

        item6 = check_model.item(6)
        if item6.checkState() == Qt.Checked:
            has_prop,non_zero_transform_list = get_non_zero_transform_from_prop()
            result_text += u'prop组内移动/旋转/缩放有值的物体:\n'
            if not has_prop:
                result_text += u'没有prop组\n'
            else:
                if non_zero_transform_list:
                    result_text += '\n'.join(non_zero_transform_list)
                    result_text += '\n'
                else:
                    result_text += u'无\n'
            result_text += '\n'

        get_non_zero_transform_from_prop

        item7 = check_model.item(7)
        if item7.checkState() == Qt.Checked:
            wrong_light_list = get_all_wrong_value_lights()
            result_text += u'arnold灯光参数值错误:\n'
            if wrong_light_list:
                result_text += '\n'.join(wrong_light_list)
                result_text += '\n'
            else:
                result_text += u'无\n'
            result_text += '\n'




        self.ui.check_result_textBrowser.setText(result_text)

    def fix_asset(self):
        result_text = u''

        check_model = self.ui.checklistView.model()

        item0 = check_model.item(0)
        if item0.checkState() == Qt.Checked:
            clean_all_models()
            result_text += u'修复: 无效的模型点\n'
        item1 = check_model.item(1)
        if item1.checkState() == Qt.Checked:
            deleteAllNamespaces()
            result_text += u'修复: 带空间名的节点\n'
        item2 = check_model.item(2)
        if item2.checkState() == Qt.Checked:
            fix_all_shader_names_from_scene()
            result_text += u'修复: 材质节点命名\n'
        item3 = check_model.item(3)
        if item3.checkState() == Qt.Checked:
            fix_all_wrong_value_cam_list()
            result_text += u'修复: 摄像机参数\n'
        item4 = check_model.item(4)
        if item4.checkState() == Qt.Checked:
            fix_all_wrong_value_aiSkyDomeLights()
            result_text += u'修复: aiSkyDomeLight缩放值\n'
        item5 = check_model.item(5)
        if item5.checkState() == Qt.Checked:
            pass
        item6 = check_model.item(6)
        if item6.checkState() == Qt.Checked:
            pass
        item7 = check_model.item(7)
        if item7.checkState() == Qt.Checked:
            fix_all_wrong_value_lights()
            result_text += u'修复: arnold灯光参数值错误\n'

        result_text += u'所有可以修复的项目修复完毕，请重新检查一次资产！\n'
        self.ui.check_result_textBrowser.setText(result_text)




def show_window():
    win_name = 'checkAssetWindow'
    if cm.window(win_name,exists = True,q = True):
        cm.deleteUI(win_name)
    window = CheckAssetWindow(getMayaWin())
    window.setObjectName(win_name)
    window.resize(300,200)
    window.show()

# if __name__ == '__main__':
#     show_window()


