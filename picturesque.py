import sys, cmd, ipic.lang, traceback
ipic.lang.out.bind("output", print)
about = """Picturesque [1.0.0]
Copyright (c) 2024."""
class Console(cmd.Cmd):
   intro = about + "\nType \"help\" for help."
   prompt = ">> "
   def emptyline(self):
      return
   def onecmd(self, *args):
      ipic.lang.lexer(" ".join(args), is_console=True)
def run_console():
   ipic.lang.iturtle.setup()
   ipic.lang.iturtle.reset()
   Console().cmdloop()
if len(sys.argv) > 1:
   def on_error(err):
      if not err.__class__.__name__.startswith("Picturesque"):
         print("Error in internal Python distribution")
         traceback.print_exception(err)
      else:
         print(str(err))
      sys.exit(1)
   ipic.lang.out.bind("error", on_error)
   if not sys.argv[1].startswith("-"):
      ipic.lang.lexer(open(sys.argv[1], "r").read())
      ipic.lang.iturtle.mainloop()
   else:
      if sys.argv[1] == "-c":
         ipic.lang.lexer(sys.argv[2])
         if not iturtle_gone:
            ipic.lang.iturtle.mainloop()
      else:
         print("Error: Unrecognized flag/option:", sys.argv[1], file=sys.stderr)
else:
   def on_error(err):
      if not err.__class__.__name__.startswith("Picturesque"):
         print("Error in internal Python distribution")
         traceback.print_exception(err)
      else:
         print(str(err))
   ipic.lang.out.bind("error", on_error)
   run_console()