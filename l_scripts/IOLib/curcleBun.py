from random import randrange
from PyQt5 import QtCore, QtGui, QtWidgets

class AngledObject(QtWidgets.QGraphicsView):
    _angle = 0

    def __init__(self, angle=0, parent=None):
        super(AngledObject, self).__init__(parent)
        # to prevent the graphics view to draw its borders or background, set the
        # FrameShape property to 0 and a transparent background
        self.setFrameShape(0)
        self.setStyleSheet('background: transparent')
        self.setScene(QtWidgets.QGraphicsScene())
        # ignore scroll bars!
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

    def angle(self):
        return self._angle

    def setAngle(self, angle):
        angle %= 360
        if angle == self._angle:
            return
        self._angle = angle
        self._proxy.setTransform(QtGui.QTransform().rotate(-angle))
        self.adjustSize()

    def resizeEvent(self, event):
        super(AngledObject, self).resizeEvent(event)
        # ensure that the scene is fully visible after resizing
        QtCore.QTimer.singleShot(0, lambda: self.centerOn(self.sceneRect().center()))

    def sizeHint(self):
        return self.scene().itemsBoundingRect().size().toSize()

    def minimumSizeHint(self):
        return self.sizeHint()


class AngledLabel(AngledObject):
    def __init__(self, text='', angle=0, parent=None):
        super(AngledLabel, self).__init__(angle, parent)
        self._label = QtWidgets.QLabel(text)
        self._proxy = self.scene().addWidget(self._label)
        self._label.setStyleSheet('background: transparent')
        self.setAngle(angle)
        self.alignment = self._label.alignment

    def setAlignment(self, alignment):
        # text alignment might affect the text size!
        if alignment == self._label.alignment():
            return
        self._label.setAlignment(alignment)
        self.setMinimumSize(self.sizeHint())

    def text(self):
        return self._label.text()

    def setText(self, text):
        if text == self._label.text():
            return
        self._label.setText(text)
        self.setMinimumSize(self.sizeHint())


class AngledButton(AngledObject):
    def __init__(self, text='', angle=0, parent=None):
        super(AngledButton, self).__init__(angle, parent)
        self._button = QtWidgets.QPushButton(text)
        self._proxy = self.scene().addWidget(self._button)
        self.setAngle(angle)


class TestWindow(QtWidgets.QWidget):
    def __init__(self):
        super(TestWindow, self).__init__()
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        self.randomizeButton = QtWidgets.QPushButton('Randomize!')
        layout.addWidget(self.randomizeButton, 0, 0, 1, 3)
        self.randomizeButton.clicked.connect(self.randomize)

        layout.addWidget(QtWidgets.QLabel('Standard label'), 1, 0)
        text = 'Some text'
        layout.addWidget(QtWidgets.QLabel(text), 1, 2)
        self.labels = []
        for row, angle in enumerate([randrange(360) for _ in range(4)], 2):
            angleLabel = QtWidgets.QLabel(u'{}°'.format(angle))
            angleLabel.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
            layout.addWidget(angleLabel, row, 0)
            label = AngledLabel(text, angle)
            layout.addWidget(label, row, 2)
            self.labels.append((angleLabel, label))

        for row, angle in enumerate([randrange(360) for _ in range(4)], row + 1):
            angleLabel = QtWidgets.QLabel(u'{}°'.format(angle))
            angleLabel.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
            layout.addWidget(angleLabel, row, 0)
            label = AngledButton('Button!', angle)
            layout.addWidget(label, row, 2)
            self.labels.append((angleLabel, label))

        separator = QtWidgets.QFrame()
        separator.setFrameShape(separator.VLine|separator.Sunken)
        layout.addWidget(separator, 1, 1, layout.rowCount() - 1, 1)

    def randomize(self):
        for angleLabel, label in self.labels:
            angle = randrange(360)
            angleLabel.setText(str(angle))
            label.setAngle(angle)
        self.adjustSize()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec_())