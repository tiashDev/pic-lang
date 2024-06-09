import ipic.errors

class PicturesqueNamespace:
    __all_cmd__ = list()
    def add_cmd(self, cmd, func):
       if cmd not in self.__all_cmd__:
          self.__all_cmd__.append((cmd, func))
       else:
          raise ipic.errors.PicturesqueCommandAlreadyInNamespaceException(cmd)
    def __interpret(self, do, val, lineno, line, is_console, filename, is_artist):
       fails = 0
       for x in self.__all_cmd__:
          if x[0] == do:
             x[1](val)
          else:
             fails += 1
       if fails == len(self):
          file = ""
          if filename != None:
             file = filename
          else:
             file = "<console>"
          markers = ""
          for x in range(len(do)):
             markers += "^"
          for x in line:
             if x in string.whitespace:
                 markers = x + markers
             else: 
                 break
          if not is_artist:
             print("Error: Unrecognized command at line", lineno, "in", file, "-", file=sys.stderr)
             print(" ", line, file=sys.stderr)
             print(" ", markers, file=sys.stderr)
             if not is_console:
                sys.exit(1)
          else:
             raise ipic.errors.PicturesqueUnreconizedCommandException(f"""Error: Unrecognized command at line {lineno} in {file}.
  {line[1:-1] if line.startswith("\n") else line}
  {markers[1:-1] if markers.startswith("\n") else markers}""")
#