import ipic.ns, PyQt5.QtCore, qtwidgets, json, ipic.util, ipic.type

class main(ipic.ns.CmdNamespace):
   """The namespace class."""
   def on_ns_init(self):
      try:
         ipic.lang.singlevar_list[ipic.lang.SVLIST_IDX_NSDATA]["QtWidgets"]
      except KeyError:
         ipic.lang.singlevar_list[ipic.lang.SVLIST_IDX_NSDATA]["QtWidgets"] = {}
      finally:
         self.qtwdict = ipic.lang.singlevar_list[ipic.lang.SVLIST_IDX_NSDATA]["QtWidgets"]
   def do_toggle(self, val, cival):
      args = json.loads(val)
      self.qtwdict[args["NAME"]] = qtwidgets.Toggle()
      self.var_dict[args["NAME"]] = f"<Qt5 (EXTRA) toggle {args['NAME']!r}>"
      self.var_dict[f"{args['NAME']}.checked".upper()] = "$false"
      def on_check(s):
         self.var_dict[f"{args['NAME']}.checked".upper()] = ipic.type.boolean(s == PyQt5.QtCore.Qt.Checked)
      self.qtwdict[args["NAME"]].stateChanged.connect(on_check)
      try:
         self.qtwdict[args["LAYOUT"]].addWidget(self.qtwdict[args["NAME"]])
      except BaseException as err:
         self.out.error(err)