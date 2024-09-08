import sys, argparse, traceback, shutil, ipic.lang, tkinter.messagebox
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--code', help='executes the code CODE')
group.add_argument('filename', help="the file to execute", nargs="?", default=None)
args = parser.parse_args()
ipic.lang.out.bind("output", lambda x: tkinter.messagebox.showinfo("Picturesque", x))
def on_error(err):
   if not err.__class__.__name__.startswith("Picturesque"):
      tkinter.messagebox.showerror(
         "Picturesque", 
         "Error in internal Python distribution",
         detail = "\n".join(traceback.format_exception(err))
      )
   else:
      tkinter.messagebox.showerror(
         "Picturesque", 
         str(err)
      )
   sys.exit(1)
ipic.lang.out.bind("error", on_error)
ipic.lang.out.bind("output_sameline", lambda x: print(x, end=""))
ipic.lang.out.bind("error_string", sys.stderr.write)
ipic.lang.out.bind("flush", sys.stderr.flush)
if args.code:
   ipic.lang.out.bind("error", on_error)
   ipic.lang.lexer(args.code)
elif args.filename:
   ipic.lang.out.bind("error", on_error)
   ipic.lang.lexer(open(args.filename).read())
   if not ipic.lang.turtle_gone:
      ipic.lang.iturtle.mainloop()