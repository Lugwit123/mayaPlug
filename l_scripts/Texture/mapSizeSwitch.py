# coding:utf-8

from PySide2 import QtWidgets, QtCore, QtGui

from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class ImageResizeApp( MayaQWidgetDockableMixin,QtWidgets.QWidget):

    def __init__(self, parent=None):

        super(ImageResizeApp, self).__init__(parent)

        self.init_ui()

    

    def init_ui(self):

        # 创建主垂直布局

        main_layout = QtWidgets.QVBoxLayout()

        

        # 创建字体对象并设置字体大小

        label_font = QtGui.QFont()

        label_font.setPointSize(10)  # 标签字体大小

        

        button_font = QtGui.QFont()

        button_font.setPointSize(10)  # 按钮字体大小



        # 创建标签

        self.info_label = QtWidgets.QLabel(

            u'选择要切换的贴图类型\n(未选择模型表示切换所有模型切图)\n(有选择模型表示只切换选择的模型贴图)', 

            self

        )

        self.info_label.setAlignment(QtCore.Qt.AlignCenter)  # 标签居中显示

        self.info_label.setFont(label_font)  # 应用标签字体



        # 创建按钮布局

        button_layout = QtWidgets.QVBoxLayout()



        # 创建每一行的水平布局

        row1_layout = QtWidgets.QHBoxLayout()

        row2_layout = QtWidgets.QHBoxLayout()



        # 创建第一个按钮

        self.original_size_button = QtWidgets.QPushButton(u'选中模型原尺寸贴图', self)

        self.original_size_button.setFixedSize(150, 60)

        self.original_size_button.clicked.connect(lambda: self.replace_texture_paths("Mod/tex/", selected=True))

        self.original_size_button.setFont(button_font)  # 应用按钮字体



        # 创建第二个按钮

        self.small_size_button = QtWidgets.QPushButton(u'选中模型小尺寸贴图', self)

        self.small_size_button.setFixedSize(150, 60)

        self.small_size_button.clicked.connect(lambda: self.replace_texture_paths("Mod/tex_eighth/", selected=True))

        self.small_size_button.setFont(button_font)  # 应用按钮字体



        # 创建第三个按钮

        self.button3 = QtWidgets.QPushButton(u'所有模型原尺寸贴图', self)

        self.button3.setFixedSize(150, 60)

        self.button3.clicked.connect(lambda: self.replace_texture_paths("Mod/tex/", selected=False))

        self.button3.setFont(button_font)  # 应用按钮字体



        # 创建第四个按钮

        self.button4 = QtWidgets.QPushButton(u'所有模型小尺寸贴图', self)

        self.button4.setFixedSize(150, 60)

        self.button4.clicked.connect(lambda: self.replace_texture_paths("Mod/tex_eighth/", selected=False))

        self.button4.setFont(button_font)  # 应用按钮字体



        # 将按钮添加到每一行的水平布局

        row1_layout.addWidget(self.original_size_button)

        row1_layout.addWidget(self.small_size_button)



        row2_layout.addWidget(self.button3)

        row2_layout.addWidget(self.button4)



        # 将每一行的布局添加到主布局

        button_layout.addLayout(row1_layout)

        button_layout.addLayout(row2_layout)



        # 将标签和按钮布局添加到主布局

        main_layout.addWidget(self.info_label)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(QtWidgets.QLabel(u"作者:阿祖"))



        # 设置主布局

        self.setLayout(main_layout)



        # 设置窗口属性

        self.setWindowTitle(u'贴图处理工具')

        self.resize(320, 160)  # 调整窗口的大小以适应按钮布局



    def replace_texture_paths(self, new_substring, selected=True):

        """

        替换 Maya 场景中所选模型或所有模型的贴图路径中的指定子字符串，并更新回原文件节点。

        

        :param new_substring: 新的路径片段

        :param selected: 是否只替换选中的模型

        """

        # 获取选中的模型

        if selected:

            selection = cmds.ls(selection=True, type="transform")

            if not selection:

                QtWidgets.QMessageBox.warning(self, u'警告', u'未选中模型')

                return

        else:

            selection = cmds.ls(type="transform")

    

        # 获取所有 file 纹理节点

        file_nodes = cmds.ls(type='file')

    

        # 遍历每个 file 节点，获取并修改文件路径

        for file_node in file_nodes:

            # 获取当前贴图路径

            file_path = cmds.getAttr(file_node + ".fileTextureName")

            

            # 打印调试信息

            print("Checking Node: {} -> Path: {}".format(file_node , file_path))

            

            # 如果旧的子字符串存在于路径中，则进行替换

            if "Mod/tex/" in file_path or "Mod/tex_eighth/" in file_path:

                new_file_path = file_path.replace("Mod/tex/", new_substring).replace("Mod/tex_eighth/", new_substring)

                

                # 如果有选中的模型，检查此文件节点是否关联到选中的模型

                if selected:

                    connected_objs = cmds.listConnections(file_node, type="transform") or []

                    print("Connected Objects for {}: {}".format(file_node , connected_objs))

                    if not any(obj in selection for obj in connected_objs):

                        print("Skipping {} as it's not connected to the selection.".format(file_node))

                        continue

                

                # 设置新的贴图路径到原文件节点

                cmds.setAttr(file_node + ".fileTextureName", new_file_path, type="string")

                print("Updated Node: {} -> New Path: {}".format(file_node , new_file_path))

            else:

                print("No change for Node: {} -> Path: {}".format(file_node , file_path))







def show_ui(*args):

    # 获取 Maya 的 QApplication 实例

    app = QtWidgets.QApplication.instance()

    if not app:

        app = QtWidgets.QApplication([])



    # 创建并显示 UI 窗口

    global window

    window = ImageResizeApp()

    window.setWindowFlags(QtCore.Qt.Window)  # 确保窗口作为独立窗口显示

    window.show()



# # 运行 UI 界面

# show_ui()

