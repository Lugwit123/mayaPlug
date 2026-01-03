# coding:utf-8
from PySide2 import QtGui, QtWidgets
import maya.cmds as cmds

def modify_font(*args):
    # 获取主窗口
    maya_main_window = cmds.window()

    # 设置字体为微软雅黑
    font_path = "C:/Windows/Fonts/msyh.ttc"
    font_id = QtGui.QFontDatabase.addApplicationFont(font_path)

    if font_id != -1:
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        # 使用样式表的方式来局部设置中文字体
        css = """
        * {{
            font-family: '{}', sans-serif;
        }}
        """.format(font_family)
        
        app = QtWidgets.QApplication.instance()
        app.setStyleSheet(css)

        print(u"字体样式表已应用，中文字体设置为：".format(font_family))
    else:
        print(u"字体设置失败，请检查字体路径")
