import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools

def load_ui(ui_file):
    """加载UI文件"""
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(ui_file)
    ui_file.open(QtCore.QFile.ReadOnly)
    ui = loader.load(ui_file)
    ui_file.close()
    return ui

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        ui_file =r"D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\fun\RenderDividelayer\main.ui"
        ui = load_ui(ui_file)
        self.setCentralWidget(ui)

if __name__ == "__main__":
    # 创建PySide2应用程序
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    # 将PySide2的顶层窗口设置为Maya的主窗口
    maya_main_window = None
    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == "MayaWindow":
            maya_main_window = obj
            break
    if maya_main_window:
        app.setParent(maya_main_window)

    # 创建自定义窗口
    window = MyWindow()
    window.show()

    # 启动PySide2应用程序
    if not cmds.about(batch=True):
        app.exec_()
