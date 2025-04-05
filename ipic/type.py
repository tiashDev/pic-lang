import ipic.util, random, shlex, ipic.errors

lang = None # to be given by the importer

def boolean(x):
   if x:
      return "$true"
   else:
      return "$false"
      
def pbool(x):
   if x.lower() == "$true":
      return True
   elif x.lower() == "$false":
      return False

def list2dict(keys, vals):
   return f"({', '.join([f'{keys[x]}: {vals[x]}' for x in range(len(keys))])})"

def py_list2dict(keys, vals):
   dictobj = {}
   for x in range(len(keys)):
      dictobj[keys[x]] = vals[x]
   return dictobj

def dictionary(dictobj):
   return f"({', '.join([f'{x}: {dictobj[x]}' for x in dictobj])})"

class Struct:
    def __init__(self, name, code=None, exts=None):
        self.vars = dict()
        self.procs = dict()
        if exts is not None:
            self.vars |= exts.vars
            self.procs |= exts.procs
        self.name = name
        if code:
            ast = lang.parse(code)
            stats = [x for x in ast if isinstance(x, str)]
            blcks = [x for x in ast if isinstance(x, tuple)]
            for stat in stats:
                if stat[0] == "~": continue
                (act, *_) = stat.split(maxsplit=1)
                if act == "var":
                    (_, name, _, value) = stat.split(maxsplit=3)
                    self.vars[name] = value
                else:
                    raise ipic.errors.PicturesqueException("Invalid syntax.")
            for blck in blcks:
                (bl_xinf, bl_text, _) = blck
                (act, *_) = bl_xinf.split(maxsplit=1)
                if act == "proc":
                    (_, name, *args_str) = bl_xinf.split(maxsplit=2)
                    args = tuple("".join(args_str).split(" ")) if not "".join(args_str) == "" else ()
                    self.procs[name] = (args, bl_text, lang.PROC_TYPE_PIC)
    def new(self, name, args):
        for vname, value in self.vars.items():
            lang.var_dict[f"{name}.{vname}".upper()] = value
        for pname, proc in self.procs.items():
            lang.proc_dict[f"{name}.{pname}".upper()] = (proc[0], f"set _name = {name};" + proc[1] if proc[2] == lang.PROC_TYPE_PIC else lambda *a: proc[2](name, *a), proc[2])
        lang.lexer(f"%{name}.{self.name.upper()} {args}", proc=f"<initialization of instance {name!r} of {self.name}>")
        if "_repr" in self.vars:
            return self.vars["_repr"]
        else:
            return f"<{self.name} of name {name!r}>"