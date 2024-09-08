import sys, argparse, tkinter, traceback, shutil, ipic.stringutil
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--code', help='executes the code CODE')
group.add_argument('filename', help="the file to execute", nargs="?", default=None)
args = parser.parse_args()
import ipic.lang
ipic.lang.out.bind("output", print)
ipic.lang.out.bind("output_sameline", lambda x: print(x, end=""))
ipic.lang.out.bind("error_string", sys.stderr.write)
ipic.lang.out.bind("flush", sys.stderr.flush)
ipic.lang.out.bind("reqinput", input)
ipic.lang.turtle.reset()
def error(err, lineno, line, filename, proc):
   if not err.__class__.__name__.startswith("Picturesque"):
      print("Error in internal Python distribution", file=sys.stderr)
      flist = traceback.format_exception(err)
      flist.insert(1, f"  File {filename!r}, line {lineno}, in {proc}\n")
      flist.insert(2, f"    {line.split('\n')[0]}\n")
      print(''.join(flist))
   else:
      print(str(err), file=sys.stderr)
def console():
   print(f"""Picturesque [1.0.0]
Copyright (c) 2024-.
Type "help" for help.""")
   while True:
      code = input(">> ")
      if code.strip().endswith(";") or code.strip().endswith("}"):
         ipic.lang.lexer(code)
      elif code == "":
         continue
      elif "{" in code:
         while not len(ipic.stringutil.findall(code.strip(), "{")) \
                   == len(ipic.stringutil.findall(code.strip(), "}")):
            code += f"\n{input('.. ')}"
         ipic.lang.lexer(code)
      else:
         while not code.strip().endswith(";"):
            code += f"\n{input('.. ')}"
         ipic.lang.lexer(code)
getfile = lambda x: open(x) if x != "." else open("./main.draw")
if args.code:
   def on_error(err, lineno, line, filename, proc):
      error(err, lineno, line, filename, proc)
      sys.exit(1)
   ipic.lang.out.bind("error", on_error)
   ipic.lang.lexer(args.code)
elif args.filename:
   def on_error(err, lineno, line, filename, proc):
      error(err, lineno, line, filename, proc)
      sys.exit(1)
   ipic.lang.out.bind("error", on_error)
   ipic.lang.lexer(getfile(args.filename).read(), filename=args.filename)
   if not ipic.lang.turtle_gone:
      ipic.lang.turtle.mainloop()
else:
   def on_error(err, lineno, line, filename, proc):
      error(err, lineno, line, filename, proc)
   ipic.lang.out.bind("error", on_error)
   console()