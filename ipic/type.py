import inspect, ipic.util, random, shlex

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

"""class Pic_class:
   is_pic = True
   def __init__(self, out):
      self.out = out
   def new(self, proc_dict, var_dict, name, lexer, args, cls, filename):
      for proc in self.procs: 
         if is_pic:
            proc_dict[f"{name}.{proc}".upper()] = (*proc, ipic.util.PROC_TYPE_PIC)
         else:
            proc_dict[f"{name}.{proc}".upper()] = (range(len(inspect.getfullargspec(self.procs[proc]))[0]), self.procs[proc], ipic.util.PROC_TYPE_PY)
      for var in self.vars: 
         var_dict[f"{name}.{var}".upper()] = self.vars[var]
      lexer(f"{name}.{cls} {shlex.join(args)}", filename=filename, proc="<class initialization process>")
      try:
         return var_dict[f"{name}._repr"]
      except KeyError:
         return f"<{name} object>"""