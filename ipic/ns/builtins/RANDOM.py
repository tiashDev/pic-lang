import ipic.ns, random
from ipic.util import TODO_CALL

class main(ipic.ns.CmdNamespace):
    def on_ns_init(self):
        (self.rangemin, self.rangemax) = (0, 10)
        self.sys_var["RANDOM"] = (lambda: random.randint(self.rangemin, self.rangemax), {"todo": TODO_CALL})
    def do_setrange(self, val, csval):
        (self.rangemin, self.rangemax) = (int(x) for x in val.split(maxsplit=2))