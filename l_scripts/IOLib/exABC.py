# -*- coding: utf8

from PySide2.QtWidgets import *

import sys,os,re


sys.path.append(LugwitPath+'/Python/PythonLib/UILib')
import PySideLib as py
from imp import reload


class UI(QWidget):
    def __init__(self, parent = None):
        super(UI, self).__init__(parent)
        self.resize(400, 300)
        self.setWindowTitle('导出ABC')
        layout = QVBoxLayout()
        fileLay = py.LChooseFileButtonGrp()
        exButton = py.Lbutton(u'导出',  c=py.chooseFile)
        sf = py.LTextGrp(textList={u'开始帧':1} )
        ef = py.LTextGrp(textList={u'结束帧':100})
        att = py.LTextGrp(textList={u'导出属性列表(空格隔开不同属性)':['shop_materialpath']})
        layout = QVBoxLayout()
        layout.addLayout(fileLay[0])
        layout.addWidget(sf)
        layout.addWidget(ef)
        layout.addWidget(att)
        layout.addWidget(exButton)
        self.setLayout(layout)

executable=sys.executable
print ('executable',executable)
if re.search('maya.*.exe',executable):
    try:
        app = QApplication([])
    except:
        app = QApplication.instance()
else:
    print ('独立运行')
    app = QApplication(sys.argv)
#有空试试setObjectName关闭存在UI
try:
    win.close()
except:
    pass
win = UI()
def winShow(*args):
    global win
    win.show()
if not re.search('maya.*.exe',executable):
    sys.exit(app.exec_())
'''
import sys
sys.path.append(r'S:\DataTrans\FQQ\plug_in\Lugwit_plug\mayaPlug\scripts')
try:
    reload(exABC)
except:
    import exABC
'''
