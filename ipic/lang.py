import turtle, time, string, matplotlib.pyplot, numpy, plotly.express, sys, ipic.errors, ipic.out, tkinter, json, tkinter.ttk, tkinter.messagebox, tkinter.colorchooser, tkinter.scrolledtext, shlex, tkinter.filedialog, os, ipic.type, webbrowser, pstats, io, ipic.path, sysconfig, platform, ftplib, configparser, textwrap, csv, ipic.table, plistlib, dbm, sqlite3, atexit, wsgiref.simple_server, tomllib, netrc, urllib.request, colorsys, getpass, ipic.stringutil, hashlib, ipic.ns, importlib, warnings, ipic.warnings, ipic.ns, collections

try: 
   import cProfile as profile
except ImportError:
   import profile
   
if platform.system() == 'Windows':
   import winsound

ipic.type.lang = sys.modules[__name__]
 
stamps = []
out = ipic.out.PicturesqueOutputHandler()
iturtle = turtle
turtle_gone = False
turtle.title("Picturesque")
tkinter_win_ids = {}
singlevar_list = [None, None, None, None, {}]
var_dict = collections.ChainMap()
proc_dict = {}
ns_list = {}
turtles = {}
struct_dict = {}
from ipic.util import (
   PROC_TYPE_PIC,
   PROC_TYPE_PY,
   PROC_IDX_ARGS,
   PROC_IDX_CODE,
   PROC_IDX_TYPE,
   SVLIST_IDX_FTP,
   SVLIST_IDX_UNIXDB,
   SVLIST_IDX_SQLDB,
   SVLIST_IDX_SQLCUR,
   SVLIST_IDX_NSDATA,
   TODO_CALL
)
ns_sys_var = {}
class_dict = {}
ns_kwargs = dict(
   stamps = stamps,
   turtle_gone = turtle_gone,
   tkinter_win_ids = tkinter_win_ids,
   PROC_TYPE_PIC = PROC_TYPE_PIC,
   PROC_TYPE_PY = PROC_TYPE_PY,
   var_dict = var_dict,
   proc_dict = proc_dict,
   singlevar_list = singlevar_list,
   out = out,
   ns_sysvar = ns_sys_var,
   ns_list = ns_list,
   cls_dict = class_dict
)

def expr_eval(expr, var_dict=var_dict):
   toks = expr.split()
   stack = collections.deque()
   for tok in toks:
       if tok.isdecimal():
           stack.append(int(tok))
       elif tok.startswith("%"):
           val = var_dict[tok.removeprefix("%")]
           if not isinstance(val, int) and val.isdecimal():
               stack.append(int(val))
           else:
               stack.append(val)
       elif tok in ("$true", "$false"):
           stack.append(tok)
       else:
           res = None
           rside = stack.pop()
           try: # Binary expressions
              lside = stack.pop()
              if tok == "+":
                  res = lside + rside
              elif tok == "-":
                  res = lside - rside
              elif tok == "*":
                  res = lside * rside
              elif tok == "/":
                  res = lside / rside
              elif tok == ">":
                  res = ipic.type.boolean(lside > rside)
              elif tok == "<":
                  res = ipic.type.boolean(lside < rside)
              elif tok == "==":
                  res = ipic.type.boolean(lside == rside)
              elif tok == "!=":
                  res = ipic.type.boolean(lside != rside)
              elif tok == ">=":
                  res = ipic.type.boolean(lside >= rside)
              elif tok == "<=":
                  res = ipic.type.boolean(lside <= rside)
           except IndexError: # Unitary expressions
              if tok == "not":
                  res = ipic.type.boolean(not ipic.type.pbool(rside))
              else:
                  stack.append(tok)
                  continue
           stack.append(res)
   return stack[0] 
   
def sub(code):
   return code.replace(",", ";").replace("`", ",")

# Microsoft Copilot has saved this function - twice! Thanks, Copilot!
def parse(code):
    ast = []
    current = ""
    blocks = 0
    block = False

    # Ensure the code ends with a semicolon or a "}"
    if not (code.endswith(";") or code.endswith("}")):
        code += ";"

    for idx, char in enumerate(code):
        current += char

        if char == "{":
            if code[idx - 1] != ".":
                block = True
            blocks += 1

        elif char == "}":
            blocks -= 1
            if blocks == 0 and block:
                strtoosmol = False
                try:
                    next_char = code[idx + 1]
                except IndexError:
                    strtoosmol = True

                if not strtoosmol and next_char == ";":  # Block treated as regular line
                    ast.append(current.strip())
                else:
                    # Extract block details
                    block_name = current[:current.find("{")].strip()
                    block_content = current[current.find("{") + 1:current.rfind("}")].strip()
                    ast.append((block_name, block_content, current.strip()))
                
                block = False
                current = ""

        elif char == ";" and not block:
            if current.strip():
                ast.append(current.removesuffix(";").strip())
            current = ""

    if current != "" and block:
        raise ipic.errors.PicturesqueException('Expected "}".')
    if ast[-1] == "":
        ast.pop()
    return ast
 
def interpret(do, val, lineno, line, filename, proc, var_dict, bl_xinf=None, bl_text=None):
   global turtle_gone, iturtle
   if do == "FORWARD":
      iturtle.forward(int(val))
   elif do == "BACKWARD":
      iturtle.backward(int(val))
   elif do == "RIGHT":
      iturtle.right(int(val))
   elif do == "LEFT":
      iturtle.left(int(val))
   elif do == "PATH.END" or do == "PEN.UP":
      iturtle.penup()
   elif do == "PATH.BEGIN" or do == "PATH.START" or do == "PEN.DOWN":
      iturtle.pendown()
   elif do == "RESET":
      iturtle.reset()
   elif do == "CLEAR":
      turtle.clearscreen()
   elif do == "COLOR":
      iturtle.color(val)
   elif do == "FILL":
      iturtle.fillcolor(val)
   elif do == "HOME":
      iturtle.home()
   elif do == "FILLCOLOR.START" or do == "FILLCOLOR.BEGIN":
      iturtle.begin_fill()
   elif do == "FILLCOLOR.END":
      iturtle.end_fill()
   elif do == "WAIT":
      time.sleep(float(val))
   elif do == "SETX":
      iturtle.setx(int(val))
   elif do == "SETY":
      iturtle.sety(int(val))
   elif do == "STAMP":
      stamps.append(iturtle.stamp())
   elif do == "STAMPS.CLEAR":
      iturtle.clearstamps()
   elif do == "SPEED":
      iturtle.speed(int(val))
   elif do == "SIZE":
      iturtle.pensize(int(val))
   elif do == "LOGLN":
      out.output(val)
   elif do == "CIRCLE":
      iturtle.circle(int(val))
   elif do == "OUTLINE":
      iturtle.pencolor(val)
   elif do == "HIDE":
      iturtle.hideturtle()
   elif do == "SHOW":
      iturtle.showturtle()
   elif do == "SCREEN.COLOR":
      turtle.getscreen().bgcolor(val)
   elif do == "SCREEN.IMAGE":
      turtle.getscreen().bgpic(val)
   elif do == "CLOSEONCLICK":
      turtle.getscreen().exitonclick()
      turtle_gone = True
   elif do == "MODE":
      iturtle.mode(val)
   elif do == "SETWORLDCOORDINATES":
      turtle.getscreen().setworldcoordinates(tuple(map(int, val.split(' '))))
   elif do == "CLOSETURTLE":
      turtle.bye()
      turtle_gone = True
   elif do == "DOT":
      args = val.split(' ')
      iturtle.dot(args[0], args[1])
   elif do == "GOTO":
      iturtle.setpos(tuple(map(int, val.split(' '))))
   elif do == "SHAPE":
      iturtle.shape(val.lower())
   elif do == "HELP":
      webbrowser.open("https://picturesque-documentation.readthedocs.io/")
   elif do == "EXIT":
      if val != "":
         sys.exit(int(val))
      else:
         sys.exit(0)
   elif do == "INCLUDE":
      lexer(open(ipic.path.path_insensitive(val), "r").read())
   elif do == "SET":
      (name, eq, value) = val.split(maxsplit=2)
      evaled = False
      if eq != "=":
          if eq.endswith("=") and not evaled:
              value = expr_eval(f"{var_dict[name]} {value} {eq.removesuffix('=')}")
              evaled = True
          else:
              raise ipic.errors.PicturesqueException(f"Invalid syntax. (line {lineno})")
      if (not evaled) and value.startswith("EXPR "):
          value = expr_eval(value.removeprefix("EXPR "))
          evaled = True
      var_dict[name] = value
   elif do == "PLOT":
      matplotlib.pyplot.figure(num = "Picturesque")
      cival = line[line.find(" ")+1:]
      xpoints = numpy.array([int(x) for x in list(val[:val.find(" * ")].split(" "))])
      if val.find(" : ") >= -1:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" : ")].split(" "))])
         matplotlib.pyplot.plot(xpoints, ypoints, cival[cival.find(" : ")+len(" : "):].lower())
      else:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         matplotlib.pyplot.plot(xpoints, ypoints)
      matplotlib.pyplot.show()
   elif do == "BAR":
      matplotlib.pyplot.figure(num = "Picturesque")
      xpoints = numpy.array([x.replace("\\S", " ").replace("\\(S)", "\\S") for x in list(val[:val.find(" * ")].split(" "))])
      if val.find(" : ") >= -1:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" : ")].split(" "))])
         matplotlib.pyplot.bar(xpoints, ypoints, color = val[val.find(" : ")+len(" : "):].lower())
      else:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         matplotlib.pyplot.bar(xpoints, ypoints)
      matplotlib.pyplot.show()
   elif do == "BARH":
      matplotlib.pyplot.figure(num = "Picturesque")
      xpoints = numpy.array([x.replace("\\S", " ").replace("\\(S)", "\\S") for x in list(val[:val.find(" * ")].split(" "))])
      if val.find(" : ") >= -1:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" : ")].split(" "))])
         matplotlib.pyplot.barh(xpoints, ypoints, color = val[val.find(" : ")+len(" : "):].lower())
      else:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         matplotlib.pyplot.barh(xpoints, ypoints)
      matplotlib.pyplot.show()
   elif do == "PIE":
      matplotlib.pyplot.figure(num = "Picturesque")
      mylabels = shlex.split(val[:val.find(" * ")])
      if val.find(" : ") >= -1:
         y = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" : ")].split(" "))])
         matplotlib.pyplot.pie(y, labels = mylabels, colors = list(val[val.find(" : ")+len(" : "):].lower().split(" ")))
      else:
         y = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         matplotlib.pyplot.pie(y, labels = mylabels)
      matplotlib.pyplot.legend(title = "Legend")
      matplotlib.pyplot.show()
   elif do == "HIST":
      matplotlib.pyplot.figure(num = "Picturesque")
      if not val.startswith("RANDOM"):
         x = numpy.array([float(i) for i in list(val.split(" "))]);
         matplotlib.pyplot.hist(x)
      else:
         args = val.split(" ")[1:]
         if len(args) > 1:
            x = numpy.random.normal(int(args[0]), int(args[1]), int(args[2]))
            matplotlib.pyplot.hist(x)
         else:
            x = numpy.random.normal(170, 10, 250)
            matplotlib.pyplot.hist(x)
      matplotlib.pyplot.show()
   elif do == "BBAR":
      xpoints = shlex.split(val[:val.find(" * ")])
      if val.find(" | ") > -1:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" | ")].split(" "))])
         plotly.express.bar(x=xpoints, y=ypoints).write_html(val[val.find(" | ")+len(" | "):])
      else:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         plotly.express.bar(x=xpoints, y=ypoints).show()
   elif do == "EVAL":
      lexer(sub(val), filename="<eval statement>")
   elif do == "FOREVER":
      while True:
         try:
            lexer(bl_text, filename="<forever loop>")
         except KeyboardInterrupt:
            break
   elif do == "INITAPP":
      tkinter_win_ids[val] = tkinter.Tk()
      tkinter_win_ids[val].title("Picturesque")
   elif do == "WININIT":
      args = shlex.split(val)
      tkinter_win_ids[args[1]] = tkinter.TopLevel(tkinter_win_ids[args[0]])
      tkinter_win_ids[args[1]].title("Picturesque")
   elif do == "WINTITLE":
      args = shlex.split(val)
      try:
         tkinter_win_ids[args[0]].title(args[1])
      except KeyError:
         raise ipic.errors.PicturesqueWindowNotFoundException(f"The window {shlex.quote(args[0])} does not exist. (line {lineno}, file {filename if filename != None else '<console>'})")
   elif do == "LOOPWIN":
      try:
         tkinter_win_ids[val].mainloop()
      except KeyboardInterrupt:
         pass
   elif do == "CLOSEWIN":
      tkinter_win_ids[val].destroy()
   elif do == "BTN":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.Button(tkinter_win_ids[args["PARENT"]], text=args["TEXT"], command=lambda *a: lexer(sub(args["ONCLICK"])), filename="<window event>")
      # define helper procedures
      proc_dict[f"{args['NAME']}.invoke".upper()] = (
         range(2), (lambda pos, text: 
            tkinter_win_ids[args["NAME"]].invoke()
         ), 
         PROC_TYPE_PY
      )
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "SBTN":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.ttk.Button(tkinter_win_ids[args["PARENT"]], text=args["TEXT"], command=lambda *a: lexer(sub(args["ONCLICK"]), filename="<window event>"))
      # define helper procedures
      proc_dict[f"{args['NAME']}.invoke".upper()] = (
         range(2), (lambda pos, text: 
            tkinter_win_ids[args["NAME"]].invoke()
         ), 
         PROC_TYPE_PY
      )
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "LBL":
      args = json.loads(val)
      tkinter.Label(tkinter_win_ids[args["PARENT"]], text=args["TEXT"]).pack()
   elif do == "IMG":
      args = json.loads(val)
      image = tkinter.PhotoImage(file=args["IMAGE"])
      tkinter.Label(tkinter_win_ids[args["PARENT"]], image=image).pack()
   elif do == "TXT":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.Text(tkinter_win_ids[args["PARENT"]], width=args["WIDTH"], height=args["HEIGHT"])
      # define helper procedures
      proc_dict[f"{args['NAME']}.insert".upper()] = (range(2), (lambda pos, text: tkinter_win_ids[args["NAME"]].insert(pos.lower(), text), PROC_TYPE_PY))
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "ENTRY":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.Entry(tkinter_win_ids[args["PARENT"]])
      # define helper procedures
      proc_dict[f"{args['NAME']}.insert".upper()] = (range(2), (lambda pos, text: tkinter_win_ids[args["NAME"]].insert(pos.lower(), text), PROC_TYPE_PY))
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "SENTRY":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.ttk.Entry(tkinter_win_ids[args["PARENT"]])
      # define helper procedures
      proc_dict[f"{args['NAME']}.insert".upper()] = (range(2), (lambda pos, text: tkinter_win_ids[args["NAME"]].insert(pos.lower(), text), PROC_TYPE_PY))
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "SCROLLTXT":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.scrolledtext.ScrolledText(tkinter_win_ids[args["PARENT"]], width=args["WIDTH"], height=args["HEIGHT"])
      # define helper procedures
      proc_dict[f"{args['NAME']}.insert".upper()] = (range(2), (lambda pos, text: tkinter_win_ids[args["NAME"]].insert(pos.lower(), text), PROC_TYPE_PY))
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "FRM":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.ttk.Frame(tkinter_win_ids[args["PARENT"]])
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "INFO":
      tkinter.messagebox.showinfo(val[:val.find(" | ")], val[val.find(" | ")+3:])
   elif do == "WRITE":
      iturtle.write(val)
   elif do == "DOTCL":
      argsx = shlex.split(val)
      argsy = shlex.split(line)
      if tkinter_win_ids[argsx[0]].__class__.__name__ == "Tk":
         tkinter_win_ids[argsx[0]].tk.eval(argsy[2])
      else:
         raise ipic.errors.PicturesqueInvalidWidgetException(f"Invalid object for command \"dotcl\". (line {lineno}, file {filename if filename != None else '<console>'})")
   elif do == "SCREEN.IMAGE":
      iturtle.getscreen().bgpic(ipic.path.path_insensitive(val))
   elif do == "WEBSITE.OPEN":
      webbrowser.open(shlex.split(line)[1])
   elif do == "WEBSITE.OPENWIN":
      webbrowser.open_new(shlex.split(line)[1])
   elif do == "WEBSITE.OPENTAB":
      webbrowser.open_new_tab(shlex.split(line)[1])
   elif do == "PROFILE":
      pr = profile.Profile()
      pr.runctx(f"lexer({bl_text!r})", globals(), locals())
      try: pr.disable()
      except: pass
      s = io.StringIO()
      sortby = pstats.SortKey.CUMULATIVE
      ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
      ps.print_stats()
      out.output(s.getvalue())
   elif do == "WINSOUND.PLAYALIAS":
      if platform.system() == "Windows":
          winsound.PlaySound(val, winsound.SND_ALIAS)
      else:
          raise ipic.errors.PicturesqueInvalidOSException("Your operating system has to be Windows for this command to work.")
   elif do == "WINSOUND.PLAYALIASASYNC":
      if platform.system() == "Windows":
          winsound.PlaySound(val, winsound.SND_ALIAS | winsound.SND_ASYNC)
      else:
          raise ipic.errors.PicturesqueInvalidOSException("Your operating system has to be Windows for this command to work.")
   elif do == "WINSOUND.STOPALL":
      if platform.system() == "Windows":
          winsound.PlaySound(None, 0)
      else:
          raise ipic.errors.PicturesqueInvalidOSException("Your operating system has to be Windows for this command to work.")
   elif do == "WINSOUND.LOOPALIASASYNC":
      if platform.system() == "Windows":
          winsound.PlaySound(val, winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
      else:
          raise ipic.errors.PicturesqueInvalidOSException("Your operating system has to be Windows for this command to work.")
   elif do == "WINSOUND.PLAYFILE":
      if platform.system() == "Windows":
          winsound.PlaySound(ipic.path.path_insensitive(val), winsound.SND_FILENAME)
      else:
          raise ipic.errors.PicturesqueInvalidOSException("Your operating system has to be Windows for this command to work.")
   elif do == "WINSOUND.PLAYFILEASYNC":
      if platform.system() == "Windows":
          winsound.PlaySound(ipic.path.path_insensitive(val), winsound.SND_FILENAME | winsound.SND_ASYNC)
      else:
          raise ipic.errors.PicturesqueInvalidOSException("Your operating system has to be Windows for this command to work.")
   elif do == "WINSOUND.LOOPFILEASYNC":
      if platform.system() == "Windows":
          winsound.PlaySound(ipic.path.path_insensitive(val), winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
      else:
          raise ipic.errors.PicturesqueInvalidOSException("Your operating system has to be Windows for this command to work.")
   elif do == "FTP.OPEN":
      try:
         singlevar_list[SVLIST_IDX_FTP] = ftplib.FTP(line[line.find(" ")+1:])
      except importlib.import_module("socket").gaierror:
         raise ipic.errors.PicturesqueInvalidURLException(f"The URL {line[line.find(' ')+1:]!r} is invalid.")
      except ftplib.all_errors as err:
         out.output(str(err))
   elif do == "FTP.LOGIN":
      try:
         if not len(val.split(" ")) > 0:
            out.output(singlevar_list[SVLIST_IDX_FTP].login())
         else:
            csval = line[line.find(" "):]
            args = csval.split(" ")
            out.output(singlevar_list[SVLIST_IDX_FTP].login(args[0], args[1]))
      except ftplib.all_errors as err:
         out.output(str(err))
   elif do == "FTP.CD":
      try:
         out.output(singlevar_list[SVLIST_IDX_FTP].cwd(line[line.find(" ")+1:]))
      except ftplib.all_errors as err:
         out.output(str(err))
   elif do == "FTP.LSDIR":
      try:
         singlevar_list[SVLIST_IDX_FTP].dir(".", out.output)
      except ftplib.all_errors as err:
         out.output(str(err))
   elif do == "FTP.CLOSE":
      try:
         out.output(singlevar_list[SVLIST_IDX_FTP].quit())
         singlevar_list[SVLIST_IDX_FTP] = None
      except ftplib.all_errors as err:
         out.output(str(err))
   elif do == "FTP.TRANSFER":
      try:
         with open(shlex.split(line[line.find(" ")+1:])[1], 'wb') as fp:
            out.output(singlevar_list[SVLIST_IDX_FTP].retrbinary(f'RETR {line[line.find(" ")+1:]}', fp.write))
      except ftplib.all_errors as err:
         out.output(str(err))
   elif do == "LOADINI":
      args = val.split(" ")
      cfg = configparser.ConfigParser(allow_no_value=True)
      cfg.read(ipic.path.path_insensitive(args[1]))
      var_dict[args[0]] = f"""configuration file (from loadini) -> {ipic.path.path_insensitive(args[1])}
sections: {", ".join(cfg.sections())}"""
      for x in cfg.sections():
         var_dict[f"{args[0]}[{x}]".upper()] = f"""configuration file section (from loadini) -> {ipic.path.path_insensitive(args[1])} ({x})
options: {", ".join([z for z in cfg[x]])}"""
         for y in cfg[x]:
             var_dict[f"{args[0]}[{x}][{y}]".upper()] = cfg[x][y]
   elif do == "WRAP":
      for x in textwrap.wrap(val):
         out.output(x)
   elif do == "LOADCSV":
      args = val.split(" ")
      with open(ipic.path.path_insensitive(args[1])) as csvfile:
         reader = csv.reader(csvfile)
         var_repllist = []
         rows = [x for x in reader]
         for row_n in range(len(rows)):
            var_dict[f"{args[0]}[{row_n}]".upper()] = ", ".join(rows[row_n])
            var_repllist.append(rows[row_n])
            cols = [x for x in rows[row_n]]
            for col_n in range(len(cols)):
               var_dict[f"{args[0]}[{row_n}][{col_n}]".upper()] = cols[col_n]
         var_dict[args[0]] = ipic.table.table(var_repllist)
   elif do == "LOADPLISTXML":
      args = val.split(" ")
      with open(ipic.path.path_insensitive(args[1]), "rb") as plistfile:
         plist = plistlib.load(plistfile, fmt=plistlib.FMT_XML)
         def arrayrepr(array, isnested=False):
            def checkval(the_val, num):
               if the_val.__class__.__name__ == "dict":
                  return f"configuration tree (from plist) -> {ipic.path.path_insensitive(args[1])} (branch: {basename}[{num}])"
               elif the_val.__class__.__name__ == "list":
                  return arrayrepr(array[num], isnested=True)
               elif the_val.__class__.__name__ == "bool":
                  return ipic.type.boolean(plist[x])
               elif the_val.__class__.__name__ == "bytes":
                  return the_val.decode("utf-8")
               else:
                  return str(the_val)
            return ("(" if isnested else "") + ", ".join([checkval(array[x], x) for x in range(len(array))]) + (")" if isnested else "")
         def loadarray(array, basename=args[0], isnested=False):
            var_dict[basename.upper()] = arrayrepr(array)
            for x in range(len(array)):
               if array[x].__class__.__name__ == "dict":
                  loadplist(array[x], basename=f"{basename}[{x}]")
               elif array[x].__class__.__name__ == "list":
                  loadarray(array[x], basename=f"{basename}[{x}]")
               elif array[x].__class__.__name__ == "bool":
                  var_dict[f"{basename}[{x}]".upper()] = ipic.type.boolean(plist[x])
               elif array[x].__class__.__name__ == "bytes":
                  var_dict[f"{basename}[{x}]".upper()] = plist[x].decode("utf-8")
               else:
                  var_dict[f"{basename}[{x}]".upper()] = array[x]
         def loadplist(plist, basename=args[0]):
            var_dict[f"{basename}".upper()] = f"""configuration tree (from plist) -> {ipic.path.path_insensitive(args[1])} (branch: {basename})
keys: {", ".join([x for x in plist])}"""
            for x in plist:
               if plist[x].__class__.__name__ == "dict":
                   loadplist(plist[x], basename=f"{basename}[{x}]")
               elif plist[x].__class__.__name__ == "list":
                   loadarray(plist[x], basename=f"{basename}[{x}]")
               elif plist[x].__class__.__name__ == "bool":
                   var_dict[f"{basename}[{x}]".upper()] = ipic.type.boolean(plist[x])
               else:
                   var_dict[f"{basename}[{x}]".upper()] = plist[x]
         loadplist(plist)
   elif do == "UNIXDB.OPEN":
      singlevar_list[SVLIST_IDX_UNIXDB] = dbm.open(line[line.find(" ")+1:], 'c')
   elif do == "UNIXDB.SETITEM":
      args = shlex.split(val)
      singlevar_list[SVLIST_IDX_UNIXDB][args[0]] = args[1]
   elif do == "UNIXDB.CLOSE":
      singlevar_list[SVLIST_IDX_UNIXDB].close()
      singlevar_list[SVLIST_IDX_UNIXDB] = None
   elif do == "UNIXDB.GETITEM":
      out.output(singlevar_list[SVLIST_IDX_UNIXDB].get(val, b'(item not present)').decode("utf-8"))
   elif do == "SQL.OPEN":
      singlevar_list[SVLIST_IDX_SQLDB] = sqlite3.connect(line[line.find(" ")+1:])
      singlevar_list[SVLIST_IDX_SQLCUR] = singlevar_list[SVLIST_IDX_SQLDB].cursor()
   elif do == "SQL.RUN":
      res = singlevar_list[SVLIST_IDX_SQLCUR].execute(line[line.find(" ")+1:])
      try:
         out.output(ipic.table.htable([col[0] for col in res.description], res.fetchall()))
      except:
         pass
   elif do == "SQL.SAVE":
      res = singlevar_list[SVLIST_IDX_SQLDB].commit()
   elif do == "SQL.CLOSE":
      singlevar_list[SVLIST_IDX_SQLDB].close()
      singlevar_list[SVLIST_IDX_SQLDB] = None
      singlevar_list[SVLIST_IDX_SQLCUR] = None
   elif do == "PROC":
      name = bl_xinf[:bl_xinf.find(" ")]
      args_str = bl_xinf[bl_xinf.find(" ")+1:]
      args = tuple(args_str.split(" ")) if not args_str == "" else ()
      proc_dict[name] = (args, bl_text, PROC_TYPE_PIC)
   elif do == "ONEXIT":
      atexit.register(lambda: lexer(bl_text, var_dict=var_dict.new_child()))
   elif do == "WIDTH":
      iturtle.width(int(val))
   elif do == "SERVER":
      args = json.loads(line[line.find(" ")+1:])
      def web_server(environ, start_response):
         def handle_response(route):
            headers = []
            for key in args["routes"][route]["headers"]:
                headers.append((key, sub(args["routes"][route]["headers"][key])))
            start_response("200 OK", headers)
            return [args["routes"][route]["text"].encode(args["routes"][route]["encoding"])]
         for route in args["routes"]:
            if environ["PATH_INFO"] == route:
                try:
                   return handle_response(args["routes"][route]["display"])
                except KeyError:
                   return handle_response(route)
         start_response("404 Not Found", [("Content-Type", "text/html; encoding=utf-8")])
         return ["""<!DOCTYPE html>
<html>
<body>

<h1>Picturesque <code>server</code> command</h1>
<h2>Error 404</h2>
<p>The page you requested was not found.</h1>

</body>
</html>""".encode("utf-8")]
      class RequestHandler(wsgiref.simple_server.WSGIRequestHandler):
         def log_message(self, format, *args):
            out.output("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))
         def get_stderr(self):
            return self.StdErr()
         class StdErr:
            def write(self, text):
               out.strerror(text)
            def flush(self):
               out.flush()
      with wsgiref.simple_server.make_server('', args["port"], web_server, handler_class=RequestHandler) as httpd:
         out.output(f"Serving HTTP on port {args['port']}...")
         try:
            httpd.serve_forever()
         except KeyboardInterrupt:
            pass
   elif do == "LOADTOML":
      name = val[:val.find(" ")]
      file = ipic.path.path_insensitive(val[val.find(" ")+1:])
      doc = tomllib.load(open(file, "rb"))
      def arrayrepr(array, nested=False):
          def checkval(item):
              if item.__class__.__name__ == "dict":
                 return "configuration tree (from loadtoml)"
              elif item.__class__.__name__ == "list":
                 return arrayrepr(item, nested=True)
              else:
                 return str(item)
          return ("(" if nested else "") + ", ".join([checkval(x) for x in array]) + (")" if nested else "") 
      def parse_array(array, basename=name):
          var_dict[basename.upper()] = arrayrepr(array)
          for idx in range(len(array)):
              value = array[idx]
              if value.__class__.__name__ == "dict":
                 parse_table(value, basename=f"{basename}[{idx}]")
              elif value.__class__.__name__ == "list":
                 parse_array(value, basename=f"{basename}[{idx}]")
              else:
                 var_dict[f"{basename}[{idx}]".upper()] = str(value)
      def parse_table(table, basename=name):
          var_dict[basename.upper()] = f"""configuration tree (from loadtoml) -> {ipic.path.path_insensitive(file)}  (branch: {basename})
keys: {", ".join([x for x in table])}"""
          for key in table:
              value = table[key]
              if value.__class__.__name__ == "dict":
                 parse_table(value, basename=f"{basename}[{key}]")
              elif value.__class__.__name__ == "list":
                 parse_array(value, basename=f"{basename}[{key}]")
              else:
                 var_dict[f"{basename}[{key}]".upper()] = str(value)
      parse_table(doc)
   elif do == "LOADNETRC":
      name = val[:val.find(" ")]
      file = ipic.path.path_insensitive(val[val.find(" ")+1:])
      doc = netrc.netrc(file)
      var_dict[name.upper()] = f"""netrc file (from loadnetrc) -> {file}
hosts: {", ".join([x for x in doc.hosts])}"""
      for host in doc.hosts:
         var_dict[f"{name}[{host}]".upper()] = f"""netrc host: {host} (from loadnetrc) -> {file}
username: {doc.hosts[host][0]}
password: {doc.hosts[host][2]}"""
         var_dict[f"{name}[{host}].username".upper()] = doc.hosts[host][0]
         var_dict[f"{name}[{host}].password".upper()] = doc.hosts[host][2]
   elif do == "OPENURL":
      csval = line[line.find(" ")+1:]
      name = val[:val.find(" ")]
      file = csval[csval.find(" ")+1:]
      with urllib.request.urlopen(file) as response:
         var_dict[name.upper()] = f"web response (from urlopen) -> {file}{f' <--> {response.geturl()}' if response.geturl() != file else ''}"
         var_dict[f"{name}.text".upper()] = response.read().decode()
         var_dict[f"{name}.headers".upper()] = f"web response headers: {json.dumps(dict(response.headers))}"
         for key in response.headers:
             value = response.headers[key]
             var_dict[f"{name}.headers[{key}]".upper()] = value
   elif do == "RGB2HSV":
      name = val[:val.find(" ")]
      icolor = val[val.find(" ")+1:].split(" ")
      ocolor = colorsys.rgb_to_hsv(*(float(x) for x in icolor))
      var_dict[name.upper()] = " ".join([str(x) for x in ocolor])
   elif do == "HSV2RGB":
      name = val[:val.find(" ")]
      icolor = val[val.find(" ")+1:].split(" ")
      ocolor = colorsys.hsv_to_rgb(*(float(x) for x in icolor))
      var_dict[name.upper()] = " ".join([str(x) for x in ocolor])
   elif do == "RGB2HLS":
      name = val[:val.find(" ")]
      icolor = val[val.find(" ")+1:].split(" ")
      ocolor = colorsys.rgb_to_hls(*(float(x) for x in icolor))
      var_dict[name.upper()] = " ".join([str(x) for x in ocolor])
   elif do == "HLS2RGB":
      name = val[:val.find(" ")]
      icolor = val[val.find(" ")+1:].split(" ")
      ocolor = colorsys.hls_to_rgb(*(float(x) for x in icolor))
      var_dict[name.upper()] = " ".join([str(x) for x in ocolor])
   elif do == "RGB2YIQ":
      name = val[:val.find(" ")]
      icolor = val[val.find(" ")+1:].split(" ")
      ocolor = colorsys.rgb_to_yiq(*(float(x) for x in icolor))
      var_dict[name.upper()] = " ".join([str(x) for x in ocolor])
   elif do == "YIQ2RGB":
      name = val[:val.find(" ")]
      icolor = val[val.find(" ")+1:].split(" ")
      ocolor = colorsys.hls_to_rgb(*(float(x) for x in icolor))
      var_dict[name.upper()] = " ".join([str(x) for x in ocolor])
   elif do == "HASH":
      occur = ipic.stringutil.findall(val, " ")
      name = val[:occur[0]]
      algo = val[occur[0]+1:occur[1]]
      to_encode = val[occur[1]+1:]
      var_dict[name.upper()] = hashlib.new(algo, to_encode.encode()).hexdigest()
   elif do == "USING":
      for x in val.split(","):
          ns = importlib.import_module(f"ipic.ns.builtins.{x.strip()}")
          ns_list[x] = ipic.ns.getnsclass(ns)(**ns_kwargs)
   elif do == "USING-FILE":
      for x in [y for y in csv.reader([val])][0]:
          ns = ipic.ns.import_module_from_file_path(ipic.path.path_insensitive(x))
          ns_list[ns.__name__] = ipic.ns.getnsclass(ns)(**ns_kwargs)
   elif do == "TURTLE.NEW":
       turtles[val] = turtle.Turtle()
   elif do == "TURTLE.SWAP":
       iturtle = turtles[val]
   elif do == "TURTLE.DEFAULT":
       iturtle = turtle
   elif do == "REGSHAPE":
       shapename = val[:val.find(' ')].lower()
       shapejson = val[val.find(' ')+1:]
       shapepnts = tuple(tuple(x) for x in json.loads(shapejson))
       turtle.register_shape(shapename, shapepnts)
   elif do == "IF":
       condt = ipic.type.pbool(expr_eval(bl_xinf))
       if condt:
           lexer(bl_text, var_dict=var_dict.new_child())
   elif do == "WHILE":
       condt = ipic.type.pbool(expr_eval(bl_xinf))
       while condt:
           lexer(bl_text, var_dict=var_dict.new_child())
           condt = ipic.type.pbool(expr_eval(bl_xinf))
   elif do == "ONKEYPRESS":
       out.output(bl_xinf.capitalize())
       turtle.onkeypress(lambda: lexer(bl_text, var_dict=var_dict.new_child()), bl_xinf.capitalize())
   elif do == "LISTEN":
       turtle.listen()
   elif do == "STRUCT":
       struct_dict[bl_xinf] = ipic.type.Struct(bl_xinf, bl_text)
   elif do.startswith("%") and do[1:] in proc_dict:
      args = shlex.split(val)
      proc = do[1:]
      if len(args) > len(proc_dict[proc][PROC_IDX_ARGS]): 
         raise ipic.errors.PicturesqueTooManyArgumentsException(f"Too many arguments for procedure {proc!r}. (line {lineno})")
      if len(args) < len(proc_dict[proc][PROC_IDX_ARGS]):
         raise ipic.errors.PicturesqueTooLittleArgumentsException(f"Too little arguments for procedure {proc!r}. (line {lineno})")
      if proc_dict[proc][PROC_IDX_TYPE] == PROC_TYPE_PIC:
         lexer(proc_dict[proc][PROC_IDX_CODE], filename=filename, proc=proc, args=ipic.type.py_list2dict(proc_dict[proc][PROC_IDX_ARGS], args), var_dict=var_dict.new_child())
      elif proc_dict[proc][PROC_IDX_TYPE] == PROC_TYPE_PY:
         proc_dict[proc][PROC_IDX_CODE](*(x for x in args))
   elif do.startswith("&") and do[1:] in struct_dict:
      (name, eq, new, *args) = val.split(maxsplit=3)
      if eq != "=" or new != "NEW":
          raise ipic.errors.PicturesqueException(f"Invalid syntax. (line {lineno})")
      stru = do[1:]
      var_dict[name] = struct_dict[stru].new(name, "".join(args))
   else:
      # namespace commands
      for ns in ns_list:
         try:
            ns_list[ns].__interpret__(do, val, line[line.find(" ")+1:])
            return
         except ipic.errors.PicturesqueCommandNotInNamespaceException:
            pass
      markers = ""
      for x in range(len(do)):
         markers += "^"
      for x in line:
         if x in string.whitespace:
             markers = x + markers
         else: 
             break
      raise ipic.errors.PicturesqueUnreconizedCommandException(f"""Error: Unrecognized command at {filename}:{lineno}, in {proc}
  {line[1:] if line.startswith("\n") else line}
  {markers[1:] if markers.startswith("\n") else markers}""")

def lexer(program, filename="<console>", proc="<global>", args={}, var_dict=var_dict):
   #*~----------------------------~( Initialization )~-----------------------------------------~*#
   global stamps, turtle_gone
   cmd_list = parse(program)
   #*~-------------------------~( End of initialization )~-------------------------------------~*#
   #*~------------------------------~( Main loop )~--------------------------------------------~*#
   for x in range(len(cmd_list)):
      cmd, bl_xinf = "", ""
      if not isinstance(cmd_list[x], tuple):
         cmd = cmd_list[x]
      else:
         (bl_xinf, bl_text, cmd) = cmd_list[x]
      line = cmd
      cmd = cmd.strip()
      cmd = cmd.upper()
      bl_xinf = bl_xinf.upper()
      cmd_len = len(cmd.split(" "))
      if cmd_len == 0 or len(cmd) == 0 or cmd[0] == "~":
         continue
      cmd_type = cmd
      num = ""
      if cmd_len > 1:
         num = cmd[cmd.find(" ")+1:]
         cmd_type = cmd[:cmd.find(" ")]
      def defsysvar(nm, val, todo=None):
          nonlocal num, bl_xinf
          if ".{$"+nm.upper()+"}" in num:
             if todo == None:
                num = num.replace(".{$"+nm.upper()+"}", str(val))
             else:
                num = num.replace(".{$"+nm.upper()+"}", str(todo(val)))
          if ".{$"+nm.upper()+"}" in bl_xinf:
             if todo == None:
                bl_xinf = bl_xinf.replace(".{$"+nm.upper()+"}", str(val))
             else:
                bl_xinf = bl_xinf.replace(".{$"+nm.upper()+"}", str(todo(val)))
      #*~---------------------------~( Variables )~-----------------------------------------~*#
      if not turtle_gone:
          try:
            defsysvar("POS", iturtle.position())
            defsysvar("X", iturtle.xcor())
            defsysvar("Y", iturtle.ycor())
            defsysvar("DOWN", ipic.type.boolean(iturtle.isdown()))
            defsysvar("OUTLINE", iturtle.pencolor())
            defsysvar("FILL", iturtle.fillcolor())
            defsysvar("COLOR", iturtle.color())
            defsysvar("VISIBLE", iturtle.isvisible())
            defsysvar("TURTLE_SHAPE_POLYGONAL_POINTS", iturtle.get_shapepoly())
            defsysvar("BGCOLOR", turtle.getscreen().bgcolor())
            defsysvar("BGIMAGE", turtle.getscreen().bgpic())
            defsysvar("WINHEIGHT", turtle.getscreen().window_height())
            defsysvar("WINWIDTH", turtle.getscreen().window_width())
            defsysvar("STAMPS", str(stamps))
            defsysvar("MODE", turtle.mode())
            defsysvar("shape", iturtle.shape())
            defsysvar("bgpic", turtle.getscreen().bgpic())
          except turtle.Terminator:
            turtle_gone=True
      #*~-------------------------------------~*~-------------------------------------------~*#
      defsysvar("tk_version", tkinter.TkVersion)
      defsysvar("tk_ext_version", tkinter.Tcl().call("info", "patchlevel"))
      defsysvar("py_version", sysconfig.get_python_version())
      defsysvar("py_ext_version", "%d.%d.%d" % sys.version_info[:3])
      defsysvar("py_sup_ext_version", sys.version)
      #*~-------------------------------------~*~-------------------------------------------~*#
      defsysvar("argv", ", ".join(sys.argv))
      for x in range(len(sys.argv)):
         defsysvar(f"argv[{x}]", sys.argv[x])
      #*~-------------------------------------~*~-------------------------------------------~*#
      try:
         defsysvar("ftp.cwd", singlevar_list[SVLIST_IDX_FTP].pwd())
         defsysvar("ftp.welcome", singlevar_list[SVLIST_IDX_FTP].getwelcome())
      except:
         pass
      #*~-------------------------------------~*~-------------------------------------------~*#
      defsysvar("cli.input", out.reqinput, todo=TODO_CALL)
      #*~-------------------------------------~*~-------------------------------------------~*#
      defsysvar("askopenfile", tkinter.filedialog.askopenfilename, todo=TODO_CALL)
      defsysvar("askdir", tkinter.filedialog.askdirectory, todo=TODO_CALL)
      #*~-------------------------------------~*~-------------------------------------------~*#
      def pic_guiinput():
         if turtle_gone:
            iturtle.Turtle._screen = None  # force recreation of singleton Screen object
            iturtle.TurtleScreen._RUNNING = True  # only set upon TurtleScreen() definition
         inputtxt = iturtle.getscreen().textinput("Picturesque", "This program wants to ask you something.")
         if turtle_gone:
            iturtle.bye()
         return inputtxt if inputtxt is not None else ""
      defsysvar("gui.input", pic_guiinput, todo=TODO_CALL)
      def pic_guinuminput():
         if turtle_gone:
            iturtle.Turtle._screen = None  # force recreation of singleton Screen object
            iturtle.TurtleScreen._RUNNING = True  # only set upon TurtleScreen() definition
         inputtxt = iturtle.getscreen().numinput(val[:val.find(" | ")], val[val.find(" | ")+3:])
         if turtle_gone:
            iturtle.bye()
         return inputtxt if inputtxt is not None else ""
      defsysvar("gui.numinput", pic_guinuminput, todo=TODO_CALL)
      #*~-------------------------------------~*~-------------------------------------------~*#
      def pic_askcolor():
         color = tkinter.colorchooser.askcolor()
         return " ".join([str(x) for x in color[0]]) if color != (None, None) else ""
      defsysvar("askcolor", pic_askcolor, todo=TODO_CALL)
      #*~-------------------------------------~*~-------------------------------------------~*#
      defsysvar("getpass", lambda: getpass.getpass(""), todo=TODO_CALL)
      #*~-------------------------------------~*~-------------------------------------------~*#
      defsysvar("json.true", "true")
      defsysvar("json.false", "false")
      #*~-------------------------------------~*~-------------------------------------------~*#
      for i in args:
         defsysvar(f"args[{i}]", args[i])
      defsysvar("args", ipic.type.dictionary(args))
      #*~-------------------------------------~*~-------------------------------------------~*#
      for i in ns_sys_var:
         defsysvar(i, ns_sys_var[i][0], **ns_sys_var[i][1])
      #*~-------------------------------------~*~-------------------------------------------~*#
      num = num.replace("($)", "$")
      #*~-------------------------------------~*~-------------------------------------------~*#
      for i in var_dict:
         num = num.replace(".{%"+i+"}", str(var_dict[i]))
      #*~-------------------------------------~*~-------------------------------------------~*#
      num = num.replace("(%)", "%")
      #*~----------------------------~( End of variables )~---------------------------------~*#
      #*~------------------------------~( Interpreting )~-----------------------------------~*#
      try:
         if not isinstance(cmd_list[x], tuple):
            interpret(cmd_type, num, x + 1, line, filename, proc, var_dict = var_dict)
         else:
            interpret(cmd_type, num, x + 1, line, filename, proc, var_dict, bl_xinf.removeprefix(cmd_type+" "), bl_text)
      except Exception as err:
         out.error(err, x + 1, line, filename, proc)
      #*~---------------------------~( End of interpreting )~-------------------------------~*#
   #*~--------------------------------~( End of main loop )~-----------------------------------~*#