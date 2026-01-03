import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *


def replace_selected_ass():
    path, _ = QFileDialog.getOpenFileName(QApplication.activeWindow(), "", "", "Ass(*.ass)")
    if not path:
        return
    for transform in pm.selected(type="transform"):
        shape = transform.getShape()
        if not shape:
            continue
        if not shape.nodeType() == "aiStandIn":
            continue
        shape.dso.set(path)

