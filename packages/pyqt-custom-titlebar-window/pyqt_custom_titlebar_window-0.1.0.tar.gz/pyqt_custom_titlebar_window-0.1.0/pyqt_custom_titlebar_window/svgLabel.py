import os

from PyQt5.QtGui import QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QLabel


class SvgLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__renderer = ''

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.__renderer:
            self.__renderer.render(painter)
        return super().paintEvent(event)

    def setSvgFile(self, filename: str):
        self.__renderer = QSvgRenderer(filename)
        self.resize(self.__renderer.defaultSize())
        length = max(self.sizeHint().width(), self.sizeHint().height())
        self.setFixedSize(length, length)