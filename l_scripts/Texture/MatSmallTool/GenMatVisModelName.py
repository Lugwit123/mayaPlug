# coding:utf-8

import sys,os
sys.path.append(os.environ.get('LugwitToolDir')+'/Lib')

from Lugwit_Module import *
import Lugwit_Module
print (dir(Lugwit_Module))
sys.path.append(Lugwit_mayaPluginPath+r'\l_scripts\Texture')

from PySide2.QtWidgets import QApplication, QMainWindow,QWidget

# 如果是使用PyQt，导入方式如下：
# from PyQt5.QtWidgets import QApplication, QMainWindow

# 导入转换后的.py文件，假设它是Ui_MainWindow.py
from uiFile import GenMatVisModelName

class MainWindow(QWidget, GenMatVisModelName.Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # 初始化UI
def main():
    if 'maya.exe' in sys.executable:
        app = QApplication(sys.argv)

    # 创建主窗口实例
    mainWindow = MainWindow()
    mainWindow.show()  # 显示窗口
    if 'maya.exe' in sys.executable:
        sys.exit(app.exec_())  # 运行应用程序
    
if __name__ == "__main__":
    main
