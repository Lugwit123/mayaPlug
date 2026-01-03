# coding:utf-8
import re
import os

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

import action
reload(action)
from action import *


qss = u"""
QTreeWidget, QPlainTextEdit {
    background: #303030;
    font-size: 16px;
} 
"""


class ItemLine(QLineEdit):
    callBackSignal = Signal(unicode)

    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        self.setValidator(QRegExpValidator(QRegExp(u"[a-zA-Z]+")))

    def keyPressEvent(self, event):
        QLineEdit.keyPressEvent(self, event)
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.callBackSignal.emit(self.text())
        event.accept()

    def focusOutEvent(self, event):
        QLineEdit.focusOutEvent(self, event)
        self.callBackSignal.emit(self.text())


file_types = [
    "Displacement", "Normal", "Metallic", "Roughness", "Color", "Albedo", "Opacity", "Translucency", "Bump", "Gloss"
]


class ItemSelect(ItemLine):

    def __init__(self, parent):
        ItemLine.__init__(self, parent)
        completer = QCompleter(file_types)
        completer.setCompletionMode(completer.UnfilteredPopupCompletion)
        completer.activated.connect(self.callBackSignal.emit)
        self.setCompleter(completer)
        self.completer().popup().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class Main(QDialog):

    def __init__(self):
        QDialog.__init__(self, QApplication.activeWindow(), Qt.Window)
        self.setStyleSheet(qss)
        self.Material = QIcon(os.path.abspath(__file__ + "/../icons/Material.png"))
        self.ShadingEngine = QIcon(os.path.abspath(__file__ + "/../icons/ShadingEngine.png"))
        self.Textures = QIcon(os.path.abspath(__file__ + "/../icons/Textures.png"))
        self.Error = QIcon(os.path.abspath(__file__ + "/../icons/Error.png"))

        self.resize(QSize(400, 600))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.prefix = QLineEdit()
        self.prefix.setValidator(QRegExpValidator(QRegExp(u"[a-zA-Z0-9]+")))

        layout.addWidget(self.prefix)
        self.tree = QTreeWidget()
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.setSelectionMode(self.tree.ExtendedSelection)
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree.setColumnCount(1)
        self.tree.header().setHidden(True)
        self.tree.itemDoubleClicked.connect(self.rename)
        self.tree.itemClicked.connect(self.select)
        self.tree.setIconSize(QSize(16,16))
        layout.addWidget(self.tree)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        update_button = QPushButton(u"刷新")
        button_layout.addWidget(update_button)
        update_button.clicked.connect(self.update_mat)

        pack_button = QPushButton(u"打包")
        button_layout.addWidget(pack_button)
        pack_button.clicked.connect(self.pack)

    def update_mat(self):
        self.tree.clear()
        for sg in get_data():
            sg_item = QTreeWidgetItem(self.tree)
            sg_item.doc = sg
            sg_item.setText(0, sg[Node].name())
            sg_item.setIcon(0, self.ShadingEngine)
            for mat in sg[Children]:
                if mat[Type] != Material:
                    continue
                sg_item.setExpanded(True)
                mat_item = QTreeWidgetItem(sg_item)
                mat_item.doc = mat
                mat_item.setText(0, mat[Node].name())
                mat_item.setIcon(0, self.Material)
                for tex in mat[Children]:
                    mat_item.setExpanded(True)
                    if tex[Type] != Textures:
                        continue
                    tex_item = QTreeWidgetItem(mat_item)
                    tex_item.doc = tex
                    if exit_tex(tex[Node]):
                        tex_item.setIcon(0, self.Textures)
                    else:
                        tex_item.setIcon(0, self.Error)
                    tex_item.setText(0, get_tex_name(tex[Node]))

    def pack(self):
        path = QFileDialog.getExistingDirectory(self)
        if not path:
            return
        pack(path)

    def show(self, *args, **kwargs):
        self.update_mat()
        QDialog.show(self)

    def rename(self, item):
        if item.doc[Type] == Textures:
            line = ItemSelect(self.tree)
            self.tree.setItemWidget(item, 0, line)
            line.setText(get_tex_name(item.doc[Node]).split("_")[-1])
            line.setFocus()
            line.selectAll()
            list_widget = line.completer().popup()
            list_widget.move(line.mapToGlobal(QPoint(0, line.height())))
            list_widget.resize(line.width(), min([10, len(file_types)]) * (list_widget.sizeHintForRow(0) + 2))
            list_widget.show()
        else:
            line = ItemLine(self.tree)
            self.tree.setItemWidget(item, 0, line)
            line.setText(item.doc[Node].name().split("_")[-2:][0])

        def slot(value):
            self.rename_item(item, value)
            self.tree.removeItemWidget(item, 0)
        line.callBackSignal.connect(slot)

    def rename_item(self, item, value):
        if item.doc[Type] == ShadingEngine:
            item.doc[Node].rename("_".join([self.prefix.text(), value, item.doc[Node].type()]))
            item.setText(0, item.doc[Node].name())
            for i in range(item.childCount()):
                self.rename_item(item.child(i), value)
        elif item.doc[Type] == Material:
            item.doc[Node].rename("_".join([self.prefix.text(), value, item.doc[Node].type()]))
            item.setText(0, item.doc[Node].name())
            name_count = {}
            for child in item.doc[Children]:
                if child[Type] == Utility:
                    name = "_".join([self.prefix.text(), value, child[Node].type()])
                    count = name_count.setdefault(name, 0)
                    name_count[name] += 1
                    if count:
                        name += str(count)
                    child[Node].rename(name)
            name_count = {}
            for child in item.doc[Children]:
                if child[Type] == Utility:
                    name = "_".join([self.prefix.text(), value, child[Node].type()])
                    count = name_count.setdefault(name, 0)
                    name_count[name] += 1
                    if count:
                        name += str(count)
                    child[Node].rename(name)
            for i in range(item.childCount()):
                v = get_tex_name(item.child(i).doc[Node]).split("_")[-1]
                if re.match(ur"([0-9]{4}|<UDIM>|<udim>)",  v):
                    v = get_tex_name(item.child(i).doc[Node]).split("_")[-2]
                self.rename_item(item.child(i), v)
        elif item.doc[Type] == Textures:
            name = item.parent().doc[Node].name().split("_")[-2:][0]
            name = "_".join([self.prefix.text(), name, value])
            rename_tex(item.doc[Node], name)
            item.doc[Node].rename(name)
            item.setText(0, get_tex_name(item.doc[Node]))

    @staticmethod
    def select(item):
        if hasattr(item, "doc"):
            pm.select(item.doc[Node], r=1)

window = None


def show():
    global window
    if window is None:
        window = Main()
    window.show()
