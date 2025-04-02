"""The Picturesque qt5 namespace."""
import ipic.ns, PyQt5.QtWidgets, sys, shlex, json, ipic.lang, PyQt5.QtCore, ipic.path, PyQt5.QtGui, ipic.type, PyQt5.uic, PyQt5.QtQml
from . import thread, wrapper
from .enumtype import LineTypes, BlockTypes

_ = """class CustomWidget(PyQt5.QtWidgets.QWidget):
   def __init__(self, ast, proc_dict, var_dict, json, qtwdict):
      super().__init__()
      self.signals = {}
      self.props = []
      self.qtwdict = qtwdict
      self.proc_dict = proc_dict
      self.var_dict = var_dict
      self.name = json["NAME"]
      for signal in filter(lambda i: i["type"] == LineTypes.Signal, ast):
         self.signals[signal["name"]] = (PyQt5.QtCore.pyqtSignal(*(str for x in range(signal["args"]))), range(signal["args"]), signal["json"])
      for prop in filter(lambda i: i["type"] == LineTypes.Property, ast):
         self.props.append(prop["name"])
      for prop in self.props:
         self.var_dict[f"{self}.{prop}"] = ""
      for key, value in enumerate(json):
         fsig = filter(lambda i: i[2] == key, self.signals)
         if len(fsig) > 0:
            fsig[0].connect(lambda *a: _lexer(value, args=ipic.type.py_list2dict([(f"signal.{key}" for key in x[1]) for x in signals], [(f"signal.{value}" for _, value in enumerate(x[1])) for x in signals])))
      _lexer(filter(lambda i: i["type"] == BlockTypes.Initialization, ast)[0]["todo"], args=json)
   def _lexer(self, code):
      for name, signal in enumerate(self.signals):
         self.proc_dict[f"_w.signals[{name}].emit".upper()] = (signal[1], lambda *a: signal[0].emit(*a), ipic.lang.PROC_TYPE_PY)
      def propset(prop, a):
         self.var_dict[f"{self}.{prop}"] = a
      for prop in self.props:
         self.proc_dict[f"_w.props[{prop}].set".upper()] = ((0,), lambda a: propset(prop, a), ipic.lang.PROC_TYPE_PY)
         self.var_dict[f"_w.props[{prop}]".upper()] = self.var_dict[f"{self}.{prop}"]
      self.qtwdict["_W"] = self.qtwdict[self.name]
      ipic.lang.lexer(ipic.lang.sub(code))
      for name in self.signals:
         del self.proc_dict[f"_w.signals[{name}].emit".upper()]
      for prop in self.props:
         del self.proc_dict[f"_w.props[{prop}].set".upper()]
         del self.var_dict[f"_w.props[{prop}]".upper()]
      del self.qtwdict["_W"]"""

def widgetblockparser(block):
   ret = []
   lineend = block.find("!")
   blckend = block.find("{")
   if lineend > blckend:
      line = block[:lineend]
      if line.find(" ") != -1:
         cmd = line[:line.find(" ")]
         val = line[line.find(" ")+1:]
      else:
         cmd = line[line.find(" ")+1:]
      match cmd:
         case LineTypes.Signal.value:
            argsnum = int(val[val.find("[")+1:val.rfind("]")])
            name = val[:val.find("[")]
            jsonname = val[val.find(" ")+1:]
            ret.append({"type": LineTypes.Signal, "name": name, "args": argsnum, "json": jsonname})
         case LineTypes.Property.value:
            ret.append({"type": LineTypes.Property, "name": val})
         case _:
            raise Exception("eww brother whats that?")
   elif blckend > lineend:
      blck = block[:blckend]
      bblck = blck[blck.find(" ")+1:]
      cmd = bblck[:bblck.find(" ")]
      extrainf = bblck[:bblck.find(" ")]
      inner = blck[blck.find("{"):blck.rfind("}")]
      print("BLOCK NAME: ("+cmd+")")
      print("INFO: ("+extrainf+")")
      print(BlockTypes.Initialization.value)
      match cmd:
         case BlockTypes.Initialization.value:
            ret.append({"type": BlockTypes.Initialization, "todo": inner})
         case _:
            raise Exception("eww brother whats that?")
   return ret

class main(ipic.ns.CmdNamespace):
   """The namespace class."""
   def on_ns_init(self):
      try:
         ipic.lang.singlevar_list[ipic.lang.SVLIST_IDX_NSDATA]["QtWidgets"]
      except KeyError:
         ipic.lang.singlevar_list[ipic.lang.SVLIST_IDX_NSDATA]["QtWidgets"] = {}
      finally:
         self.qtwdict = ipic.lang.singlevar_list[ipic.lang.SVLIST_IDX_NSDATA]["QtWidgets"]
      self.app = None
      self.threadpool = PyQt5.QtCore.QThreadPool()
      self.cmenus = []
      self.sys_var["version"] = (PyQt5.QtCore.QT_VERSION_STR, {})
      self.tab_dir = {
         "NORTH": PyQt5.QtWidgets.QTabWidget.North,
         "SOUTH": PyQt5.QtWidgets.QTabWidget.South,
         "EAST": PyQt5.QtWidgets.QTabWidget.East,
         "WEST": PyQt5.QtWidgets.QTabWidget.West
      }
      self.ps = []
      self.dlgbtn = {
         "OK": PyQt5.QtWidgets.QDialogButtonBox.Ok,
         "OPEN": PyQt5.QtWidgets.QDialogButtonBox.Open,
         "SAVE": PyQt5.QtWidgets.QDialogButtonBox.Save,
         "CANCEL": PyQt5.QtWidgets.QDialogButtonBox.Cancel,
         "CLOSE": PyQt5.QtWidgets.QDialogButtonBox.Close,
         "DISCARD": PyQt5.QtWidgets.QDialogButtonBox.Discard,
         "APPLY": PyQt5.QtWidgets.QDialogButtonBox.Apply,
         "RESET": PyQt5.QtWidgets.QDialogButtonBox.Reset,
         "RESTORE-DEFAULTS": PyQt5.QtWidgets.QDialogButtonBox.RestoreDefaults,
         "HELP": PyQt5.QtWidgets.QDialogButtonBox.Help,
         "SAVEALL": PyQt5.QtWidgets.QDialogButtonBox.SaveAll,
         "YES": PyQt5.QtWidgets.QDialogButtonBox.Yes,
         "YES2ALL": PyQt5.QtWidgets.QDialogButtonBox.YesToAll,
         "NO": PyQt5.QtWidgets.QDialogButtonBox.No,
         "NO2ALL": PyQt5.QtWidgets.QDialogButtonBox.NoToAll,
         "ABORT": PyQt5.QtWidgets.QDialogButtonBox.Abort,
         "RETRY": PyQt5.QtWidgets.QDialogButtonBox.Retry,
         "IGNORE": PyQt5.QtWidgets.QDialogButtonBox.Ignore,
         "NOBTN": PyQt5.QtWidgets.QDialogButtonBox.NoButton,
      }
      self.msgboxicon = {
         "NOICON": PyQt5.QtWidgets.QMessageBox.NoIcon,
         "QUESTION": PyQt5.QtWidgets.QMessageBox.Question,
         "INFO": PyQt5.QtWidgets.QMessageBox.Information,
         "WARN": PyQt5.QtWidgets.QMessageBox.Warning,
         "ERR": PyQt5.QtWidgets.QMessageBox.Critical
      }
   def getborset(self, enum, opt):
      ret = 0
      for x in opt:
         ret |= enum[x]
      return ret
   def do_qtCHAR0__initapp(self, val, csval):
      self.app = PyQt5.QtWidgets.QApplication(sys.argv)
   def do_quit(self, val, csval):
      self.app.quit()
   def do_initguiapp(self, val, csval):
      self.app = PyQt5.QtGui.QGuiApplication(sys.argv)
   def do_quitonlastwinclose(self, val, csval):
      self.app.setQuitOnLastWindowClosed(ipic.type.pbool(val))
   def do_quit(self, val, csval):
      self.app.quit()
   def do_qtCHAR0__wininit(self, val, csval):
      self.qtwdict[val] = PyQt5.QtWidgets.QMainWindow()
      self.var_dict[val] = f"<Qt5 window {val!r}>"
      self.proc_dict[f"{val}.setfixedsize".upper()] = (
        range(2), (lambda w, h:
           self.qtwdict[val].setFixedSize(PyQt5.QtCore.QSize(int(w), int(h)))
        ),
        self.PROC_TYPE_PY
      )
      self.proc_dict[f"{val}.setcentralwidget".upper()] = (
        (0,), (lambda container:
           self.qtwdict[val].setCentralWidget(self.qtwdict[container])
        ),
        self.PROC_TYPE_PY
      )
      self.proc_dict[f"{val}.setminsize".upper()] = (
        (0,), (lambda minsize:
           self.qtwdict[val].setMinimumSize(int(minsize))
        ),
        self.PROC_TYPE_PY
      )
      self.proc_dict[f"{val}.setmaxsize".upper()] = (
        (0,), (lambda minsize:
           self.qtwdict[val].setMaximumSize(int(maxsize))
        ),
        self.PROC_TYPE_PY
      )
      self.proc_dict[f"{val}.setcentralwidget".upper()] = (
        (0,), (lambda container:
           self.qtwdict[val].setCentralWidget(self.qtwdict[container])
        ),
        self.PROC_TYPE_PY
      )
      self.proc_dict[f"{val}.show".upper()] = (
        (), (lambda:
           self.qtwdict[val].show()
        ),
        self.PROC_TYPE_PY
      )
   def do_winfromuifile(self, val, csval):
      args = shlex.split(val)
      self.qtwdict[args[0]] = PyQt5.uic.loadUi(ipic.path.path_insensitive(args[1]))
      self.var_dict[args[0]] = f"<Qt5 window {args[0]!r} generated from {ipic.path.path_insensitive(args[1])!r}>"
      self.proc_dict[f"{val}.show".upper()] = (
        (), (lambda:
           self.qtwdict[args[0]].show()
        ),
        self.PROC_TYPE_PY
      )
   
   def do_loadqmlfile(self, val, csval):
      args = shlex.split(val)
      args2 = shlex.split(csval)
      self.qtwdict[args[0]] = PyQt5.QtQml.QQmlApplicationEngine()
      self.qtwdict[args[0]].quit.connect(self.app.quit)
      self.qtwdict[args[0]].load(args2[1])
      self.var_dict[args[0]] = f"<Qt5 QtQuick application {args[0]!r} generated from {ipic.path.path_insensitive(args[1])!r}>"
   def do_qtCHAR0__wintitle(self, val, csval):
      args = shlex.split(val)
      self.qtwdict[args[0]].setWindowTitle(args[1])
   def do_qtCHAR0__btn(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QPushButton(args["TEXT"])
      self.qtwdict[args["NAME"]].clicked.connect(lambda: ipic.lang.lexer(ipic.lang.sub(args["ONCLICK"])))
      self.var_dict[args["NAME"]] = f"<Qt5 button {args['NAME']!r}>"
      self.proc_dict[f"{args['NAME']}.set_enabled".upper()] = (
        (0,), (lambda x: 
           self.qtwdict[args["NAME"]].setEnabled(ipic.type.pbool(x))
        ), 
        self.PROC_TYPE_PY
      )
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_cmenu(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["PARENT"]].setContextMenuPolicy(PyQt5.QtCore.Qt.CustomContextMenu)
      self.cmenus.append(wrapper.ContextMenu(args["ACTIONS"], self.qtwdict[args["PARENT"]]))
      idx = len(self.cmenus)-1
      def cmenu(pos):
         self.cmenus[idx].exec(self.qtwdict[args["PARENT"]].mapToGlobal(pos))
      self.qtwdict[args["PARENT"]].customContextMenuRequested.connect(cmenu)
   def do_menubar(self, val, csval):
      args = json.loads(val)
      menubar = self.qtwdict[args["PARENT"]].menuBar()
      for menu in args["MENUS"]:
         qmenu = menubar.addMenu(menu["NAME"])
         for x in menu["ACTIONS"]:
            qmenu.addAction(wrapper.Action(x, self.qtwdict[args["PARENT"]]))
   def do_toolbar(self, val, csval):
      args = json.loads(val)
      toolbar = PyQt5.QtWidgets.QToolBar(args["NAME"])
      for x in args["ACTIONS"]:
         toolbar.addAction(wrapper.Action(x, self.qtwdict[args["PARENT"]]))
      self.qtwdict[args["PARENT"]].addToolBar(toolbar)
   # def do_systrayicon(self, val, csval):
      # args = json.loads(val)
      # self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QSystemTrayIcon()
      # self.qtwdict[args["NAME"]].setIcon(wrapper.Icon(args["ICON"]))
      # self.qtwdict[args["NAME"]].setVisible(True)
      # menu = wrapper.ContextMenu(args["MENU"])
      # print(menu)
      # self.qtwdict[args["NAME"]].setContextMenu(menu) 
   def do_chkbox(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QCheckBox()
      self.var_dict[args["NAME"]] = f"<Qt5 checkbox {args['NAME']!r}>"
      self.var_dict[f"{args['NAME']}.checked".upper()] = "$false"
      def on_check(s):
         self.var_dict[f"{args['NAME']}.checked".upper()] = ipic.type.boolean(s == PyQt5.QtCore.Qt.Checked)
      self.qtwdict[args["NAME"]].stateChanged.connect(on_check)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_qtCHAR0__entry(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QLineEdit()
      self.var_dict[args["NAME"]] = f"<Qt5 entry {args['NAME']!r}>"
      self.var_dict[f"{args['NAME']}.text".upper()] = ""
      try:
         self.qtwdict[args["NAME"]].setMaxLength(args["MAXLEN"])
      except KeyError:
         pass
      try:
         self.qtwdict[args["NAME"]].setPlaceholderText(args["PLACEHOLDER"])
      except KeyError:
         pass
      try:
         self.qtwdict[args["NAME"]].setReadOnly(args["READONLY"])
      except KeyError:
         pass
      def on_text_changed(s):
         self.var_dict[f"{args['NAME']}.text".upper()] = s
         try:
            ipic.lang.lexer(args["ONCHANGED"], args={"text":s})
         except KeyError:
            pass
      self.qtwdict[args["NAME"]].textChanged.connect(on_text_changed)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_combobox(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QComboBox()
      self.qtwdict[args["NAME"]].addItems(args["OPTS"])
      self.var_dict[args["NAME"]] = f"<Qt5 combobox {args['NAME']!r}>"
      self.var_dict[f"{args['NAME']}.selected".upper()] = self.qtwdict[args["NAME"]].currentText()
      def on_change_text(s):
         self.var_dict[f"{args['NAME']}.selected".upper()] = s
      self.qtwdict[args["NAME"]].currentTextChanged.connect(on_change_text)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_fontcombobox(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QFontComboBox()
      self.var_dict[args["NAME"]] = f"<Qt5 font combobox {args['NAME']!r}>"
      self.var_dict[f"{args['NAME']}.selected".upper()] = self.qtwdict[args["NAME"]].currentText()
      def on_change_text(s):
         self.var_dict[f"{args['NAME']}.selected".upper()] = s
      self.qtwdict[args["NAME"]].currentTextChanged.connect(on_change_text)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_spinbox(self, val, csval):
      args = json.loads(val)
      self.var_dict[args["NAME"]] = f"<Qt5 spinbox {args['NAME']!r}>"
      try:
         self.qtwdict[args["NAME"]].setRange(*args["RANGE"])
      except KeyError:
         pass
      try:
         self.qtwdict[args["NAME"]].setPrefix(args["PREFIX"])
      except KeyError:
         pass
      try:
         self.qtwdict[args["NAME"]].setSuffix(args["SUFFIX"])
      except KeyError:
         pass
      self.var_dict[f"{args['NAME']}.val".upper()] = "0"
      def on_change_text(s):
         self.var_dict[f"{args['NAME']}.val".upper()] = s
      self.qtwdict[args["NAME"]].textChanged.connect(on_change_text)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_dblspinbox(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QDoubleSpinBox()
      self.var_dict[args["NAME"]] = f"<Qt5 double spinbox {args['NAME']!r}>"
      try:
         self.qtwdict[args["NAME"]].setRange(*args["RANGE"])
      except KeyError:
         pass
      try:
         self.qtwdict[args["NAME"]].setPrefix(args["PREFIX"])
      except KeyError:
         pass
      try:
         self.qtwdict[args["NAME"]].setSuffix(args["SUFFIX"])
      except KeyError:
         pass
      self.var_dict[f"{args['NAME']}.val".upper()] = "0"
      def on_change_text(s):
         self.var_dict[f"{args['NAME']}.val".upper()] = s
      self.qtwdict[args["NAME"]].textChanged.connect(on_change_text)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_slider(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QSlider()
      self.var_dict[args["NAME"]] = f"<Qt5 slider {args['NAME']!r}>"
      try:
         self.qtwdict[args["NAME"]].setRange(*args["RANGE"])
      except KeyError:
         pass
      self.var_dict[f"{args['NAME']}.val".upper()] = "0"
      def on_value_changed(s):
         self.var_dict[f"{args['NAME']}.val".upper()] = str(s)
      self.qtwdict[args["NAME"]].valueChanged.connect(on_value_changed)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_dial(self, val, csval):
      args = json.loads(val)
      self.var_dict[args["NAME"]] = f"<Qt5 dial {args['NAME']!r}>"
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QDial()
      try:
         self.qtwdict[args["NAME"]].setRange(*args["RANGE"])
      except KeyError:
         pass
      self.var_dict[f"{args['NAME']}.val".upper()] = "0"
      def on_value_changed(s):
         self.var_dict[f"{args['NAME']}.val".upper()] = str(s)
      self.qtwdict[args["NAME"]].valueChanged.connect(on_value_changed)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_lswidget(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QListWidget()
      self.qtwdict[args["NAME"]].addItems(args["OPTS"])
      self.var_dict[args["NAME"]] = f"<Qt5 list widget {args['NAME']!r}>"
      self.var_dict[f"{args['NAME']}.selected".upper()] = args["OPTS"][0]
      def on_change_text(s):
         self.var_dict[f"{args['NAME']}.selected".upper()] = s
      self.qtwdict[args["NAME"]].currentTextChanged.connect(on_change_text)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_qtCHAR0__lbl(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QLabel(args["TEXT"])
      self.var_dict[args["NAME"]] = f"<Qt5 label {args['NAME']!r}>"
      self.proc_dict[f"{args['NAME']}.set_text".upper()] = ((0,), self.qtwdict[args["NAME"]].setText, self.PROC_TYPE_PY)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_qtCHAR0__img(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QLabel()
      self.qtwdict[args["NAME"]].setPixmap(PyQt5.QtGui.QPixmap(ipic.path.path_insensitive(args["IMAGE"])))
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_vlayout(self, val, csval):
      args = shlex.split(val)
      self.qtwdict[args[1]] = PyQt5.QtWidgets.QVBoxLayout()
      container = self.qtwdict[args[0]]
      container.setLayout(self.qtwdict[args[1]])
   def do_hlayout(self, val, csval):
      args = shlex.split(val)
      self.qtwdict[args[1]] = PyQt5.QtWidgets.QHBoxLayout()
      container = self.qtwdict[args[0]]
      container.setLayout(self.qtwdict[args[1]])
   def do_addvlayout(self, val, csval):
      args = shlex.split(val)
      self.qtwdict[args[1]] = PyQt5.QtWidgets.QVBoxLayout()
      self.qtwdict[args[0]].addLayout(self.qtwdict[args[1]])
   def do_addhlayout(self, val, csval):
      args = shlex.split(val)
      self.qtwdict[args[1]] = PyQt5.QtWidgets.QHBoxLayout()
      self.qtwdict[args[0]].addLayout(self.qtwdict[args[1]])
   def do_appexec(self, val, csval):
      sys.exit(self.app.exec())
   def do_threadCHAR0__start(self, val, csval):
      worker = thread.Worker(ipic.lang.sub(csval))
      self.threadpool.start(worker)
   def do_qtCHAR0__frm(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QWidget()
      self.var_dict[args["NAME"]] = f"<Qt5 frame {args['NAME']!r}>"
      try:
         args["ADD"]
      except KeyError:
         args["ADD"] = True
      if args["ADD"]:
         try:
            self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
         except BaseException as err:
            self.out.error(err)
   def do_tabs(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QTabWidget()
      try:
         self.qtwdict[args["NAME"]].setTabPosition(self.tab_dir[args["TAB_POS"]])
      except KeyError:
         pass
      try:
         self.qtwdict[args["NAME"]].setMovable(args["MOVABLE"])
      except KeyError:
         pass
      for x in args["TABS"]:
         self.qtwdict[args["NAME"]].addTab(self.qtwdict[x["WIDGET"]], x["NAME"])
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_qtCHAR0__txt(self, val, csval):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = PyQt5.QtWidgets.QPlainTextEdit()
      self.var_dict[args["NAME"]] = f"<Qt5 text {args['NAME']!r}>"
      self.proc_dict[f"{args['NAME']}.insert".upper()] = ((0,), self.qtwdict[args["NAME"]].appendPlainText, self.PROC_TYPE_PY)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)
   def do_statusbar(self, val, csval):
      self.qtwdict[val].setStatusBar(PyQt5.QtWidgets.QStatusBar(self.qtwdict[val]))
   def do_processCHAR0__start(self, val, csval):
      args = json.dumps(val)
      self.ps.append(PyQt5.QtCore.QProcess())
      idx = len(self.ps)-1
      p = self.ps[idx]
      def finished():
         try:
            ipic.lang.lexer(ipic.lang.sub(args["ONFINISHED"]), proc="<Qt5 process finished>")
         except KeyError:
            pass
         del p
      def hnd_stdout():
         data = bytes(p.readAllStandardOutput()).decode("utf8")
         try:
            ipic.lang.lexer(ipic.lang.sub(args["HND_STDOUT"]), proc="<Qt5 handle stdout>", args={"data": data})
         except KeyError:
            pass
      def hnd_stderr():
         data = bytes(p.readAllStandardError()).decode("utf8")
         try:
            ipic.lang.lexer(ipic.lang.sub(args["HND_STDERR"]), proc="<Qt5 handle stderr>", args={"data": data})
         except KeyError:
            pass
      p.readyReadStandardOutput.connect(self.handle_stdout)
      p.readyReadStandardError.connect(self.handle_stderr)
      p.finished.connect(finished)
      p.start(args["EXEC"], args["ARGS"])
   # def do_widget(self, val, csval):
      # wname = val[:val.find("{")].strip()
      # wbody = val[val.find("{")+1:val.rfind("}")]
      # ast = widgetblockparser(wbody)
      # def widget(j):
         # args = json.loads(j)
         # self.qtwdict[args["NAME"]] = CustomWidget(ast, proc_dict, var_dict, args, self.qtwdict)
         # if args["ADD"]:
            # self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      # self.proc_dict[wname] = ((0,), widget, ipic.lang.PROC_TYPE_PY) 