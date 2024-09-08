"""A threading helper to implement the thread.start command in the Picturesque qt5 namespace."""
import PyQt5.QtCore, ipic.lang

class Worker(PyQt5.QtCore.QRunnable):
    """A QRunnable modified to run Picturesque code."""
    def __init__(self, code):
        super(Worker, self).__init__()
        self.code = code

    @PyQt5.QtCore.pyqtSlot()
    def run(self):
        ipic.lang.lexer(self.code)