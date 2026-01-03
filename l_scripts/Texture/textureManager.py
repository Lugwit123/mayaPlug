# coding:utf-8
# print ('run module{}'.format(__file__))
import os,sys
import re
import shutil
import maya.cmds as cm
import traceback
cmds=cm
import maya.OpenMayaUI as apiUI
from maya import OpenMayaUI as omui 
import maya.mel as mm
LugwitPath=os.environ.get('LugwitPath')
Lugwit_PluginPath=os.environ.get('Lugwit_PluginPath')
Lugwit_publicPath=os.environ.get('Lugwit_publicPath')

from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
from PySide2 import __version__
from shiboken2 import wrapInstance 

from Lugwit_Module.l_src.UILib.QTLib import PySideLib

mayaMainWindowPtr = omui.MQtUtil.mainWindow()

class pm_class():
    def __init__(self):
        pass
    def __getattr__(self,name):
        global pm
        sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
        import load_pymel
        pm=load_pymel.pm
        func=eval('pm.{}'.format(name))
        return func
pm=pm_class()


class Node(object):

    def __init__(self, node):
        self.node = node

    @classmethod
    def nodes(cls):
        return [cls(node) for node in pm.ls(type="file")] + [cls(node) for node in pm.ls(type="RedshiftNormalMap")] + \
        [cls(node) for node in pm.ls(type="aiImage")]

    @classmethod
    def data(cls):
        data = {}
        for node in cls.nodes():
            data.setdefault(node.get_dir(), {}).setdefault(node.exit(), []).append(node)
        return data

    def name(self):
        return self.node.name()

    def get_path(self):
        path = ""
        if self.node.type() == "file":
            if self.node.fileTextureName.get():
                path = self.node.fileTextureName.get().replace("\\", "/")
        elif self.node.type() == "RedshiftNormalMap":
            if self.node.tex0.get():
                path = self.node.tex0.get().replace("\\", "/")
        elif self.node.type() == "aiImage":
            if self.node.filename.get():
                path = self.node.filename.get().replace("\\", "/")
        if len(path) > 0 and path[0] == "$":
            env = path.split("/")[0]
            if env[1:] in os.environ:
                path = path.replace(env, os.environ[env[1:]]).replace("\\", "/")
        return path

    def exit(self):
        path = self.get_path()
        if os.path.isfile(path):
            return True
        dir_name, basename = os.path.split(path)
        ud = re.sub(u"([0-9]{4}|<UDIM>|<udim>)", "<UDIM>", basename)
        if not os.path.isdir(dir_name):
            return False
        for name in os.listdir(dir_name):
            if re.sub(u"([0-9]{4}|<UDIM>|<udim>)", "<UDIM>", name) == ud:
                return True
        return False

    def get_dir(self):
        return os.path.dirname(self.get_path())

    def select(self):
        self.node.select(add=1)

    def deselect(self):
        self.node.select(d=1)

    def get_src_dst(self, dst, prefix="", suffix="", old="", new=""):
        if not dst:
            return []
        if not self.exit():
            return []
        if not os.path.isdir(dst):
            os.makedirs(dst)
        path = self.get_path()
        result = []
        src, basename = os.path.split(path)
        ud = re.sub(u"([0-9]{4}|<UDIM>|<udim>)", "<UDIM>", basename)
        for name in os.listdir(src):
            if re.sub(u"([0-9]{4}|<UDIM>|<udim>)", "<UDIM>", name) == ud:
                result.append((os.path.join(src, name), os.path.join(dst, name)))
        return result

    def move(self, dst, prefix="", suffix="", old="", new="",forceOveride=False):
        for src, dst in self.get_src_dst(dst, prefix, suffix, old, new):
            src = src.replace("\\", "/")
            dst = dst.replace("\\", "/")
            if not os.path.isfile(dst) or forceOveride==True:
                print (src, dst)
                os.rename(src, dst)

    def copy(self, dst, prefix="", suffix="", old="", new="",forceOveride=False,withTxFile=False):
        for src, dst in self.get_src_dst(dst, prefix, suffix, old, new):
            if not os.path.isfile(dst) or forceOveride==True:
                if withTxFile:
                    for ext in ['jpg','tif','tiff','tga','png','psd','exr','hdr','tx','iff']:
                        newSrc = src.replace('.'+ext, '.tx')
                        if os.path.exists(newSrc) and newSrc!=src :
                            newDst = os.path.dirname(dst)+'/'+os.path.basename(newSrc)
                            shutil.copy(newSrc, newDst)
                            shutil.copystat(newSrc, newDst)
                shutil.copy(src, dst)
                shutil.copystat(src, dst)


    def saveSetFileTextureName(self,fileNode,textureFilePath):
        colorSpace = ''
        if cm.attributeQuery('colorSpace',ex = True,node = fileNode):
            colorSpace = cm.getAttr('{}.colorSpace'.format(fileNode))        
        cm.setAttr('{}.fileTextureName'.format(fileNode),textureFilePath,type = 'string')    
        if colorSpace:
            try:
                cm.setAttr('{}.colorSpace'.format(fileNode),colorSpace,type = 'string')
            except:
                pass

    def set_path(self, path):
        if self.node.type() == "file":
            return self.saveSetFileTextureName(self.node.longName(),path)
        elif self.node.type() == "RedshiftNormalMap":
            return self.node.tex0.set(path)
        elif self.node.type() == "aiImage":
            return self.node.filename.set(path)

    def edit(self, dst, prefix="", suffix="", old="", new=""):
        if not os.path.isdir(dst):
            return
        basename = os.path.split(self.get_path())[-1]
        basename = prefix + basename.replace(old, new) + suffix
        self.set_path(os.path.join(dst, basename).replace("\\", "/"))

    def setattr(self):
        if self.node.type() != "file":
            return
        if "dif-c" in self.get_path():
            self.node.filterType.set(0)
            self.node.alphaIsLuminance.set(False)
            self.node.colorSpace.set("sRGB")
        else:
            self.node.filterType.set(0)
            self.node.alphaIsLuminance.set(True)
            self.node.colorSpace.set("Raw")


class TexTu(QWidget):

    def __init__(self):
        #QWidget.__init__(self, QApplication.activeWindow(), Qt.Window)
        try:
            mayaMainWindow= wrapInstance(long(mayaMainWindowPtr), QWidget)
        except:
            mayaMainWindow=mm.eval('$tmpVar=$gMainWindow')
        super(TexTu, self).__init__(mayaMainWindow)
        self.resize(540, 620)
        self.setWindowIcon(QIcon(r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\mayaPlug\icon\tx.jpg'))
        self.data = {}
        layout = QVBoxLayout()
        self.setLayout(layout)
        button = QPushButton(u"检查场景贴图")
        button.setFixedHeight(35)
        layout.addWidget(button)
        button.clicked.connect(self.reload)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.header().setHidden(True)
        self.tree.setStyleSheet("QTreeWidget {background: #383838}")
        layout.addWidget(self.tree)
        
        #self.tree.itemDoubleClicked.connect(self.doubleClickedFunc)

        path_layout = QHBoxLayout()
        layout.addLayout(path_layout)
        path_layout.addWidget(QLabel(u"目标路径："))
        self.path = QLineEdit()
        self.path.setFixedHeight(25)
        path_layout.addWidget(self.path)
        path_button = QPushButton(u"选择路径")
        path_button.setFixedHeight(25)
        path_layout.addWidget(path_button)
        path_button.clicked.connect(self.select_dir)

        edit_layout = QHBoxLayout()
        layout.addLayout(edit_layout)

        add_layout = QVBoxLayout()
        edit_layout.addLayout(add_layout)
        add_check = QCheckBox(u"修改")
        add_check.stateChanged.connect(self.add_changed)
        add_layout.addWidget(add_check)
        add_form = QFormLayout()
        add_layout.addLayout(add_form)
        self.prefix = QLineEdit()
        self.prefix.setEnabled(False)
        add_form.addRow(u"前缀：", self.prefix)
        self.suffix = QLineEdit()
        self.suffix.setEnabled(False)
        add_form.addRow(u"后缀：", self.suffix)

        replace_layout = QVBoxLayout()
        edit_layout.addLayout(replace_layout)
        replace_check = QCheckBox(u"替换")
        replace_check.stateChanged.connect(self.replace_changed)
        replace_layout.addWidget(replace_check)
        replace_form = QFormLayout()
        replace_layout.addLayout(replace_form)
        self.old = QLineEdit()
        self.old.setEnabled(False)
        replace_form.addRow(u"旧字符：", self.old)
        self.new = QLineEdit()
        self.new.setEnabled(False)
        replace_form.addRow(u"新字符：", self.new)

        button_layoutA = QHBoxLayout()
        button_layoutB = QHBoxLayout()

        layout.addLayout(button_layoutA)
        layout.addLayout(button_layoutB)
        
        self.forceOverodeCKB=QCheckBox(u'强制覆盖')
        button_layoutA.addWidget(self.forceOverodeCKB)
        self.ArnoldTxFileWgt = QCheckBox(u"包括Arnold_TX文件或者TX文件对应的贴图")
        button_layoutA.addWidget(self.ArnoldTxFileWgt)
        button_layoutA.addStretch(10)
        
        copy = QPushButton(u"复制贴图")
        button_layoutB.addWidget(copy)
        copy.setFixedHeight(25)
        copy.clicked.connect(self.copy)

        move = QPushButton(u"移动贴图")
        button_layoutB.addWidget(move)
        move.setFixedHeight(25)
        move.clicked.connect(self._move)

        edit = QPushButton(u"修改路径")
        button_layoutB.addWidget(edit)
        edit.setFixedHeight(25)
        edit.clicked.connect(self.edit)

        attr = QPushButton(u"设置属性")
        button_layoutB.addWidget(attr)
        attr.clicked.connect(self.setattr)
        attr.setFixedHeight(25)

        close = QPushButton(u"关闭界面")
        close.clicked.connect(self.close)
        close.setFixedHeight(25)
        button_layoutB.addWidget(close)
        self.tree.itemChanged.connect(self.select_changed)
        #self.tree.itemChanged.connect(self.select_changed)
        self.tree.itemDoubleClicked.connect(self.doubleClickedFunc)

    # @staticmethod
    def doubleClickedFunc(self):
        selectedItems=self.tree.selectedItems()
        for item in selectedItems:
            print (item,dir(item))
            print (item.text(0))
            pm.select(item.text(0))
        # for i in range(item.childCount()):
        #     item.child(i).setCheckState(0, item.checkState(0))
        # if hasattr(item, "node"):
        #     item.node.select()

        
    def reload(self):
        self.data = Node.data()
        self.tree.clear()
        top = QTreeWidgetItem(self.tree)
        top.setText(0, u"共{0}个贴图节点，{1}个贴图路径".format(len(Node.nodes()), len(self.data)))
        top.setCheckState(0, Qt.Unchecked)
        for key, value in self.data.items():
            dir_item = QTreeWidgetItem(top)
            dir_item.setText(0, u"共{0}个节点在路径{1}".format(len(value.get(True,[]) + value.get(False, [])), key))
            dir_item.setCheckState(0, Qt.Unchecked)
            for exist, label in ((True, u"存在"), (False, u"丢失")):
                exist_item = QTreeWidgetItem(dir_item)
                exist_item.setText(0, u"共{0}个节点{1}".format(len(value.get(exist, [])), label))
                exist_item.setCheckState(0, Qt.Unchecked)
                for node in value.get(exist, []):
                    node_item = QTreeWidgetItem(exist_item)
                    node_item.setText(0, node.name())
                    node_item.setCheckState(0, Qt.Unchecked)
                    node_item.node = node
                    #node_item.doubleClicked.connect(lambda *args:print ('aa'))
            dir_item.setExpanded(True)
        top.setExpanded(True)

    def replace_changed(self, state):
        if state:
            self.old.setEnabled(True)
            self.new.setEnabled(True)
        else:
            self.new.setText("")
            self.old.setText("")
            self.old.setEnabled(False)
            self.new.setEnabled(False)

    def add_changed(self, state):
        if state:
            self.prefix.setEnabled(True)
            self.suffix.setEnabled(True)
        else:
            self.prefix.setText("")
            self.suffix.setText("")
            self.prefix.setEnabled(False)
            self.suffix.setEnabled(False)

    @staticmethod
    def select_changed(item, *args):
        for i in range(item.childCount()):
            item.child(i).setCheckState(0, item.checkState(0))
        if hasattr(item, "node"):
            if item.checkState(0):
                item.node.select()
            else:
                item.node.deselect()

    def select_dir(self):
        path = QFileDialog.getExistingDirectory(self)
        self.path.setText(path)
    
    @staticmethod   
    def getSize(x):
        x=x.get_path().replace('<UDIM>','1001')
        if os.path.exists(x):
            return  str(os.path.getsize(x)/1024.0/1024)[:6]
        else:
            return u'未知'

    def copy(self):
        iterList=[(x.get_path(),x.get_path(),self.getSize(x),1) for x in self.select_nodes()]
        process=PySideLib.L_ProgressDialog(title=u'复制文件',processList=iterList)
        fininished=[]
        for i,node in enumerate(self.select_nodes()):
            process.ProgressDialog_Procecss(index=i)
            path=node.get_path()
            if path in fininished:
                continue
            forceOveride=self.forceOverodeCKB.isChecked()
            withTxFile=self.ArnoldTxFileWgt.isChecked()
            node.copy(self.path.text(), self.prefix.text(), self.suffix.text(), self.old.text(), self.new.text(),forceOveride,withTxFile)
            fininished.append(path)
        QMessageBox.about(self, u"提示", u"贴图复制完毕！")

    def _move(self):
        iterList=[(x.get_path(),x.get_path(),self.getSize(x),1) for x in self.select_nodes()]
        process=PySideLib.L_ProgressDialog(title=u'复制文件',processList=iterList)
        fininished=[]
        for i,node in enumerate(self.select_nodes()):
            process.ProgressDialog_Procecss(index=i)
            path=node.get_path()
            if path in fininished:
                continue
            forceOveride=self.forceOverodeCKB.isChecked()
            node.move(self.path.text(), self.prefix.text(), self.suffix.text(), self.old.text(), self.new.text(),forceOveride)
            fininished.append(path)
        QMessageBox.about(self, u"提示", u"贴图移动完毕！")

    def edit(self):
        for node in self.select_nodes():
            node.edit(self.path.text(), self.prefix.text(), self.suffix.text(), self.old.text(), self.new.text())
        QMessageBox.about(self, u"提示", u"路径修改完毕！")

    def setattr(self):
        for node in self.select_nodes():
            node.setattr()
        QMessageBox.about(self, u"提示", u"属性修改完毕！")

    def select_nodes(self):
        nodes = []
        self.append_nodes(self.tree.topLevelItem(0), nodes)
        return nodes

    def append_nodes(self, item, nodes):
        for i in range(item.childCount()):
            self.append_nodes(item.child(i), nodes)
        if hasattr(item, "node"):
            if item.checkState(0):
                nodes.append(item.node)

    def showNormal(self):
        self.data = {}
        self.tree.clear()
        QWidget.show(self)

def main(*args):
    ui = TexTu()
    ui.setWindowFlags(Qt.WindowStaysOnTopHint)
    ui.setWindowFlags(Qt.Window)
    ui.showNormal()



