from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import *

class SectorButton(QPushButton):
    def __init__(self, start_angle, end_angle, inner_radius, outer_radius, text, parent=None):
        super().__init__(parent)
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.span_angle = end_angle - start_angle
        self.text_str = text
        self.hovered = False
        self.pressed = False
        self.setFixedSize(250, 250)

        path = QPainterPath()
        path.moveTo(self.width() / 2, self.height() / 2)
        path.arcTo(QRectF(self.width() / 2 - self.outer_radius, self.height() / 2 - self.outer_radius, self.outer_radius * 2, self.outer_radius * 2), self.start_angle, self.span_angle)
        path.arcTo(QRectF(self.width() / 2 - self.inner_radius, self.height() / 2 - self.inner_radius, self.inner_radius * 2, self.inner_radius * 2), self.start_angle + self.span_angle, -self.span_angle)
        path.closeSubpath()
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

        self.clicked.connect(self.on_clicked)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.moveTo(self.width() / 2, self.height() / 2)
        path.arcTo(QRectF(self.width() / 2 - self.outer_radius, self.height() / 2 - self.outer_radius, self.outer_radius * 2, self.outer_radius * 2), self.start_angle, self.span_angle)
        path.arcTo(QRectF(self.width() / 2 - self.inner_radius, self.height() / 2 - self.inner_radius, self.inner_radius * 2, self.inner_radius * 2), self.start_angle + self.span_angle, -self.span_angle)
        path.closeSubpath()

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(240, 240, 240))
        gradient.setColorAt(1, QColor(200, 200, 200))

        if self.hovered:
            gradient.setColorAt(0, QColor(255, 255, 255))
            gradient.setColorAt(1, QColor(220, 220, 220))

        if self.pressed:
            gradient.setColorAt(0, QColor(180, 180, 180))
            gradient.setColorAt(1, QColor(140, 140, 140))

        painter.setBrush(QBrush(gradient))
        painter.drawPath(path)

        # Draw 3D effect
        painter.setPen(QColor(150, 150, 150, 100))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        # Draw arc text
        font = QFont()
        font.setPointSize(14)
        painter.setFont(font)
        painter.setPen(Qt.black)

        text_path = QPainterPath()
        text_path.addText(0, 0, font, self.text_str)
        text_center = text_path.boundingRect().center()
        text_path.translate(-text_center.x(), -text_center.y())
        
        text_angle = (self.start_angle + self.end_angle) / 2
        text_radius = (self.inner_radius + self.outer_radius) / 2

        transform = QTransform()
        transform.translate(self.width() / 2, self.height() / 2)
        transform.rotate(-text_angle)
        transform.translate(text_radius, 10)
        painter.setWorldTransform(transform)
        painter.drawPath(text_path)


    def enterEvent(self, event):
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.pressed:
            self.pressed = False
            self.update()

    def on_clicked(self):
        print(f'Button {self.text_str} clicked')
        
class CircularButtonsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Circular Buttons')

        self.buttons = []
        for i in range(8):
            start_angle = 22.5 + i * 45
            end_angle = start_angle + 45
            btn = SectorButton(start_angle, end_angle, 80, 100, '理你理你领', self)
            self.buttons.append(btn)


def main():
    app = QApplication([])
    window = CircularButtonsWidget()
    window.setWindowTitle('Circular Buttons')

    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

