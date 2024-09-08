import PyQt5.QtGui, ipic.lang, PyQt5.QtWidgets, ipic.path, ipic.type

class Action(PyQt5.QtWidgets.QAction):
   def __init__(self, json, parent=None):
      if parent is not None:
         super().__init__(parent)
      else:
         super().__init__()
      try:
         self.setText(json["TEXT"])
      except KeyError:
         pass
      try:
         try:
            if json["CHECKABLE"]:
               self.setCheckable(True)
               self.triggered.connect(lambda c: ipic.lang.lexer(ipic.lang.sub(json["ACTION"]), args={"checked": ipic.type.boolean(c)}))
            else:
               self.triggered.connect(lambda _: ipic.lang.lexer(ipic.lang.sub(json["ACTION"])))
         except KeyError:
            self.triggered.connect(lambda _: ipic.lang.lexer(ipic.lang.sub(json["ACTION"])))
      except KeyError:
         pass
      try:
         self.setStatusTip(json["STATUSTIP"])
      except KeyError:
         pass
      try:
         self.setIcon(Icon(json["ICON"]))
      except KeyError:
         pass
      try:
         self.setShortcut(PyQt5.QtGui.QKeySequence(json["SHORTCUT"]))
      except KeyError:
         pass

class Icon(PyQt5.QtGui.QIcon):
   def __init__(self, path):
      super().__init__(ipic.path.path_insensitive(path))

class ContextMenu(PyQt5.QtWidgets.QMenu):
   def __init__(self, actions, parent=None):
      super().__init__()
      for action in actions:
         if parent is not None:
            self.addAction(Action(action, parent))
         else:
            self.addAction(Action(action))