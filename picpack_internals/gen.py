import platform, zipfile;

def _genfile_console(args, log, f, code):
   if args.additional_filenames:
      fcode = ""
      for x in args.additional_filenames:
        fcode += f"""f = open({f"{code}/{x}"!r}, "wb")
f.write({open(x, "rb").read()!r})
"""
      f.write(f"""import tkinter, os, shutil
os.mkdir({code!r})
{fcode}scwd = os.getcwd()
os.chdir({code!r})
import ipic.lang
ipic.lang.out.bind("output", print)
def on_error(err):
   if not err.__class__.__name__.startswith("Picturesque"):
      print("Error in internal Python distribution")
      traceback.print_exception(err)
   else:
      print(str(err))
   sys.exit(1)
ipic.lang.out.bind("error", on_error)
ipic.lang.lexer({open(args.filename).read()!r})
if not ipic.lang.turtle_gone:
   ipic.lang.iturtle.mainloop()
os.chdir(scwd)
shutil.rmtree({code!r})""")
      return
   if args.additional_filenames_zip:
      log.info("  Creating zip for included files...")
      tempzip = zipfile.ZipFile(f"files@{code}.zip", "w")
      log.info("  Adding files to zip...")
      for x in args.additional_filenames_zip:
         tempzip.write(x)
      log.info("  Closing zip...")
      tempzip.close()
      log.info(f"  Writing to {args.filename}.{code}.py...")
      f.write(f"""import tkinter, os, shutil, zipfile
f = open({code+".zip"!r})
f.write({open(f"files@{code}.zip", "rb").read()!r})
f.close()
zipfile.ZipFile({code+".zip"!r})).extractall({code!r})
scwd = os.getcwd()
os.chdir({code!r})
import ipic.lang
ipic.lang.out.bind("output", print)
def on_error(err):
   if not err.__class__.__name__.startswith("Picturesque"):
      print("Error in internal Python distribution")
      traceback.print_exception(err)
   else:
      print(str(err))
   sys.exit(1)
ipic.lang.out.bind("error", on_error)
ipic.lang.lexer({open(args.filename).read()!r})
if not ipic.lang.turtle_gone:
   ipic.lang.iturtle.mainloop()
os.chdir(scwd)
shutil.rmtree({code!r})""")
      log.info(f"  Deleting zip...")
      os.unlink(f"files@{code}.zip")
      return
   f.write(f"""import tkinter, shutil
import ipic.lang
ipic.lang.out.bind("output", print)
def on_error(err):
   if not err.__class__.__name__.startswith("Picturesque"):
      print("Error in internal Python distribution")
      traceback.print_exception(err)
   else:
      print(str(err))
   sys.exit(1)
ipic.lang.out.bind("error", on_error)
ipic.lang.lexer({open(args.filename).read()!r})
if not ipic.lang.turtle_gone:
   ipic.lang.iturtle.mainloop()""")

def _genfile_windowed(args, log, f, code):
   if args.additional_filenames:
      fcode = ""
      for x in args.additional_filenames:
        fcode += f"""f = open({f"{code}/{x}"!r}, "wb")
f.write({open(x, "rb").read()!r})
"""
      f.write(f"""import tkinter, os, shutil, tkinter.messagebox
os.mkdir({code!r})
{fcode}scwd = os.getcwd()
os.chdir({code!r})
import ipic.lang
ipic.lang.out.bind("output", lambda x: tkinter.messagebox.showinfo("Picturesque", x))
def on_error(err):
   if not err.__class__.__name__.startswith("Picturesque"):
      tkinter.messagebox.showerror(
         "Picturesque", 
         "Error in internal Python distribution",
         detail = "\\n".join(traceback.format_exception(err))
      )
   else:
      tkinter.messagebox.showerror(
         "Picturesque", 
         str(err)
      )
   sys.exit(1)
ipic.lang.out.bind("error", on_error)
ipic.lang.lexer({open(args.filename).read()!r})
if not ipic.lang.turtle_gone:
   ipic.lang.iturtle.mainloop()
os.chdir(scwd)
shutil.rmtree({code!r})""")
      return
   if args.additional_filenames_zip:
      log.info("  Creating zip for included files...")
      tempzip = zipfile.ZipFile(f"files@{code}.zip", "w")
      log.info("  Adding files to zip...")
      for x in args.additional_filenames_zip:
         tempzip.write(x)
      log.info("  Closing zip...")
      tempzip.close()
      log.info(f"  Writing to {args.filename}.{code}.py...")
      f.write(f"""import tkinter, os, shutil, zipfile, tkinter.messagebox
f = open({code+".zip"!r})
f.write({open(f"files@{code}.zip", "rb").read()!r})
f.close()
zipfile.ZipFile({code+".zip"!r})).extractall({code!r})
scwd = os.getcwd()
os.chdir({code!r})
import ipic.lang
ipic.lang.out.bind("output", lambda x: tkinter.messagebox.showinfo("Picturesque", x))
def on_error(err):
   if not err.__class__.__name__.startswith("Picturesque"):
      tkinter.messagebox.showerror(
         "Picturesque", 
         "Error in internal Python distribution",
         detail = "\\n".join(traceback.format_exception(err))
      )
   else:
      tkinter.messagebox.showerror(
         "Picturesque", 
         str(err)
      )
   sys.exit(1)
ipic.lang.out.bind("error", on_error)
ipic.lang.lexer({open(args.filename).read()!r})
if not ipic.lang.turtle_gone:
   ipic.lang.iturtle.mainloop()
os.chdir(scwd)
shutil.rmtree({code!r})""")
      log.info(f"  Deleting zip...")
      os.unlink(f"files@{code}.zip")
      return
   f.write(f"""import tkinter, tkinter.messagebox
import ipic.lang
ipic.lang.out.bind("output", lambda x: tkinter.messagebox.showinfo("Picturesque", x))
def on_error(err):
   if not err.__class__.__name__.startswith("Picturesque"):
      tkinter.messagebox.showerror(
         "Picturesque", 
         "Error in internal Python distribution",
         detail = "\\n".join(traceback.format_exception(err))
      )
   else:
      tkinter.messagebox.showerror(
         "Picturesque", 
         str(err)
      )
   sys.exit(1)
ipic.lang.out.bind("error", on_error)
ipic.lang.lexer({open(args.filename).read()!r})
if not ipic.lang.turtle_gone:
   ipic.lang.iturtle.mainloop()""")

def genfile(args, log, f, code):
   if args.windowed and (platform.system() == "Windows" or platform.system() == "Darwin"):
      _genfile_windowed(args, log, f, code)
   else:
      _genfile_console(args, log, f, code)