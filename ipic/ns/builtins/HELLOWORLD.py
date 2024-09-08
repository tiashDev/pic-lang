import ipic.ns, ipic.type

class main(ipic.ns.CmdNamespace):
   def do_hello(self, val, cival):
      self.out.output("Hello world!")
   class cls_hello(ipic.type.Pic_class):
      is_pic = False
      def proc_hello(self):
         self.out.output("Hello world!")