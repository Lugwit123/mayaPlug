# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainBDDfYb.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1009, 886)
        Form.setStyleSheet(u"QMainWindow{\n"
"background-color:#1d1d1d;\n"
"}\n"
"\n"
"QWidget{\n"
"  background-color: #181818;\n"
"}\n"
"\n"
"QMenuBar{\n"
"background-color:#1d1d1d;\n"
"padding:5px;\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"}\n"
"\n"
"QMenuBar::item{\n"
"background-color:#1d1d1d;\n"
"color:#fff;\n"
"padding:5px;\n"
"\n"
"}\n"
"\n"
"QMenu{\n"
"color:#fff;\n"
"padding:0;\n"
"}\n"
"\n"
"QMenu::item:selected{\n"
"color:#fff;\n"
"background-color:#00aba9;\n"
"}\n"
"\n"
"QTableWidget{\n"
"\n"
"background-color:#3d3d3d;\n"
"color:#fff;\n"
"  selection-background-color: #da532c;\n"
"border:solid;\n"
"border-width:3px;\n"
"border-color:#da532c;\n"
"}\n"
"QHeaderView::section{\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(20, 158, 217, 255), stop:1 rgba(36, 158, 217, 255));\n"
"border:none;\n"
"border-top-style:solid;\n"
"border-width:1px;\n"
"border-top-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(20, 158, 217, 255), stop:1 rgba(36, 158, 217, 255));\n"
"color:#fff;\n"
""
                        "\n"
"}\n"
"QHeaderView{\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(20, 158, 217, 255), stop:1 rgba(36, 158, 217, 255));\n"
"\n"
"border:none;\n"
"border-top-style:solid;\n"
"border-width:1px;\n"
"border-top-color:#149ED9;\n"
"color:#fff;\n"
"font: 12px;\n"
"}\n"
"\n"
"QTableCornerButton::section{\n"
"border:none;\n"
"background-color:#149ED9;\n"
"}\n"
"\n"
"QListWidget{\n"
"background-color:#3d3d3d;\n"
"color:#fff;\n"
"}\n"
"\n"
"QMenu{\n"
"background-color:#3d3d3d;\n"
"}\n"
"QStatusBar{\n"
"background-color:#7e3878;\n"
"color:#fff;\n"
"}\n"
"\n"
"\n"
"QLabel{\n"
"border-style:solid;\n"
"background-color:#3d3d3d;\n"
"color:#fff;\n"
"border-radius:7px;\n"
"font: 15 10pt \"Open Sans\";\n"
"padding:5px;\n"
"}\n"
"\n"
"\n"
"QRadioButton{\n"
"\n"
"color:#ccc;\n"
"\n"
"}\n"
"\n"
"QCheckBox{\n"
"\n"
"color:#ccc;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton{\n"
"border-style:solid;\n"
"background-color:#3d3d3d;\n"
"color:#fff;\n"
"border-radius:7px;\n"
"font: 15 10pt \"Open Sans\";\n"
""
                        "padding:5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"color:#ccc;\n"
"	background-color: qlineargradient(spread:pad, x1:0.517, y1:0, x2:0.517, y2:1, stop:0 rgba(45, 45, 45, 255), stop:0.505682 rgba(45, 45, 45, 255), stop:1 rgba(29, 29, 29, 255));\n"
"	border-color:#2d89ef;\n"
"border-width:1px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0.517, y1:0, x2:0.517, y2:1, stop:0 rgba(29, 29, 29, 255), stop:0.505682 rgba(45, 45, 45, 255), stop:1 rgba(29, 29, 29, 255));\n"
"}\n"
"\n"
"\n"
"QTabWidget::tab{\n"
"background-color:#3d3d3d;\n"
"}\n"
"\n"
"QLineEdit{\n"
"border-radius:0;\n"
"background-color:#a4dbdb;\n"
"font-family: \"Microsoft YaHei\";\n"
"\n"
"}\n"
"\n"
"QProgressBar{\n"
"border-radius:0;\n"
"text-align:center;\n"
"color:#fff;\n"
"background-color:transparent;\n"
"border: 2px solid #e3a21a;\n"
"border-radius:7px;\n"
"	font: 75 12pt \"Open Sans\";\n"
"  font-family: \"Microsoft YaHei\";\n"
"\n"
"}\n"
"\n"
"QProgressBar::chunk{\n"
"background-color:#2d89ef;\n"
"wid"
                        "th:20px;\n"
"}\n"
"\n"
"\n"
"QComboBox {\n"
"    background: #3c3737;\n"
"    color: #dbdbdb;\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    border-style: solid;\n"
"}\n"
"\n"
"/* \u8bbe\u7f6e\u4e0b\u62c9\u6846\u4e2d\u5217\u8868\u7684\u80cc\u666f\u989c\u8272\u4e3a\u9ec4\u8272\uff0c\u6587\u5b57\u989c\u8272\u4e3a\u84dd\u8272 */\n"
"QComboBox QAbstractItemView {\n"
"    background: #3c3737;\n"
"    color: #dbdbdb;\n"
"}\n"
"\n"
"\n"
"\n"
"QGroupBox {\n"
"\n"
"    color: #ffffff;\n"
"    background-color: #454545;\n"
"    text-align: top;\n"
"    border: 2px solid gray;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* position at the top center */\n"
"    font :  55 5pt \"Open Sans\";\n"
"\n"
"\n"
"}\n"
"\n"
"QGroupBox::!enabled {\n"
"	background-color: rgb(220, 220, 220);\n"
"    title{ color: red ;};\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox{\n"
"    border-color:#2d89ef;\n"
"    border-width:2px"
                        ";\n"
"    height:25px;\n"
"    border-radius: 2px;\n"
"    background-color:#c2c4c9;\n"
"}\n"
"\n"
"\n"
"\n"
"QTabBar[orientation=\"horizontal\"]{\n"
"  text-transform: uppercase;\n"
"  font-weight: bold;\n"
"  font-size: 15px;\n"
"}\n"
"\n"
"QTabBar[orientation=\"horizontal\"]::tab {\n"
"  color: #808080;\n"
"  border: 4px;\n"
"  width: 20px;\n"
"  height: 30px;\n"
"}\n"
"\n"
"\n"
"\n"
"QTabBar[orientation=\"horizontal\"]::tab:selected {\n"
"  color: #222222;\n"
"  border: 4px;\n"
"  width: 25px;\n"
"  height: 30px;\n"
"}\n"
"\n"
"\n"
"QTabBar[orientation=\"horizontal\"]::tab::hover {\n"
"  color: #18292c;\n"
"  border: 1px solid;\n"
"  width: 25px;\n"
"  height: 30px;\n"
"}\n"
"\n"
"QTabBar[orientation=\"vertical\"]{\n"
"  text-transform: uppercase;\n"
"  font-weight: bold;\n"
"  font-size: 15px;\n"
"}\n"
"\n"
"QTabBar[orientation=\"vertical\"]::tab {\n"
"  color: #808080;\n"
"  border: 4px;\n"
"  width: 20px;\n"
"  height: 100px;\n"
"}\n"
"\n"
"\n"
"\n"
"QTabBar[orientation=\"vertical\"]::tab:selected {\n"
""
                        "  color: #222222;\n"
"  border: 4px;\n"
"  width: 25px;\n"
"  height: 100px;\n"
"}\n"
"\n"
"\n"
"QTabBar[orientation=\"vertical\"]::tab::hover {\n"
"  color: #18292c;\n"
"  border: 1px solid;\n"
"  width: 25px;\n"
"  height: 250px;\n"
"}\n"
"\n"
"QTreeWidget::branch: {\n"
"    border-image: url(branch-end.png) 0;}\n"
"\n"
"QSplitter::handle {\n"
"    image: url(images/splitter.png);\n"
"}\n"
"\n"
"QSplitter::handle:horizontal {\n"
"    width: 2px;\n"
"}\n"
"\n"
"QSplitter::handle:vertical {\n"
"    height: 2px;\n"
"}\n"
"\n"
"QSplitter::handle:pressed {\n"
"    url(images/splitter_pressed.png);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(9, 9, 878, 773))
        self.topLay = QVBoxLayout(self.widget)
        self.topLay.setSpacing(4)
        self.topLay.setObjectName(u"topLay")
        self.topLay.setContentsMargins(5, 5, 5, 5)
        self.groupBox_5 = QGroupBox(self.widget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMaximumSize(QSize(16777215, 50))
        self.yuSeLPathSel_lay = QHBoxLayout(self.groupBox_5)
        self.yuSeLPathSel_lay.setObjectName(u"yuSeLPathSel_lay")
        self.yuSeLPathSel = QLabel(self.groupBox_5)
        self.yuSeLPathSel.setObjectName(u"yuSeLPathSel")
        self.yuSeLPathSel.setMaximumSize(QSize(16777215, 30))
        self.yuSeLPathSel.setBaseSize(QSize(0, 30))

        self.yuSeLPathSel_lay.addWidget(self.yuSeLPathSel)

        self.pushButton_3 = QPushButton(self.groupBox_5)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.yuSeLPathSel_lay.addWidget(self.pushButton_3)

        self.yuSeLPathSel_lay.setStretch(0, 5)

        self.topLay.addWidget(self.groupBox_5)

        self.groupBox_4 = QGroupBox(self.widget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_6.addWidget(self.label_8)

        self.lineEdit_4 = QLineEdit(self.groupBox_4)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout_6.addWidget(self.lineEdit_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_6.addWidget(self.label_9)

        self.lineEdit_5 = QLineEdit(self.groupBox_4)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_6.addWidget(self.lineEdit_5)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_6.addWidget(self.label_10)

        self.lineEdit_6 = QLineEdit(self.groupBox_4)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.horizontalLayout_6.addWidget(self.lineEdit_6)


        self.topLay.addWidget(self.groupBox_4)

        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 50))
        self.groupBox.setAcceptDrops(True)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton = QRadioButton(self.groupBox)
        self.buttonGroup = QButtonGroup(Form)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.horizontalLayout_3.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.groupBox)
        self.buttonGroup.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_3.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.groupBox)
        self.buttonGroup.addButton(self.radioButton_3)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout_3.addWidget(self.radioButton_3)

        self.radioButton1 = QRadioButton(self.groupBox)
        self.radioButton1.setObjectName(u"radioButton1")

        self.horizontalLayout_3.addWidget(self.radioButton1)


        self.topLay.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_4.addWidget(self.lineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.lineEdit_2 = QLineEdit(self.groupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_4.addWidget(self.lineEdit_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_3 = QLineEdit(self.groupBox_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_4.addWidget(self.lineEdit_3)


        self.topLay.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 220))
        font = QFont()
        font.setFamily(u"Nirmala UI")
        self.groupBox_3.setFont(font)
        self.groupBox_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(9, 15, -1, -1)
        self.usualAovList_GB_1 = QGroupBox(self.groupBox_3)
        self.usualAovList_GB_1.setObjectName(u"usualAovList_GB_1")
        font1 = QFont()
        font1.setFamily(u"Algerian")
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setWeight(50)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.usualAovList_GB_1.setFont(font1)
        self.usualAovList_GB_1.setCursor(QCursor(Qt.ArrowCursor))
        self.usualAovList_GB_1.setFlat(False)
        self.usualAovList_GL_1 = QGridLayout(self.usualAovList_GB_1)
        self.usualAovList_GL_1.setSpacing(2)
        self.usualAovList_GL_1.setObjectName(u"usualAovList_GL_1")
        self.checkBox_10 = QCheckBox(self.usualAovList_GB_1)
        self.checkBox_10.setObjectName(u"checkBox_10")

        self.usualAovList_GL_1.addWidget(self.checkBox_10, 0, 0, 1, 1)

        self.checkBox_8 = QCheckBox(self.usualAovList_GB_1)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.usualAovList_GL_1.addWidget(self.checkBox_8, 0, 1, 1, 1)

        self.checkBox_9 = QCheckBox(self.usualAovList_GB_1)
        self.checkBox_9.setObjectName(u"checkBox_9")

        self.usualAovList_GL_1.addWidget(self.checkBox_9, 0, 2, 1, 1)

        self.checkBox_7 = QCheckBox(self.usualAovList_GB_1)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.usualAovList_GL_1.addWidget(self.checkBox_7, 0, 3, 1, 1)

        self.checkBox_6 = QCheckBox(self.usualAovList_GB_1)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.usualAovList_GL_1.addWidget(self.checkBox_6, 0, 4, 1, 1)


        self.verticalLayout_3.addWidget(self.usualAovList_GB_1)

        self.usualAovList_GB_2 = QGroupBox(self.groupBox_3)
        self.usualAovList_GB_2.setObjectName(u"usualAovList_GB_2")
        font2 = QFont()
        font2.setFamily(u"Algerian")
        font2.setPointSize(8)
        self.usualAovList_GB_2.setFont(font2)
        self.usualAovList_GL_2 = QGridLayout(self.usualAovList_GB_2)
        self.usualAovList_GL_2.setObjectName(u"usualAovList_GL_2")
        self.checkBox_11 = QCheckBox(self.usualAovList_GB_2)
        self.checkBox_11.setObjectName(u"checkBox_11")

        self.usualAovList_GL_2.addWidget(self.checkBox_11, 0, 0, 1, 1)

        self.checkBox_12 = QCheckBox(self.usualAovList_GB_2)
        self.checkBox_12.setObjectName(u"checkBox_12")

        self.usualAovList_GL_2.addWidget(self.checkBox_12, 0, 1, 1, 1)

        self.checkBox_13 = QCheckBox(self.usualAovList_GB_2)
        self.checkBox_13.setObjectName(u"checkBox_13")

        self.usualAovList_GL_2.addWidget(self.checkBox_13, 0, 2, 1, 1)

        self.checkBox_14 = QCheckBox(self.usualAovList_GB_2)
        self.checkBox_14.setObjectName(u"checkBox_14")

        self.usualAovList_GL_2.addWidget(self.checkBox_14, 0, 3, 1, 1)

        self.checkBox_15 = QCheckBox(self.usualAovList_GB_2)
        self.checkBox_15.setObjectName(u"checkBox_15")

        self.usualAovList_GL_2.addWidget(self.checkBox_15, 0, 4, 1, 1)


        self.verticalLayout_3.addWidget(self.usualAovList_GB_2)

        self.usualAovList_GB_3 = QGroupBox(self.groupBox_3)
        self.usualAovList_GB_3.setObjectName(u"usualAovList_GB_3")
        font3 = QFont()
        font3.setPointSize(8)
        self.usualAovList_GB_3.setFont(font3)
        self.usualAovList_GL_3 = QGridLayout(self.usualAovList_GB_3)
        self.usualAovList_GL_3.setObjectName(u"usualAovList_GL_3")
        self.checkBox_16 = QCheckBox(self.usualAovList_GB_3)
        self.checkBox_16.setObjectName(u"checkBox_16")

        self.usualAovList_GL_3.addWidget(self.checkBox_16, 0, 0, 1, 1)

        self.checkBox_17 = QCheckBox(self.usualAovList_GB_3)
        self.checkBox_17.setObjectName(u"checkBox_17")

        self.usualAovList_GL_3.addWidget(self.checkBox_17, 0, 1, 1, 1)

        self.checkBox_18 = QCheckBox(self.usualAovList_GB_3)
        self.checkBox_18.setObjectName(u"checkBox_18")

        self.usualAovList_GL_3.addWidget(self.checkBox_18, 0, 2, 1, 1)

        self.checkBox_19 = QCheckBox(self.usualAovList_GB_3)
        self.checkBox_19.setObjectName(u"checkBox_19")

        self.usualAovList_GL_3.addWidget(self.checkBox_19, 0, 3, 1, 1)

        self.checkBox_20 = QCheckBox(self.usualAovList_GB_3)
        self.checkBox_20.setObjectName(u"checkBox_20")

        self.usualAovList_GL_3.addWidget(self.checkBox_20, 0, 4, 1, 1)


        self.verticalLayout_3.addWidget(self.usualAovList_GB_3)

        self.usualAovList_GB_4 = QGroupBox(self.groupBox_3)
        self.usualAovList_GB_4.setObjectName(u"usualAovList_GB_4")
        self.usualAovList_GB_4.setFont(font3)
        self.usualAovList_GL_4 = QGridLayout(self.usualAovList_GB_4)
        self.usualAovList_GL_4.setObjectName(u"usualAovList_GL_4")
        self.checkBox_21 = QCheckBox(self.usualAovList_GB_4)
        self.checkBox_21.setObjectName(u"checkBox_21")

        self.usualAovList_GL_4.addWidget(self.checkBox_21, 0, 0, 1, 1)

        self.checkBox_22 = QCheckBox(self.usualAovList_GB_4)
        self.checkBox_22.setObjectName(u"checkBox_22")

        self.usualAovList_GL_4.addWidget(self.checkBox_22, 0, 1, 1, 1)

        self.checkBox_23 = QCheckBox(self.usualAovList_GB_4)
        self.checkBox_23.setObjectName(u"checkBox_23")

        self.usualAovList_GL_4.addWidget(self.checkBox_23, 0, 2, 1, 1)

        self.checkBox_24 = QCheckBox(self.usualAovList_GB_4)
        self.checkBox_24.setObjectName(u"checkBox_24")

        self.usualAovList_GL_4.addWidget(self.checkBox_24, 0, 3, 1, 1)

        self.checkBox_25 = QCheckBox(self.usualAovList_GB_4)
        self.checkBox_25.setObjectName(u"checkBox_25")

        self.usualAovList_GL_4.addWidget(self.checkBox_25, 0, 4, 1, 1)


        self.verticalLayout_3.addWidget(self.usualAovList_GB_4)


        self.topLay.addWidget(self.groupBox_3)

        self.groupBox_6 = QGroupBox(self.widget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setEnabled(True)
        self.groupBox_6.setMinimumSize(QSize(0, 0))
        self.groupBox_6.setMaximumSize(QSize(16777215, 120))
        self.horizontalLayout = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_7 = QGroupBox(self.groupBox_6)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout = QVBoxLayout(self.groupBox_7)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textEdit = QTextEdit(self.groupBox_7)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)


        self.horizontalLayout.addWidget(self.groupBox_7)

        self.groupBox_9 = QGroupBox(self.groupBox_6)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.textEdit_3 = QTextEdit(self.groupBox_9)
        self.textEdit_3.setObjectName(u"textEdit_3")

        self.verticalLayout_5.addWidget(self.textEdit_3)


        self.horizontalLayout.addWidget(self.groupBox_9)

        self.groupBox_8 = QGroupBox(self.groupBox_6)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.textEdit_2 = QTextEdit(self.groupBox_8)
        self.textEdit_2.setObjectName(u"textEdit_2")

        self.verticalLayout_4.addWidget(self.textEdit_2)


        self.horizontalLayout.addWidget(self.groupBox_8)


        self.topLay.addWidget(self.groupBox_6)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"QMainWindow{\n"
"background-color:#1d1d1d;\n"
"}\n"
"\n"
"QWidget{\n"
"  background-color: #181818;\n"
"}\n"
"\n"
"QMenuBar{\n"
"background-color:#1d1d1d;\n"
"padding:5px;\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"}\n"
"\n"
"QMenuBar::item{\n"
"background-color:#1d1d1d;\n"
"color:#fff;\n"
"padding:5px;\n"
"\n"
"}\n"
"\n"
"QMenu{\n"
"color:#fff;\n"
"padding:0;\n"
"}\n"
"\n"
"QMenu::item:selected{\n"
"color:#fff;\n"
"background-color:#00aba9;\n"
"}\n"
"\n"
"QTableWidget{\n"
"\n"
"background-color:#3d3d3d;\n"
"color:#fff;\n"
"  selection-background-color: #da532c;\n"
"border:solid;\n"
"border-width:3px;\n"
"border-color:#da532c;\n"
"}\n"
"QHeaderView::section{\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(20, 158, 217, 255), stop:1 rgba(36, 158, 217, 255));\n"
"border:none;\n"
"border-top-style:solid;\n"
"border-width:1px;\n"
"border-top-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(20, 158, 217, 255), stop:1 rgba(36, 158, 217, 255));\n"
"color:#fff;\n"
""
                        "\n"
"}\n"
"QHeaderView{\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(20, 158, 217, 255), stop:1 rgba(36, 158, 217, 255));\n"
"\n"
"border:none;\n"
"border-top-style:solid;\n"
"border-width:1px;\n"
"border-top-color:#149ED9;\n"
"color:#fff;\n"
"font: 12px;\n"
"}\n"
"\n"
"QTableCornerButton::section{\n"
"border:none;\n"
"background-color:#149ED9;\n"
"}\n"
"\n"
"QListWidget{\n"
"background-color:#3d3d3d;\n"
"color:#fff;\n"
"}\n"
"\n"
"QMenu{\n"
"background-color:#3d3d3d;\n"
"}\n"
"QStatusBar{\n"
"background-color:#7e3878;\n"
"color:#fff;\n"
"}\n"
"\n"
"\n"
"QLabel{\n"
"border-style:solid;\n"
"background-color:#3d3d3d;\n"
"color:#fff;\n"
"border-radius:7px;\n"
"font: 15 10pt \"Open Sans\";\n"
"padding:5px;\n"
"}\n"
"\n"
"\n"
"QRadioButton{\n"
"\n"
"color:#ccc;\n"
"\n"
"}\n"
"\n"
"QCheckBox{\n"
"\n"
"color:#ccc;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton{\n"
"border-style:solid;\n"
"background-color:#3d3d3d;\n"
"color:#fff;\n"
"border-radius:7px;\n"
"font: 15 10pt \"Open Sans\";\n"
""
                        "padding:5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"color:#ccc;\n"
"	background-color: qlineargradient(spread:pad, x1:0.517, y1:0, x2:0.517, y2:1, stop:0 rgba(45, 45, 45, 255), stop:0.505682 rgba(45, 45, 45, 255), stop:1 rgba(29, 29, 29, 255));\n"
"	border-color:#2d89ef;\n"
"border-width:1px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0.517, y1:0, x2:0.517, y2:1, stop:0 rgba(29, 29, 29, 255), stop:0.505682 rgba(45, 45, 45, 255), stop:1 rgba(29, 29, 29, 255));\n"
"}\n"
"\n"
"\n"
"QTabWidget::tab{\n"
"background-color:#3d3d3d;\n"
"}\n"
"\n"
"QLineEdit{\n"
"border-radius:0;\n"
"background-color:#a4dbdb;\n"
"font-family: \"Microsoft YaHei\";\n"
"\n"
"}\n"
"\n"
"QProgressBar{\n"
"border-radius:0;\n"
"text-align:center;\n"
"color:#fff;\n"
"background-color:transparent;\n"
"border: 2px solid #e3a21a;\n"
"border-radius:7px;\n"
"	font: 75 12pt \"Open Sans\";\n"
"\n"
"}\n"
"\n"
"QProgressBar::chunk{\n"
"background-color:#2d89ef;\n"
"width:20px;\n"
"}\n"
"\n"
"\n"
"QComboBox {"
                        "\n"
"    background: #3c3737;\n"
"    color: #dbdbdb;\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    border-style: solid;\n"
"}\n"
"\n"
"/* \u8bbe\u7f6e\u4e0b\u62c9\u6846\u4e2d\u5217\u8868\u7684\u80cc\u666f\u989c\u8272\u4e3a\u9ec4\u8272\uff0c\u6587\u5b57\u989c\u8272\u4e3a\u84dd\u8272 */\n"
"QComboBox QAbstractItemView {\n"
"    background: #3c3737;\n"
"    color: #dbdbdb;\n"
"}\n"
"\n"
"\n"
"\n"
"QGroupBox {\n"
"\n"
"    color: #ffffff;\n"
"    background-color: #454545;\n"
"    text-align: center;\n"
"\n"
"}\n"
"\n"
"\n"
"QGroupBox::!enabled {\n"
"	background-color: rgb(220, 220, 220);\n"
"    title{ color: red ;};\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox{\n"
"    border-color:#2d89ef;\n"
"    border-width:2px;\n"
"    height:25px;\n"
"    border-radius: 2px;\n"
"    background-color:#c2c4c9;\n"
"}\n"
"\n"
"\n"
"\n"
"QTabBar[orientation=\"horizontal\"]{\n"
"  text-transform: uppercase;\n"
"  font-weight: bold;\n"
"  font-size: 15px;\n"
"}\n"
"\n"
"QTabBar[orientation=\"horizontal\""
                        "]::tab {\n"
"  color: #808080;\n"
"  border: 4px;\n"
"  width: 20px;\n"
"  height: 30px;\n"
"}\n"
"\n"
"\n"
"\n"
"QTabBar[orientation=\"horizontal\"]::tab:selected {\n"
"  color: #222222;\n"
"  border: 4px;\n"
"  width: 25px;\n"
"  height: 30px;\n"
"}\n"
"\n"
"\n"
"QTabBar[orientation=\"horizontal\"]::tab::hover {\n"
"  color: #18292c;\n"
"  border: 1px solid;\n"
"  width: 25px;\n"
"  height: 30px;\n"
"}\n"
"\n"
"QTabBar[orientation=\"vertical\"]{\n"
"  text-transform: uppercase;\n"
"  font-weight: bold;\n"
"  font-size: 15px;\n"
"}\n"
"\n"
"QTabBar[orientation=\"vertical\"]::tab {\n"
"  color: #808080;\n"
"  border: 4px;\n"
"  width: 20px;\n"
"  height: 100px;\n"
"}\n"
"\n"
"\n"
"\n"
"QTabBar[orientation=\"vertical\"]::tab:selected {\n"
"  color: #222222;\n"
"  border: 4px;\n"
"  width: 25px;\n"
"  height: 100px;\n"
"}\n"
"\n"
"\n"
"QTabBar[orientation=\"vertical\"]::tab::hover {\n"
"  color: #18292c;\n"
"  border: 1px solid;\n"
"  width: 25px;\n"
"  height: 250px;\n"
"}\n"
"\n"
"QTreeWidget::branch: {\n"
"  "
                        "  border-image: url(branch-end.png) 0;}\n"
"\n"
"QSplitter::handle {\n"
"    image: url(images/splitter.png);\n"
"}\n"
"\n"
"QSplitter::handle:horizontal {\n"
"    width: 2px;\n"
"}\n"
"\n"
"QSplitter::handle:vertical {\n"
"    height: 2px;\n"
"}\n"
"\n"
"QSplitter::handle:pressed {\n"
"    url(images/splitter_pressed.png);\n"
"}\n"
"\n"
"\n"
"\n"
"")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.verticalLayout_2.addWidget(self.pushButton_4)


        self.topLay.addLayout(self.verticalLayout_2)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.topLay.addWidget(self.label)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6e32\u67d3\u5c42AOV\u5de5\u5177", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"\u9884\u8bbe\u6587\u4ef6", None))
        self.yuSeLPathSel.setText(QCoreApplication.translate("Form", u"\u9884\u8bbe\u6587\u4ef6", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"\u8d44\u4ea7\u7c7b\u578b\u4ece\u76ee\u5f55\u8bc6\u522b,\u591a\u4e2a\u7528\u9017\u53f7\u9694\u5f00", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u89d2\u8272", None))
        self.lineEdit_4.setText(QCoreApplication.translate("Form", u"Chr,Char", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u9053\u5177", None))
        self.lineEdit_5.setText(QCoreApplication.translate("Form", u"Pro,PRP", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u573a\u666f", None))
        self.lineEdit_6.setText(QCoreApplication.translate("Form", u"Env,Set", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u8d44\u4ea7\u7c7b\u578b", None))
        self.radioButton.setText(QCoreApplication.translate("Form", u"\u89d2\u8272", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"\u573a\u666f", None))
        self.radioButton_3.setText(QCoreApplication.translate("Form", u"\u9053\u5177", None))
        self.radioButton1.setText(QCoreApplication.translate("Form", u"\u81ea\u52a8", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u6e32\u67d3\u5c42\u524d\u7f00", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u89d2\u8272", None))
        self.lineEdit.setText(QCoreApplication.translate("Form", u"CH00", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u9053\u5177", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Form", u"PR00", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u573a\u666f", None))
        self.lineEdit_3.setText(QCoreApplication.translate("Form", u"Env00", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"AOV(\u91cc\u9762\u7684\u5185\u5bb9\u8bfb\u53d6\u6e32\u67d3\u5668\u7684AOV\u5217\u8868)", None))
        self.usualAovList_GB_1.setTitle(QCoreApplication.translate("Form", u"\u901a\u7528", None))
        self.checkBox_10.setText(QCoreApplication.translate("Form", u"AA_inv_density", None))
        self.checkBox_8.setText(QCoreApplication.translate("Form", u"N", None))
        self.checkBox_9.setText(QCoreApplication.translate("Form", u"P", None))
        self.checkBox_7.setText(QCoreApplication.translate("Form", u"RGBA", None))
        self.checkBox_6.setText(QCoreApplication.translate("Form", u"Pref", None))
        self.usualAovList_GB_2.setTitle(QCoreApplication.translate("Form", u"\u89d2\u8272", None))
        self.checkBox_11.setText(QCoreApplication.translate("Form", u"AA_inv_density", None))
        self.checkBox_12.setText(QCoreApplication.translate("Form", u"N", None))
        self.checkBox_13.setText(QCoreApplication.translate("Form", u"P", None))
        self.checkBox_14.setText(QCoreApplication.translate("Form", u"RGBA", None))
        self.checkBox_15.setText(QCoreApplication.translate("Form", u"Pref", None))
        self.usualAovList_GB_3.setTitle(QCoreApplication.translate("Form", u"\u9053\u5177", None))
        self.checkBox_16.setText(QCoreApplication.translate("Form", u"AA_inv_density", None))
        self.checkBox_17.setText(QCoreApplication.translate("Form", u"N", None))
        self.checkBox_18.setText(QCoreApplication.translate("Form", u"P", None))
        self.checkBox_19.setText(QCoreApplication.translate("Form", u"RGBA", None))
        self.checkBox_20.setText(QCoreApplication.translate("Form", u"Pref", None))
        self.usualAovList_GB_4.setTitle(QCoreApplication.translate("Form", u"\u573a\u666f", None))
        self.checkBox_21.setText(QCoreApplication.translate("Form", u"AA_inv_density", None))
        self.checkBox_22.setText(QCoreApplication.translate("Form", u"N", None))
        self.checkBox_23.setText(QCoreApplication.translate("Form", u"P", None))
        self.checkBox_24.setText(QCoreApplication.translate("Form", u"RGBA", None))
        self.checkBox_25.setText(QCoreApplication.translate("Form", u"Pref", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"\u7279\u6b8a\u8bbe\u7f6e", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Form", u"\u89d2\u8272", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Form", u"\u9053\u5177", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Form", u"\u573a\u666f", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u5efa\u7acb\u6e32\u67d3\u5c42", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u5efa\u7acbAOV", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"\u521b\u5efa\u7eb9\u7406\u53c2\u8003\u7269\u4f53", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u4f7f\u7528\u8bf4\u660e:", None))
    # retranslateUi

