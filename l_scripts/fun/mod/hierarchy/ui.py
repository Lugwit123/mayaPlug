# coding:utf-8
from Lugwit_Module import isMayaEnv
from Lugwit_Module import l_src
reload (l_src)
lprint = l_src.lprint
from Lugwit_Module.l_src.UILib.QTLib import self_qss
from Lugwit_Module.l_src.UILib.QTLib import PySideLib
import re,sys,codecs,os
os.environ['QT_API']='PySide2'
import glob
from functools import partial


# import pkmg
# fileIfnoDict=pkmg.getPkmgEnv()

if isMayaEnv():
    import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import shiboken2,inspect

__file__=inspect.getfile(inspect.currentframe())


import shiboken2
    
keyWordList=[('sim','mesh'),('L','R'),('top','dow'),('HIGH','LOW'),('GRP','')]

import action
reload(action)
import readExcel
reload(readExcel)
from action import *

if not sys.executable.endswith('maya.exe'):
    #app = QApplication(sys.argv)
    pass
    #app.quit()
    #gui_app = QGuiApplication(sys.argv)
else:
    import maya.OpenMayaUI as omui



class LabelLine(QLineEdit):
    try:
        try:
            callBackSignal = Signal(unicode)
        except:
            callBackSignal = Signal(str)
    except:
        callBackSignal = pyqtSignal(unicode)

    def keyPressEvent(self, event):
        QLineEdit.keyPressEvent(self, event)
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.callBackSignal.emit(self.text())
        event.accept()

    def focusOutEvent(self, event):
        QLineEdit.focusOutEvent(self, event)
        self.callBackSignal.emit(self.text())
        


class NameLine(LabelLine):

    def __init__(self, parent):
        LabelLine.__init__(self, parent)
        self.setValidator(QRegExpValidator(QRegExp(u"[a-zA-Z]+")))
        
class TreeItemMimeData(QMimeData):
    def __init__(self):
        self._format = []
        self._item = None
        super(TreeItemMimeData,self).__init__()
 
    def set_drag_data(self, fmt, item):
        self._format.append(fmt)
        self._item = item
 
    def get_drag_data(self):
        return self._item
 
    def formats(self):
        return self._format
 
    def retrieveData(self, mimetype, preferredType):
        if mimetype == 'ItemMimeData':
            return self._item
        else:
            return QMimeData.retrieveData(mimetype, preferredType)

class Hierarchy(QTreeWidget):
    
    def __init__(self,presetFile=r'D:\TD_Depot\TD\hyws\maya\scripts\fun\mod\hierarchy\template\aa.json',parentWgt=None):
        QTreeWidget.__init__(self)
        
        
        global mesh_icon,group_icon,select_icon,putin_icon
        mesh_icon = QIcon(os.path.abspath(__file__ + "/../icons/mesh.png"))
        group_icon = QIcon(os.path.abspath(__file__ + "/../icons/group.png"))
        select_icon = QIcon(os.path.abspath(__file__ + "/../icons/select.png"))
        putin_icon = QIcon(os.path.abspath(__file__ + "/../icons/putin.png"))

            
        if parentWgt:
            self.parentWgt=parentWgt
        self.presetFile=presetFile
        if isMayaEnv():
            self.MayaFileName=cmds.file(q=True, sceneName=True)
        else:
            self.MayaFileName='D:/aa_aa.ma'
        MayaFileBaseName=os.path.basename(self.MayaFileName).rsplit('.',1)[0]
        try:
            #self.AssetName=self.MayaFileName.rsplit('/',1)[1].split('_')[0]
            self.AssetName=MayaFileBaseName.split('_')[0]
            #self.AssetName=re.search('(.+)_*\.+',MayaFileBaseName).group(1)
        except Exception as e:
            self.AssetName=u'资产名称'
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.header().setHidden(True)
        self.setColumnCount(3)
        self.hierarchy = action.load_hierarchy(self.presetFile)
       
        print (self.hierarchy)
        #sys.exit()
        for document in self.hierarchy:
            item = self.create_item_by_document(self, document)
            self.set_expanded(item, True)
        self.setExpandsOnDoubleClick(False)
        self.setIconSize(QSize(16, 16))
        self.itemDoubleClicked.connect(self.edit_hierarchy)
        self.itemClicked.connect(self.select_hierarchy)
        
        # =允许拖拽
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.viewport().setAcceptDrops(True)
        # self.setDropIndicatorShown(True)


        self.menu = QMenu(self)
        self.menu.addAction(u"放入模型", self.move_selected)
        if liscense:
            self.menu.addAction(u"添加组层级", lambda:self.add_hierarchy(name="name_GRP",label="description",icon='',modifyOutline=False))
            self.menu.addAction(u"添加模型层级", lambda:self.add_hierarchy(name="name",label="description",icon='',modifyOutline=False))
            self.menu.addAction(u"移除层级", self.remove_hierarchy)
            self.menu.addAction(u"组层级与模型层级切换", self.scene_hierarchy)
            #self.menu.addAction(u"替换为场景层级", self.scene_hierarchy)
            self.menu.addSeparator()
            self.menu.addAction(u'复制层级',lambda *args :self._action_cutOrCopy_handler(cutOrCopy='copy'))
            self.menu.addAction(u'剪切层级',lambda *args :self._action_cutOrCopy_handler(cutOrCopy='cut'))
            self.menu.addAction(u'粘贴层级',lambda *args :self._action_paste_handler())
            self.menu.addAction(u'搜索和替换',lambda *args :self._serachAndReplace())
            self.keyMeun=QMenu(u'添加字段')
            self.menu.addMenu(self.keyMeun)
            for index,keyWords in enumerate(keyWordList):
                for keyWord in keyWords:
                    if keyWord:
                        self.keyMeun.addAction(keyWord,partial(self.addKeyWord,'',keyWord))
                self.keyMeun.addSeparator()

            self.menu.addSeparator()
            self.menu.addAction(u"保存模板...", self.save_hierarchy)
            self.menu.addAction(u"导入模板...", self.load_hierarchy)
        
        
        self.itemChanged.connect(self.handle_item_changed)
        self.itemClicked.connect(self.getTextBeforeModify)
        
        self._index_cmb = 1
        self._index_btn = 2
        self._cutOrCopy_item = None
        self._last_bg_colord_item = None
        self._start_drag_pnt = None
        self.modifyOutline=True
        self.dragging=False
        self.setIndentation(20)
        self.setRootIsDecorated(True)
        
        



    def addKeyWord(self,item='',keyWord='Sim',ignoreExitZiDuan=False):
        ignoreExitZiDuan=self.parentWgt.ignoreExitZiDuanCKB.isChecked()
        if not item:
            item=self.currentItem()
        itemText=item.text(0)
        result = action.add_suffix(inputStr=itemText, suffix=keyWord,ignoreExitZiDuan=ignoreExitZiDuan)
        if result:
            if keyWord=='GRP' and not item.childCount():
                pass
            else:
                item.setText(0,result)

        for i in range(item.childCount()):
            child_item = item.child(i)
            lprint (child_item)
            self.addKeyWord(child_item, keyWord=keyWord,ignoreExitZiDuan=ignoreExitZiDuan)
        
        
    def _serachAndReplace(self):
        if isMayaEnv():
            self.SearchReplaceAddDialog=PySideLib.SearchReplaceAddDialog(parent=get_maya_window(),treeWidget=self)
        else:
            self.SearchReplaceAddDialog=PySideLib.SearchReplaceAddDialog(treeWidget=self)
        self.SearchReplaceAddDialog.show()

        
    def _set_item_bg(self, item):
        if item is not None and item != self._last_bg_colord_item:
            self._clear_bg_color()
 
            col_cnt = self.columnCount()
            # for ci in range(col_cnt):
            #     item.setBackground(ci, QBrush(QColor(130, 130, 225)))
            # self._last_bg_colord_item = item
            
    def _add_btn(self, item, cmbbox):
        btn = QPushButton('Btn')
        btn.clicked.connect(lambda: self._btn_clicked(item, cmbbox))
        return btn
    
    def _action_cutOrCopy_handler(self, cutOrCopy='cut'):
        try:
            self.cutOrCopy=cutOrCopy
            self._cutOrCopy_item = self.currentItem()
        except Exception as e:
            print(e)
            
    def _action_paste_handler(self):
        lprint (self._cutOrCopy_item)
        try:
            if self._cutOrCopy_item is None:
                return

            cur_item = self.currentItem()
 
            # 粘贴item为空
            if cur_item is None:
                return
 
            # 粘贴item不允许drop
            flags = cur_item.flags().__int__()
            if flags & Qt.ItemIsDropEnabled == 0:
                return
 
            new_item = self._cutOrCopy_item.clone()
            cur_item.addChild(new_item)
            cur_item.setExpanded(True)
            
            new_item.document.setdefault("subs", []).append(self._cutOrCopy_item.document)
            cur_item.document.setdefault("subs", []).append(self._cutOrCopy_item.document)
            #self.create_item_by_document(item, document)
            
            if self.cutOrCopy=='cut':
                self._remove_item(self._cutOrCopy_item)
                
            self._cutOrCopy_item = None
            
            #self._update_custom_control()
        except Exception as e:
            print(e)
            
            
    def getTextBeforeModify(self,item, column): #itemClicked 事件
        self.preText=self.getItemAbsPath(item,column)

    def handle_item_changed(self,  item, column):
        return 
        old_text = self.preText
        new_text = item.text(column)
        lprint("Item changed: ", old_text, " -> ", new_text)
        if old_text != new_text and column==0 :
            if self.parentWgt.synModifyDaGangCKB.isChecked() and self.modifyOutline==True:
                if cmds.objExists(old_text):
                    cmds.rename(old_text,new_text)
        


    
    def update(self,jsonFile):
        self.hierarchy = action.load_hierarchy(jsonFile)
        for document in self.hierarchy:
            item = self.create_item_by_document(self, document)
            self.set_expanded(item, True)
    

    def create_item_by_document(self, parent, document):
        if not isinstance(document, dict):
            return
        item = QTreeWidgetItem(parent)
        name=document.get("name", "")
        serachVar=re.search('{.+}',name)
        if serachVar:
            item.setToolTip(0,name)
            name=re.sub('{.+}',self.AssetName,name)
        item.setText(0, name)
        item.setText(1, document.get("description", ""))
        if item.parent():
            item.setData(2, Qt.AlignCenter, select_icon)
            item.setIcon(2, putin_icon)
        else:
            item.setText(2, u"放入")
        item.document = document
        for child in document.get("subs", []):
            key=document["subs"]
            self.create_item_by_document(item, child)
        if document.get("subs", []) or re.search('_Grp$',document[u'name'],flags=re.I):
            item.setIcon(0, group_icon)
        else:
            item.setIcon(0, mesh_icon)
        return item

     
    def _add_combobox(self, item):
        combobox = QComboBox()
        combobox.addItems(['item1', 'item2'])
        return combobox
    
    def _clear_bg_color(self):
        pass
        # 清除之前的背景色
        # if self._last_bg_colord_item is not None:
        #     col_cnt = self.columnCount()
        #     for ci in range(col_cnt):
        #         self._last_bg_colord_item.setBackground(ci, QBrush(QColor(255, 255, 255)))
        #     self._last_bg_colord_item = None
            
    def startDrag(self, supportedActions):
        item = self.currentItem()
 
        mime_data = TreeItemMimeData()
        mime_data.set_drag_data('ItemMimeData', item)
 
        drag = QDrag(self)
 
        # 定义drag事件，自定义的Mimedata传递到dragEnterEvent, dragMoveEvent, dropEvent
        drag.setMimeData(mime_data)
 
        # 记录下垂直滚动条的值，如果拖动没有改变滚动条，则用这个值，否则用改变之后的
        self._vertical_scroll_value = self.verticalScrollBar().value()
 
        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
            # 新的item已经克隆并添加之后，移除拖动之前的item
            self._remove_item(item)
 
            #self._update_custom_control()
 
            # 垂直滚动条设置新的值
            self.verticalScrollBar().setValue(self._vertical_scroll_value)
            self._clear_bg_color()
            
            
    def mousePressEvent(self, event):
        QTreeWidget.mousePressEvent(self, event)
        if event.button() == Qt.LeftButton and QApplication.keyboardModifiers() == Qt.ShiftModifier:
            item = self.itemAt(event.pos())
            #index = treeWidget.indexAt(event.pos())
            if isinstance(item, QTreeWidgetItem):
                self.set_expanded(item, item.isExpanded())
            # column = item.column() 
            # print (item,column)
        if event.button() == Qt.MiddleButton:
            self.setDragEnabled(True)
            self.item = self.currentItem()
            #super().mousePressEvent(event)
        else:
            event.ignore()

    def set_expanded(self, item, expanded):
        item.setExpanded(expanded)
        for i in range(item.childCount()):
            self.set_expanded(item.child(i), expanded)

    def edit_hierarchy(self, item, i):
        keys = ["name", "description"]
        lines = [NameLine, LabelLine]
        line = lines[i](self)
        line.setText(item.text(i))
        line.setFixedHeight(16)
        self.setItemWidget(item, i, line)
        line.setFocus()
        line.selectAll()

        def slot(value):
            # item.document[keys[i]] = value
            self.removeItemWidget(item, i)
            item.setText(i, value)
        line.callBackSignal.connect(slot)

    def dragEnterEvent(self, event):
        # 内部item移动
        lprint (event)
        if event.source() == self:
            if event.mimeData().hasFormat('ItemMimeData'):
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.ignore()
 
        # 外部item移动进TreeWidget
        else:
            if event.mimeData().hasText():
                event.accept()
            else:
                event.ignore()

    def drawRow(self, painter, option, index):
        super(Hierarchy, self).drawRow(painter, option, index)
        return
        if not self.dragging:
            return
        black_pen = QPen(QColor(0, 0, 0))  # 使用黑色画笔
        painter.setPen(black_pen)
        
        if self.dropIndicatorPosition() == QAbstractItemView.BelowItem:
            print ('BelowItem')
            y = option.rect.bottom() - 1
            painter.drawLine(option.rect.left(), y, option.rect.right(), y)

        elif self.dropIndicatorPosition() == QAbstractItemView.AboveItem:
            print ('AboveItem')
            y = option.rect.top()
            painter.drawLine(option.rect.left(), y, option.rect.right(), y)
            
    def dragMoveEvent(self, event):
        super(Hierarchy, self).dragMoveEvent(event)
        self.dragging = True
        try:
            # 拖动到边界，自动滚动
            y = event.pos().y()
            height = self.height()
            if y <= 20:
                self._vertical_scroll_value = self.verticalScrollBar().value() - 1
                self.verticalScrollBar().setValue(self._vertical_scroll_value)
            elif y >= height - 50:
                self._vertical_scroll_value = self.verticalScrollBar().value() + 1
                self.verticalScrollBar().setValue(self._vertical_scroll_value)
 
            item = self.itemAt(event.pos())
            # 如果拖动目的item为空
            if item is None:
                event.ignore()
                return
 
            # 如果拖动目的item不允许drop
            des_flags = self.itemAt(event.pos()).flags().__int__()
            if des_flags & Qt.ItemIsDropEnabled == 0:
                event.ignore()
                return
 
            # 内部拖拽item
            if event.source() == self:
                if event.mimeData().hasFormat('ItemMimeData'):
                    mime_data = event.mimeData()
                    item = mime_data.get_drag_data()
 
                    current_item = self.itemAt(event.pos())
                    is_ok = True
                    while current_item is not None:
                        if current_item == item:
                            is_ok = False
                            break
                        current_item = current_item.parent()
                    if is_ok:
                        item = self.itemAt(event.pos())
                        self._set_item_bg(item)
 
                        event.setDropAction(Qt.CopyAction)
                        event.accept()
                    else:
                        event.ignore()
                else:
                    event.ignore()
 
            # 外部拖拽进来
            elif event.mimeData().hasText():
                item = self.itemAt(event.pos())
                if item is not None:
                    self._set_item_bg(item)
 
                    event.setDropAction(Qt.MoveAction)
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        except Exception as e:
            print(e)
            
        # 更新item高亮显示
        index = self.indexAt(event.pos())
        if index.isValid():
            self.setCurrentIndex(index)




            
    def dropEvent(self, event):
        super(Hierarchy, self).dropEvent(event)
        try:
            # 内部拖拽item
            if event.source() == self:
                if event.mimeData().hasFormat('ItemMimeData'):
                    mime_data = event.mimeData()
                    item = mime_data.get_drag_data()
                    new_item = item.clone()
                    current_item = self.itemAt(event.pos())
 
                    if current_item is None:
                        event.ignore()
                    else:
                        current_item.addChild(new_item)
                        current_item.setExpanded(True)
                        event.setDropAction(Qt.MoveAction)
                        event.accept()
                else:
                    event.ignore()
 
            # 外部拖拽进来
            else:
                multi_file_path = event.mimeData().text()
                file_path_list = multi_file_path.split('\n')
 
                parent_item = self.itemAt(event.pos())
                if parent_item is None:
                    return
                else:
                    for file_path in file_path_list:
                        if file_path == '':
                            continue
 
                        file_path = file_path.replace('file:///', '', 1)
                        _, file_name = os.path.split(file_path)
 
                        child = QTreeWidgetItem(parent_item)
                        self._set_testcase_def_param(child, file_name)
                        child.setCheckState(0, Qt.Unchecked)
                        new_flags = Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | \
                                    Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable
                        child.setFlags(new_flags)
 
                        #combobox = self._add_combobox(child)
                        #self.setItemWidget(child, self._index_cmb, combobox)
                        #self.setItemWidget(child, self._index_btn, self._add_btn(child, combobox))
                        parent_item.setExpanded(True)
 
        except Exception as e:
            print(e)
        self.dragging = False

    def move_selected(self):
        item = self.currentItem()
        if item is None: #如果没有选中，不允许移动
            return
        # if item.childCount():# 如果有字层级，不允许移动
        #     return
        #if
        name = "|" + item.text(0) #获取当前层级的名字
        while item.parent(): #如果有父层级，继续获取父层级的名字
            item = item.parent() #获取父层级
            name = "|" + item.text(0) + name #拼接父层级的名字
        action.move_selected(name) #移动选中的物体到当前层级
        # if cmds.nodeType(name) == "transform":
        #     cmds.select(name)
        # print ('name:',name)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    def add_hierarchy(self,item='',name="name",label="description",icon='',modifyOutline=False):
        self.modifyOutline=modifyOutline
        if not item:
            item = self.currentItem()
        document = dict(
            name=name,
            description=label,
            children=[]
        )
        if item is None:
            self.create_item_by_document(self, document)
        else:
            item.document.setdefault("subs", []).append(document)
            self.create_item_by_document(item, document)
            
        if icon:
            item.setIcon(0, icon)
        else:
            if re.search(r"_Grp",self.currentItem().text(0),flags=re.I):
                item.setIcon(0, group_icon)
            else:
                item.setIcon(0, mesh_icon)
        self.modifyOutline=True


    def getItemAbsPath(self,item,column):
        name = "|" + item.text(column)
        while item.parent():
            item = item.parent()
            name = "|" + item.text(column) + name
        return name
    
    def _remove_item(self, item):
        item_parent = item.parent()
        if item_parent is not None:
            item_parent.removeChild(item)
        else:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
            
    def remove_hierarchy(self):
        item = self.currentItem()
        if item is None:
            return
        parent = item.parent()
        if parent is None:
            if item.document in self.hierarchy:
                self.hierarchy.remove(item.document)
            self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        else:
            if item.document in parent.document.setdefault("subs", []):
                parent.document.setdefault("subs", []).remove(item.document)
            parent.takeChild(parent.indexOfChild(item))
            if parent.childCount():
                parent.setIcon(0, group_icon)
            else:
                parent.setIcon(0, mesh_icon)

    def save_hierarchy(self):

        # default_path = os.path.abspath(__file__ + "/../hierarchy.json")
        default_path = os.path.abspath(__file__ + "/../template")
        path, _ = QFileDialog.getSaveFileName(self, "save hierarchy", default_path, "json(*.json)")
        # if not path:
        #     return
        # with open(path, "w") as write:
        #     for key,val in self.hierarchy.items():
        #         write.write(json.dumps(self.hierarchy, indent=2))
        # def traverse(item, level):
        #     for i in range(item.childCount()): 
        #         child = item.child(i) 
        #         print("Level", level, "Item:", child.text(0)) 
        #         traverse(child, level + 1)
        # traverse(self.invisibleRootItem(), 0)
        data = []
        def save_tree_to_json(root, data):
            for i in range(root.childCount()):
                item = root.child(i)
                children = []
                if item.toolTip(0):
                    name=item.toolTip(0)
                    if self.AssetName in item.text(0):
                        name=item.text(0).replace(self.AssetName,'{asset}')
                    else:
                        name=item.text(0)
                else:
                    name=item.text(0)
                print (root,root.childCount(),name,255)
                description=item.text(1)
                lprint (description)
                try:
                    description=description.decode('unicode_escape')
                except:
                    pass
                data.append({'name': name,
                             'expanded':True,
                             'description': description,
                             'condition': 'True',
                             'subs': children,
                             },
                            )
                save_tree_to_json(item, children)
        save_tree_to_json(self.invisibleRootItem(), data)
        with codecs.open(path, 'w',encoding='utf8') as file:
            json.dump(data, file, indent=2)

    def load_hierarchy(self):
        self.modifyOutline==False
        default_path = os.path.abspath(__file__ + "/../template")
        path, _ = QFileDialog.getOpenFileName(self, "load hierarchy", default_path, "json(*.json)")
        if not path:
            return
        if not os.path.isfile(path):
            return
        with open(path, "r") as read:
            self.hierarchy = json.loads(read.read())
        self.clear()
        for document in self.hierarchy:
            item = self.create_item_by_document(self, document)
            self.set_expanded(item, True)
        self.modifyOutline==True

    def scene_hierarchy(self):
        self.hierarchy = action.get_data_by_scene()
        self.clear()
        for document in self.hierarchy:
            item = self.create_item_by_document(self, document)
            self.set_expanded(item, True)

    @staticmethod
    def select_hierarchy(item):
        print ('select_hierarchy')
        if item is None:
            return
        name = "|" + item.text(0)
        while item.parent():
            item = item.parent()
            name = "|" + item.text(0) + name
        print (name)
        if isMayaEnv():
            if pm.objExists(name):
                return pm.select(name)
        
    def show_ChildrenInOutline(self,item):
        lprint (item,)
        if not item:
            item = self.currentItem()
        childCount=item.childCount()
        while item.childCount:
            for i in range(childCount):
                child_item=item.child(i)
                lprint (child_item,child_item.text(0))
                itemAbsPath=self.getItemAbsPath(child_item,0)
                lprint (itemAbsPath)
                childObjs=pm.listRelatives(itemAbsPath,ad=True,fullPath=True)
                for childObj in childObjs:
                    childObjName=childObj.split('|')[-1]
                    self.add_hierarchy(item,name=childObjName,label="00*物体",icon=mesh_icon)
                    
    def _btn_clicked(self, item, cmbbox):
        print(item.text(0))
        print(cmbbox.currentText())

    def _update_custom_control(self):
        try:
            it = QTreeWidgetItemIterator(self)
            while True:
                it_item = it.value()
                if it_item is None:
                    break

                if it_item.childCount() > 0 or it_item.parent() is None:
                    if self.itemWidget(it_item, self._index_cmb) is not None:
                        self.removeItemWidget(it_item, self._index_cmb)
                        self.removeItemWidget(it_item, self._index_btn)
                else:
                    if self.itemWidget(it_item, self._index_cmb) is None:
                        combobox = self._add_combobox(it_item)
                        self.setItemWidget(it_item, self._index_cmb, combobox)
                        self.setItemWidget(it_item, self._index_btn, self._add_btn(it_item, combobox))
                it = it.__iadd__(1)
        except Exception as e:
            print(e)

    def get_items_and_widgets_at_level(self, level):
        def get_items_recursive(parent_item, current_level):
            items = {}
            for i in range(parent_item.childCount()):
                child_item = parent_item.child(i)
                if current_level == level:
                    parent_items = []
                    current_item = child_item
                    while current_item.parent():
                        current_item = current_item.parent()
                        parent_items.insert(0, current_item)
                    items[child_item] = parent_items
                else:
                    items.update(get_items_recursive(child_item, current_level + 1))
            return items

        if level == 0:
            items = {}
            for i in range(self.topLevelItemCount()):
                top_level_item = self.topLevelItem(i)
                items[top_level_item] = []
            return items
        else:
            return get_items_recursive(self.invisibleRootItem(), 1)


    def hide_items_with_text_in_list(self, checkbox_state_list):
        # This function checks if all children of a given item are hidden.
        def all_children_hidden(item):
            for i in range(item.childCount()):
                child_item = item.child(i)
                if not child_item.isHidden():
                    return False
            return True

        # This function updates the visibility of the given item and its parents.
        def update_item_visibility(item, hidden):
            item.setHidden(not hidden)

            # If all children are hidden, hide the parent item as well
            parent_item = item.parent()
            if parent_item and all_children_hidden(parent_item):
                parent_item.setHidden(True)
            # If the item is being shown, make sure all its parents are also shown
            
            if  hidden:
                while parent_item:
                    parent_item.setHidden(False)
                    parent_item = parent_item.parent()

        # For each checkbox and state in the checkbox_state_list, update the item visibility accordingly
        for checkbox, state in checkbox_state_list:
            item = getattr(checkbox, 'Wgt', None)
            if item:
                update_item_visibility(item, state)




           
class Main(QDialog):
    def __init__(self):

        if sys.executable.endswith('maya.exe'):
            QDialog.__init__(self, QApplication.activeWindow(), Qt.Window)
        else:
            super().__init__()
        self.setStyleSheet(self_qss)
        
        self.setWindowTitle(u"大纲层级命名")
        
        self.MaintopLay= QHBoxLayout()

        self.MainWgt=QWidget()
        self.MainWgtLay = QVBoxLayout()
        self.MainWgt.setLayout(self.MainWgtLay)
        
        jsonFileList=[]
        lprint (os.path.dirname(__file__) + "/template")
        if Lugwit_publicPath:
            for jsonDir in [Lugwit_publicPath+r"\Template\Model\Outline",os.path.dirname(__file__) + "/template",]:
                jsonFileList+=[x for x in glob.glob(jsonDir+'/*.json')]
        else:
            for jsonDir in [os.path.dirname(__file__) + "/template",]:
                jsonFileList+=[x for x in glob.glob(jsonDir+'/*.json')]
        #return
        
        self.hierarchyWgt = Hierarchy(jsonFileList[0],self)
        
        
        self.MaintopLay.addWidget(self.filterHierarchyWgt())
        self.MaintopLay.addWidget(self.MainWgt)
        self.MainWgt.setFixedWidth(500)
        
        
        self.setLayout(self.MaintopLay)
        try:
            self.MayaFileName=cmds.file(q=True, sceneName=True)
        except:
            self.MayaFileName='D:/AA.ma'
            
        self.ShowWindow=True
        if not self.MayaFileName:
            cmds.confirmDialog( title=u'请先打开一个Maya文件', message=u'请先打开一个Maya文件', button=['Yes'] )
            self.ShowWindow=False
            self.destroy()
            return
        
        presetWgt=QWidget()
        presetWgtLayout=QVBoxLayout()
        presetWgtLayout=QHBoxLayout()
        presetWgt.setStyleSheet('Background-color:#08ffffff;')
        presetWgt.setLayout(presetWgtLayout)
        
        
        self.presetNameWgt=PySideLib.LPathSel(par=self.MainWgtLay,l_lab=u'',DialogCommit=u'预设文件',fileType="*.json",buttonName=u'...',chooseFunc=u'getOpenFileName',defaultPath=jsonFileList[0])
        
        self.presetNameWgt.widget[0].addItems(jsonFileList)
        self.presetNameWgt.widget[0].currentIndexChanged.connect(self.jsonFileChangeFunc)
        presetWgtLayout.addWidget(QLabel('预设文件'),1)
        presetWgtLayout.addWidget(self.presetNameWgt,30)
        self.MainWgtLay.addWidget(presetWgt)
        
        btnWgt=QWidget()
        btnWgt.setStyleSheet('Background-color:#08ffffff;')
        btnWgtLayout=QHBoxLayout()
        btnWgt.setLayout(btnWgtLayout)
        
        self.synModifyDaGangCKB=QCheckBox(u'同步修改\n大纲命名')
        btnWgtLayout.addWidget(self.synModifyDaGangCKB,1)
        self.synModifyDaGangCKB.setChecked(True)
        self.synModifyDaGangCKB.setVisible(liscense)
        
        self.ignoreExitZiDuanCKB=QCheckBox(u'忽略已存\n在的字段')
        btnWgtLayout.addWidget(self.ignoreExitZiDuanCKB,1)
        self.ignoreExitZiDuanCKB.setChecked(True)
        self.ignoreExitZiDuanCKB.setVisible(liscense)
        
        # 此功能还要完善
        # upToP4Btn=QPushButton(u'显示/隐藏大纲中的模型')
        # btnWgtLayout.addWidget(upToP4Btn,10)
        # upToP4Btn.clicked.connect(self.upToP4_Func)
        
        #此功能还要bug
        upToP4Btn=QPushButton(u'上传json配\n置文件到P4')
        btnWgtLayout.addWidget(upToP4Btn,10)
        upToP4Btn.clicked.connect(self.upToP4_Func)
        upToP4Btn.setVisible(liscense)
        upToP4Btn.setEnabled(0)
        
        addHierarchyBtn=QPushButton(u'从excel文件\n预设添加层级')
        btnWgtLayout.addWidget(addHierarchyBtn,10)
        addHierarchyBtn.clicked.connect(self.add_hierarchyFromExcel_Func)
        addHierarchyBtn.setVisible(liscense)

        
        # refreshNodeExistStateBtn=QPushButton('刷新节点存在状态')
        # btnWgtLayout.addWidget(refreshNodeExistStateBtn,10)
        # refreshNodeExistStateBtn.clicked.connect(self.refreshNodeExistState_Func)
        
        helpButton=QPushButton('?')
        helpButton.setStyleSheet('height:5px;background-color:#888a99;')
        btnWgtLayout.addWidget(helpButton,5)
        helpButton.setFixedSize(35,35)

        self.MainWgtLay.addWidget(btnWgt)
        
        
        self.MainWgtLay.addWidget(self.hierarchyWgt)
        self.resize(600, 850)
        
        
        
    def filterHierarchyWgt(self):
        wgt=QWidget()
        wgt.setFixedWidth(150)
        wgt.setObjectName('filterHierarchyWgt')
        lay=QVBoxLayout()
        wgt.setLayout(lay)
        filterDisplay=QHBoxLayout()
        refreshBtn=QPushButton(text=u'刷新')
        lay.addWidget(refreshBtn)
        lay.addWidget(QLabel(u'过滤显示'))
        selLayout=QHBoxLayout()
        lay.addLayout(selLayout)
        selLayout.addWidget(QPushButton(text=u'全选'))
        selLayout.addWidget(QPushButton(text=u'反选'))
        
        filterDict= self.hierarchyWgt.get_items_and_widgets_at_level( 4 )

        self.filterBtnGrp=QButtonGroup()
        self.filterBtnGrp.setExclusive(False)
        parent_levelList=[]
        for key,val in filterDict.items():
            level2_Wgt=val[-2]
            tt=level2_Wgt.text(0)
            
            label=key.text(1)
            qh=QHBoxLayout()
            ckb=QCheckBox(label)
            ckb.setChecked(True)
            ckb.stateChanged.connect(partial(self.filterCkbChangeCommand,ckb))
            setattr(ckb,'Wgt',key)
            setattr(ckb,'parent',val[-2])
            self.filterBtnGrp.addButton(ckb)
            
            qh.addWidget(ckb,10)
            fbtn=QPushButton('F')
            fbtn.setFixedSize(15,15)
            fbtn.setStyleSheet("QPushButton { padding: 0; }")
            qh.addWidget(fbtn,1)
            qh.setContentsMargins(0,0,0,0)
            if tt not in parent_levelList:
                setattr(self,tt+'_GB',QGroupBox(tt))
                setattr(self,tt+'_Lay',QVBoxLayout())
                getattr(self,tt+'_GB').setLayout(getattr(self,tt+'_Lay'))
                lay.addWidget(getattr(self,tt+'_GB'))
                parent_levelList.append(tt)
                getattr(self,tt+'_Lay').setContentsMargins(0,0,0,0)

            getattr(self,tt+'_Lay').addLayout(qh)
            #lprint(parent_levelList);
            #lprint (getattr(self,tt+'_Lay'),tt)
            #lprint (getattr(self,tt+'_Lay').itemAt(0).itemAt(0))
            fbtn.clicked.connect(partial(self.highDisItem,key))
            
            
        lay.addStretch(20)
        wgt.setStyleSheet('''#filterHierarchyWgt{
                        Background-color:#15acacac;
                        border: 2px solid #15c3c3c3;
                        }''')
        return wgt
    
    def highDisItem(self,key):
        
        self.hierarchyWgt.scrollToItem(key, self.hierarchyWgt.PositionAtTop)
        def unhighlight_item(item, column):
            if item.background(column) != Qt.transparent:
                item.setBackground(column, Qt.transparent)
            for i in range(item.childCount()):
                unhighlight_item(item.child(i), column)
        # 取消所有项的高亮显示
        if hasattr(self,'highlightItem'):
            for item in self.highlightItem:
                unhighlight_item(item, 0)
        self.highlightItem=[]
        # 更改特定项的背景颜色
        highlight_color = QColor(255, 255, 0,10)  # 黄色
        
        def highlight_item(item, column, color):
            item.setBackgroundColor(column, color)
            self.highlightItem.append(item)
            for i in range(item.childCount()):
                highlight_item(item.child(i), column, color)
        highlight_item(key,0,highlight_color)
            
            
    def closeEvent(self, event):
        print("Window is closing...")
        # global hierarchyMainwindowB
        #   del hierarchyMainwindowB
        # hierarchyFromExcelwin.destroy() 
        
    def upToP4_Func(self):
        self.hierarchyWgt.show_ChildrenInOutline(self.hierarchyWgt.invisibleRootItem())
    
    def jsonFileChangeFunc(self):
        print ('changg to {}'.format(self.presetNameWgt.widget[0].currentText()))
        self.hierarchyWgt.clear()
        self.hierarchyWgt.update(self.presetNameWgt.widget[0].currentText())
        
    def add_hierarchyFromExcel_Func(self):
        if not hasattr(self, 'hierarchyFromExcelwin'):
            self.hierarchyFromExcelwin=hierarchy_QTableWidget(self)
            self.MaintopLay.addWidget(self.hierarchyFromExcelwin)
            self.hierarchyFromExcelwin.setFixedWidth(500)
        if self.hierarchyFromExcelwin.isVisible():
            self.hierarchyFromExcelwin.setVisible(False)
            #self.setMinimumWidth(1300)
        else:
            self.hierarchyFromExcelwin.setVisible(True)
            #self.setMinimumWidth(600)
        self.adjustSize()
        self.setFixedHeight(900)

        
    def refreshNodeExistState_Func(self):
        pass
    
    def doShake(self):
        self.doShakeWindow(self)

    # 下面这个方法可以做成这样的封装给任何控件
    def doShakeWindow(self, target):
        """窗口抖动动画
        :param target:        目标控件
        """
        if hasattr(target, '_shake_animation'):
            # 如果已经有该对象则跳过
            return

        animation = QPropertyAnimation(target, b'pos', target)
        target._shake_animation = animation
        animation.finished.connect(lambda: delattr(target, '_shake_animation'))

        pos = target.pos()
        x, y = pos.x(), pos.y()

        animation.setDuration(200)
        animation.setLoopCount(2)
        animation.setKeyValueAt(0, QPoint(x, y))
        animation.setKeyValueAt(0.09, QPoint(x + 2, y - 2))
        animation.setKeyValueAt(0.18, QPoint(x + 4, y - 4))
        animation.setKeyValueAt(0.27, QPoint(x + 2, y - 6))
        animation.setKeyValueAt(0.36, QPoint(x + 0, y - 8))
        animation.setKeyValueAt(0.45, QPoint(x - 2, y - 10))
        animation.setKeyValueAt(0.54, QPoint(x - 4, y - 8))
        animation.setKeyValueAt(0.63, QPoint(x - 6, y - 6))
        animation.setKeyValueAt(0.72, QPoint(x - 8, y - 4))
        animation.setKeyValueAt(0.81, QPoint(x - 6, y - 2))
        animation.setKeyValueAt(0.90, QPoint(x - 4, y - 0))
        animation.setKeyValueAt(0.99, QPoint(x - 2, y + 2))
        animation.setEndValue(QPoint(x, y))

        animation.start(animation.DeleteWhenStopped)

    def filterCkbChangeCommand(self,ckb,state):
        self.hierarchyWgt.hide_items_with_text_in_list([(ckb,state)])
        
        
class hierarchy_QTableWidget(QWidget):
    def __init__(self,parentWidget=''):
        #super(hierarchy_QTableWidget,self).__init__(QApplication.activeWindow(),Qt.Window)
        super(hierarchy_QTableWidget,self).__init__()
        self.parentWidget=parentWidget
        self.hierarchyWgt=parentWidget.hierarchyWgt
        self.topLay=QHBoxLayout()
        self.setLayout(self.topLay)
        self.Left1_HLay=QVBoxLayout()
        self.Left2_HLay=QVBoxLayout()
        self.topLay.addLayout(self.Left1_HLay)
        self.topLay.addLayout(self.Left2_HLay)
        self.resize(500, 900)
        self.typeBtnGroup()
        self.excel()
    
    
    
    def typeBtnGroup(self):
        btnWgtLayout=QVBoxLayout()
        btnWgtLayout.setContentsMargins(0,0,0,0)
        self.Left1_HLay.addLayout(btnWgtLayout)

        DirectionWgtGroupBox = QGroupBox(u'方向选择')
        Direction_bntLayout=QVBoxLayout()
        Direction_bntLayout.setContentsMargins(0,0,0,0)
        DirectionWgtGroupBox.setLayout(Direction_bntLayout)
        btnWgtLayout.addWidget(DirectionWgtGroupBox)
        
        Node_DirectionWgtA=QRadioButton(u'自动')
        Node_DirectionWgtA.setToolTip(u'根据选择的节点是否包含"_L|_R"关键字决定方向')
        Node_DirectionWgtA.setChecked(1)
        Node_DirectionWgtB=QRadioButton(u'无')
        Node_DirectionWgtC=QRadioButton(u'左')
        Node_DirectionWgtD=QRadioButton(u'右')
        self.Node_DirectionGrp=QButtonGroup(self)
        self.Node_DirectionGrp.addButton(Node_DirectionWgtA)
        self.Node_DirectionGrp.addButton(Node_DirectionWgtB)
        self.Node_DirectionGrp.addButton(Node_DirectionWgtC)
        self.Node_DirectionGrp.addButton(Node_DirectionWgtD)
        Direction_bntLayout.addWidget(Node_DirectionWgtA)
        Direction_bntLayout.addWidget(Node_DirectionWgtB)
        Direction_bntLayout.addWidget(Node_DirectionWgtC)
        Direction_bntLayout.addWidget(Node_DirectionWgtD)
        
        createPosWgtGroupBox = QGroupBox(u'创建位置')
        createPos_bntLayout=QVBoxLayout()
        createPos_bntLayout.setContentsMargins(0,0,0,0)
        createPosWgtGroupBox.setLayout(createPos_bntLayout)
        btnWgtLayout.addWidget(createPosWgtGroupBox)
        
        Node_createPosWgtA=QRadioButton(u'替换')
        Node_createPosWgtB=QRadioButton(u'下一层级')
        Node_createPosWgtB.setChecked(1)

        self.Node_createPosGrp=QButtonGroup(self)
        self.Node_createPosGrp.addButton(Node_createPosWgtA)
        self.Node_createPosGrp.addButton(Node_createPosWgtB)

        createPos_bntLayout.addWidget(Node_createPosWgtA)
        createPos_bntLayout.addWidget(Node_createPosWgtB)
        
        self.assetTypeWgtGroupBox = QGroupBox(u'资产类型')
        assetType_bntLayout=QVBoxLayout()
        assetType_bntLayout.setContentsMargins(0,0,0,0)
        self.assetTypeWgtGroupBox.setLayout(assetType_bntLayout)
        self.Left1_HLay.addWidget(self.assetTypeWgtGroupBox)
        
        Node_assetTypeWgtA=QRadioButton(u'角色')
        Node_assetTypeWgtA.setChecked(1)
        Node_assetTypeWgtB=QRadioButton(u'道具')
        Node_assetTypeWgtC=QRadioButton(u'场景')

        self.Node_assetTypeGrp=QButtonGroup(self)
        self.Node_assetTypeGrp.addButton(Node_assetTypeWgtA)
        self.Node_assetTypeGrp.addButton(Node_assetTypeWgtB)
        self.Node_assetTypeGrp.addButton(Node_assetTypeWgtC)
        self.Node_assetTypeGrp.buttonToggled.connect(self.assetTypeChange)

        assetType_bntLayout.addWidget(Node_assetTypeWgtA)
        assetType_bntLayout.addWidget(Node_assetTypeWgtB)
        assetType_bntLayout.addWidget(Node_assetTypeWgtC)
        
        editExcelBtn=QPushButton(u'编辑excel表格')
        self.Left1_HLay.addWidget(editExcelBtn)
        editExcelBtn.clicked.connect(lambda:os.startfile(u'A:/TD/Template/Model/Outline/资产分组命名规范索引表.xls'))
        
        self.Left1_HLay.addStretch(2)

    def assetTypeChange(self):
        text=self.Node_assetTypeGrp.checkedButton().text()
        rangeDict={u'角色':[1,2],u'道具':[3,4],u'场景':[5,6]}
        self.excel(init=0,readRowList=rangeDict[text])
        print (text)
        
    def excel(self,init=1,readRowList=[1,2]):
        hierarchyNameDict=self.getHierarchyNameDict(readRowList)
        row1,row2=hierarchyNameDict
        columnAmount=2
        if init:
            self.nstable = QTableWidget(300, columnAmount)
            self.nstable.setHorizontalHeaderLabels([u'英文',u'中文'])
            self.Left2_HLay.addWidget(self.nstable)
            self.nstable.doubleClicked.connect(self.setCellContentFunc)
        else:
            self.nstable.clear()
            
        
        for  i in range(300-1):
            if i>300:
                break
            self.nstable.verticalHeader().resizeSection(i, 18)
            # lockItem= QTableWidgetItem()
            # #lockItem.setIcon(QIcon(group_icon if ))
            # self.nstable.setVerticalHeaderItem(i,lockItem)
            for j in range(columnAmount):
                self.nstable.horizontalHeader().resizeSection(j, 173)
                widgetName=hierarchyNameDict[j][i+1]
                widget= QTableWidgetItem(widgetName)
                if j%2==0 and widgetName:
                    widget.setIcon(group_icon if re.search('_Grp$',widgetName,flags=re.I)  else mesh_icon)
                self.nstable.setItem(i, j, widget)
                try:
                    widget.setFlags( Qt.ItemFlag.ItemIsEnabled)
                except:
                    pass

        try:
            self.setWindowModality(Qt.WindowModality.NonModal)
        except:
            pass
        
    def getHierarchyNameDict(self,readRowList=[1,2]):
        HierarchyNameDict=readExcel.readHierarchyNameDict(readRowList)
        lprint (HierarchyNameDict)
        return HierarchyNameDict
    
    # 双击时设置父级单元格内容
    def setCellContentFunc(self,ModelIndex):
        itemRowIndex=ModelIndex.row()
        lprint (itemRowIndex)
        row0Text=self.nstable.item(itemRowIndex,0).text()
        row1Text=self.nstable.item(itemRowIndex,1).text()
        parWinSelectedItems=self.hierarchyWgt.selectedItems()
        if parWinSelectedItems:
            parWinSelectedItem=parWinSelectedItems[0]
            self.hierarchyWgt.preText=self.hierarchyWgt.getItemAbsPath(parWinSelectedItem,0)
            parWinSelectedItem_text=parWinSelectedItem.text(0)

            Direction_text=self.Node_DirectionGrp.checkedButton().text()
            if Direction_text==u'自动':
                search_direct=re.search('_L|_R', parWinSelectedItem_text,flags=re.I)
                if search_direct:
                    Direction_text=search_direct.group()
                else:
                    Direction_text=u'无'
            lprint (Direction_text)
            Direction_text_Dict={u'左':'_L',u'右':'_R',u'无':'','_L':'_L','_R':'_R'}
            direction=Direction_text_Dict[Direction_text]
            row0Text=re.sub('_Grp','{}_Grp'.format(direction),row0Text,flags=re.I) if re.search('_Grp',row0Text,flags=re.I) else row0Text+direction
            
            Node_createPos_text=self.Node_createPosGrp.checkedButton().text()
            icon=self.nstable.item(itemRowIndex,0).icon()
            if Node_createPos_text==u'替换':
                parWinSelectedItem.setText(0, row0Text)
                parWinSelectedItem.setText(1, row1Text)
                parWinSelectedItem.setIcon(0, icon)
                cmds.warning(parWinSelectedItem)
            elif Node_createPos_text==u'下一层级':
                self.hierarchyWgt.add_hierarchy(parWinSelectedItem,name=row0Text,label=row1Text)
        # cmds.warning(itemRowIndex)

def get_maya_window():
    # get the maya main window as a QMainWindow instance
    win = omui.MQtUtil_mainWindow()
    ptr = shiboken2.wrapInstance(long(win), QWidget)
    return ptr

window = None

@try_exp
def show_Main(*args):
    
    if sys.executable.endswith('maya.exe'):
        lprint (sys.executable)
    else:
        print ('---------')
        app = QApplication(sys.argv)
    
    if 'hierarchyMainwindowB' in globals() and globals()['hierarchyMainwindowB'].ShowWindow:
        lprint(globals()['hierarchyMainwindowB'])
        win=globals()['hierarchyMainwindowB']
        try:
            if win.isMinimized() or win.isHidden():
                globals()['hierarchyMainwindowB'].showNormal()
            else:
                globals()['hierarchyMainwindowB'].doShake()
        except:
            print (u'创建窗口hierarchyMainwindowB')
            global hierarchyMainwindowB
            hierarchyMainwindowB = Main()
            if hierarchyMainwindowB.ShowWindow:
                globals()['hierarchyMainwindowB'].show()
            else:
                print (u'删除{}'.format('hierarchyMainwindowB'))
            del globals()['hierarchyMainwindowB']
    else:
        print (u'创建窗口hierarchyMainwindowB')
        
        hierarchyMainwindowB = Main()
        if hierarchyMainwindowB.ShowWindow:
            globals()['hierarchyMainwindowB'].show()
        else:
            print (u'删除{}'.format('hierarchyMainwindowB'))
        del globals()['hierarchyMainwindowB']


    if not sys.executable.endswith('maya.exe'):
        app.exec_()








        
def show_hierarchy_QTableWidget_Win(*args):
    if sys.executable.endswith('maya.exe'):
        pass
    else:
        pass
    if 'hierarchy_QTableWidget_win' not in globals():
        global hierarchy_QTableWidget_win
        hierarchy_QTableWidget_win=hierarchy_QTableWidget()
        hierarchy_QTableWidget_win.show()
    if not sys.executable.endswith('maya.exe'):
        
        sys.exit(app.exec_())

print (__name__)
if __name__ == '__main__':
    #show_hierarchy_QTableWidget_Win()
    show_Main()
    
'''
import sys
sys.path.append(r'D:\TD_Depot\TD\hyws\maya\scripts\fun')
import mod.hierarchy.ui as ui
reload(ui)
ui.show_Main()

'''
