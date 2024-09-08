import ipic.ns

class main(ipic.ns.CmdNamespace):
   def do_yay(self, val, csval):
      print("hello world!")
   def do_woo(self, val, csval):
      print(val)
   def do_foo_bar(self, val, csval):
      print(csval)