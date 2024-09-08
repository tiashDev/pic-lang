import ipic.ns, pyqtgraph, json, shlex, PyQt5.QtCore

class main(ipic.ns.CmdNamespace):
   """The namespace class."""
   def on_ns_init(self):
      try:
         ipic.lang.singlevar_list[ipic.lang.SVLIST_IDX_NSDATA]["QtWidgets"]
      except KeyError:
         ipic.lang.singlevar_list[ipic.lang.SVLIST_IDX_NSDATA]["QtWidgets"] = {}
      finally:
         self.qtwdict = ipic.lang.singlevar_list[ipic.lang.SVLIST_IDX_NSDATA]["QtWidgets"]
      self.linedict = {}
      self.penstyle = {
         "SOLID": PyQt5.QtCore.Qt.SolidLine,
         "DASHED": PyQt5.QtCore.Qt.DashLine,
         "DOTTED": PyQt5.QtCore.Qt.DotLine,
         "DASHDOT": PyQt5.QtCore.Qt.DashDotLine,
         "DASH2XDOT": PyQt5.QtCore.Qt.DashDotDotLine,
      }
   def do_qtCHAR0__plot(self, val, cival):
      parsestr = val[val.find("|")+1:].strip()
      data = shlex.split(val[:val.find("|")].strip())
      self.qtwdict[data[0]] = pyqtgraph.PlotWidget()
      xpoints = [int(x) for x in list(parsestr[:parsestr.find(" * ")].split(" "))]
      if parsestr.find(" : ") >= -1:
         ypoints = [int(x) for x in list(parsestr[parsestr.find(" * ")+len(" * "):parsestr.find(" : ")].split(" "))]
         args = json.loads(parsestr[parsestr.find(" : ")+len(" : "):])
      else:
         ypoints = [int(x) for x in list(parsestr[parsestr.find(" * ")+len(" * "):].split(" "))]
         args = {"ADD":True}
      pnkw = {}
      plkw = {}
      gdkw = {"x":False,"y":False}
      try:
         if args["ADD"]:
            self.qtwdict[data[1]].addWidget(self.qtwdict[data[0]])
      except:
         self.qtwdict[data[1]].addWidget(self.qtwdict[data[0]])
      try:
         self.qtwdict[data[0]].setBackground(args["BGCOLOR"].lower())
      except KeyError:
         pass
      try:
         pnkw["color"] = args["COLOR"].lower()
      except KeyError:
         pass
      try:
         pnkw["style"] = self.penstyle[args["STYLE"]]
      except KeyError:
         pass
      try:
         plkw["symbol"] = args["SYMBOL"]["CODE"].lower()
      except KeyError:
         pass
      try:
         plkw["symbolSize"] = args["SYMBOL"]["SIZE"]
      except KeyError:
         pass
      try:
         plkw["symbolBrush"] = args["SYMBOL"]["BRUSH"].lower()
      except KeyError:
         pass
      try:
         gdkw["x"] = args["GRID"]["X"]
      except KeyError:
         pass
      try:
         gdkw["y"] = args["GRID"]["Y"]
      except KeyError:
         pass
      try:
         self.qtwdict[data[0]].setXRange(*args["RANGE"]["X"])
      except KeyError:
         pass
      try:
         self.qtwdict[data[0]].setYRange(*args["RANGE"]["Y"])
      except KeyError:
         pass
      self.qtwdict[data[0]].showGrid(**gdkw)
      pen = pyqtgraph.mkPen(**pnkw)
      self.linedict[data[0]] = self.qtwdict[data[0]].plot(xpoints, ypoints, pen=pen, **plkw)
      print(data[0])
      self.proc_dict[f"{data[0]}.set_data"] = (
         range(2), lambda x, y:
            self.linedict[data[0]].setData(json.loads(x), json.loads(y)),
         self.PROC_TYPE_PY
      )