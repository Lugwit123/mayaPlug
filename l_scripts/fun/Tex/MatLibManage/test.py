import sys
import os
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

app = QApplication(sys.argv)

# 创建一个 QTreeWidget
tree_widget = QTreeWidget()

# 启用缩进和装饰根节点
tree_widget.setIndentation(20)
tree_widget.setRootIsDecorated(True)

# 设置样式表
current_dir = os.path.dirname(os.path.abspath(__file__))
tree_widget.setStyleSheet(f"""
QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {{
    image: url({os.path.join(current_dir, 'icons', 'plus.png')});
    border-image: none;
}}
QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {{
    image: url({os.path.join(current_dir, 'icons', 'minus.png')});
    border-image: none;
}}
""")

# 添加示例数据
root_item = QTreeWidgetItem(tree_widget, ['Root'])
child_item = QTreeWidgetItem(root_item, ['Child 1'])
child_item2 = QTreeWidgetItem(root_item, ['Child 2'])
grandchild_item = QTreeWidgetItem(child_item2, ['Grandchild'])

#
