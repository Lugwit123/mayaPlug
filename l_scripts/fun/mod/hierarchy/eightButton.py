import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from functools import partial
from math import cos, sin, pi,radians
import math

class CircularButtons(QWidget):
    def __init__(self, parent=None):
        super(CircularButtons, self).__init__(parent)
        self.radius = 100

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Circular Buttons")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        circle_radius = 100
        center_x = 200
        center_y = 200
        num_buttons = 8

        for i in range(8):
            button = QPushButton(self)
            button_texts = ["右", "右下", "下", "左下", "左", "左上", "上", "右上"]
            button.setText(button_texts[i])
            button.setGeometry(QRect(0, 0, 40, 40))
            angle = math.radians(i * 45)
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            button.move(x + self.radius - 20, y + self.radius - 20)
            button.setStyleSheet("background-color: white; color: black; border: 1px solid black;")


            
    def button_clicked(self,button):
        print(button.text())
        




class Overlay(QWidget):
    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)
        self.custom_popup = CustomPopup(self)
        self.setMouseTracking(True)
        self.installEventFilter(self.custom_popup)

    def resizeEvent(self, event):
        self.custom_popup.setGeometry(self.rect())
        super(Overlay, self).resizeEvent(event)



class CustomPopup(QWidget):
    def __init__(self, table_widget, parent=None):
        super(CustomPopup, self).__init__(parent)
        self.circular_buttons = None
        self.start_point = None
        self.end_point = None
        self.drawing = False
        self.target_widget = None
        self.table_widget = table_widget

        self.setMouseTracking(True)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton:
            local_pos = self.mapFromGlobal(event.globalPos())
            self.target_widget = self.table_widget.itemAt(local_pos)

            self.start_point = local_pos
            self.end_point = local_pos
            self.drawing = True
            self.circular_buttons = CircularButtons(self)
            self.circular_buttons.move(self.start_point - self.circular_buttons.rect().center())
            self.circular_buttons.show()
            self.update()
            return True

        return super(CustomPopup, self).eventFilter(obj, event)




    def paintEvent(self, event):
        if self.start_point is not None and self.end_point is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(self.start_point, self.end_point)


    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.update()

            if self.circular_buttons is not None and self.circular_buttons.isVisible():
                line = QLineF(self.start_point, self.end_point)
                line_length = line.length()

                # 取消高亮显示，如果鼠标位置距离起点较近
                if line_length < self.circular_buttons.radius:
                    for button in self.circular_buttons.findChildren(QPushButton):
                        button.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
                    return

                line_angle = line.angle()
                angle_ranges = []
                for i in range(8):
                    start_angle = (i * 45) + 22.5
                    end_angle = start_angle + 45
                    angle_ranges.append((start_angle, end_angle))
                angle_ranges.reverse()

                # Check which button the line intersects
                for i, button in enumerate(self.circular_buttons.findChildren(QPushButton)):
                    start_angle, end_angle = angle_ranges[i]
                    if start_angle <= line_angle < end_angle or start_angle < 0 and line_angle + 360 < end_angle:
                        button.setStyleSheet("background-color: red; color: black; border: 1px solid black;")
                    else:
                        button.setStyleSheet("background-color: white; color: black; border: 1px solid black;")


    def mousePressEvent(self, event):
        if event.buttons() & Qt.RightButton:
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.drawing = True
            self.circular_buttons = CircularButtons(self)
            self.circular_buttons.show()
            self.circular_buttons.setGeometry(QRect(self.start_point.x() - self.circular_buttons.width() // 2,
                                                    self.start_point.y() - self.circular_buttons.height() // 2,
                                                    self.circular_buttons.width(), self.circular_buttons.height()))
            self.move(event.globalPos() - QPoint(self.width() // 2, self.height() // 2))
        super(CustomPopup, self).mousePressEvent(event)





class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Circular Buttons Example")
        self.setGeometry(100, 100, 800, 600)

        # 创建 QTableWidget
        self.table_widget = QTableWidget(1, 1, self)
        self.table_widget.setGeometry(100, 100, 200, 100)
        self.table_widget.setItem(0, 0, QTableWidgetItem("Right-click me"))

        # 创建 Overlay
        self.overlay = CustomPopup(self.table_widget, self)

        # 设置透明度
        opacity_effect = QGraphicsOpacityEffect(self.overlay)
        opacity_effect.setOpacity(0.3)
        self.overlay.setGraphicsEffect(opacity_effect)

        self.overlay.setGeometry(self.rect())  # 设置 Overlay 的初始几何形状
        self.overlay.raise_()  # 将 Overlay 置于其他小部件之上

    def resizeEvent(self, event):
        self.overlay.setGeometry(self.rect())  # 调整 Overlay 的几何形状以适应主窗口大小
        super(MainWindow, self).resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

