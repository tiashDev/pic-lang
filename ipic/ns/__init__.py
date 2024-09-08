"""Implements Picturesque namespaces."""
import ipic.errors, shlex, importlib.machinery, os.path

nsclasses = ["main", "Main", "ns", "Namespace"]

escvals = [".", "-", "[", "]"]

def cmd2meth(do, prefix="do_"):
   """The function used by namespaces to turn a command name into a Python method name. The symbols and what they are turned into are described in the table below.
   
   =======  ===========================
   Symbol   Substitute (must be exact)
   =======  ===========================
   .        CHAR0__
   -        CHAR1__
   [        CHAR2__
   ]        CHAR3__
   =======  ===========================
   
   For example:
   
      * if you wanted to define a command called ``hello.world``, you'd need to define a method called :py:func:`do_helloCHAR0__world` in your :py:class:`main` class.
      * if you wanted to define a command called ``hello-world``, you'd need to define a method called :py:func:`do_helloCHAR1__world` in your :py:class:`main` class.
      * if you wanted to define a command called ``hello[world]``, you'd need to define a method called :py:func:`do_helloCHAR2__worldCHAR3__` in your :py:class:`main` class.
      
   Note that these examples assume that you are using a class that uses this function in their :py:func:`__interpret__` methods, as both :py:class:`CmdNamespace` and :py:class:`ShlexNamespace` do."""
   do = do.lower()
   for idx, val in enumerate(escvals):
      do = do.replace(val, f"CHAR{idx}__")
   do = prefix + do
   return do

def meth2cmd(do, prefix="do_"):
   """The reverse of cmd2meth."""
   do = do.lower()
   for idx, val in enumerate(escvals):
      do = do.replace(f"CHAR{idx}__", val)
   do = do.removeprefix(prefix)
   return do.upper()

class PicturesqueNamespace:
   """The base class for all Picturesque namespaces.
   
   All Picturesque namespace files need to have a class with a name from ipic.ns.nsclasses (or have the __pic_ns_class__ string to point to the class), and it has to be a subclass of :py:class:`PicturesqueNamespace`. There are a few classes to make things easier, such as:
   
   * :py:class:`CmdNamespace`
   * :py:class:`ShlexNamespace`
   
   These classes work by having an ``__interpret__`` method which has the signature
   
   code-block:: python
   
      def __interpret__(self, do, val, csval)
   
   Where ``do`` is the command name, ``val`` is the case-insensitive arguments with variables, and ``csval`` is the arguments without variables - case-sensitive.
   
   Note that :py:class:`PicturesqueNamespace` does not have the ``__interpret__`` method. Of course you can define
   your own ``__interpret__`` method to interpret it in your own way. In that case you should extend 
   :py:class:`PicturesqueNamespace`, as it does not have a defined ``__interpret__`` method."""
   def __init__(self,
                stamps,
                turtle_gone,
                tkinter_win_ids,
                PROC_TYPE_PIC,
                PROC_TYPE_PY,
                var_dict,
                proc_dict,
                out,
                singlevar_list,
                ns_sysvar,
                ns_list,
                cls_dict):
       self.out = out
       self.stamps = stamps
       self.turtle_gone = turtle_gone
       self.tkinter_win_ids = tkinter_win_ids
       self.PROC_TYPE_PIC = PROC_TYPE_PIC
       self.PROC_TYPE_PY = PROC_TYPE_PY
       self.var_dict = var_dict
       self.proc_dict = proc_dict
       self.singlevar_list = singlevar_list
       self.sys_var = ns_sysvar
       self.ns_list = ns_list
       """print(vars(self))
       for attr in vars(self):
          if attr.startswith("cls_"):
             cls_dict[meth2cmd(attr, prefix="cls_")] = getattr(self, attr)
             print(attr)"""
       self.on_ns_init()
   def on_ns_init(self):
       pass

class CmdNamespace(PicturesqueNamespace):
   """A base class for Picturesque namespaces, where val (the arguments with variables - case-insensitive) and 
   csval (the arguments without variables - case-sensitive) are passed as seperate arguments to the do_* function 
   for the command.
   
   You might like this kind of namespace if you are familiar with the ``cmd`` module."""
   
   def __interpret__(self, do, val, csval):
       """The method used by ipic.lang to interpret Picturesque namespace commands."""
       try:
          getattr(self, cmd2meth(do))(val, csval)
       except AttributeError as err:
          if str(err).startswith(f"{self.__class__.__name__!r} object has no attribute '{cmd2meth(do)}'"):
             raise ipic.errors.PicturesqueCommandNotInNamespaceException()
          else:
             raise err

class ShlexNamespace(PicturesqueNamespace):
   """A base class for Picturesque namespaces, where val (the arguments with variables - case-insensitive) is
   split into different arguments using ``shlex.split``, and then passed to the ``do_*`` function for the command
   using the star operator.
   
   You might use this kind of namespace if you are a beginner."""
   
   def __interpret__(self, do, val, csval):
       """The method used by ipic.lang to interpret Picturesque namespace commands."""
       try:
          getattr(self, cmd2meth(do))(*shlex.split(val))
       except AttributeError as err:
          if str(err).startswith(f"{self.__class__.__name__!r} object has no attribute '{cmd2meth(do)}'"):
             raise ipic.errors.PicturesqueCommandNotInNamespaceException()
          else:
             raise err

def import_module_from_file_path(path, name=None):
   """Import a module using a file path, instead of a module path."""
   return importlib.machinery.SourceFileLoader(
      name or os.path.basename(path).removesuffix(".py"),
      path
   ).load_module()

def getnsclass(mod):
   """Gets the namespace class for a namespace, and returns it."""
   if not hasattr(mod, "__pic_ns_class__"):
      for nsclass in nsclasses:
         if hasattr(mod, nsclass):
            return getattr(mod, nsclass)
   else:
      return mod.__pic_ns_class__
   raise ipic.errors.PicturesqueNotANamespaceException(f"The Python module {mod.__name__!r} is not a Picturesque namespace, as it does not have {', '.join([repr(x) for x in nsclasses[:-1]])} or {nsclasses[-1]!r} classes, and there is not any __pic_ns_class__ specified.")