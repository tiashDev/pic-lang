from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPalette, QColor
from ipic.ns import ShlexNamespace

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class main(ShlexNamespace):
    def on_ns_init(self):
        self.qtwdict = self.ns_list["QT5"].qtwdict
    def do_qtCHAR0__color(self, name, color, layout):
        self.qtwdict[name] = Color(color)
        try:
           self.qtwdict[layout].addWidget(self.ns_list["QT5"].qtwdict[name])
        except BaseException as err:
           self.out.error(err)