# -*- coding:utf-8 -*-
import maya.cmds as cm
import os
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import re
import functools
import time
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import *
    from PySide import __version__
    from shiboken import wrapInstance
except:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtUiTools import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance

import BibleReaderTools as uitools
reload(uitools)


def paintEvent(self,event):
    opt = QStyleOption()
    opt.initFrom(self)
    p = QPainter(self)
    self.style().drawPrimitive(QStyle.PE_Widget,opt,p,self)

        
class TestWidget(QWidget):
    def __init__(self,parent = None):
        super(TitleWidget,self).__init__(parent)
        
TestWidget.paintEvent = paintEvent


def compare(pic1,pic2):
    pic1_name = os.path.basename(pic1).split('.')[0]
    pic2_name = os.path.basename(pic2).split('.')[0]
    return 1 if int(pic1_name) > int(pic2_name) else -1


class UIWin(QWidget):
    def __init__(self,parent = None):
        super(UIWin,self).__init__(parent)

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'资产规范')
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        loader = QUiLoader()
        # loader.registerCustomWidget(InteractiveListView)
        file = QFile(uitools.getUIPath('main.ui'))
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=uitools.getMayaWin())
        layout.addWidget(self.ui)
        file.close()

        # self.ui.xxx
        # item = QStandardItem('a')
        # item.setIcon(QIcon(r'D:\maya\EaToolBox\maya\Tools\public\BibleReader\scripts\bible\1.jpeg')))
        # model.appendRow(item)
        # self.ui.pic_view.setModel(model) 
        bible_path = uitools.getBiblePath()
        files = [os.path.join(bible_path,f) for f in os.listdir(bible_path) if f.endswith('.jpg')]
        self.files_size = len(files)
        files = sorted(files, cmp = compare)
        # files.sort()
        row_space = 5
        scale = 1
        self.row_space = row_space
        if files:
            model = QStandardItemModel()
            for i in range(len(files)):
                index_str = os.path.basename(files[i]).split('.')[0]
                model.appendRow(QStandardItem('%s'%index_str))
            self.ui.index_view.setModel(model)
            selection_model = self.ui.index_view.selectionModel()
            

            label = QLabel(self.ui.content_widget)
            image = QImage(files[0])
            image_w = image.width() * scale
            image_h = image.height() * scale
            self.image_h = image_h 
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(image_w,image_h)
            label.setPixmap(pixmap)
            selection_model.currentChanged.connect(self.ccc)
            self.ui.pic_view.verticalScrollBar().valueChanged.connect(self.show_pic_index)
            if len(files) > 1:
                for i in range(1,len(files)):
                    label = QLabel(self.ui.content_widget)
                    image = QImage(files[i])
                    pixmap = QPixmap.fromImage(image)
                    pixmap = pixmap.scaled(image_w,image_h)
                    # pixmap.load(files[i])
                    label.setPixmap(pixmap)
                    label.move(0,i * (image_h + row_space))

            self.ui.content_widget.resize(image_w,len(files) * image_h + (len(files) - 1) * row_space)
        self.ui.splitter.setSizes([200,800])
        #self.ui.pic_view.verticalScrollBar().setValue(1024)
        self.setStyleSheet(uitools.getStyleSheet('main.qss'))

        self.show_pic_index(0)

    def ccc(self,current):
        self.ui.pic_view.verticalScrollBar().setValue(current.row() * (self.image_h + self.row_space))

    def show_pic_index(self,value):
        
        index = value / (self.image_h + self.row_space) + 1
        self.ui.label.setText('{}/{}'.format(index,self.files_size))
    
def mainUI():
    winName = 'Bible_Reader_Win'
    if cm.window(winName,q = True,exists = True):
        cm.deleteUI(winName)

    win = UIWin(uitools.getMayaWin())
    win.setObjectName(winName)
    win.resize(1000,800)
    win.show()