import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QAbstractItemView


class CustomTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 启用拖拽功能
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)

        # 添加示例数据
        for i in range(5):
            item = QTreeWidgetItem(self, [f"Item {i+1}"])
            for j in range(3):
                child_item = QTreeWidgetItem(item, [f"Child {j+1}"])

    def dragMoveEvent(self, event):
        super().dragMoveEvent(event)

        # 更新item高亮显示
        index = self.indexAt(event.pos())
        if index.isValid():
            self.setCurrentIndex(index)

    def drawRow(self, painter, option, index):
        super().drawRow(painter, option, index)

        y = option.rect.bottom() - 1
        painter.drawLine(option.rect.left(), y, option.rect.right(), y)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    tree_widget = CustomTreeWidget()
    tree_widget.show()
    sys.exit(app.exec_())
