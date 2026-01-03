# coding:utf-8
import os,sys,traceback
import maya.cmds as cmds
from PySide2.QtWidgets import *
# 假设 your_output_file.py 是转换出来的文件，且包含一个名为 Ui_Form 的类
import  GenMatVisModelName
reload (GenMatVisModelName)
LugwitToolDir=os.environ.get('LugwitToolDir')
sys.path.append(LugwitToolDir+'/Lib')
import Lugwit_Module as LM

class MyForm(QWidget, GenMatVisModelName.Ui_Form):
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        # 设置 UI
        self.setupUi(self)
        self.applyToSelBtn.setVisible(False)
        self.saveSetingBtn.setVisible(False)
        # 因为隐藏了模型组件,设置尺寸自适应
        self.adjustSize()
        
        self.connectSignal()
        
    def renameMatAndSg(self):
        renameMatAndSg([self.matPrefixLineEdit.text(),self.sgPrefixLineEdit.text()],
                        [self.matSuffixLineEdit.text(),self.sgSuffixLineEdit.text()])
        
    def connectSignal(self):
        self.applyBtn.clicked.connect(self.renameMatAndSg)

def get_objects_and_materials_from_sg_node(sg_node):
    members = cmds.sets(sg_node, query=True)
    if members:
        objects = [member for member in members if cmds.objectType(member) != 'shadingEngine']
        materials = [cmds.listConnections(sg_node + '.surfaceShader', source=True)[0]]
        return objects, materials

def renameMatAndSg(MatName=['','_M'],SgName=['','_Inst']):
    sg_nodes = [x for x in cmds.ls(type='shadingEngine') if cmds.objExists(x)]
    for sg_node in sg_nodes:
        if sg_node in ['initialParticleSE','initialShadingGroup']:
            continue
        objects_and_materials = get_objects_and_materials_from_sg_node(sg_node)
        if not objects_and_materials:
            continue
        objects,materials = objects_and_materials
        object=objects[0].split('.')[0]
        object = cmds.listRelatives(object,p=1)[0]
        material = materials[0]
        NewMatName =object[0]+object+MatName[1]
        NewSgName = SgName[0]+object+SgName[1]
        if not cmds.objExists(NewMatName):
            cmds.rename(material,NewMatName)
        else:
            print (materials,sg_node)
        if not cmds.objExists(NewSgName):
            cmds.rename(sg_node,NewSgName)

def main():
    if not LM.isMayaEnv():
        app = QApplication(sys.argv)
    global form
    form = MyForm()
    form.show()
    if not LM.isMayaEnv():
        sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()
    

'''
import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\Texture\uiFile')
import ruiUI
reload (ruiUI)
ruiUI.main()
'''
